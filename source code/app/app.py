from models import *
from sqlalchemy import func, and_, extract
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import models
import pandas as pd
import plotly
import plotly_conf as conf
## local scripts
from Ploty.plot_victim import *
from Ploty.worldmap_freq import freq
from Ploty.worldmap_woundkill import kill_wound
from Ploty.worldmap_trend import gt_freq
from Ploty.weapon_type import weapon
from Ploty.attack_info import attack_info
import Ploty.trend as trend
import Ploty.google_trend as GT
import pickle

cache = pickle.load(open("cache.pickle","rb"))
plotly.tools.set_credentials_file(username=conf.pp_conf["username"], api_key=conf.pp_conf["api_key"])

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
countries = db.session.query(models.Location.country).distinct(models.Location.country).all()

@app.route('/')
def homepage():
	return render_template("index.html")


@app.route('/visual/')
def visual():
	return render_template("visual.html")

@app.route('/world-map/',methods = ['GET', 'POST'])
def world_map():
	trend_map = cache["tm"]
	if request.method == "GET":
		frequency = cache["frequency"]
		return render_template("world-map.html", overall_map = frequency, trend_map = trend_map)

	code = pd.read_csv("Ploty/code_correct.csv")
	map_type = request.form.get("map_type")
	startDate = request.form.get("startDate")
	endDate = request.form.get("endDate")

	if map_type == "0":
		query_fq = (db.session.query(Location.country)
			.join(Happened, and_(Location.latitude==Happened.latitude, Location.longitude == Happened.longitude))
			.join(Incident, Happened.incident_id == Incident.id)
			.filter(and_(Incident.date <= endDate,Incident.date >= startDate))
			.all())
		query_fq = pd.DataFrame(query_fq)
		frequency= freq(query_fq,code)
	else:
		query_wk = (db.session.query(Incident.nkill, Incident.nwound, Location.country)
			.join(Happened, and_(Happened.incident_id==Incident.id))
			.join(Location, and_(Location.latitude==Happened.latitude, Location.longitude == Happened.longitude))
			.filter(and_(Incident.date <= endDate,Incident.date >= startDate))
			.all())
		query_wk = pd.DataFrame(query_wk)
		frequency= kill_wound(query_wk,code)

	return render_template("world-map.html", overall_map = frequency, trend_map = trend_map)


@app.route('/attack-type/', methods = ['GET', 'POST'])
def attackType():
	attack_country = request.form.get("type")
	if attack_country is None:
		#attack_type = (db.session.query(Incident.international, Incident.property_damage, BelongedTo.suicide_attack, BelongedTo.succussful_attack).
		#	   join(BelongedTo, Incident.id == BelongedTo.incident_id).all())
		#attack_type =  pd.DataFrame(attack_type)
		Attack = cache['Attack']
		return render_template("attack-type.html", Attack = Attack, countries = countries)
	else:
		attack_type = int(attack_type)
		attack_type = (db.session.query(Incident.international, Incident.property_damage, BelongedTo.suicide_attack, BelongedTo.succussful_attack).
		join(BelongedTo, Incident.id == BelongedTo.incident_id).join(Incident,Incident.id == Used.incident_id).
		join(Happened,Happened.incident_id == Incident.id).
		join(Location,and_(Location.latitude == Happened.latitude,Location.longitude == Happened.longitude)).
		filter(Location.country == attack_country).all()) 
		attack_type =  pd.DataFrame(attack_type)
		Attack = attack_info(attack_type)
		return render_template("attack-type.html", Attack = Attack, countries = countries)

@app.route('/trend/', methods = ['GET', 'POST'])
def trends():
	# Trend = trend.trend(trend.base_query)
	trend_type = request.form.get("graph_type")
	base_query = (db.session.query(extract('year',Incident.date), func.sum(Incident.nkill), func.sum(Incident.nwound)).
		filter(Incident.date.isnot(None)).group_by(extract('year', Incident.date)).
		order_by(extract('year',Incident.date))).all()
	if trend_type is None:
		#trend_plot = trend.trend(base_query)
		trend_plot = cache["trend"]
	elif trend_type == "0":
		trend_plot = trend.trend(base_query)
	else:
		base_query = (db.session.query(GoogleTrend.date, GoogleTrend.weighted_avg)).all()
		trend_plot = GT.google_trend(base_query)

	return render_template("trend.html", Trend = trend_plot)
	#return render_template("trend.html", Google_trend = Google_trend, Victim = Victim)

@app.route('/victim-type/', methods = ['GET', 'POST'])
def victimType():
	victim_types = db.session.query(Targeted.victim_type).distinct(Targeted.victim_type).all()  
	country = request.form.get("country")
	graph_type = request.form.get("graph_type")
	victim_type = request.form.get("victim_type")

	if country is None and graph_type is None and victim_type is None:
		plot_victim = cache["plot_victim"]
		plot_subtype = cache["plot_subtype"]
		return render_template("victim-type.html", Victim = plot_victim, Victim_Subtype = plot_subtype, countries = countries, Victim_types = victim_types)

	if country is None:
		victim_frequency_all = db.session.query(func.count(Targeted.incident_id).label('count'), Targeted.victim_type).group_by(Targeted.victim_type).order_by(func.count(Targeted.incident_id)).all()  
	else:
		victim_frequency_country = db.session.query(func.count(Targeted.incident_id).label('count'), Targeted.victim_type).join(Happened,Happened.incident_id == Targeted.incident_id).join(Location,and_(Location.latitude == Happened.latitude,Location.longitude == Happened.longitude)).filter(Location.country == country).group_by(Targeted.victim_type).order_by(func.count(Targeted.incident_id)).all()


	if graph_type is None:
		if country is None:
			plot_victim = plot_victim_frequency(victim_frequency_all)
		else:
			plot_victim = plot_victim_frequency(victim_frequency_country)
	elif graph_type == "0":
		if country is None:
			plot_victim = plot_victim_frequency(victim_frequency_all)
		else:
			plot_victim = plot_victim_frequency(victim_frequency_country)       
	else:
		if country is None:
			victim_fatality = (db.session.query(Targeted.victim_type, func.sum(Incident.nkill).label('fatality'), func.sum(Incident.nwound).label('injury'))
				.join(Targeted.incident)
				.group_by(Targeted.victim_type)
				.order_by(func.sum(Incident.nkill))).all()
		else:
			victim_fatality = (db.session.query(Targeted.victim_type, func.sum(Incident.nkill).label('fatality'), func.sum(Incident.nwound).label('injury'))
				.join(Targeted.incident).join(Happened,Happened.incident_id == Targeted.incident_id)
				.join(Location,and_(Location.latitude == Happened.latitude,Location.longitude == Happened.longitude))
				.filter(Location.country==country)
				.group_by(Targeted.victim_type)
				.order_by(func.sum(Incident.nkill))).all()
		plot_victim = plot_victim_fatality(victim_fatality)
	
	if victim_type is None:
		if country is None:
			victim_subtype = (db.session.query(Targeted.subtype, func.sum(Incident.nkill), func.sum(Incident.nwound))
				.filter(Targeted.victim_type=="Private Citizens & Property")
				.join(Targeted.incident)
				.group_by(Targeted.subtype)).all()
		else:
			victim_subtype = (db.session.query(Targeted.subtype, func.sum(Incident.nkill), func.sum(Incident.nwound))
				.filter(Targeted.victim_type=="Private Citizens & Property")
				.join(Happened,Happened.incident_id == Targeted.incident_id)
				.join(Location,and_(Location.latitude == Happened.latitude,Location.longitude == Happened.longitude))
				.filter(Location.country==country)          
				.join(Targeted.incident)
				.group_by(Targeted.subtype)).all()          
	else:
		if country is None:
			victim_subtype = (db.session.query(Targeted.subtype, func.sum(Incident.nkill), func.sum(Incident.nwound))
				.filter(Targeted.victim_type==victim_type)
				.join(Targeted.incident)
				.group_by(Targeted.subtype)).all()          
		else:
			victim_subtype = (db.session.query(Targeted.subtype, func.sum(Incident.nkill), func.sum(Incident.nwound))
				.filter(Targeted.victim_type==victim_type)
				.join(Happened,Happened.incident_id == Targeted.incident_id)
				.join(Location,and_(Location.latitude == Happened.latitude,Location.longitude == Happened.longitude))
				.filter(Location.country==country)
				.join(Targeted.incident)
				.group_by(Targeted.subtype)).all()
	
	plot_subtype = plot_victim_subtype(victim_subtype)          
	return render_template("victim-type.html", Victim = plot_victim, Victim_Subtype = plot_subtype, countries = countries, Victim_types = victim_types)

@app.route('/weapon-type/', methods = ['GET', 'POST'])
def weaponType():
		country = request.form.get("country")  
		if country is None:
			#weapon_type = (db.session.query(func.count(Used.incident_id).label('count'), Used.weapon_type,(func.sum(Incident.nkill)+func.sum(Incident.nwound)).label('fatality'))
			#	.join(Incident,Incident.id == Used.incident_id)
			#	.group_by(Used.weapon_type)
			#	.order_by(func.count(Used.incident_id).desc())).all()
			Weapon = cache["Weapon"]
			return render_template("weapon-type.html", Weapon = Weapon, countries = countries)
		else:
			weapon_type = (db.session.query(func.count(Used.incident_id).label('count'), Used.weapon_type,(func.sum(Incident.nkill)+func.sum(Incident.nwound)).label('fatality'))
				.join(Incident,Incident.id == Used.incident_id)
				.join(Happened,Happened.incident_id == Incident.id)
						.join(Location,and_(Location.latitude == Happened.latitude,Location.longitude == Happened.longitude))
						.filter(Location.country == country)
				.group_by(Used.weapon_type)
				.order_by(func.count(Used.incident_id).desc())).all()

			weapon_type = pd.DataFrame(weapon_type)

			Weapon = weapon(weapon_type)
			return render_template("weapon-type.html", Weapon = Weapon, countries = countries)
#       return render_template("weapon-type.html")

#@app.route('/comments/')
#def comments():
#	return render_template("comments.html")

@app.route("/test" , methods=['GET', 'POST'])
def test():
	select = request.form.get('type')
	return(str(select))

if __name__ == "__main__":
	app.run(host = "0.0.0.0")

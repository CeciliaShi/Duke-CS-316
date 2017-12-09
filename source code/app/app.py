from models import *
from sqlalchemy import func, and_
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import models
import pandas as pd
import plotly
import plotly_conf as conf
## local scripts
from Ploty.kw import kill_wound
from Ploty.freq import freq
from Ploty.plot_victim import plot_victim, victim_type
from Ploty.query_freq import freq, fq
from Ploty.weapon_type import weapon
from Ploty.victim_damage import victim_damage, base_query
#from Ploty.attack_info import attack_type, attack_info
from Ploty.attack_info import attack_info
import Ploty.trend as trend
from Ploty.victim_subtype import victim_subtype, query_subtype
import Ploty.google_trend as GT
from Ploty.weighted_avg import search_map, gt_freq

plotly.tools.set_credentials_file(username=conf.pp_conf["username"], api_key=conf.pp_conf["api_key"])

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
countries = db.session.query(models.Location.country).distinct(models.Location.country).all()

@app.route('/')
def homepage():
    return render_template("index.html")

# @app.route('/about-us/')
# def worldmap():
# 	return render_template("about-us.html")

@app.route('/visual/')
def visual():
	return render_template("visual.html")

@app.route('/world-map/')
def world_map():
	code = pd.read_csv("Ploty/code_correct.csv")
	#df = pd.read_csv("Ploty/freq.csv")
	#iframe = freq(df,code)
	#df = pd.read_csv("Ploty/kw.csv")
	#iframe = kill_wound(df,code)
	#iframe = "https://plot.ly/~KimJin/0/550/550"
#	victim = plot_victim(victim_type)

	frequency = freq(fq, code)
	trend_map = gt_freq(search_map, code)
	return render_template("world-map.html", frequency = frequency, trend_map = trend_map)
		#Trend = Trend, Google_trend = Google_trend)
		#trend_map = trend_map)
#	return render_template("world-map.html", iframe = iframe, victim = victim)
#	return render_template("world-map.html", victim = victim)


@app.route('/attack-type/', methods = ['GET', 'POST'])
def attackType():
	attack_country = request.form.get("type")
	if attack_country is None:
		attack_type = (db.session.query(Incident.international, Incident.property_damage, BelongedTo.suicide_attack, BelongedTo.succussful_attack).
               join(BelongedTo, Incident.id == BelongedTo.incident_id).all()) 
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

@app.route('/trend/')
def trends():
	# Trend = trend.trend(trend.base_query)
	Google_trend = GT.google_trend(GT.base_query)
	Victim = victim_damage(base_query)
	#return render_template("trend.html", Trend = Trend, Google_trend = Google_trend)
	return render_template("trend.html", Google_trend = Google_trend, Victim = Victim)

@app.route('/victim-type/', methods = ['GET', 'POST'])
def victimType():
	victim_types = db.session.query(Targeted.victim_type).distinct(Targeted.victim_type).all()
	country = request.form.get("country")
	graph_type = request.form.get("graph_type")
	victim_type = request.form.get("victim_type")

	if graph_type is None | graph_type == "0":
		victim_frequency = db.session.query(func.count(Targeted.incident_id).label('count'), Targeted.victim_type).group_by(Targeted.victim_type).order_by(func.count(Targeted.incident_id)).all()
        plot_victim = plot_victim_frequency(victim_frequency)
    else:
    	victime_fatality = (db.session.query(Targeted.victim_type, func.sum(Incident.nkill).label('fatality'), func.sum(Incident.nwound).label('injury'))
    		.join(Targeted.incident)
    		.group_by(Targeted.victim_type)
    		.order_by(func.sum(Incident.nkill))).all()
    	plot_victim = plot_victim_fatality(victime_fatality)
    
    if victim_type is None | victim_type == "Private Citizens & Property":
    	victim_subtype = (db.session.query(Targeted.subtype, func.sum(Incident.nkill), func.sum(Incident.nwound))
    		.filter(Targeted.victim_type=="Private Citizens & Property")
    		.join(Targeted.incident)
    		.group_by(Targeted.subtype)).all()
    else:
     	victim_subtype = (db.session.query(Targeted.subtype, func.sum(Incident.nkill), func.sum(Incident.nwound))
    		.filter(Targeted.victim_type==victim_type)
    		.join(Targeted.incident)
    		.group_by(Targeted.subtype)).all()
    
    plot_subtype = plot_victim_subtype(victim_subtype)		   	
	return render_template("victim-type.html", Victim = plot_victim, Victim_Subtype = plot_subtype, countries = countries, Victime_types = victim_types)

@app.route('/weapon-type/', methods = ['GET', 'POST'])
def weaponType():
        country = request.form.get("country")  
        if country is None:
        	weapon_type = (db.session.query(func.count(Used.incident_id).label('count'), Used.weapon_type,(func.sum(Incident.nkill)+func.sum(Incident.nwound)).label('fatality'))
        		.join(Incident,Incident.id == Used.incident_id)
      			.group_by(Used.weapon_type)
     			.order_by(func.count(Used.incident_id).desc())).all()

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

@app.route('/comments/')
def comments():
	return render_template("comments.html")

@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('type')
    return(str(select))

if __name__ == "__main__":
    app.run(host = "0.0.0.0")

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
from Ploty.query_weapon_type import weapon, weapon_type
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
	Trend = trend.trend(trend.base_query)
	Google_trend = GT.google_trend(GT.base_query)
	return render_template("world-map.html", frequency = frequency, Trend = Trend, 
		Google_trend = Google_trend, 
		trend_map = trend_map)
#	return render_template("world-map.html", iframe = iframe, victim = victim)
#	return render_template("world-map.html", victim = victim)


@app.route('/attack-type/', methods = ['GET', 'POST'])
def attackType():
	a = request.form.get("type")
	attack_type = (db.session.query(Incident.international,Incident.property_damage, BelongedTo.suicide_attack, BelongedTo.succussful_attack).
               join(BelongedTo, Incident.id == BelongedTo.incident_id).filter(BelongedTo.suicide_attack == a).all()) 
	attack_type =  pd.DataFrame(attack_type)
	Attack = attack_info(attack_type)
	return render_template("attack-type.html", Attack = Attack)

@app.route('/victim-type/')
def victimType():
	Victim = victim_damage(base_query)
	Victim2 = plot_victim(victim_type)
	Victim3 = victim_subtype(query_subtype)
	return render_template("victim-type.html", Victim = Victim, Victim2 = Victim2, Victim3 = Victim3)

@app.route('/weapon-type/')
def weaponType():
	Weapon = weapon(weapon_type)
	return render_template("weapon-type.html", Weapon = Weapon)
#	return render_template("weapon-type.html")

@app.route('/comments/')
def comments():
	return render_template("comments.html")

@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('type')
    return(str(select))

if __name__ == "__main__":
    app.run(host = "0.0.0.0")

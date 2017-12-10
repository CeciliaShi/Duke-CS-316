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
#from Ploty.attack_info import attack_type, attack_info
from Ploty.attack_info import attack_info
import Ploty.trend as trend
import Ploty.google_trend as GT

import pickle

plotly.tools.set_credentials_file(username=conf.pp_conf["username"], api_key=conf.pp_conf["api_key"])
db = SQLAlchemy(app, session_options={'autocommit': False})
countries = db.session.query(models.Location.country).distinct(models.Location.country).all()

def cache_tm(cache):
	'''
	world_map: trend_map default
	'''
	code = pd.read_csv("Ploty/code_correct.csv")  
	search_map = (db.session.query(GoogleTrend.year,GoogleTrend.month, GoogleTrend.weighted_avg, Location.country).
		filter(Incident.date.isnot(None)).
		join(Incident,and_(GoogleTrend.year == extract('year', Incident.date),GoogleTrend.month == extract('month', Incident.date))).
		join(Happened,Happened.incident_id == Incident.id).
		join(Location,and_(Location.latitude == Happened.latitude,Location.longitude == Happened.longitude))).all()

	search_map = pd.DataFrame(search_map)
	trend_map = gt_freq(search_map, code)

	cache["tm"] = trend_map

def cache_frequency(cache):
	'''
	world_map: frequency
	'''
	code = pd.read_csv("Ploty/code_correct.csv")  
	query_fq = (db.session.query(Location.country).
		join(Happened, and_(Location.latitude==Happened.latitude, Location.longitude == Happened.longitude)).all())
	query_fq = pd.DataFrame(query_fq)
	frequency= freq(query_fq,code)

	cache["frequency"] = frequency

def cache_at(cache):
	'''
	attack-type: Attack
	'''
	attack_type = (db.session.query(Incident.international, Incident.property_damage, BelongedTo.suicide_attack, BelongedTo.succussful_attack).
			   join(BelongedTo, Incident.id == BelongedTo.incident_id).all()) 
	attack_type =  pd.DataFrame(attack_type)
	Attack = attack_info(attack_type)

	cache["Attack"] = Attack

def cache_trend(cache):
	'''
	trend
	'''
	base_query = (db.session.query(extract('year',Incident.date), func.sum(Incident.nkill), func.sum(Incident.nwound)).
		filter(Incident.date.isnot(None)).group_by(extract('year', Incident.date)).
		order_by(extract('year',Incident.date))).all()
	trend_plot = trend.trend(base_query)

	cache['trend'] = trend_plot

def cache_vt(cache):
	'''
	victim-type
	'''
	victim_types = db.session.query(Targeted.victim_type).distinct(Targeted.victim_type).all()  
	victim_frequency_all = db.session.query(func.count(Targeted.incident_id).label('count'), Targeted.victim_type).group_by(Targeted.victim_type).order_by(func.count(Targeted.incident_id)).all()
	plot_victim = plot_victim_frequency(victim_frequency_all)
	cache["plot_victim"] = plot_victim

	victim_subtype = (db.session.query(Targeted.subtype, func.sum(Incident.nkill), func.sum(Incident.nwound))
				.filter(Targeted.victim_type=="Private Citizens & Property")
				.join(Targeted.incident)
				.group_by(Targeted.subtype)).all()
	plot_subtype = plot_victim_subtype(victim_subtype)

	cache["plot_subtype"] = plot_subtype

def cache_wt(cache):
	'''
	weapon-type
	'''
	weapon_type = (db.session.query(func.count(Used.incident_id).label('count'), Used.weapon_type,(func.sum(Incident.nkill)+func.sum(Incident.nwound)).label('fatality'))
		.join(Incident,Incident.id == Used.incident_id)
		.group_by(Used.weapon_type)
		.order_by(func.count(Used.incident_id).desc())).all()
	weapon_type = pd.DataFrame(weapon_type)
	Weapon = weapon(weapon_type)
	cache["Weapon"] = Weapon

def main():
	cache = {}
	cache_tm(cache)
	cache_frequency(cache)
	cache_at(cache)
	cache_trend(cache)
	cache_vt(cache)
	cache_wt(cache)
	with open("cache.pickle","wb") as f:
		pickle.dump(cache,f)

if __name__ == "__main__":
	main()


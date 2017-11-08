from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import models
import pandas as pd
## local scripts
from Ploty.kw import kill_wound
from Ploty.freq import freq
from Ploty.plot_victim import plot_victim, victim_type
from Ploty.query_freq import freq, fq
from Ploty.query_weapon_type import weapon, weapon_type

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
	return render_template("world-map.html", frequency = frequency)
#	return render_template("world-map.html", iframe = iframe, victim = victim)
#	return render_template("world-map.html", victim = victim)


@app.route('/attack-type/')
def attack_type():
	return render_template("attack-type.html")

@app.route('/victim-type/')
def victim_type():
	return render_template("victim-type.html")

@app.route('/weapon-type/')
def weapon_type():
	Weapon = weapon(weapon_type)
	return render_template("weapon-type.html")

@app.route('/comments/')
def comments():
	return render_template("comments.html")

@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('type')
    return(str(select))

if __name__ == "__main__":
    app.run()

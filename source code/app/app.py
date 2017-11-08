from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import models

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
	iframe = "https://plot.ly/~KimJin/0/550/550"
	return render_template("world-map.html", iframe = iframe)

@app.route('/comments/')
def comments():
	return render_template("comments.html")

if __name__ == "__main__":
    app.run()
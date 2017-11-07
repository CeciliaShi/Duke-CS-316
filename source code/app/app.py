from flask import Flask, render_template

app = Flask(__name__)

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
	return render_template("world-map.html")

@app.route('/comments/')
def comments():
	return render_template("comments.html")

if __name__ == "__main__":
    app.run()
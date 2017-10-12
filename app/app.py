from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/worldmap/')
def worldmap():
	return render_template("worldmap.html")

@app.route('/trend/')
def trend():
	return render_template("trend.html")

@app.route('/about-us/')
def about_us():
	return render_template("about-us.html")

@app.route('/comments/')
def comments():
	return render_template("comments.html")

if __name__ == "__main__":
    app.run()
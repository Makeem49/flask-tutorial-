from flask import Flask, request, make_response, abort, render_template

from flask_bootstrap import Bootstrap  #this is a flask-boostrap extension 
from flask_moment import Moment
from datetime import datetime

#initialization of Flask
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)



# Setting route & view function 
@app.route("/")  # setting static route
def index():
	return render_template("index.html",current_time=datetime.utcnow())

@app.route("/user/<name>")  # setting dynamic route
def user(name):
	# response = make_response('<h1>This document carries a cookie!</h1>') 
	return render_template('user.html', name = name)

@app.route('/login')
def login():
	return render_template("form.html", form=) 

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# Server set up 
if __name__ == "__main__":
	app.run(debug=True)







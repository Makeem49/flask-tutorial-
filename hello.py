from flask import Flask, render_template
from flask_bootstrap import Bootstrap




app = Flask(__name__)
bootstrap = Bootstrap(app) 


@app.route('/') 
def index():    
	return render_template('index.html', title = "home")

@app.route('/user/<name>') 
def user(name):    
	return render_template('user.html', name = name, title = "user")

@app.errorhandler(500) 
def page_not_found(e): 
	return render_template('500.html'), 500

@app.errorhandler(404) 
def page_not_found(e): 
	return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
from flask import render_template

from app.main import main

@main.app_errorhandler(500) 
def page_not_found(e): 
	db.session.rolback()
	return render_template('500.html', title = "Server Error"), 500

@main.app_errorhandler(404) 
def page_not_found(e): 
	return render_template('404.html', title = "Page Error"), 404






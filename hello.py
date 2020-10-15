from flask import Flask, render_template, url_for, redirect, session, flash
from flask_mail import Mail
from threading import Thread





app = Flask(__name__)


def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)




def send_mail(to, subject, template, **kwargs):
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
					sender = app.config['FLASKY_MAIL_SENDER'], recipients = [to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.txt', **kwargs)
	thr = Thread(target=send_async_email, args=[app,msg])
	thr.start()
	return thr
 

@app.route('/user/<name>') 
def user(name):    
	return render_template('user.html', name=name)



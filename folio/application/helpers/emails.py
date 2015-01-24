from flask import render_template
from flask.ext.mail import Message
from application import mail
from application import app
from decorators import async

@async
def send_async_email(msg):
    with app.app_context():
       mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)

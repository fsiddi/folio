from flask import render_template
from flask.ext.mail import Message
from application import mail
from application import app


def send_email(subject, sender, text):
    SENDMAIL = "/usr/sbin/sendmail" # sendmail location 
    TO = app.config['user_email']
    # Prepare actual message 
    message = """From: {0} 
To: {1}
Subject: {2}
{3}
""".format(sender, TO, subject, text) 

    print message
    # Send the mail 
    import os 
    p = os.popen("{0} -t -i {1}".format(SENDMAIL, TO), "w") 
    p.write(message) 
    status = p.close() 
    if status: 
        print "Sendmail exit status", status 


from application import app
from application.modules.theme import get_theme_dir

from flask import request
from flask import render_template
from flask import redirect
from flask import flash
from flask import url_for

from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import validators

from application.helpers.emails import send_email


class ContactForm(Form):
    # name = StringField('Name', [
    #     validators.InputRequired()
    # ])
    email = StringField('Email', [
        validators.InputRequired(),
        validators.Length(min=6, message='Too short'),
        validators.Email(message='A valid email address is required')
    ])
    subject = StringField('Subject', [
        validators.Length(max=78, message='Limited to 78 characters')
    ])
    content = TextAreaField('Content', [
        validators.InputRequired()
    ])


@app.route('/contact', methods=('GET', 'POST'))
def contact():
    form = ContactForm(request.form)

    if request.method == 'POST' and form.validate():
        send_email(form.subject.data, form.email.data, form.content.data)
        flash('Your email has been sent successfully. Thanks!', 'success')
        return redirect(url_for('contact'))

    return render_template(
        get_theme_dir() + '/contact.html',
        form=form,
        title='contact')

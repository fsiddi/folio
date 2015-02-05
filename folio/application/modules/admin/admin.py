from functools import wraps
import os
import os, hashlib, time
import os.path as op
from werkzeug import secure_filename

from flask import request, Response, render_template, redirect, url_for, Markup
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import Form, form, fields, validators, TextField, TextAreaField
from wtforms.validators import DataRequired

from sqlalchemy import event

from application import app
from application import db

from application.modules.main.model_user_settings import User
from application.modules.main.model_user_settings import Setting
from application.modules.main.model_projects import Category
from application.modules.main.model_projects import Project
from application.modules.main.model_projects import Picture

from flask.ext import admin, login
from flask.ext.admin import helpers, expose, BaseView
from flask.ext.admin import form as admin_form
from flask.ext.admin.form import RenderTemplateWidget
from flask.ext.admin.model.form import InlineFormAdmin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import filters, ModelView
from flask.ext.admin.contrib.sqla.form import InlineModelConverter
from flask.ext.admin.contrib.sqla.fields import InlineModelFormList
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.login import current_user, UserMixin


class SettingsForm(Form):
    folio_theme = TextField('Theme', validators=[DataRequired()])
    folio_title = TextField('Title', validators=[DataRequired()])
    folio_footer = TextField('Footer', validators=[DataRequired()])
    folio_bio = TextAreaField('Short Bio', validators=[DataRequired()])
    google_analytics_id = TextField('Google Analytics', validators=[DataRequired()])

# Create directory for file fields to use
file_path = app.config['MEDIA_FOLDER']
try:
    os.mkdir(file_path)
except OSError:
    pass

def prefix_name(obj, file_data):
    # Collect name and extension
    parts = op.splitext(file_data.filename)
    # Get current time (for unique hash)
    timestamp = str(round(time.time()))
    # Has filename only (not extension)
    file_name = secure_filename(timestamp + '%s' % parts[0])
    # Put them together
    full_name = hashlib.md5(file_name).hexdigest() + parts[1]
    return full_name

def _list_thumbnail(view, context, model, name):
    if not getattr(model,name):  #model.name only does not work because name is a string
        return ''
    return Markup('<img src="%s">' % url_for('filemanager.static', filename=admin_form.thumbgen_filename(getattr(model,name))))


# Register after_delete handler which will delete image file after model gets deleted
@event.listens_for(Picture, 'after_delete')
def _handle_image_delete(mapper, conn, target):
    try:
        if target.path:
            os.remove(op.join(file_path, target.path))
    except:
        pass


# This widget uses custom template for inline field list
class CustomInlineFieldListWidget(RenderTemplateWidget):
    def __init__(self):
        super(CustomInlineFieldListWidget, self).__init__('admin/field_list.html')


# This InlineModelFormList will use our custom widget
class CustomInlineModelFormList(InlineModelFormList):
    widget = CustomInlineFieldListWidget()


# Create custom InlineModelConverter and tell it to use our InlineModelFormList
class CustomInlineModelConverter(InlineModelConverter):
    inline_field_list_type = CustomInlineModelFormList


# Customized inline form handler
class InlineModelForm(InlineFormAdmin):
    form_excluded_columns = ('path',)

    form_label = 'Image'

    def __init__(self):
        return super(InlineModelForm, self).__init__(Picture)

    def postprocess_form(self, form_class):
        form_class.upload = fields.FileField('Image')
        return form_class

    def on_model_change(self, form, model):
        file_data = request.files.get(form.upload.name)

        if file_data:
            model.path = prefix_name(None, file_data)
            file_data.save(op.join(file_path, model.path))


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        # return db.session.query(User).filter_by(login=self.login.data).first()
        return User.get(self.login.data)


image_upload_field = admin_form.ImageUploadField('Image',
                    base_path=file_path,
                    thumbnail_size=(100, 50, True),
                    namegen=prefix_name,
                    endpoint='filemanager.static')


class SettingsView(BaseView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = SettingsForm()

        if request.method == 'POST' and form.validate():
            for fieldname, fieldvalue in form.data.items():
                setting = Setting.query.filter_by(name=str(fieldname)).one()
                setting.value = str(fieldvalue)
                db.session.add(setting)
            db.session.commit()
            return redirect(url_for('.index'))

        form.folio_theme.data = Setting.query.filter_by(name='folio_theme').one()
        form.folio_title.data = Setting.query.filter_by(name='folio_title').one()
        form.folio_footer.data = Setting.query.filter_by(name='folio_footer').one()
        form.folio_bio.data = Setting.query.filter_by(name='folio_bio').one()
        form.google_analytics_id.data = Setting.query.filter_by(name='google_analytics_id').one()
        return self.render('admin/settings.html', form=form)


class DesignView(BaseView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

    @expose('/')
    def index(self):
        return self.render('admin/design.html')




# Create customized views with access restriction
class CustomModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()


    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class ProjectView(CustomModelView):
    column_list = ('name', 'url', 'picture')
    column_formatters = { 'picture': _list_thumbnail }
    form_extra_fields = {'picture': image_upload_field}

    inline_model_form_converter = CustomInlineModelConverter
    inline_models = (
        InlineModelForm(),
    )


# Create admin
admin = admin.Admin(
    app,
    'Backfolio',
    index_view=MyAdminIndexView(),
    base_template='admin/layout_admin.html')

# Add views
admin.add_view(CustomModelView(Category, db.session))
admin.add_view(ProjectView(Project, db.session))
admin.add_view(CustomModelView(Setting, db.session))
admin.add_view(SettingsView(name='General', endpoint='settings', category='Settings'))
admin.add_view(DesignView(name='Design', endpoint='design', category='Settings'))
admin.add_view(FileAdmin(file_path, '/static/files/', name='Static Files'))



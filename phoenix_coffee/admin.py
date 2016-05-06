from phoenix_coffee import app
from flask import flash, redirect, url_for, render_template,request
from wtforms import Form, StringField, TextAreaField, SubmitField, BooleanField, form, fields, validators
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

#Create the user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


#Define authentication (Flask-Login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()

#Initialise login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


#Allow access to model
class ModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


#Create class for login page
class AdminPannel(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login'))
        return super(AdminPannel, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(AdminPannel, self).index()


    @expose('/logout/')
    def logout(self):
        login.logout_user()
        return redirect(url_for('.index'))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    message = db.Column(db.Text)
    mailing = db.Column(db.Integer)

    def __unicode__(self):
        return self.username

class Mailing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)

    def __unicode__(self):
        return self.username

#Initialise Flask-Login
init_login()

#Create admin instance
admin = admin.Admin(app, name='Phoenix Coffee Admin', index_view=AdminPannel(), template_mode='bootstrap3')

#Add models to views
admin.add_view(ModelView(Contact, db.session, name='Contact Form', endpoint='contact'))
admin.add_view(ModelView(User, db.session, name='Users', endpoint='users'))
admin.add_view(ModelView(Mailing, db.session, name='Mailing', endpoint='Mailing'))
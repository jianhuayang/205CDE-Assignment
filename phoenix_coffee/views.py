from phoenix_coffee import app
from flask import flash, redirect, url_for, render_template,request
from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, TextAreaField, SubmitField, form, fields, validators
from wtforms.validators import DataRequired, Length, Email
from flask_mail import Mail, Message
import sqlite3
import os
from flask_wtf import Form
import os.path as op
from flask_sqlalchemy import SQLAlchemy
from wtforms import validators
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)
Bootstrap(app)
mail = Mail(app)

class ContactForm(Form):
    name = StringField('Name:', validators=[DataRequired(), Length(min=5)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    message = TextAreaField('Message:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('index.html', banner="static/img/slider_1.jpg", title='Home')

@app.route('/about')
def about():
    return render_template('about.html', banner="static/img/slider_2.jpg", title='About' )

@app.route('/coffee')
def coffee():
    return render_template('coffee.html', banner="static/img/slider_3.jpg", title='Coffee')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        msg = Message("Website Contact Form Message From " + form.name.data,
                      sender='website@benjaminbogdanovic.co.uk',
                      recipients=['test@benjaminbogdanovic.co.uk'])
        msg.body = """
        From: %s
        Email: %s
        Message: %s
        """ % (form.name.data, form.email.data, form.message.data)
        mail.send(msg)
        flash("Message sent!")
        with sqlite3.connect(app.config['DATABASE']) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO contact (name, email, message) VALUES (?,?,?)", (name, email, message))
            con.commit()    
    return render_template('contact.html', banner="static/img/slider_4.jpg", title='Contact', contact=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='Page Not Found'), 404

# Create user model.
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


# Define login and registration forms (for flask-login)
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

# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Create customized model view class
class ModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized index view class that handles login & registration
class AdminPannel(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(AdminPannel, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
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
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    message = db.Column(db.Text)

    def __unicode__(self):
        return self.username

# Initialize flask-login
init_login()

# Create admin
admin = admin.Admin(app, name='Phoenix Coffee Admin', index_view=AdminPannel(), template_mode='bootstrap3')

# Add views
admin.add_view(ModelView(Contact, db.session, name='Contact Form', endpoint='contact'))
admin.add_view(ModelView(User, db.session, name='Users', endpoint='users'))
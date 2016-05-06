from phoenix_coffee import app
from flask import flash, redirect, url_for, render_template,request
from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, TextAreaField, SubmitField, BooleanField, form, fields, validators
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import Form
from flask_mail import Mail, Message
import sqlite3

Bootstrap(app)
mail = Mail(app)

#Create the user model
class ContactForm(Form):
    name = StringField('Name:', validators=[DataRequired(), Length(min=5, max=100)])
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(min=5, max=150)])
    message = TextAreaField('Message:', validators=[DataRequired()])
    mailing = BooleanField('Receive Newsletter:')
    submit = SubmitField('Submit')

#URL routing
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
    #Validation
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        mailing = form.mailing.data
        #Flask-Mail
        msg = Message("Website Contact Form Message From " + form.name.data,
                      sender='website@benjaminbogdanovic.co.uk',
                      recipients=['test@benjaminbogdanovic.co.uk'])
        msg.body = """
        From: %s
        Email: %s
        Message: %s
        Mailing: %s
        """ % (form.name.data, form.email.data, form.message.data, form.mailing.data)
        mail.send(msg)
        flash("Message sent!")
        #Add to database
        with sqlite3.connect(app.config['DATABASE']) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO contact (name, email, message, mailing) VALUES (?,?,?,?)", (name, email, message, mailing))
            con.commit()    
    return render_template('contact.html', banner="static/img/slider_4.jpg", title='Contact', contact=form)
#Error handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', banner="img/slider_1.jpg", title='Page Not Found'), 404

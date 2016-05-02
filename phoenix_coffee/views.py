from phoenix_coffee import app
from flask import flash, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_mail import Mail, Message
import sqlite3
import os

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
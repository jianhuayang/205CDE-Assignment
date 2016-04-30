from flask import Flask, flash, redirect, url_for, render_template
import os
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
import sqlite3

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'coffee.db'),
    SECRET_KEY='phoenix'
))
Bootstrap(app)

class ContactForm(Form):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    message = TextAreaField('Message:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('index.html', banner="/static/img/slider_1.jpg")

@app.route('/about')
def about():
    return render_template('about.html', banner="/static/img/slider_2.jpg")

@app.route('/coffee')
def coffee():
    return render_template('coffee.html', banner="/static/img/slider_3.jpg")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        flash("Message sent!")
        with sqlite3.connect(app.config['DATABASE']) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO contact (name, email, message) VALUES (?,?,?)", (name, email, message))
            con.commit()    
    return render_template('contact.html', banner="/static/img/slider_4.jpg", contact=form)

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
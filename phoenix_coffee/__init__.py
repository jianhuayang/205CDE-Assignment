from flask import Flask
import sqlite3
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'coffee.db'),
    SECRET_KEY='phoenix'
))

app.config['MAIL_SERVER'] = 'mail.benjaminbogdanovic.co.uk'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'test@benjaminbogdanovic.co.uk'
app.config['MAIL_PASSWORD'] = 'tempemail'

app.config['DATABASE_FILE'] = 'coffee.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

import phoenix_coffee.views
import phoenix_coffee.admin
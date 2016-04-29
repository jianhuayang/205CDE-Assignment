from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', banner="/static/img/slider_1.jpg", title="Home")

@app.route('/about')
def about():
    return render_template('about.html', banner="/static/img/slider_2.jpg", title="About")

@app.route('/coffee')
def coffee():
    return render_template('coffee.html', banner="/static/img/slider_3.jpg", title="Coffee")

@app.route('/contact')
def contact():
    return render_template('contact.html', banner="/static/img/slider_4.jpg", title="Contact")

if __name__ == '__main__':
    Bootstrap(app)
    app.run(port=8080, host='0.0.0.0', debug=True)
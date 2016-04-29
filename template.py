from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
def nominee():
    return render_template('index.html')

if __name__ == '__main__':
    Bootstrap(app)
    app.run(port=8080, host='0.0.0.0', debug=True)
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route('/binance')
def binance():
    return render_template('binance.html', title="Binance")
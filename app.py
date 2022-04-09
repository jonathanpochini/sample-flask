from flask import Flask
from flask import render_template
import jon_functions as jon

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route('/binance')
def binance():
    watchlist = jon.check_the_watchlist()
    return render_template('binance.html', title="Binance", posts=watchlist)
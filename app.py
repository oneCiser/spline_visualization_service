##Flask packages
from flask import Flask


##App packages
## Import the routes of the app
from src.routes.route import splines


##Initialize the app
app = Flask(__name__)


##Register the routes of the app
app.register_blueprint(splines)
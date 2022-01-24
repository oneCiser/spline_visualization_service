##Flask packages
from flask import  Blueprint
from flask_restful import Api

##Controller packages
from ..controllers.spline import SplineController


##Initialize the blueprint
splines = Blueprint('splines', __name__)

##Initialize the api
api = Api(splines)

##Register the controllers of the app in the api
api.add_resource(SplineController, '/api/splines/', endpoint='splines_route')
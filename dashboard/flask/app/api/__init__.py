from flask import Blueprint
from flask_restful import Api

from app.api.resources import StartHping, StartGoldenEye, StartHULK, StartLOIC, StartSlowloris, Stop

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

# ======== Routes
api.add_resource(StartHping, '/<string:partner>/start/hping')
api.add_resource(StartGoldenEye, '/<string:partner>/start/goldeneye')
api.add_resource(StartHULK, '/<string:partner>/start/hulk')
api.add_resource(StartLOIC, '/<string:partner>/start/loic')
api.add_resource(StartSlowloris, '/<string:partner>/start/slowloris')
api.add_resource(Stop, '/<string:partner>/stop')
# ========

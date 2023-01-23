import os

from dotenv import find_dotenv, load_dotenv
from flask import Blueprint
from flask_restful import Api

from app.api.resources import StartHping, generate_attack_resource, Stop

load_dotenv(find_dotenv('dashboard.env'))

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

# ======== Routes
api.add_resource(StartHping, '/<string:organization>/start/hping')
for attack_name in os.getenv('ATTACKS').split(':'):
    api.add_resource(generate_attack_resource(attack_name), f'/<string:organization>/start/{attack_name}')
api.add_resource(Stop, '/<string:organization>/stop')
# ========

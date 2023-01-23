import os
from flask import Blueprint, render_template, abort

website_blueprint = Blueprint('website', __name__, template_folder='templates', static_folder='static')


@website_blueprint.route('/')
def home():
    return render_template('home.html', organizations=os.getenv('ORGANIZATIONS').split(':'))


@website_blueprint.route('/<string:organization>')
def dashboard(organization: str):
    if organization.lower() not in [p.lower().replace(' ', '-') for p in os.getenv('ORGANIZATIONS').split(':')]:
        return abort(404)
    return render_template('dashboard.html',
                           organization=organization.lower(),
                           fqdn=os.getenv('FQDN'),
                           attacks=os.getenv('ATTACKS').split(':'))


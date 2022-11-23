import os
from flask import Blueprint, render_template, abort

website_blueprint = Blueprint('website', __name__, template_folder='templates', static_folder='static')


@website_blueprint.route('/')
def home():
    return render_template('home.html', partners=os.getenv('PARTNERS').split(':'))


@website_blueprint.route('/<string:partner>')
def dashboard(partner: str):
    if partner.lower() not in [name.lower().replace(' ', '-') for name in os.getenv('PARTNERS').split(':')]:
        abort(404)
    return render_template("dashboard.html", partner=partner.upper(), fqdn=os.getenv('FQDN'))


import os
from flask import Blueprint, render_template, abort

website_blueprint = Blueprint('website', __name__, template_folder='templates', static_folder='static')


@website_blueprint.route('/')
def home():
    return render_template('home.html', partners=os.getenv('PARTNERS').split(':'))


@website_blueprint.route('/<string:partner>')
def dashboard(partner: str):
    print(partner)
    if partner not in os.getenv('PARTNERS').split(':'):
        abort(404)
    return render_template("dashboard.html", partner=partner, fqdn=os.getenv('FQDN'))


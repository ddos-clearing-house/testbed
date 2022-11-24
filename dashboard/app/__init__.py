import os
from flask import Flask, redirect
from flask_cors import CORS
from dotenv import load_dotenv

from app.website import website_blueprint
from app.api import api_blueprint

load_dotenv()
app = Flask(__name__, subdomain_matching=True)
CORS(app)  # CORS normally handled by NGINX. For local deployment we need to do it here.
app.config['SERVER_NAME'] = os.getenv('FQDN')

app.register_blueprint(website_blueprint, subdomain='www')  # Dashboard
app.register_blueprint(api_blueprint, subdomain='api')  # API


@app.errorhandler(404)
def page_not_found(error):
    return redirect(f"http://www.{app.config['SERVER_NAME']}")

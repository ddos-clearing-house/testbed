from flask import Flask, redirect

from app.website import website_blueprint
from app.api import api_blueprint

app = Flask(__name__, subdomain_matching=True)
app.config['SERVER_NAME'] = 'ddosclearinghouse.eu'

app.register_blueprint(website_blueprint, subdomain='www')  # Dashboard
app.register_blueprint(api_blueprint, subdomain='api')  # API


@app.errorhandler(404)
def page_not_found(error):
    return redirect(f"https://www.{app.config['SERVER_NAME']}")

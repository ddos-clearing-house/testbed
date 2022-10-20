# Dashboard

This is the dashboard from which simulated attacks can be started (and stopped).

Each connected organization has their own dashboard at `/$name`. Through this dashboard, a partner can start and stop attack traffic to their own designated target machine.
Organizations can reach their dashboard only with IP whitelist and HTTP Basic Auth credentials.

## Architecture
The dashboard is a Flask application with a Flask RESTful API which functions as the interface between the dashboard
and ansible playbooks that start or stop an attack on the attack nodes. 
The website is hosted in docker containers using docker-compose. The compose configuration lists
the following services:
- flask: the Flask application with the dashboard and API
- nginx: the nginx webserver
- certbot: ensures the SSL certificate
- ipv6nat: helper container to allow IPv6 connections. Assigns an IPv6 address to each container.

Make sure docker and docker-compose are installed on the system, then run `docker-compose up -d --build` in this directory.

### Flask
The entrypoint to the Flask application is [run.py](/flask/run.py). The application is served with uWSGI using 
instructions in [app.ini](/flask/app.ini).
The application consists of a Flask application that hosts the webpages (home page and dashboards for each
partner), and a Flask RESTful API, which serves as an interface between the Flask application and the ansible playbooks.
[app/](/flask/app) contains one module for the website and one for the api. The [\_\_init__.py](/flask/app/__init__.py)
binds these two to the www and api subdomains respectively. 

From the dashboard, the start and stop buttons send a request to the API with the given instructions though a simple 
XMLHttpRequest in [the dashboard's javascript](/flask/app/website/static/js/content.js).

#### dashboard.env
[dashboard.env](dashboard.env.sample) contains the environment variables required by the flask container. 
`PARTNERS` is a list of names of connected organizations, separated by a colon (`:`), e.g. PARTNERS=SIDN:SURF. 
Then, for each defined partner `X`, add a variable `X_TARGET` that is that organization's target IP address or DNS name.
E.g., `SIDN_TARGET=sidn.nl`, `SURF_TARGET=1.2.3.4`.

### Nginx
The application is secured with IP-whitelisting and HTTP Basic authentication in the 
[nginx config](/nginx/nginx.conf.sample). For each partner, create a `location` block in the configuration. Copy an existing
one as a template. Search and replace the domainname `ddosclearinghouse.eu` if you will use a different domain.
Whitelist the IP addresses from where the dashboard should be available. Add all IP addresses to the `location /` block 
at the end of the file.

To setup the HTTP Basic Authentication, create a configuration using `htpasswd -c name.htpasswd name`, where `name` is the 
name of the connected organization. Create the configuration in the nginx directory, and add it to the location block of 
the corresponding organization in the nginx config.

### SSL/TLS certificate (certbot)
Easily obtain a certificate with Let's encrypt and certbot using [this repository](https://github.com/wmnnd/nginx-certbot)
Copy the resulting `/data/certbot` directory to this directory (such that `/certbot` is next to `/flask`). 
Remember to bring down the docker containers when you're done. 

## Dashboard instructions
[Visit the dashboard homepage](https://www.ddosclearinghouse.eu) --> select your dashboard --> Login with HTTP basic 
auth --> enter attack details --> start / stop the simulated attack --> login with HTTP basic auth again 
(for api.domainname, doubles as confirmation).
# Dashboard

This is the dashboard from which simulated attacks can be started (and stopped).

The dashboard is hosted at [ddosclearinghouse.eu](https://www.ddosclearinghouse.eu). Each partner has their own 
dashboard at /partnername. Through this dashboard, a partner can start and stop attack traffic to their own 
target machine (located in a test network which is not critical to operations).

## Documentation
The dashboard is a Flask application with a Flask RESTful API which functions as the interface between the dashboard
and attack scripts. The website is hosted in docker containers using docker-compose. The compose configuration lists
the following services:
- flask: the Flask application with the dashboard and API
- nginx: the nginx webserver
- certbot: ensures validity of the SSL certificate
- ipv6nat: helper container to allow IPv6 connections. Assigns an IPv6 address to each container.

Make sure docker and docker-compose are installed on the system. After setting everything up, cd to this directory and 
run `docker-compose up -d --build`.

### Flask
The entrypoint to the Flask application is [run.py](/flask/run.py). The application is served with uWSGI using 
instructions in [app.ini](/flask/app.ini).\
The application consists of a generic Flask application which hosts the webpages (home page and dashboards for each
partner), and a Flask RESTful API, which serves as an interface between the Flask application and the attack scripts.
[app/](/flask/app) contains one module for the website and one for the api. The [\_\_init__.py](/flask/app/__init__.py)
binds these two to the www and api subdomains respectively. 

From the dashboard, the start and stop buttons send a request to the API with the given instructions though a simple 
XMLHttpRequest in [the dashboard's javascript](/flask/app/website/static/js/content.js).

The API runs the entrypoint script (located in the attack-scripts directory in this repository) from its end points
defined in [app/api/resources](/flask/app/api/resources.py). The API passes the required arguments to the entrypoint, 
which starts the attack script on the attack source machines (defined by $SOURCE_IPS in [dashboard.env](dashboard.env.sample))

#### dashboard.env
[dashboard.env](dashboard.env.sample) should contain the environment variables required by the flask container. 
SOURCE_IPS is a list of IP addresses from the attack source machines, separated by a colon (`:`). PARTNERS is a list of 
partners in the pilot, separated by a colon (`:`). The partners defined here will have a dashboard in the flask 
application (www.domain/partner). remove the suffix `.sample` from the provided file. 

### Nginx
The application is secured with IP-whitelisting and HTTP Basic authentication in the 
[nginx config](/nginx/nginx.conf). For each partner, create a `location` block in the configuration. Copy an existing
one as a template. Search and replace the domainname `ddosclearinghouse.eu` if you will use a different domain.

### SSL/TLS certificate (certbot)
Easily obtain a certificate with Let's encrypt and certbot using [this repository](https://github.com/wmnnd/nginx-certbot)
Copy the resulting /data/certbot directory to this directory (such that /certbot is next to /flask)

### Filesystem details
The dashboard should be ran on a linux system by user "admin" (which should be added to the docker group). 
The attack scripts in `attack-scripts` in the root of the repository should be available in `/home/admin/attacks`.

Create a directory /home/admin/ips. For each partner defined in [dashboard.env](dashboard.env.sample), create a file
with the name of that partner (lowercase, no extension) which contains only the IP address of that partner.\
E.g.: `mkdir ~/ips ; echo -n "192.168.0.100" > ~/ips/sidnlabs`

Communication with the attack source machines happens through SSH with ssh keys. Make sure each attack source machine 
is reachable through SSH using ssh keys. (copy /home/admin/.ssh/id_rsa.pub to the source machine's 
/home/admin/.ssh/authorized_keys)

## Dashboard instructions
[Visit the dashboard homepage](https://www.ddosclearinghouse.eu) --> select your dashboard --> Login with HTTP basic 
auth --> enter attack details --> start / stop the simulated attack --> login with HTTP basic auth again 
(for api.domainname, doubles as confirmation).
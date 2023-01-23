# Dashboard

This is the dashboard from which simulated attacks can be started (and stopped).

Each connected organization has their own dashboard at `/$name`. Through this dashboard, a organization can start and stop attack traffic to their own designated target machine.
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
organization), and a Flask RESTful API, which serves as an interface between the Flask application and the ansible playbooks.
[app/](/flask/app) contains one module for the website and one for the api. The [\_\_init__.py](/flask/app/__init__.py)
binds these two to the www and api subdomains respectively. 

From the dashboard, the start and stop buttons send a request to the API with the given instructions though a simple 
XMLHttpRequest in [the dashboard's javascript](/flask/app/website/static/js/content.js).

#### dashboard.env
[dashboard.env](dashboard.env.sample) contains the environment variables required by the flask container. 
`FQDM` is the fully-qualified domain name on which the dashboard is hosted (use localhost to test locally).
`ORGANIZATIONS` is a list of names of connected organizations, separated by a colon (`:`), e.g. ORGANIZATIONS=SIDN:SURF. 
Then, for each defined organization `X`, add a variable `X_TARGET` that is that organization's target IP address or DNS name.
E.g., `SIDN_TARGET=sidn.nl`, `SURF_TARGET=1.2.3.4`. Be sure to remove the .sample extension and edit dashboard.env

### Nginx
The application is secured with IP-whitelisting and HTTP Basic authentication in the 
[nginx config](/nginx/nginx.conf.sample). For each organization, create a `location` block in the configuration. Copy an existing
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

## How to run the dashboard
1. Edit dashboard.env to match your setup (see dashboard.env section above)
2. Edit the Nginx config to use your domain name and your dashboard users (see Nginx section above)
3. Generate TLS certificate following the instruction above
4. in this directory, run `docker-compose up -d --build`

## Adding a new organization
1. Edit [dashboard.env](dashboard.env.sample) to include the new organization/user in the list of ORGANIZATIONS, and define a target variable, following the same format as in the template.
2. Create HTTP Basic Authentication credentials in the nginx directory for the new user, using `htpasswd -c user.htpasswd user`
3. Edit the Nginx configuration to create a location block for the new organization. copy an existing one as template and edit the IP whitelist and HTTP basic auth file location. Also add the whitelisted IP addresses to the `location /` block.
4. Restart the dashboard (`docker-compose up -d --build`)
5. If needed, force-recrease the Nginx container (`docker-compose restart nginx`)

## Adding a new attack (dashboard part)
1. Setup the ansible playbook following the instructions in the corresponding [README](../ansible/README.md#Adding-a-new-attack-(Ansible-part)).
2. Add the name of the attack (and the name of the playbook without file extension) to [dashboard.env](dashboard.env.sample) in the `ATTACKS` list (`:`-separated)
3. rebuild and deploy using docker-compose.
# DDoS Clearing House distributed testbed

The DDoS Testbed is a platform with which DDoS attacks can be simulated with a small volume. 
It was orginally developed to pilot the DDoS Clearing House without the need for datasharing agreements or liability waivers. 
You can read about it in our [blog1](https://www.sidnlabs.nl/en/news-and-blogs/developing-and-running-a-testbed-for-the-ddos-clearing-house), [blog2](https://www.sidnlabs.nl/en/news-and-blogs/push-the-button-our-updated-ddos-testbed-in-action-at-concordia-open-door-2022).

Since its development the pilots of the DDoS Clearing House in The Netherlands and Italy have picked up traction.
Now the DDoS Testbed is mainly used to demonstrate the DDoS Clearing House and as a playground for small-scale DDoS drills and attack fingerprinting.

The testbed consists of 
1. A web-based dashboard
2. VMs that simulate attack nodes in a botnet
3. Ansible playbooks that connect the dashboard to the attack nodes

## 1. Run dashboard locally

The dashboard is a Flask application on which partners can initiate (and stop) a simulated attack on **themselves**. 

To run the dashboard locally (not connected to the internet), follow these instructions in the dashboard directory:
1. Create a python virtual environment and activate it: `python3 -m venv venv && source venv/bin/activate`
2. Install the python dependencies: `pip install --upgrade pip && pip install wheel && pip install -r requirements.txt` 
3. Copy the .env.example to .env and edit it with your details: `cp .env.example .env`
   1. Pick a local FQDN (like ddos.local), and keep the port :8989 in the .env
   2. Edit yout `/etc/hosts` to point the FQDN to 127.0.0.1: `127.0.0.1 ddos.local www.ddos.local api.ddos.local`
   3. Add all organizations on the testbed to the PARTNERS environment variable, separated by `:`
   4. For each added organization `X`, add an environment variable `X_TARGET` that points to the target server of that organization (IP address or DNS name)
4. In the ansible directory (`../ansible`), edit the `inventory` file to list the attacker servers under the [attackers] block (IP addresses or DNS names). e.g.:
   ```ini
   [attackers]
   172.17.0.2
   attacker.somesite.net
   ```
5. In the dashboard directory, run the dashboard with `python run.py` and visit at http://ddos.local:8989   
6. Follow the rest of this README. Any changes require a restart of the dashboard.

## 2. Attack nodes

We use 5 small VMs located across the world to send DDoS traffic to a specified target on the testbed. The nodes 
are set up and instructed using ansible. See the [ansible directory](/ansible) for the set up scripts and attack commands.

## 3. Ansible

[Ansible](https://www.ansible.com/) is a tool used mainly to automate the deployment and instruction of multiple systems simultaneously. 
The testbed uses Ansible to setup the attack nodes and to provide them the instructions to start or stop an attack.

## Setup attack nodes

The attack node setup is done using Ansible; follow this instructions in the corresponding [README](ansible/README.md).

## Adding a partner (user) on the testbed
Follow the instructions in the [dashboard's README](dashboard/README.md).

## Adding a new attack
1. Follow instructions for the [ansible part](ansible/README.md#Adding-a-new-attack-(Ansible-part)).
2. Follow instructions for the [dashboard part](dashboard/README.md#Adding-a-new-attack-(dashboard-part)). 
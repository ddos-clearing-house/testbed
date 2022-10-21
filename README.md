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

## 1. [Dashboard](/dashboard)

The dashboard is a Flask application on which partners can initiate (and stop) a simulated attack on **themselves**. 
It is hosted in docker containers using docker-compose. 
See the [readme](dashboard/README.md) for more information and instructions.

## 2. Attack nodes

We use 5 small VMs located across the world to send DDoS traffic to a specified target on the testbed. The nodes 
are set up and instructed using ansible. See the [ansible directory](/ansible) for the set up scripts and attack commands.

## 3. Ansible

[Ansible](https://www.ansible.com/) is a tool used mainly to automate the deployment and instruction of multiple systems simultaneously. 
The testbed uses Ansible to setup the attack nodes and to provide them the instructions to start or stop an attack.

## Setup attack nodes

The attack node setup is done using Ansible; follow this instructions in the corresponding [README](ansible/README.md).

## Adding a partner (user) on the testbed
...

## Adding a new attack
...
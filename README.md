# DDoS Clearing House distributed testbed

This project contains the setup for a simulated pilot between the hosting partners of a DDoS Clearing House. \
For this purpose we have developed a testbed on which we can pilot the Clearing House. You can read about it in our [blog](https://www.sidnlabs.nl/en/news-and-blogs/developing-and-running-a-testbed-for-the-ddos-clearing-house).


### [Dashboard](/dashboard)

The dashboard is a Flask application on which partners can initiate (and stop) a simulated attack on themselves. It is hosted in docker containers using docker-compose. See the [readme](dashboard/README.md) for more information and instructions.


### Attack nodes

We make use of 5 small VMs located across the world to send DDoS traffic to a specified target on the testbed. The nodes 
are set up and instructed using ansible. See the [ansible directory](/ansible) for the set up scripts and attack commands.
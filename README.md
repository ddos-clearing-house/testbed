# DDoS Clearing House distributed testbed

This project contains the setup for a simulated pilot between the hosting partners of a DDoS Clearing House. \
For this purpose we have developed a testbed on which we can pilot the Clearing House


### [Dashboard](/dashboard)

The dashboard is a Flask application on which partners can initiate (and stop) a simulated attack on themselves. It is hosted in docker containers using docker-compose. See the readme in this directory for more information and instructions.


### [Attack scripts](/attack-scripts)

This directory contains scripts for various attacks (using hping3), as well as an entrypoint for the dashboard. Its contents should be available on an attack source machine at `/home/admin/attacks`.

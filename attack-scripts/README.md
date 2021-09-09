# Attack scripts

This directory contains the scripts that "simulate" various DOS attacks using the hping3 package.

### Entrypoint
[entrypoint](entrypoint) is the script which is called from the Flask API in the docker container (see the dashboard 
directory in the repository root). This script takes five parameters:
1. Hping flags: the flags for a particular attack using hping3
2. Partner name: passed implicitly from the partner's dashboard
3. Duration: duration of the attack in seconds
4. Port: the port to which to send the attack traffic
5. Speed: the speed (volume) of the attack, passed as the u+\[number of microseconds between packets] (e.g. u1000 for 
   100 packets/s)
   
The parameters are selected by the user on the dashboard and passed through the Flask API to this entrypoint. The 
entrypoint will start hping3 on the attack source machines (defined in dashboard.env in the dashboard 
directory in this repository) through SSH.

### Stop
[stop](stop) is the script that will stop any traffic coming from the attack source machines (kills the hping3 
processes). This is called directly from the Flask API in the docker container (see the dashboard directory in the 
repository root). Like the entrypoint script, it uses SSH to run a command on each attack source machine.

## Attack source machines

Each attack source machine should be configured to have the following:
- hping3 installed (`sudo apt install hping3`)
- a user named _admin_
- /home/admin/.ssh/authorized_keys containing the public ssh key of the dashboard server to allow ssh login without password from the dashboard 
  server
- Make sure _admin_ can run hping3 (`admin$ sudo chmod u+x /usr/sbin/hping3 && ln -s /usr/sbin/hping3 /usr/bin/hping3`)
- The contents of this directory should be executable by _admin_ in `/home/admin/attacks`

Add the IP address of the attack source machine to dashboard.env on the server hosting the dashboard.

# Ansible

## Setup attack nodes

1. Create (virtual) machines that will function as attacking nodes. Preferably using Ubuntu (or Debian).
2. Prepare the VMs for further setup with ansible by running the following commands as root (or run this as a startup script):

```bash
# Add ansible user with passwordless sudo access
adduser --disabled-password --gecos "" ansible
echo "ansible:nopass" | chpasswd
adduser ansible sudo
echo "ansible ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers

# Setup ssh and ssh keys (insert your key(s))
mkdir /home/ansible/.ssh
cat >> /home/ansible/.ssh/authorized_keys << EOF

# SSH key for dashboard server (required)
ssh-rsa AAA....etc
# SSH public key for administration
ssh-rsa AAA....etc

EOF

# Disallow root or password login and restart sshd
cd /etc/ssh/sshd_config.d
echo "PermitRootLogin no" > my.conf
echo "PasswordAuthentication no" >> my.conf
systemctl restart sshd
```

3. Clone this repository on the server that will host the dashboard and install ansible on that server.
4. On the dashboard sevrer, add the IP addresses or DNS names of the attacking machines to the [inventory](inventory) file under the attackers block.
6. From this directory, run `ansible-playbook -i ./inventory setup.yml` - this will install all the attack tools on all attack nodes defined in the inventory file.
7. When adding an attack node, make sure to execute step 2 on the new machine, then simply run the setup playbook using ansible again. 

## Adding a new attack (Ansible part)
1. In the [setup playbook](setup.yml), add a `task` item with instructions to install the new attack tool (from [git](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html#examples), or by [copying](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html#examples) a local file).
2. Run the setup playbook again (step 5 in the attack nodes setup).
3. In the [attacks](attacks) directory, add a yml file which runs the attack for a time specified by the variable "duration". Other variables may be included, using the [Jinja2 templating style](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_variables.html#using-variables-with-jinja2). It is easiest to copy a simple attack playbook like [hulk.yml](attacks/hulk.yml) and make changes.
4. Make sure to also add the attack on the [dashboard side](../dashboard/README.md).

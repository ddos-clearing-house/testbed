#!/bin/bash
echo 'done'
#apt install openssh-server
#
## Add user and ssh key
#adduser --disabled-password --gecos "" ansible
#echo "ansible:changeme" | chpasswd
#adduser ansible sudo
## Enable passwordless sudo for ansible
#echo "ansible ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers
#mkdir /home/ansible/.ssh
#
#cat >> /home/ansible/.ssh/authorized_keys << EOF
## Local machine
#$SSHPUBKEY
#EOF
#
## SSH config
#
#cd /etc/ssh/sshd_config.d
#echo "PermitRootLogin no" > my.conf
#echo "PasswordAuthentication no" >> my.conf
#systemctl restart sshd
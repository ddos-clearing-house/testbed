#! /usr/bin/python3

import os

while True:
    try:
        nr_nodes = int(input('How many attack nodes to start?\n> '))
        assert 1 <= nr_nodes <= 10
        break
    except (ValueError, AssertionError):
        print('Please enter a number between 1 and 10')

while True:
    sshpubkey_path = input('Please enter the path to your SSH public key (press enter for ~/.ssh/id_rsa.pub). '
                           'This is required for ansible to connect to the attack nodes.\n> ')
    if sshpubkey_path == '':
        sshpubkey_path = os.path.expanduser('~/.ssh/id_rsa.pub')
    try:
        assert os.path.isfile(sshpubkey_path)
        with open(sshpubkey_path, 'r') as file:
            sshpubkey = file.read()
        break
    except AssertionError:
        print('Path does not exist or os not a file.')

print('Building attacker docker image...')
os.system(f'docker build -t testbed-attack-node --build-arg SSHPUBKEY="{sshpubkey}" .')

print(f'Starting {nr_nodes} attack nodes.')
for i in range(1, nr_nodes + 1):
    os.system(f'docker run -dit --name attack_node{i} testbed-attack-node')

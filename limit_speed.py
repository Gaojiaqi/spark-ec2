import sys
import os
import subprocess

def get_slaves():
    slaves = subprocess.check_output(['cat', '/root/spark-ec2/slaves'])
    return slaves.strip().split('\n')

slaves = get_slaves()
speed = '1.1Gbit'

commands = ["tc qdisc del dev eth0 root".split(' '),
            "tc qdisc add dev eth0 handle 1: root htb default 11".split(' '),
            "tc class add dev eth0 parent 1: classid 1:1 htb rate 1250Mbps".split(' '),
            ("tc class add dev eth0 parent 1:1 classid 1:11 htb rate " + speed).split(' ')]

for command in commands:
    subprocess.call(command)

for slave in slaves:
    for command in commands:
        subprocess.call(['ssh', slave] + command)

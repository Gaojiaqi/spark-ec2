import sys
import os
import subprocess

# ./cluster get-slave-ip
# ./cluster get-master-ip
# masters
# slaves

ssh_opt = ['ssh', '-o', 'StrictHostKeyChecking=no', '-i', 'spark-ec2.pem']

master = subprocess.check_output(['bash', 'cluster', 'get-master-ip']).strip().split('\n')[-1]
slaves = subprocess.check_output(['bash', 'cluster', 'get-slave-ip']).strip().split('\n')[2:]
print master
for slave in slaves:
    print slave

subprocess.call(ssh_opt + ['ubuntu@'+master, 'rm', 'tools/masters', 'tools/slaves'])
subprocess.call(ssh_opt + ['ubuntu@'+master, 'echo', master, '>>', 'tools/masters'])
subprocess.call(ssh_opt + ['ubuntu@'+master, 'echo', ' '.join(slaves), '>>', 'tools/slaves'])

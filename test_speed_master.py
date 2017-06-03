import sys
import os
import subprocess

def get_slaves():
    slaves = subprocess.check_output(['cat', '/root/spark-ec2/slaves'])
    return slaves.strip().split('\n')

slaves = get_slaves()
slaves = ['172.31.25.9']

iperf_master = subprocess.Popen(['iperf3', '-s', '-p', '80'])
iperf_slaves = []

for slave in slaves:
    subprocess.call(['scp', 'test_speed_slave.py', slave+':/root/'])
    iperf_slaves.append(subprocess.check_output(['ssh', slave, 'python', 'test_speed_slave.py']))

print "checking slaves speed"
for iperf_slave in iperf_slaves:
    print iperf_slave

print "terminating master"
iperf_master.terminate()

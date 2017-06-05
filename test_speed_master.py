import sys
import os
import subprocess
import time

def get_slaves():
    slaves = subprocess.check_output(['cat', '/root/spark-ec2/slaves'])
    return slaves.strip().split('\n')

slaves = get_slaves()

for slave in slaves:
    subprocess.call(['ssh', slave, 'killall', 'iperf3'])
    subprocess.call(['scp', '/root/spark-ec2/test_speed_slave.py', slave+':/root/'])

iperf_master = subprocess.Popen(['iperf3', '-s', '-p', '6789'])
iperf_slaves = []

for slave in slaves:
    iperf_slaves.append(subprocess.check_output(['ssh', slave, 'python', 'test_speed_slave.py']))
    time.sleep(1)

print "terminating master"
iperf_master.terminate()
subprocess.call(['killall', 'iperf3'])

time.sleep(1)

print "checking slaves speed"
for iperf_slave in iperf_slaves:
    print iperf_slave.strip()

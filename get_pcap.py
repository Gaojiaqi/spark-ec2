#! /usr/bin/env python27
import sys
import os
import time
import subprocess

def get_slaves():
    slaves = subprocess.check_output(['cat', '/root/spark-ec2/slaves'])
    return slaves.strip().split('\n')

def get_master():
    master = subprocess.check_output(['cat', '/root/spark-ec2/masters']).strip()
    return master

def check_spark_running():
    processes = subprocess.check_output(['ps', 'aux'])
    a = filter(lambda x : x.find('ml-matrix') > 0, processes.strip().split('\n'))
    return len(a)

slaves = get_slaves()
master = get_master()
print "master ip", master
print "slaves ip", slaves
sshs = []

command = "tcpdump -ieth0 -s96 -w traffic.dump 'tcp'"

for slave in slaves:
    sshs.append(subprocess.Popen(["ssh", slave, command]))

subprocess.Popen(["tcpdump", "-ieth0", "-s96", "-w", "/root/traffic.dump", "tcp"])

subprocess.Popen("/root/spark/bin/spark-submit --class edu.berkeley.cs.amplab.mlmatrix.BlockCoordinateDescent --driver-memory 20G --driver-class-path /root/ml-matrix/target/scala-2.11/mlmatrix-assembly-0.2.jar /root/ml-matrix/target/scala-2.11/mlmatrix-assembly-0.2.jar".split(' ') + ["spark://"+master+":7077"] + "4096 16 4096 5 1".split(' '))

try:
    counter = 0
    while(1):
        time.sleep(1)
        if check_spark_running() == 0:
            counter += 1
        if counter >= 10:
            print "program has finished, returning"
            break
except KeyboardInterrupt:
    pass

print "collecting data"
for ssh in sshs:
    ssh.terminate()
for slave in slaves:
    subprocess.call(["ssh", slave, "killall", "tcpdump"])
subprocess.call(["killall", "tcpdump"])

for idx, slave in enumerate(slaves):
    subprocess.call(["scp", slave+":~/traffic.dump", "/root/traffic_%d.dump" % idx])
    subprocess.call(["ssh", slave, "rm", "traffic.dump"])

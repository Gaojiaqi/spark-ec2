import sys
import os
import subprocess

def get_master():
    master = subprocess.check_output(['cat', '/root/spark-ec2/masters']).strip()
    return master

master_ip = get_master()

ret = subprocess.check_output(['iperf3', '-c', master_ip, '-i', '1', '-p', '80', '-t', '5'])
send_speed = ret.strip().split('\n')[-4]
recv_speed = ret.strip().split('\n')[-3]

send_speed = filter(lambda x : x, send_speed.split(' '))[6]
recv_speed = filter(lambda x : x, recv_speed.split(' '))[6]

print send_speed, recv_speed

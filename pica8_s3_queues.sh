#!/bin/sh

#requires sshpass to be installed on the machine running the script

# adds the qos/queues to the pica8 switch
# q2 highest priority
# q0 lowest priority
PICA8SETUP="source /etc/profile;\
ovs-vsctl set port s3-eth2 qos=@newqos -- --id=@newqos create qos type=linux-htb queues:0=@q0 queues:1=@q1 queues:2=@q2 -- --id=@q0 create queue other-config:max-rate=10000000000 -- --id=@q1 create queue other-config:max-rate=10000000000 -- --id=@q2 create queue other-config:max-rate=10000000000;"

sshpass -p "sdne123" ssh admin@172.22.5.45 "${PICA8SETUP}"
echo "Pica8 switch queues installed"
#!/bin/sh

#requires sshpass to be installed on the machine running the script

# adds the qos/queues to the pica8 switch
# q0 lowest priority - max rate 600 Mbps
PICA8SETUP="source /etc/profile;\
ovs-vsctl set port ge-1/1/3 qos=@newqos -- --id=@newqos create qos type=PRONTO_STRICT queues:0=@q0 -- --id=@q0 create queue other-config:max-rate=600000000;"

sshpass -p "sdne123" ssh admin@172.22.5.45 "${PICA8SETUP}"
echo "Pica8 switch queues installed"
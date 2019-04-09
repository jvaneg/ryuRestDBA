#!/bin/sh

#requires sshpass to be installed on the machine running the script

# adds the qos/queues to the pica8 switch (switch 2)
# q1 highest priority
# q0 lowest priority
PICA8SETUP="source /etc/profile;\
ovs-vsctl set port ge-1/1/2 qos=@newqos -- --id=@newqos create qos type=PRONTO_STRICT queues:0=@q0 queues:1=@q1 -- --id=@q0 create queue other-config:max-rate=10000000000 -- --id=@q1 create queue other-config:max-rate=10000000000;"

sshpass -p "sdne123" ssh admin@172.22.5.45 "${PICA8SETUP}"
echo "Pica8 switch queues installed"
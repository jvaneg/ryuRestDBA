#!/bin/sh

#requires sshpass to be installed on the machine running the script

#resets the flow tables, meters, and qos on the pica8 switch
PICA8CLEAR="source /etc/profile;\
ovs-vsctl clear port ge-1/1/1 qos; ovs-vsctl clear port ge-1/1/2 qos;\
ovs-vsctl clear port ge-1/1/3 qos; ovs-vsctl --all destroy qos;\
ovs-vsctl --all destroy queue;"

sshpass -p "sdne123" ssh admin@172.22.5.37 "${PICA8CLEAR}"
echo "Pica8 switch cleared!"

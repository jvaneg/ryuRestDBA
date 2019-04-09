#!/bin/bash

# requires sudo
# port 2 of switch 2 going to switch 3
# no min rate, just remark based
# q1 highest priority
# q0 lowest priority
ovs-vsctl set port s2-eth2 qos=@newqos -- --id=@newqos create qos type=linux-htb queues:0=@q0 queues:1=@q1 -- --id=@q0 create queue other-config:max-rate=10000000000 -- --id=@q1 create queue other-config:max-rate=10000000000
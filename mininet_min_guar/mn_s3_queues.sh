#!/bin/bash

# requires sudo
# 3rd switch port going to h3, 600 Mbps (or whatever you set it to)
# q0 lowest priority
ovs-vsctl set port s3-eth2 qos=@newqos -- --id=@newqos create qos type=linux-htb queues:0=@q0 -- --id=@q0 create queue other-config:max-rate=600000000
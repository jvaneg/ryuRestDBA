#!/bin/sh

#requires sshpass to be installed on the machine running the script

#resets the and qos/queues on the pica8 switch
ovs-vsctl clear port s2-eth2 qos
ovs-vsctl --all destroy qos
ovs-vsctl --all destroy queue
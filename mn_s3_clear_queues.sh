#!/bin/sh

# requires sudo

ovs-vsctl clear port s3-eth2 qos
ovs-vsctl --all destroy qos
ovs-vsctl --all destroy queue

import argparse
import time
# from datetime import datetime
from pathlib import Path

import dbaAlgorithms

import switchTools

import toml

# from ryuswitch import RyuSwitch


def main(args):
    if(not Path(args.config_file).is_file()):
        print("Error loading config file")
        exit(-1)

    with Path(args.config_file).open() as config_file:
        config = toml.load(config_file)["config"]

    link_capacity = config["link_capacity"]

    # setup switches
    switch_list = switchTools.setup_switch(args.config_file)

    print(switch_list)

    flow_bytes, timestamp = switchTools.get_flow_bytes(switch_list[1][0])

    print(timestamp)
    print(flow_bytes)

    flow_list = switch_list[1][2]

    print("Link capacity: {}".format(link_capacity))

    for flow_id, flow in flow_list.items():
        print("Flow: {} - Meter: {} - Min rate: {} Mbps".format(flow_id, flow.get_meter(), flow.get_minimum_rate()))

    print("--- Flow bandwidth ---")
    # print("1\t2\t3\t4")

    while(True):
        for flow_id, flow in flow_list.items():
            flow.update_demand_bw(flow_bytes[flow_id], timestamp)

        excess_bandwidth = calc_excess_bandwidth(flow_list, link_capacity)

        dbaAlgorithms.allocate_egalitarian(flow_list, excess_bandwidth)

        flow_demand_display = "Demand: "
        for flow_id, flow in flow_list.items():
            flow_demand_display += "{} - {}\t  ".format(flow_id, flow.get_demand_bw())

        flow_allocated_display = "Allocated: "
        for flow_id, flow in flow_list.items():
            flow_demand_display += "{} - {}\t  ".format(flow_id, flow.get_allocated_bw())

        print(flow_demand_display)
        print("Excess: {} Mbps".format(excess_bandwidth))
        print(flow_allocated_display)

        flow_bytes, timestamp = switchTools.get_flow_bytes(switch_list[1][0])

        time.sleep(2)

    # loop forever
    #   poll flows
    #   calculate bandwidth usage (target bandwidth)
    #   calculate tier 2 meter maximums (dependent on algorithm)
    #   modify tier 2 meters structures
    #   install changes on switch


# this function will let you return negative numbers
# TODO: write something to throw an error if sum of the meter min rates
#       is higher than the link capacity
def calc_excess_bandwidth(flow_list, link_capacity):
    excess_bandwidth = link_capacity

    for _flow_id, flow in flow_list.items():
        flow_demand = flow.get_bandwidth()
        flow_min = flow.get_minimum_rate()

        # if demand <= min rate -> subtract demand
        if(flow_demand <= flow_min):
            excess_bandwidth -= flow_demand
        # if demand > min_rate -> subtract min rate
        else:
            excess_bandwidth -= flow_min

    return excess_bandwidth


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="the config file describing the flows and switches")
    args = parser.parse_args()
    main(args)

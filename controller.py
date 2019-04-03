# stdlib imports
import argparse
import time
from pathlib import Path

# my module imports
import dbaAlgorithms
import switchTools

# 3rd party imports
import toml


def main(args):

    # check if config file exists and load it
    if(not Path(args.config_file).is_file()):
        print("Error loading config file")
        exit(-1)

    with Path(args.config_file).open() as config_file:
        config = toml.load(config_file)["config"]

    link_capacity = config["link_capacity"]

    # setup switches
    switch_list = switchTools.setup_switches(args.config_file)

    print(switch_list)  # TODO: remove debug

    tier1_switch = switch_list[TIER1_SWITCH]
    tier2_switch = switch_list[TIER2_SWITCH]
    tier3_switch = switch_list[TIER3_SWITCH]

    # get initial flow bytes usage
    flow_bytes, timestamp = switchTools.get_flow_bytes(switch_list[1][0])

    print(timestamp)    # TODO: remove debug
    print(flow_bytes)

    flow_list = switch_list[1][2]

    print("Link capacity: {}".format(link_capacity))

    for flow_id, flow in flow_list.items():
        print("Flow: {} - Meter: {} - Min rate: {} Mbps".format(flow_id, flow.get_meter(), flow.get_minimum_rate()))

    print("--- Flow bandwidth ---")

    if(args.log is not None):
        # open log file
        log_file = open(args.log, "w+")

    try:
        # TODO: cleanup switches when loop is broken
        while(True):
            for flow_id, flow in flow_list.items():
                flow.update_demand_bw(flow_bytes[flow_id], timestamp)

            excess_bandwidth = calc_excess_bandwidth(flow_list, link_capacity)

            dbaAlgorithms.allocate_egalitarian(flow_list, excess_bandwidth)

            if(args.log is not None):
                flow_demand_display = "Demand:\t"
                demand_csv_string = ""
                for flow_id, flow in flow_list.items():
                    flow_demand_display += "{} - {}\t  ".format(flow_id, flow.get_demand_bw())
                    demand_csv_string += "{},".format(flow.get_demand_bw())

                flow_allocated_display = "Allocated:\t"
                allocated_csv_string = ""
                for flow_id, flow in flow_list.items():
                    flow_allocated_display += "{} - {}\t  ".format(flow_id, flow.get_allocated_bw())
                    allocated_csv_string += "{},".format(get_allocated_bw())

                actual_csv_string = "10,13,"  # change this to read from s3

                # display stuff
                print(flow_demand_display)
                print("Excess:\t{} Mbps".format(excess_bandwidth))
                print(flow_allocated_display)
                print("---")

                # log to file
                log_file.write("{},{}{}{}\n".format(excess_bandwidth, demand_csv_string, allocated_csv_string, actual_csv_string))

            # read again 
            flow_bytes, timestamp = switchTools.get_flow_bytes(switch_list[1][0])
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit, Exception):
        print("Cleaning up...")
        if(args.log is not None):
            log_file.close()
        switchTools.clean_switches(args.config_file)

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
        flow_demand = flow.get_demand_bw()
        flow_min = flow.get_minimum_rate()

        # if demand <= min rate -> subtract demand
        if(flow_demand <= flow_min):
            excess_bandwidth -= flow_demand
        # if demand > min_rate -> subtract min rate
        else:
            excess_bandwidth -= flow_min

    return excess_bandwidth


# Constants
TIER1_SWITCH = 0
TIER2_SWITCH = 1
TIER3_SWITCH = 2

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="the config file describing the flows and switches")
    parser.add_argument("-l", "--log", metavar="[log file name]", help="specify a log file")
    args = parser.parse_args()
    main(args)

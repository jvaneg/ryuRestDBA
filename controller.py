# stdlib imports
import argparse
import time
from pathlib import Path

# my module imports
from backend import dbaAlgorithms
from backend import switchTools

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
    switch_list = switchTools.setup_switches(Path(args.config_file))

    print(switch_list)  # TODO: remove debug

    tier1_switch = switch_list[TIER1_SWITCH]
    tier2_switch = switch_list[TIER2_SWITCH]
    tier3_switch = switch_list[TIER3_SWITCH]

    # get initial flow bytes usage TODO: remove this
    t1_flow_bytes, t1_timestamp = switchTools.get_flow_bytes(tier1_switch[0])

    print(t1_timestamp)    # TODO: remove debug
    print(t1_flow_bytes)

    # link flows
    link_flows(tier1_switch, tier2_switch)

    print("Link capacity: {}".format(link_capacity))  # TODO: remove debug

    # TODO: remove this debug stuff
    t1_flow_list = tier1_switch[2]
    for flow_id, flow in t1_flow_list.items():
        print("Flow: {} - Meter: {} - Min rate: {} Mbps".format(flow_id, flow.get_meter(), flow.get_minimum_rate()))

    print("--- Flow bandwidth ---")

    # open log file
    if(args.log is not None):
        log_file = open(args.log, "w+")

    try:
        # loop forever:
        #   poll tier 1 flows
        #   calculate bandwidth usage (target bandwidth)
        #   calculate tier 2 meter maximums (dependent on algorithm)
        #   modify tier 2 meters structures
        #   install changes on switch
        #   if logging:
        #       poll tier 3 flows
        #       log data to file
        t1_flow_list = tier1_switch[2]
        t2_flow_list = tier2_switch[2]
        t3_flow_list = tier3_switch[2]
        while(True):
            # poll t1 switch flows for flow information
            t1_flow_bytes, t1_timestamp = switchTools.get_flow_bytes(tier1_switch[0])

            # calculate demand bandwidth for each flow
            for flow_id, flow in t1_flow_list.items():
                flow.update_demand_bw(t1_flow_bytes[flow_id], t1_timestamp)

            # calculate excess bandwidth TODO: may not need this with different alg implementation
            excess_bandwidth = calc_excess_bandwidth(t1_flow_list, link_capacity)

            # calculate bandwidth allocation for each flow TODO: value in config to determine which alg
            dbaAlgorithms.allocate_egalitarian(t1_flow_list, excess_bandwidth)

            # install allocated bandwidth changes on t2 switch meters
            switchTools.update_meters(tier2_switch[0], tier2_switch[2])

            # logging data
            if(args.log is not None):
                # poll t3 switch for flow data
                t3_flow_bytes, t3_timestamp = switchTools.get_flow_bytes(tier3_switch[0])
                # calculate demand bw for t3 flows (high, med, low)
                for flow_id, flow in t3_flow_list.items():
                    flow.update_demand_bw(t3_flow_bytes[flow_id], t3_timestamp)

                # poll t2 switch for flow data
                t2_flow_bytes, t2_timestamp = switchTools.get_flow_bytes(tier2_switch[0])
                # calculate demand bw for t2 flows (min, over min)
                for flow_id, flow in t2_flow_list.items():
                    flow.update_demand_bw(t2_flow_bytes[flow_id], t2_timestamp)

                flow_demand_display = "S1 - Demand:\t"
                demand_csv_string = ""
                for flow_id, flow in t1_flow_list.items():
                    flow_demand_display += "{} - {}\t  ".format(flow_id, flow.get_demand_bw())
                    demand_csv_string += "{},".format(flow.get_demand_bw())

                flow_allocated_display = "Allocated:\t"
                allocated_csv_string = ""
                for flow_id, flow in t1_flow_list.items():
                    flow_allocated_display += "{} - {}\t  ".format(flow_id, flow.get_allocated_bw())
                    allocated_csv_string += "{},".format(flow.get_allocated_bw())

                flow_min_display = "Min rate:\t"
                min_csv_string = ""
                for flow_id, flow in t1_flow_list.items():
                    flow_min_display += "{} - {}\t  ".format(flow_id, flow.get_minimum_rate())
                    min_csv_string += "{},".format(flow.get_minimum_rate())

                flow_high_display = "S3 - High Priority:\t"
                high_csv_string = ""
                flow_high_display += "{} - {}\t  {} - {}\t  ".format(1, t3_flow_list[1].get_demand_bw(),
                                                                     2, t3_flow_list[2].get_demand_bw())
                high_csv_string += "{},{},".format(t3_flow_list[1].get_demand_bw(), t3_flow_list[2].get_demand_bw())

                flow_med_display = "S3 - Medium Priority:\t"
                med_csv_string = ""
                flow_med_display += "{} - {}\t  {} - {}\t  ".format(3, t3_flow_list[3].get_demand_bw(),
                                                                    4, t3_flow_list[4].get_demand_bw())
                med_csv_string += "{},{},".format(t3_flow_list[3].get_demand_bw(), t3_flow_list[4].get_demand_bw())

                flow_low_display = "S3 - Low Priority:\t"
                low_csv_string = ""
                flow_low_display += "{} - {}\t  {} - {}\t  ".format(5, t3_flow_list[5].get_demand_bw(),
                                                                    6, t3_flow_list[6].get_demand_bw())
                low_csv_string += "{},{},".format(t3_flow_list[5].get_demand_bw(), t3_flow_list[6].get_demand_bw())

                flow_s2_high_display = "S2 - High Priority:\t"
                s2_high_csv_string = ""
                flow_s2_high_display += "{} - {}\t  {} - {}\t  ".format(10, t2_flow_list[10].get_demand_bw(),
                                                                        11, t2_flow_list[11].get_demand_bw())
                s2_high_csv_string += "{},{},".format(t2_flow_list[10].get_demand_bw(), t2_flow_list[11].get_demand_bw())

                flow_s2_rmk_display = "S2 - Remarked:\t"
                s2_rmk_csv_string = ""
                flow_s2_rmk_display += "{} - {}\t  {} - {}\t  ".format(1, t3_flow_list[1].get_demand_bw(),
                                                                        2, t3_flow_list[2].get_demand_bw())
                s2_rmk_csv_string += "{},{},".format(t3_flow_list[2].get_demand_bw(), t3_flow_list[2].get_demand_bw())

                # display stuff
                print(flow_min_display)
                print(flow_demand_display)
                print("Excess:\t{} Mbps".format(excess_bandwidth))
                print(flow_allocated_display)
                print(flow_s2_high_display)
                print(flow_s2_rmk_display)
                print(flow_high_display)
                print(flow_med_display)
                print(flow_low_display)
                print("---")

                # log to file
                # log csv line format:
                # excess,demand_h1,demand_h2,alloc_h1,alloc_h2,high_h1,high_h2,med_h1,med_h2,low_h1,low_h2,min_h1,min_h2,
                log_file.write("{},{}{}{}{}{}{}\n".format(excess_bandwidth, demand_csv_string, allocated_csv_string,
                                                          high_csv_string, med_csv_string,
                                                          low_csv_string, min_csv_string))

            # wait
            time.sleep(1)

            # read again
            t1_flow_bytes, t1_timestamp = switchTools.get_flow_bytes(tier1_switch[0])
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        print(e)
    finally:
        print("Cleaning up...")

        # close log file
        if(args.log is not None):
            log_file.close()

        # clean switch
        switchTools.clean_switches(Path(args.config_file))


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


# links the flows of the t1 switch with the corresponding flows of the t2 switch
# this is to make it easier to set the meter maximums
def link_flows(tier1_switch_tuple, tier2_switch_tuple):
    t1_flows = tier1_switch_tuple[2]
    t2_flows = tier2_switch_tuple[2]

    for t1_flow_id, t1_flow in t1_flows.items():
        try:
            t2_linked_flow = t2_flows[t1_flow_id]
            t1_flow.add_linked_flow(t2_linked_flow)
            t2_linked_flow.add_linked_flow(t1_flow)
        except Exception:
            pass


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

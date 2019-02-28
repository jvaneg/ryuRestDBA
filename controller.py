import argparse
import time
from datetime import datetime
from pathlib import Path

import switchTools

from ryuswitch import RyuSwitch


def main(args):
    if(not Path(args.config_file).is_file()):
        print("Error loading config file")
        exit(-1)

    # setup switches
    switch_list = switchTools.setup_switch(args.config_file)

    print(switch_list)

    flow_bytes, timestamp = switchTools.get_flow_bytes(switch_list[1][0])

    print(timestamp)
    print(flow_bytes)

    flow_list = switch_list[1][2]

    print("--- Flow bandwidth ---")
    print("1\t2\t3\t4")

    for _i in range(0, 5):
        for flow in flow_list:
            flow.update_bandwidth(flow_bytes[flow.get_id], timestamp)

        flow_bandwidth_display = ""
        for flow in flow_list:
            flow_bandwidth_display += "{}\t".format(flow.get_bandwidth())

        time.sleep(2)

    # loop forever
    #   poll flows
    #   calculate bandwidth usage (target bandwidth)
    #   calculate tier 2 meter maximums (dependent on algorithm)
    #   modify tier 2 meters structures
    #   install changes on switch


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="the config file describing the flows and switches")
    args = parser.parse_args()
    main(args)

import argparse
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

    flow_stats = switchTools(switch_list[0])

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

import argparse
import pprint
import subprocess
from pathlib import Path

from ryuswitch import RyuSwitch

import toml


def main(args):
    if(not Path(args.configFile).is_file()):
        print("Error loading config file")
        exit(-1)

    # setup switches
    switches = setup_switch(args.configFile)

    # loop forever
    #   poll flows
    #   calculate bandwidth usage (target bandwidth)
    #   calculate tier 2 meter maximums (dependent on algorithm)
    #   modify tier 2 meters structures
    #   install changes on switch


# Sets up the queues, meters, and flows for each switch
def setup_switch(config_file_name):
    pp = pprint.PrettyPrinter(indent=2)

    with Path(config_file_name).open() as config_file:
        config = toml.load(config_file)
        # pp.pprint(config)

    switches = {}

    for switch_config in config["switches"]:
        # pp.pprint(switchConfig)

        switch = RyuSwitch(switch_config["dpid"])
        switch = None
        switches[switch_config["dpid"]] = (switch, switch_config["meters"], switch_config["flows"])

        install_queues(switch_config["queues"])
        install_meters(switch_config["meters"], switch)
        install_flows(switch_config["flows"], switch)

    return switches


# Installs the meters onto the switch
def install_meters(meter_configs, switch):

    pp = pprint.PrettyPrinter(indent=2)

    for meter_config in meter_configs:
        # pp.pprint(meterConfig)
        switch.add_meter(meter_config)

    return


# Installs the flows onto the switch
def install_flows(flow_configs, switch):

    pp = pprint.PrettyPrinter(indent=2)

    for flow_config in flow_configs:
        # pp.pprint(flowConfig)
        switch.add_flow(flow_config)

    return


# Installing queues is not supported by the ryu rest API, so currently this calls a bash subprocess
def install_queues(queue_configs):
    # do nothing
    output = subprocess.check_output(["bash", str(queue_configs["queueScript"])])
    print(str(output, "utf-8"))

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config file", help="the config file describing the flows and switches")
    args = parser.parse_args()
    main(args)

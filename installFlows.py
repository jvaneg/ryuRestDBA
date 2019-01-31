import argparse
from pathlib import Path
import toml
import json
from ryuswitch import RyuSwitch
import pprint

def main(args):

    pp = pprint.PrettyPrinter(indent=2)

    if(not Path(args.configFile).is_file()):
        print("Error loading config file")
        exit(-1)

    
    with Path(args.configFile).open() as configFile:
        config = toml.load(configFile)
        pp.pprint(config)
    
    switches = {}

    for switchConfig in config["switches"]:
        pp.pprint(switchConfig)

        #switch = RyuSwitch(switchConfig["dpid"])
        switch = None
        switches[switchConfig["dpid"]] = switch

        installQueues(switchConfig, switch)
        installMeters(switchConfig["meters"], switch)
        installFlows(switchConfig["flows"], switch)

    print(switches)

def installMeters(meterConfigs, switch):

    pp = pprint.PrettyPrinter(indent=2)

    for meterConfig in meterConfigs:
        pp.pprint(meterConfig)

        #switch.add_meter(meterConfig)

def installFlows(flowConfigs, switch):

    pp = pprint.PrettyPrinter(indent=2)

    for flowConfig in flowConfigs:
        pp.pprint(flowConfig)

        #switch.add_flow(flowConfig)

# Installing queues is not supported by the ryu rest API, so currently this calls a bash subprocess
def installQueues(switchConfig, switch):
    #do nothing
    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile", help="the config file describing the flows and switches")
    args = parser.parse_args()
    main(args)


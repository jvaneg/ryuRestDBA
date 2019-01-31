import argparse
from pathlib import Path
import toml
import json
from ryuswitch import RyuSwitch
import pprint
import subprocess

def main(args):
    
    if(not Path(args.configFile).is_file()):
        print("Error loading config file")
        exit(-1)

    # setup switches
    switches = setupSwitch(args.configFile)

    # loop forever
        # poll flows
        # calculate bandwidth usage (target bandwidth)
        # calculate tier 2 meter maximums (dependent on algorithm)
        # modify tier 2 meters structures
        # install changes on switch


# Sets up the queues, meters, and flows for each switch
def setupSwitch(configFileName):
    pp = pprint.PrettyPrinter(indent=2)

    with Path(configFileName).open() as configFile:
        config = toml.load(configFile)
        #pp.pprint(config)
    
    switches = {}

    for switchConfig in config["switches"]:
        pp.pprint(switchConfig)

        #switch = RyuSwitch(switchConfig["dpid"])
        switch = None
        switches[switchConfig["dpid"]] = (switch, switchConfig["meters"], switchConfig["flows"])

        installQueues(switchConfig["queues"])
        installMeters(switchConfig["meters"], switch)
        installFlows(switchConfig["flows"], switch)

    return switches


# Installs the meters onto the switch
def installMeters(meterConfigs, switch):

    pp = pprint.PrettyPrinter(indent=2)

    for meterConfig in meterConfigs:
        pp.pprint(meterConfig)
        #switch.add_meter(meterConfig)

    return


# Installs the flows onto the switch
def installFlows(flowConfigs, switch):

    pp = pprint.PrettyPrinter(indent=2)

    for flowConfig in flowConfigs:
        pp.pprint(flowConfig)
        #switch.add_flow(flowConfig)

    return


# Installing queues is not supported by the ryu rest API, so currently this calls a bash subprocess
def installQueues(queueConfigs):
    #do nothing
    output = subprocess.check_output(["bash", str(queueConfigs["queueScript"])])
    print(str(output, "utf-8"))

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile", help="the config file describing the flows and switches")
    args = parser.parse_args()
    main(args)


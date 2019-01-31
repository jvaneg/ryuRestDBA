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
    
        for switch in config["switches"]:
            pp.pprint(switch)
            
            installMeters(switch)
            installFlows(switch)

def installMeters(switch):

    pp = pprint.PrettyPrinter(indent=2)

    for meter in switch["meters"]:
        pp.pprint(meter)

def installFlows(switch):

    pp = pprint.PrettyPrinter(indent=2)

    for flow in switch["flows"]:
        pp.pprint(flow)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile", help="the config file describing the flows and switches")
    args = parser.parse_args()
    main(args)


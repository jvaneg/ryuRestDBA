import argparse
from pathlib import Path
import toml
import json
from ryuswitch import RyuSwitch
import pprint

def main(args):

    pp = pprint.PrettyPrinter(indent=2)

    try:
        with Path(args.configFile).open() as configFile:
            config = toml.load(configFile)
            pp.pprint(config)
    except Exception as error:
        print("Error loading config file")
        exit(-1)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile", help="the config file describing the flows and switches")
    args = parser.parse_args()
    main(args)


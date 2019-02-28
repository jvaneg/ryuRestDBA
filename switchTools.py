import pprint
import subprocess
from pathlib import Path

from flow import Flow

from meter import Meter

from ryuswitch import RyuSwitch

import toml


# Sets up the queues, meters, and flows for each switch
def setup_switch(config_file_name):
    # pp = pprint.PrettyPrinter(indent=2)

    with Path(config_file_name).open() as config_file:
        config = toml.load(config_file)
        # pp.pprint(config)

    switch_list = {}

    for switch_config in config["switches"]:
        # pp.pprint(switchConfig)

        switch = RyuSwitch(switch_config["dpid"])

        install_queues(switch_config["queues"])
        meter_list = install_meters(switch_config["meters"], switch)
        install_flows(switch_config["static_flows"], switch)
        flow_list = install_flows(switch_config["flows"], switch)

        switch_list[switch_config["dpid"]] = (switch, meter_list, flow_list)

    return switch_list


# Installs the meters onto the switch
def install_meters(meter_configs, switch):

    pp = pprint.PrettyPrinter(indent=2)

    meter_list = {}

    print("\n---Meters---")
    for meter_config in meter_configs:
        print("Meter id: {}".format(meter_config["meter_id"]))
        pp.pprint(meter_config)

        switch.add_meter(meter_config)
        meter = Meter(meter_config)
        meter_list[meter.get_id()] = meter

    return meter_list


# Installs the flows onto the switch
def install_flows(flow_configs, switch):

    pp = pprint.PrettyPrinter(indent=2)

    flow_list = {}

    print("\n---Flows---")
    for flow_config in flow_configs:
        try:
            print("Flow id: {}".format(flow_config["cookie"]))
        except Exception:
            print("not an id'd flow")
        pp.pprint(flow_config)

        switch.add_flow(flow_config)
        flow = Flow(flow_config)
        flow_list[flow.get_id()] = flow

    return flow_list


# Installing queues is not supported by the ryu rest API, so currently this calls a bash subprocess
def install_queues(queue_configs):
    # do nothing
    print("\n---Queues---")
    output = subprocess.check_output(["bash", str(queue_configs["queue_script"])])
    print(str(output, "utf-8"))

    return

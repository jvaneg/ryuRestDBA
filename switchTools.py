import pprint
import subprocess
from datetime import datetime
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
        install_flows(switch_config["static_flows"], switch, False)
        flow_list = install_flows(switch_config["flows"], switch, True)

        switch_list[switch_config["dpid"]] = (switch, sorted(meter_list, key=sort_by_id),
                                              sorted(flow_list, key=sort_by_id))

    return switch_list


def sort_by_id(elem):
    return elem.get_id()


# Installs the meters onto the switch
def install_meters(meter_configs, switch):

    pp = pprint.PrettyPrinter(indent=2)

    meter_list = []

    print("\n---Meters---")
    for meter_config in meter_configs:
        print("Meter id: {}".format(meter_config["meter_id"]))
        pp.pprint(meter_config)

        switch.add_meter(meter_config)
        meter = Meter(meter_config)
        meter_list.append(meter)

    return meter_list


# Installs the flows onto the switch
def install_flows(flow_configs, switch, save_results):

    pp = pprint.PrettyPrinter(indent=2)

    flow_list = []

    print("\n---Flows---")
    for flow_config in flow_configs:
        try:
            print("Flow id: {}".format(flow_config["cookie"]))
        except Exception:
            print("not an id'd flow")
        pp.pprint(flow_config)

        switch.add_flow(flow_config)

        if(save_results):
            flow = Flow(flow_config)
            flow_list.append(flow)

    if(save_results):
        return flow_list
    else:
        return None


# Installing queues is not supported by the ryu rest API, so currently this calls a bash subprocess
def install_queues(queue_configs):
    # do nothing
    print("\n---Queues---")
    output = subprocess.check_output(["bash", str(queue_configs["queue_script"])])
    print(str(output, "utf-8"))

    return


def get_flow_stats(switch):

    flow_stats = switch.get_flows()

    return flow_stats[str(switch.DPID)], datetime.now()


def get_flow_bytes(switch):

    all_flow_stats, timestamp = get_flow_stats(switch)

    flow_bytes = {}

    for flow_stat in all_flow_stats:
        if(flow_stat["cookie"] > 0):
            flow_bytes[flow_stat["cookie"]] = flow_stat["byte_count"]

    return flow_bytes, timestamp
# stdlib imports
import pprint
import subprocess
from datetime import datetime
from pathlib import Path

# my module imports
from flow import Flow
from meter import Meter
from ryuswitch import RyuSwitch

# 3rd party imports
import toml


# Sets up the queues, meters, and flows for each switch
# Reads from the config file specified on the command line
#
# Args:
#   config_file_name - name of the config file, string
# Returns:
#   switch_list - dictionary of triplets indexed by switch dpid
#                 format: (switch, meter_list, flow_list)
#                   switch - ryurest object representing the switch
#                   meter_list - dictionary of meter objects installed on switch
#                   flow_list - dictionary of dynamic flow objects installed on switch
#                               (does not include the static flows)
def setup_switches(config_file_name):

    with Path(config_file_name).open() as config_file:
        config = toml.load(config_file)

    switch_list = []

    for switch_config in config["switches"]:

        # get the switch object from the dpid
        switch = RyuSwitch(switch_config["dpid"])

        # clear the switch of existing flows/meters/queues
        clear_switch(switch, switch_config["queues"])

        # install the queues, then meters, then flows (has to be in this order or flows can error)
        install_queues(switch_config["queues"])
        meter_list = install_meters(switch_config["meters"], switch)
        install_flows(switch_config["static_flows"], switch, False)
        flow_list = install_flows(switch_config["flows"], switch, True)

        # link flows to meters
        link_flows_to_meters(flow_list, meter_list)

        switch_list.append((switch, meter_list, flow_list))

    return switch_list


# Clears the switches of flows, meters, and queues
# Reads from the config file specified on the command line
#
# Args:
#   config_file_name - name of the config file, string
def clean_switches(config_file_name):
    with Path(config_file_name).open() as config_file:
        config = toml.load(config_file)

    for switch_config in config["switches"]:
        # get the switch object from the dpid
        switch = RyuSwitch(switch_config["dpid"])
        
        # clear the switch of existing flows/meters/queues
        clear_switch(switch, switch_config["queues"])

    return



# Installs the meters onto the switch
# Args:
#   meter_configs - dictionary containing all the meter configs
#   switch - ryurest switch object representing the switch the meters will be installed on
# Returns:
#   meter_list - dictionary of meter objects installed on the switch, indexed by meter id
#
# TODO: currently outputting the config dictionaries as a debug thing, remove that when its done
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
# Args:
#   flow_configs - dictionary containing all the flow configs
#   switch - ryurest switch object representing the switch the flows will be installed on
#   save_results - whether or not to return the flow_list (ie static flows are just installed but not returned), bool
#                       True - return flow_list
#                       False - return None
# Returns:
#   flow_list - dictionary of flow objects installed on the switch, indexed by cookie field
#               (I'm using the cookie field as a pseudo flow_id since the flows aren't given actual ids in Ryu)
#
# TODO: currently outputting the config dictionaries as a debug thing, remove that when its done
def install_flows(flow_configs, switch, save_results):

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

        if(save_results):
            flow = Flow(flow_config)
            flow_list[flow.get_id()] = flow

    if(save_results):
        return flow_list
    else:
        return None


# Installs queues on the switch
# Installing queues is not supported by the ryu rest API, so currently this calls a bash subprocess
# The name of the bash file is currently specified in the config file
# Note: This is NOT portable and only works with the pica8 switch, would need to be updated for
#       other switches
# Args:
#   queue_configs - dictionary containing queue config information (in this case just the script name)
def install_queues(queue_configs):

    print("\n---Queues---")
    output = subprocess.check_output(["bash", str(queue_configs["queue_script"])])
    print(str(output, "utf-8"))

    return


# Associates each flow object with its corresponding meter object
# Corresponding meter is indicated by the meter field in under actions in the config file
# Ex:
#
# [[switches.flows.actions]]
#        type = "METER"
#        meter_id = 1
#
# Only used for dynamic flows, as static flows shouldnt be metered
# Args:
#   flow_list - dictionary of flow objects, indexed by cookie (pseudo flow id)
#   meter_list - dictionary of meter objects, indexed by meter id
# Note: needs more error handling for cases where the meter id is wrong
def link_flows_to_meters(flow_list, meter_list):

    for _flow_id, flow in flow_list.items():
        try:
            meter = meter_list[flow.get_meter_id()]
            flow.add_meter(meter)
        except Exception:
            flow.add_meter(None)

    return


# Gets all stats from the flows with a timestamp
# Thin wrapper for a the ryurest get_flows() method
# TODO: document the exact stats (or just link the ryu rest api docs lol)
# Args:
#   switch - ryurest switch object representing the switch the stats will be gathered from
# Returns:
#   flow_stats[switch] - flow stats for the specific switch
#   datetime.now() - current timestamp
# Note: Probably don't use this function unless you want stats for only one switch
#       Make a different one to pull from all switches (less http overhead)
def get_flow_stats(switch):

    flow_stats = switch.get_flows()

    return flow_stats[str(switch.DPID)], datetime.now()


# Gets the bytes field from the stats for every flow with a timestamp
# Bytes are cumulative so you can use the difference to compute the bandwidth
# Args:
#   switch - ryurest switch object representing the switch the stats will be gathered from
# Returns:
#   flow_bytes - dictionary containing the bytes used for each flow, indexed by cookie (pseudo flow id)
#   timestamp - the time the data was pulled from the switch
def get_flow_bytes(switch):

    all_flow_stats, timestamp = get_flow_stats(switch)

    flow_bytes = {}

    for flow_stat in all_flow_stats:
        if(flow_stat["cookie"] > 0):
            flow_bytes[flow_stat["cookie"]] = flow_stat["byte_count"]

    return flow_bytes, timestamp


# Clears the switch of existing flows/meters/queues
# Args:
#   switch - ryurest switch object representing the switch that the meters, flows will be deleted from
#   queue_configs - dictionary containing queue config information (in this case just the script name)
def clear_switch(switch, queue_configs):

    # delete flows
    switch.delete_flow_all()

    # get meters and delete them
    meters = switch.get_meter_stats()[str(switch.DPID)]
    for meter in meters:
        delete_meter_payload = {
            "dpid": switch.DPID,
            "meter_id": meter["meter_id"],
        }
        switch.delete_meter(delete_meter_payload)

    # delete flows (from config file)
    output = subprocess.check_output(["bash", str(queue_configs["clear_queue_script"])])
    print(str(output, "utf-8"))

    return

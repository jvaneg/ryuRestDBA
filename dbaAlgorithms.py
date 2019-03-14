# TODO: change this to have an allocation cap but not allocate beyond the cap
def allocate_egalitarian(flow_list, excess_bandwidth):

    active_flows = []

    # determine active flows (flows using bandwidth)
    for _flow_id, flow in flow_list.items():
        if(flow.get_demand_bw() > 0):
            active_flows.append(flow)
        else:
            flow.allocate(0, 0)

    # calculate egalitarian split of excess bandwidth
    try:
        excess_share = excess_bandwidth/len(active_flows)
    except Exception:
        excess_share = 0

    # allocate bandwidth
    for flow in active_flows:
        if(flow.get_demand_bw() >= flow.get_minimum_rate()):
            allocated_bandwidth = excess_share + flow.get_minimum_rate()
        else:
            allocated_bandwidth = excess_share + flow.get_demand_bw()

        flow.allocate(allocated_bandwidth, excess_share)

    return


# TODO: change this to have an allocation cap but not allocate beyond the cap
def allocate_proportional(flow_list, excess_bandwidth):

    active_flows = []

    # determine active flows (flows using bandwidth)
    for _flow_id, flow in flow_list.items():
        if(flow.get_demand_bw() > 0):
            active_flows.append(flow)
        else:
            flow.allocate(0, 0)

    total_flow_weight = sum(flow.get_minimum_rate() for flow in active_flows)

    # if no min rates are set just do egalitarian distribution
    if(total_flow_weight <= 0):
        allocate_egalitarian(flow_list, excess_bandwidth)
        return

    # calculate and allocate bandwidth
    for flow in active_flows:

        excess_share = (excess_bandwidth * flow.get_minimum_rate()) / total_flow_weight

        if(flow.get_demand_bw() >= flow.get_minimum_rate()):
            allocated_bandwidth = excess_share + flow.get_minimum_rate()
        else:
            allocated_bandwidth = excess_share + flow.get_demand_bw() 

        flow.allocate(allocated_bandwidth, excess_share)

    return


# TODO: change this to have an allocation cap but not allocate beyond the cap
def allocate_hybrid(flow_list, excess_bandwidth, max_fraction):

    active_flows = []

    # determine active flows (flows using bandwidth)
    for _flow_id, flow in flow_list.items():
        if(flow.get_demand_bw() > 0):
            active_flows.append(flow)
        else:
            flow.allocate(0, 0)

    # calculate flow maximums (fractions of the minimum bandwidth), and total maximum
    active_flow_maximums = {}

    for flow in active_flows:
        active_flow_maximums[flow.get_id()] = (flow.get_minimum_rate() * max_fraction) - flow.get_minimum_rate()

    total_flow_maximum = sum(active_flow_maximums.items())

    # if the sum of the fraction maximums is more than the excess bandwidth
    # just do proportional allocation instead (basically the same)
    if(total_flow_maximum >= excess_bandwidth):
        allocate_proportional(flow_list, excess_bandwidth)
        return

    remaining_excess = excess_bandwidth - total_flow_maximum

    # calculate egalitarian split of remaining excess bandwidth
    try:
        excess_share = remaining_excess/len(active_flows)
    except Exception:
        excess_share = 0

    # allocate bandwidth
    for flow in active_flows:
        if(flow.get_demand_bw() >= flow.get_minimum_rate()):
            allocated_bandwidth = excess_share + active_flow_maximums[flow.get_id()] + flow.get_minimum_rate()
        else:
            allocated_bandwidth = excess_share + active_flow_maximums[flow.get_id()] + flow.get_demand_bw()

        flow.allocate(allocated_bandwidth, excess_share + active_flow_maximums[flow.get_id()])

    return

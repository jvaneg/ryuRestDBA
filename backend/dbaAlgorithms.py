# from copy import copy


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


# probably dont need the list copy iteration stuff because it should only take one
def new_allocate_egalitarian(flow_list, excess_bandwidth):
    active_flows = []
    # determine active flows (flows using bandwidth)
    for _flow_id, flow in flow_list.items():
        if(flow.get_demand_bw() > 0):
            active_flows.append(flow)
        else:
            flow.allocate(0, 0)

    # sorts flows in ascending order
    active_flows.sort(key=sort_by_demand)

    remaining_excess = excess_bandwidth
    max_items = len(active_flows)
    current_item = 1
    for flow in active_flows:
        flow_demand = flow.get_demand_bw()
        flow_min = flow.get_minimum_rate()
        flow_extra = flow_demand - flow_min

        if(flow_demand <= flow_min):
            flow.allocate_bw(flow_demand)
        elif((flow_extra * (max_items - current_item + 1)) <= remaining_excess):
            flow.allocate_bw(flow_demand)
            remaining_excess -= flow_extra
        else:
            flow.allocate_bw(flow_min + (remaining_excess / (max_items - current_item + 1)))
            remaining_excess -= (remaining_excess / (max_items - current_item + 1))

        current_item += 1

    return


# key function to sort flows by demand bw
def sort_by_demand(flow_pair):
    return flow_pair[1].get_demand_bw()


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

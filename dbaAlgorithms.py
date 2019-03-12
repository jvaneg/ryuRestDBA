# TODO: change this to have an allocation cap but not allocate beyond the cap
def allocate_egalitarian(flow_list, excess_bandwidth):

    active_flows = []

    for _flow_id, flow in flow_list.items():
        if(flow.get_demand_bw() > 0):
            active_flows.append(flow)
        else:
            flow.allocate(0, 0)

    try:
        excess_share = excess_bandwidth/len(active_flows)
    except Exception:
        excess_share = 0

    for flow in active_flows:
        if(flow.get_demand_bw() >= flow.get_minimum_rate()):
            allocated_bandwidth = excess_share + flow.get_minimum_rate()
        else:
            allocated_bandwidth = excess_share

        flow.allocate(allocated_bandwidth, excess_share)

    return


def allocate_proportional(flow_list, excess_bandwidth):

    return


def allocate_hybrid(flow_list, excess_bandwidth):

    return


# Calculates a weighted average of a list
# TODO: Should just do this with pandas or numpy but they segfault on the NUCs for some reason
def weighted_average(items, weights):
    if(len(items) > len(weights)):
        raise Exception("items list cannot be longer than weight list")

    weighted_items = []

    for i in range(0, len(items)):
        weighted_items.append(items[i] * weights[i])

    total_weight = sum(weights[:len(items)])
    total_weighted_items = sum(weighted_items)

    return total_weighted_items/total_weight

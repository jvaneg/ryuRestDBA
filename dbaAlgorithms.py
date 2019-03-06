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
        if(flow.demand_bw() >= flow.get_minimum_rate()):
            allocated_bandwidth = excess_share + flow.get_minimum_rate()
        else:
            allocated_bandwidth = excess_share

        flow.allocate(allocated_bandwidth, excess_share)

    return


def allocate_proportional(flow_list, excess_bandwidth):

    return


def allocate_hybrid(flow_list, excess_bandwidth):

    return

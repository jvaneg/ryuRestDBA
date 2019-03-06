def allocate_egalitarian(flow_list, excess_bandwidth):

    active_flows = []

    for _flow_id, flow in flow_list.items():
        if(flow.get_demand_bw() > 0):
            active_flows.append(flow)
        else:
            flow.allocate(0)

    try:
        allocated_bandwidth = excess_bandwidth/len(active_flows)
    except Exception:
        allocated_bandwidth = 0

    for flow in active_flows:
        flow.allocate(allocated_bandwidth)

    return


def allocate_proportional(flow_list, excess_bandwidth):

    return


def allocate_hybrid(flow_list, excess_bandwidth):

    return

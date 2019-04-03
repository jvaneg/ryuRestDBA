# stdlib imports
from datetime import datetime


BYTE_TO_MEGABIT_FACTOR = 125000
BANDWIDTH_MEAN_WEIGHTS = [1, 2, 4, 8, 16, 32, 64]


# This class mostly exists as a container because I wanted to avoid using pure dicts for everything
class Flow:

    def __init__(self, property_dict):
        self.properties = property_dict
        self.prev_byte_count = 0
        self.prev_polled_time = datetime.now()
        self.prev_demand_bws = [0, 0, 0]
        self.demand_bandwidth = 0
        self.allocated_bw = 0
        self.allocated_excess_share = 0
        self.meter = None
        self.linked_flow = None

    def __repr__(self):
        return str(self.get_id())

    def __str__(self):
        return str(self.get_id())

    def get_id(self):
        return self.properties["cookie"]

    def get_demand_bw(self):
        return self.demand_bandwidth

    def update_demand_bw(self, new_byte_count, new_polled_time):

        byte_delta = new_byte_count - self.prev_byte_count
        poll_time_delta = new_polled_time - self.prev_polled_time

        megabit_delta = byte_delta/BYTE_TO_MEGABIT_FACTOR

        demand_bandwidth = megabit_delta/poll_time_delta.total_seconds()

        self.prev_demand_bws.append(demand_bandwidth)
        self.prev_demand_bws.pop(0)
        self.demand_bandwidth = weighted_average(self.prev_demand_bws, BANDWIDTH_MEAN_WEIGHTS)

        self.prev_byte_count = new_byte_count
        self.prev_polled_time = new_polled_time

        return

    def add_meter(self, meter):
        self.meter = meter

        return

    def get_meter(self):
        return self.meter

    # add more error handling here
    def get_meter_id(self):
        actions = self.properties["actions"]

        meter_id = None

        for action in actions:
            try:
                if(action["type"] == "METER"):
                    meter_id = int(action["meter_id"])
            except Exception:
                meter_id = None

        return meter_id

    def get_minimum_rate(self):
        if(self.meter is not None):
            return self.meter.get_min_rate()
        else:
            return 0

    def allocate(self, allocated_bandwidth, excess_share):
        self.allocated_bw = allocated_bandwidth
        self.excess_share = excess_share
        if(self.linked_flow is not None):
            print(excess_share)
            self.linked_flow.set_meter_rate(excess_share)

    def get_allocated_bw(self):
        return self.allocated_bw

    def set_meter_rate(self, new_rate_mbps):
        print(new_rate_mbps)
        if(self.meter is not None):
            self.meter.set_rate(new_rate_mbps)

    def add_linked_flow(self, linked_flow):
        self.linked_flow = linked_flow


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

from datetime import datetime

BYTE_TO_MEGABIT_FACTOR = 125000
BANDWIDTH_MEAN_WEIGHTS = [1, 2, 4, 8, 16, 32, 64]


# This class mostly exists as a container because I wanted to avoid using pure dicts for everything
class Flow:

    def __init__(self, property_dict):
        self.properties = property_dict
        self.prev_byte_count = 0
        self.prev_polled_time = datetime.now()
        self.prev_bandwidths = [0, 0, 0]
        self.bandwidth = 0
        self.meter = None

    def __repr__(self):
        return str(self.get_id())

    def __str__(self):
        return str(self.get_id())

    def get_id(self):
        return self.properties["cookie"]

    def get_bandwidth(self):
        return self.bandwidth

    def update_bandwidth(self, new_byte_count, new_polled_time):

        byte_delta = new_byte_count - self.prev_byte_count
        poll_time_delta = new_polled_time - self.prev_polled_time

        megabit_delta = byte_delta/BYTE_TO_MEGABIT_FACTOR

        bandwidth = megabit_delta/poll_time_delta.total_seconds()

        self.prev_bandwidths.append(bandwidth)
        self.prev_bandwidths.pop(0)
        self.bandwidth = weighted_average(self.prev_bandwidths, BANDWIDTH_MEAN_WEIGHTS)

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
                    meter_id = int(action["type"])
            except Exception:
                meter_id = None

        return meter_id


def weighted_average(items, weights):
    if(len(items) > len(weights)):
        raise Exception("items list cannot be longer than weight list")

    weighted_items = []

    for i in range(0, len(items)):
        weighted_items.append(items[i] * weights[i])

    total_weight = sum(weights)
    total_weighted_items = sum(weighted_items)

    return total_weighted_items/total_weight

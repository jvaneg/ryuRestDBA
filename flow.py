from datetime import datetime

BYTE_TO_MEGABIT_FACTOR = 125000


# This class mostly exists as a container because I wanted to avoid using pure dicts for everything
class Flow:

    def __init__(self, property_dict):
        self.properties = property_dict
        self.prev_byte_count = 0
        self.prev_polled_time = datetime.now()
        self.prev_bandwidths = []
        self.bandwidth = 0

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
        self.bandwidth = bandwidth

        self.prev_byte_count = new_byte_count
        self.prev_polled_time = new_polled_time

from datetime import datetime


# This class mostly exists as a container because I wanted to avoid using pure dicts for everything
class Flow:

    def __init__(self, property_dict):
        self.properties = property_dict
        self.prev_bytes = 0
        self.last_polled_time = datetime.now()
        self.prev_bandwidths = []

    def __repr__(self):
        return str(self.get_id())

    def __str__(self):
        return str(self.get_id())

    def get_id(self):
        return self.properties["cookie"]

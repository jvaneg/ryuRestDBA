# This class mostly exists as a container because I wanted to avoid using pure dicts for everything
class Meter:

    def __init__(self, property_dict):
        self.properties = property_dict

    def __repr__(self):
        return str(self.get_id())

    def __str__(self):
        return str(self.get_id())

    def get_id(self):
        return int(self.properties["meter_id"])

    def get_min_rate(self):
        return int(self.properties["bands"]["rate"])

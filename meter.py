# Constants
KILOBIT_TO_MEGABIT_FACTOR = 1000    # conversion factor to convert kilobits to megabits


# This class mostly exists as a container because I wanted to avoid using pure dicts for everything
class Meter:

    def __init__(self, property_dict):
        self.properties = property_dict

    def __repr__(self):
        return str(self.get_id())

    def __str__(self):
        return str(self.get_id())

    # Returns the meter's id from the property dict
    def get_id(self):
        return int(self.properties["meter_id"])

    # returns the meter's minimum rate in mbps
    # TODO: could probably use some error handling incase the meter doesn't have a band
    def get_min_rate(self):
        return int(self.properties["bands"][0]["rate"])/KILOBIT_TO_MEGABIT_FACTOR

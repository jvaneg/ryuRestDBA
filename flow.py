# This class mostly exists as a container because I wanted to avoid using pure dicts for everything
class Flow:

    def __init__(self, property_dict):
        self.properties = property_dict

        def get_id(self):
            return self.properties["cookie"]

        def __repr__(self):
            return str(get_id())

        def __str__(self):
            return str(get_id())

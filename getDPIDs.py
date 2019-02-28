# Mini script that exists just to learn the DPIDs of any connected switches

from ryuswitch import RyuSwitch

# Instantiate a new switch
switch1 = RyuSwitch()

# Get the DPIDs of all switches connected to the controller as an array.
DPID_list = switch1.get_switches()

print("DPIDs:")
print(DPID_list)

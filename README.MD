# Installation
Note: Requires Ryu be installed in environment to run.
```
git clone https://github.com/jvaneg/ryuRestDBA.git
cd ryuRestDBA
pipenv install
```

# Learn DPIDs
To learn the DPIDs of the switches the controller is connected to:
```
pipenv run python ./getDPIDs.py
```

# Run (Pica 8 Testbed)

## Run with test script
### Start ryu rest API
In one terminal, ssh into the controller (Host 4) and start the ryu rest API.

Using alias:
```
ryurest
```
Without alias:
```
ryu-manager --verbose ryu.app.simple_switch_13 ryu.app.ofctl_rest
```

### Run test script
In a second terminal, move into the main ryuRestDBA directory (on your regular PC), and run a test.

Ex:
```
bash ./tests/pica8_dba_egal/dbae_nc_udp.sh
```

Simply wait for the test to finish.

## Run manually
### Start ryu rest API
In one terminal, ssh into the controller (Host 4) and start the ryu rest API.

Using alias:
```
ryurest
```
Without alias:
```
ryu-manager --verbose ryu.app.simple_switch_13 ryu.app.ofctl_rest
```

### Start the controller
In a second terminal, ssh into the controller (Host 4) and start the controller.
```
cd ryuRestDBA
pipenv run python ./controller.py [controller config] [-l [log file]]
```


### Generate traffic
On host 3 terminal - start a server:

UDP:
```
iperf -s -u -p 5503
```
TCP
```
iperf -s -p 5503
```


On host 1/2 terminal - start a client:

UDP:
```
iperf -c 192.168.2.3 -u -b 200M -t 30 -p 5503
```
TCP
```
iperf -c 192.168.2.3 -b 200M -t 30 -p 5503
```


# Run (mininet)
Note: Requires Aaron's custom ovs on mininet (TODO: get install intructions from him).

## Start config in mininet
```
cd ryuRestDBA
sudo mn --custom ./mininet/3switchtest.py --controller=remote --topo testbed
```

## Start Ryu controller/REST API
In another terminal:
```
ryu-manager --verbose ryu.app.simple_switch_13 ryu.app.ofctl_rest
```

## Start controller application
In another terminal:
```
cd ryuRestDBA
sudo pipenv run python ./controller.py [controller config] [-l [log file]]
```
Requires sudo for queue installation and cleanup.

For min guarantee version run:
In another terminal:
```
cd ryuRestDBA
sudo pipenv run python ./controller.py ./mininet_min_guar/mn_min_guar_setup.toml [-l [log file]]
```
Requires sudo for queue installation and cleanup.
## Clean up mininet
```
sudo mn --clean
```

# Host commands (mininet)
xterm into hosts from mininet (may require xquartz to be running on macos):
```
xterm h1 h2 h3
```

## Start iperf server
On host 3 terminal:
```
iperf -s -u -p 5503
```

## Start iperf clients
On host 1 and host 2 terminals:
```
iperf -c 10.0.0.3 -u -b 200M -t 30 -p 5503
```
Note: Do not try to use a demand higher than the network can support or you will drop many packets.

# Plot tool
Note: plotTool depends on orca to output graphs. Install orca with:
```
npm install -g electron@1.8.4 orca
```
To plot the resulting data:
```
pipenv run ./tools/plotTool.py [-h] [-o output_name] [-gt graph_title] [-t graph_type] [-s stats] target_csv
```
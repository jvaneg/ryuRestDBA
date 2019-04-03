# Installation
Note: Requires Ryu be installed in environment to run.
```
git clone https://github.com/jvaneg/ryuRestDBA.git
cd ryuRestDBA
pipenv install
```

# Run (mininet)
Note: Requires Aaron's custom ovs on mininet (TODO: get install intructions from him).

## Start config in mininet
```
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
sudo pipenv run python ./controller.py [controller]
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
iperf -c 10.0.0.3 -u -b 400M -t 30 -p 5503
```
Note: Do not try to use a demand higher than the network can support or you will drop many packets.
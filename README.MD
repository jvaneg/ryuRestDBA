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


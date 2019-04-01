# Start config in mininet
sudo mn --custom /home/mininet/mininet/custom/3switchtest.py --controller=remote --topo testbed

# Clean up mininet
sudo mn --clean
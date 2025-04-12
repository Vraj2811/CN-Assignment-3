from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import OVSSwitch, OVSController
import time
import os

# Clear any existing Mininet setup
os.system('mn -c')

class CustomTopo(Topo):
    def build(self):
        # Create switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Create hosts with specified IP addresses
        h1 = self.addHost('h1', ip='10.0.0.2/24')
        h2 = self.addHost('h2', ip='10.0.0.3/24')
        h3 = self.addHost('h3', ip='10.0.0.4/24')
        h4 = self.addHost('h4', ip='10.0.0.5/24')
        h5 = self.addHost('h5', ip='10.0.0.6/24')
        h6 = self.addHost('h6', ip='10.0.0.7/24')
        h7 = self.addHost('h7', ip='10.0.0.8/24')
        h8 = self.addHost('h8', ip='10.0.0.9/24')

        # Add links between switches with latency of 7ms each
        self.addLink(s1, s2, cls=TCLink, delay='7ms')
        self.addLink(s2, s3, cls=TCLink, delay='7ms')
        self.addLink(s3, s4, cls=TCLink, delay='7ms')
        self.addLink(s4, s1, cls=TCLink, delay='7ms')
        self.addLink(s1, s3, cls=TCLink, delay='7ms')

        # Add links between hosts and switches with latency of 5ms each
        self.addLink(h1, s1, cls=TCLink, delay='5ms')
        self.addLink(h2, s1, cls=TCLink, delay='5ms')
        self.addLink(h3, s2, cls=TCLink, delay='5ms')
        self.addLink(h4, s2, cls=TCLink, delay='5ms')
        self.addLink(h5, s3, cls=TCLink, delay='5ms')
        self.addLink(h6, s3, cls=TCLink, delay='5ms')
        self.addLink(h7, s4, cls=TCLink, delay='5ms')
        self.addLink(h8, s4, cls=TCLink, delay='5ms')

def run():
    topo = CustomTopo()
    net = Mininet(topo=topo, controller=OVSController, link=TCLink, switch=OVSSwitch)
    net.start()

    # Enable STP on all switches
    for sw in ['s1', 's2', 's3', 's4']:
        sw_obj = net.get(sw)
        sw_obj.cmd('ovs-vsctl set Bridge {} stp_enable=true'.format(sw))

    h3 = net.get('h3')
    h5 = net.get('h5')
    h8 = net.get('h8')

    print("\nTesting connectivity (each test runs 3 times with 30s interval):")

    time.sleep(30)
    for i in range(3):
        print(f"\n--- Test {i+1}/3: Ping h1 from h3 ---")
        print(h3.cmd('ping -c 4 10.0.0.2'))
        time.sleep(30)

    for i in range(3):
        print(f"\n--- Test {i+1}/3: Ping h7 from h5 ---")
        print(h5.cmd('ping -c 4 10.0.0.8'))
        time.sleep(30)

    for i in range(3):
        print(f"\n--- Test {i+1}/3: Ping h2 from h8 ---")
        print(h8.cmd('ping -c 4 10.0.0.3'))
        time.sleep(30)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()

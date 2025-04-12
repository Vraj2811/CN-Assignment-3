from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
import os
import time

# Clean previous Mininet state
os.system('mn -c')

class CustomTopo(Topo):
    def build(self):
        # Create switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Create hosts with specific IPs
        h1 = self.addHost('h1', ip='10.0.0.2/24')
        h2 = self.addHost('h2', ip='10.0.0.3/24')
        h3 = self.addHost('h3', ip='10.0.0.4/24')
        h4 = self.addHost('h4', ip='10.0.0.5/24')
        h5 = self.addHost('h5', ip='10.0.0.6/24')
        h6 = self.addHost('h6', ip='10.0.0.7/24')
        h7 = self.addHost('h7', ip='10.0.0.8/24')
        h8 = self.addHost('h8', ip='10.0.0.9/24')

        # Add switch-switch links (ring topology)
        self.addLink(s1, s2, cls=TCLink, delay='7ms')
        self.addLink(s2, s3, cls=TCLink, delay='7ms')
        self.addLink(s3, s4, cls=TCLink, delay='7ms')
        self.addLink(s4, s1, cls=TCLink, delay='7ms')
        self.addLink(s1, s3, cls=TCLink, delay='7ms')

        # Add host-switch links
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
    net = Mininet(topo=topo, controller=None, link=TCLink)
    net.start()

    h2 = net.get('h2')
    h8 = net.get('h8')

    print("Starting tcpdump on h8 and h2...\n")
    
    # Run tcpdump in background and redirect to files
    h8.cmd('tcpdump -i h8-eth0 arp or icmp > h8_dump.txt 2>&1 &')
    h2.cmd('tcpdump -i h2-eth0 arp or icmp > h2_dump.txt 2>&1 &')

    time.sleep(2)  # Give tcpdump time to start

    print("Running ping from h8 to h2...\n")
    # Run ping
    output = h8.cmd('ping -c 4 10.0.0.3')
    with open('ping_output.txt', 'w') as f:
        f.write(output)

    time.sleep(3) 
    
    print("Killing background tcpdump processes...\n")
    # Kill tcpdump
    h8.cmd("pkill -f 'tcpdump -i h8-eth0'")
    h2.cmd("pkill -f 'tcpdump -i h2-eth0'")

    print("Outputs saved to: ping_output.txt, h8_dump.txt, h2_dump.txt")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()

# =============================================================================
# MININET TOPOLOGY
# File: ~/sdn_project/topology.py
# =============================================================================
# Creates:
#   h1 (10.0.0.1) ──port1──┐
#   h2 (10.0.0.2) ──port2──┤── s1 ←── POX Controller (127.0.0.1:6633)
#   h3 (10.0.0.3) ──port3──┘
# =============================================================================

from mininet.topo   import Topo
from mininet.net    import Mininet
from mininet.node   import RemoteController, OVSSwitch
from mininet.cli    import CLI
from mininet.log    import setLogLevel, info

class StarTopo(Topo):
    def build(self):
        # Add ONE switch (OpenFlow 1.0 — POX default)
        s1 = self.addSwitch('s1')

        # Add three hosts with FIXED MACs for easy identification in logs
        h1 = self.addHost('h1',
                          ip  = '10.0.0.1/24',
                          mac = '00:00:00:00:00:01')
        h2 = self.addHost('h2',
                          ip  = '10.0.0.2/24',
                          mac = '00:00:00:00:00:02')
        h3 = self.addHost('h3',
                          ip  = '10.0.0.3/24',
                          mac = '00:00:00:00:00:03')

        # Link hosts to switch (creates ports 1, 2, 3 on s1)
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)


def run():
    setLogLevel('info')
    topo = StarTopo()

    net = Mininet(
        topo       = topo,
        controller = RemoteController(
            'c0',
            ip   = '127.0.0.1',
            port = 6633           # POX listens on 6633 (not 6653)
        ),
        switch = OVSSwitch
    )

    net.start()

    info('\n' + '=' * 50 + '\n')
    info('  Network is UP\n')
    info('  h1 = 10.0.0.1  MAC=00:00:00:00:00:01\n')
    info('  h2 = 10.0.0.2  MAC=00:00:00:00:00:02\n')
    info('  h3 = 10.0.0.3  MAC=00:00:00:00:00:03\n')
    info('  Controller: POX at 127.0.0.1:6633\n')
    info('=' * 50 + '\n')
    info('  Commands to try:\n')
    info('    h1 ping h2 -c 3\n')
    info('    pingall\n')
    info('    sh ovs-ofctl dump-flows s1\n')
    info('=' * 50 + '\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    run()
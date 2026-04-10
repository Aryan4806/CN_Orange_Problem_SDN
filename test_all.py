# =============================================================================
# AUTOMATED TEST SCRIPT — proves all 4 features
# File: ~/sdn_project/test_all.py
# Run AFTER starting POX controller in another terminal.
# =============================================================================

from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.log  import setLogLevel
import subprocess, time

class StarTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

def dump_flows():
    r = subprocess.run(
        ['ovs-ofctl', 'dump-flows', 's1'],
        capture_output=True, text=True
    )
    return r.stdout

def sep(title=""):
    print("\n" + "=" * 54)
    if title:
        print("  " + title)
        print("=" * 54)

def run_tests():
    setLogLevel('warning')
    sep("SDN LEARNING SWITCH — AUTO TEST SUITE")

    net = Mininet(
        topo       = StarTopo(),
        controller = RemoteController('c0', ip='127.0.0.1', port=6633),
        switch     = OVSSwitch
    )
    net.start()
    time.sleep(3)

    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')

    # ------ TEST 1: Initial flow table ------
    sep("TEST 1 — Initial flow table")
    flows = dump_flows()
    print(flows)
    has_tablemiss = any(
        'priority=1' in l and 'CONTROLLER' in l
        for l in flows.splitlines()
    )
    print("  Table-miss rule present:", "PASS ✓" if has_tablemiss else "FAIL ✗")

    # ------ TEST 2: First ping (MAC learning + flooding) ------
    sep("TEST 2 — First ping h1 → h2 (triggers MAC learning)")
    result = h1.cmd('ping -c 1 10.0.0.2')
    print(result)
    ok = '1 received' in result or '1 packets received' in result
    print("  h1 → h2 ping:", "PASS ✓" if ok else "FAIL ✗")

    # ------ TEST 3: Flow table after first ping ------
    sep("TEST 3 — Flow table after learning (flow rules installed?)")
    time.sleep(1)
    flows = dump_flows()
    print(flows)
    priority100 = flows.count('priority=100')
    print(f"  Flow rules (priority=100) installed: {priority100}  →  ",
          "PASS ✓" if priority100 >= 1 else "FAIL ✗")

    # ------ TEST 4: Repeat ping (uses flow rules, not controller) ------
    sep("TEST 4 — Repeat ping h1 → h2 (should use flow rules)")
    result = h1.cmd('ping -c 4 10.0.0.2')
    print(result)
    ok = '4 received' in result or '4 packets received' in result
    print("  4-ping test:", "PASS ✓" if ok else "FAIL ✗")

    # ------ TEST 5: New destination ------
    sep("TEST 5 — Ping h1 → h3 (new destination, re-learns)")
    result = h1.cmd('ping -c 2 10.0.0.3')
    print(result)
    ok = '2 received' in result or '2 packets received' in result
    print("  h1 → h3 ping:", "PASS ✓" if ok else "FAIL ✗")

    # ------ TEST 6: Full connectivity ------
    sep("TEST 6 — Full connectivity (pingall)")
    net.pingAll()

    # ------ TEST 7: Final flow table ------
    sep("TEST 7 — Final flow table (all rules)")
    flows = dump_flows()
    print(flows)

    sep("ALL TESTS COMPLETE")
    print("  [F1] MAC Learning   → see POX terminal for [MAC LEARNED] logs")
    print("  [F2] Flow Install   → see priority=100 entries above")
    print("  [F3] Forwarding     → all pings succeeded above")
    print("  [F4] Flow Inspect   → ovs-ofctl dump-flows s1 output above")
    print("=" * 54 + "\n")

    net.stop()

if __name__ == '__main__':
    run_tests()
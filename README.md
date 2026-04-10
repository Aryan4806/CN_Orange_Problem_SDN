# SDN Learning Switch Controller

## Problem Statement

Implement a Software-Defined Networking (SDN) controller that mimics the behavior of a traditional learning switch by dynamically learning MAC addresses and installing forwarding rules.

---

## Objective

The goal of this project is to:

- Learn MAC-to-port mappings dynamically
- Forward packets efficiently without unnecessary flooding
- Install flow rules in switches to optimize performance
- Validate packet forwarding behavior
- Inspect flow tables in the switch

---

## Key Functionalities

### 1. MAC Address Learning Logic

The controller learns the source MAC address from incoming packets and stores the mapping of MAC → Port.

**Example mappings:**

| MAC Address       | Port   |
|-------------------|--------|
| 00:00:00:00:00:01 | Port 1 |
| 00:00:00:00:00:02 | Port 2 |

### 2. Dynamic Flow Rule Installation

Once the destination MAC is known, a flow rule is installed directly in the switch. This avoids repeated communication with the controller on subsequent packets.

### 3. Packet Forwarding Logic

| Destination Status | Action         | Effect                               |
|--------------------|----------------|--------------------------------------|
| Unknown            | FLOOD          | Packet sent to all ports             |
| Known              | DIRECT FORWARD | Packet sent to specific port only    |

This reduces network overhead after the initial learning phase.

### 4. Flow Table Inspection

Flow entries can be verified using:

```bash
ovs-ofctl dump-flows s1
```

The output shows:
- Source MAC address
- Destination MAC address
- Output port

---

## Implementation Details

| Component   | Technology                    |
|-------------|-------------------------------|
| Controller  | POX (Python-based SDN controller) |
| Emulator    | Mininet                       |
| Protocol    | OpenFlow 1.0                  |

---

## Execution Steps

### Step 1 — Run the Controller

```bash
cd ~/pox
sudo python3 pox.py openflow.of_01 --port=6633 learning_switch
```

### Step 2 — Start Mininet

```bash
sudo mn -c
sudo mn --topo single,3 --controller=remote,ip=127.0.0.1,port=6633
```

### Step 3 — Test Connectivity

```
mininet> pingall
```

### Step 4 — Inspect the Flow Table

```bash
sudo ovs-ofctl dump-flows s1
```

---

## Output Analysis

### Controller Output

Displays switch connection events, MAC learning, flooding of unknown packets, and direct forwarding after learning.

```
Learning Switch Started 🚀
Switch connected
Flooding packet
Forwarding MAC1 -> MAC2 via port X
```

### Mininet Output

Shows the network topology with 3 hosts and ping results confirming full connectivity.

```
*** Results: 0% dropped (6/6 received)
```

### Flow Table Output

Displays the dynamically installed flow rules in the switch.

```
dl_src=MAC1, dl_dst=MAC2, actions=output:port
```

---

## Screenshots

| Screenshot             | Description                                              |
|------------------------|----------------------------------------------------------|
| Controller Output      | Shows MAC learning, flooding, and forwarding behavior    |
| Mininet Ping Test      | Shows successful communication between hosts (0% loss)   |
| Flow Table             | Shows dynamically installed flow entries in the switch   |

---

## Results

The implementation successfully demonstrated a learning switch using SDN principles:

- **Efficient packet forwarding** — direct routing after MAC learning
- **Reduced flooding** — only during the initial discovery phase
- **Dynamic flow rule installation** — rules pushed directly to the switch
- **Verified behavior** — confirmed via ping tests and flow table inspection

---

## Conclusion

The SDN Learning Switch Controller effectively replicates the behavior of a traditional network switch by learning MAC addresses dynamically, reducing unnecessary flooding, and improving network efficiency through programmatic flow rules. This demonstrates the flexibility and power of SDN in controlling network behavior at the application layer.

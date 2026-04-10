📘 SDN Learning Switch Controller
📌 Project Title
SDN Learning Switch Controller
🎯 Problem Statement
Implement a Software-Defined Networking (SDN) controller that mimics the behavior of a traditional learning switch by dynamically learning MAC addresses and installing forwarding rules.
🧠 Objective
The goal of this project is to:
Learn MAC-to-port mappings dynamically
Forward packets efficiently without unnecessary flooding
Install flow rules in switches to optimize performance
Validate packet forwarding behavior
Inspect flow tables in the switch
⚙️ Key Functionalities
🔹 1. MAC Address Learning Logic
The controller learns the source MAC address from incoming packets.
Stores mapping: MAC → Port
Example:
00:00:00:00:00:01 → Port 1
00:00:00:00:00:02 → Port 2
🔹 2. Dynamic Flow Rule Installation
Once destination MAC is known:
A flow rule is installed in the switch
This avoids repeated communication with the controller
🔹 3. Packet Forwarding Logic
Unknown destination → FLOOD
Known destination → DIRECT FORWARD
Reduces network overhead after learning phase
🔹 4. Flow Table Inspection
Flow entries can be verified using:
ovs-ofctl dump-flows s1
Shows:
Source MAC
Destination MAC
Output port
🏗️ Implementation Details
Controller: POX (Python-based SDN controller)
Emulator: Mininet
Protocol: OpenFlow 1.0
🚀 Execution Steps
Step 1: Run Controller
cd ~/pox
sudo python3 pox.py openflow.of_01 --port=6633 learning_switch
Step 2: Start Mininet
sudo mn -c
sudo mn --topo single,3 --controller=remote,ip=127.0.0.1,port=6633
Step 3: Test Connectivity
mininet> pingall
Step 4: Inspect Flow Table
sudo ovs-ofctl dump-flows s1
📊 Output Analysis
🖥️ 1. Controller Output
Displays:
Switch connection
MAC learning
Flooding of unknown packets
Forwarding after learning
Example:
Learning Switch Started 🚀
Switch connected
Flooding packet
Forwarding MAC1 -> MAC2 via port X
🌐 2. Mininet Output
Shows network topology with 3 hosts
Ping results confirm connectivity
Example:
*** Results: 0% dropped (6/6 received)
📋 3. Flow Table Output
Displays installed flow rules
Example:
dl_src=MAC1, dl_dst=MAC2, actions=output:port
📸 Screenshots
🔹 Controller Output
Shows MAC learning, flooding, and forwarding behavior.
🔹 Mininet Ping Test
Shows successful communication between hosts (0% packet loss).
🔹 Flow Table
Shows dynamically installed flow entries in the switch.
✅ Results
Successfully implemented a learning switch using SDN principles
Achieved:
Efficient packet forwarding
Reduced flooding after learning
Dynamic flow rule installation
Verified using:
Ping tests
Flow table inspection
🧠 Conclusion
The SDN Learning Switch Controller effectively replicates the behavior of a traditional switch by:
Learning MAC addresses dynamically
Reducing unnecessary flooding
Improving network efficiency using flow rules
This demonstrates the flexibility and power of SDN in controlling network behavior programmatically.

# cn-mini-project

SDN SOCKET PROGRAMMING MINI PROJECT | FINAL PROJECT REPORT

PES UNIVERSITY

SDN SOCKET PROGRAMMING
MINI PROJECT — FINAL REPORT

Deliverable 1 and Deliverable 2

Project Title: Remote System Health Monitoring using UDP Socket Programming and SDN
Project Number: 11

Submitted by
1. Name: Rohitsamartha B | SRN : PES1UG25AM321
2. Name: Rohan R Sakhare | SRN : PES1UG25AM316
3. Name: Sanvi S Shetty | SRN : PES1UG25AM352
   
Subject: Computer Networks

Department: Computer Science and Engineering (AI & ML)
Submitted to: Vidya K

Academic Year: 2026 -27

<img width="685" height="305" alt="Screenshot 2026-11-19 at 10 05 26 PM" src="https://github.com/user-attachments/assets/342e5dec-e23f-4a3a-b370-9e56bcc1387b" />


SDN Socket Programming Project Report
SDN SOCKET PROGRAMMING MINI PROJECT | FINAL PROJECT REPORT

MININET TOPOLOGY — ORIGINAL OUTPUT SCREENSHOT
The following is the original topology screenshot supplied for the project. It is inserted without editing.

<img width="668" height="418" alt="Screenshot 2026-11-19 at 10 05 48 PM" src="https://github.com/user-attachments/assets/509af677-1262-4afa-b5eb-48ff53c94330" />


Figure 1. Mininet startup showing hosts h1, h2, h3 and switch s1.

<img width="666" height="402" alt="Screenshot 2026-11-19 at 10 07 36 PM" src="https://github.com/user-attachments/assets/a22ebed5-d7ee-407b-b778-2a9576c0deac" />


SDN Socket Programming Project Report
SDN SOCKET PROGRAMMING MINI PROJECT | FINAL PROJECT REPORT

ABSTRACT

This project demonstrates a remote system health monitoring application integrated with Software-Defined Networking (SDN). Monitoring agents send system reports to a server using UDP sockets. The reports contain a host identifier and resource information such as CPU and memory usage. The server checks the received values against configured thresholds. When a high-resource condition is detected, the application can request a network action by installing a flow rule on an Open vSwitch switch. Mininet is used to create and test a virtual network containing three hosts and one switch.
The project is organised into two stages. Deliverable 1 establishes the basic topology, UDP communication, monitoring-server operation and SDN flow verification. Deliverable 2 extends the monitoring demonstration with multiple agents, additional resource fields, alert handling and a broader testing and evaluation plan. The screenshots in this report are the evidence supplied for the demonstrated runs; they are described according to what is visible in each image.


1. INTRODUCTION
Modern computer networks need ways to monitor endpoint resources and respond to changing conditions. CPU and memory usage can indicate that a device is overloaded. This project combines socket programming with SDN so that monitoring information can be collected centrally and network traffic can be controlled using flow rules.

1.1 Objectives

• Create a virtual network using Mininet.
• Implement communication between monitoring agents and a server using UDP sockets.
• Represent monitoring reports in JSON format.
• Check CPU and memory values and display alerts when configured thresholds are crossed.
• Demonstrate an SDN flow rule on an Open vSwitch switch.
• Verify network behaviour using ping tests and flow-table inspection.
• Extend the monitoring demonstration to multiple agents and additional report fields.

1.2 Tools and technologies

Technology Purpose
Python 3 | Implementation of agents and monitoring server.

UDP sockets | Transport monitoring reports from agents to server.

JSON | Structured representation of report data.

Mininet | Creation of the virtual network topology.

Open vSwitch | Software switch used to apply flow rules.

OpenFlow 1.3 | Flow-rule interface used in switch verification.

Ubuntu | Development and demonstration environment.


2. SYSTEM ARCHITECTURE

The system follows a monitoring-and-response workflow. Agents collect or generate resource values and send
reports to the server. The server decodes each report, identifies the host, checks the configured thresholds and
triggers the SDN rule operation when required. The switch enforces the matching flow rule.

Monitoring Agent(s) (h1 / h2 / h3) | UDP + JSON Report | Monitoring Server  (10.0.0.1:5005/integrated port)
↓                                   ↓                    ↓
Mininet Hosts                       Open vSwitch         OpenFlow Rule
h1, h2, h3                          s1                   Allow / Drop selected traffic
Figure 2. Logical architecture of the monitoring and SDN response system.

2.1 Component descriptions
Component                           | Function
Monitoring agent                      Creates a report containing the host identifier and resource values, then sends it to the server.
UDP socket                            Sends report data as a datagram without establishing a TCP connection.
JSON encoder/decoder                  Converts the report dictionary to bytes for transmission and back to structured data at the server.
Monitoring server                     Receives reports, displays the values and checks thresholds.
Mininet topology                      Provides the virtual hosts and switch used for network experiments.
Open vSwitch s1                       Applies flow rules that match selected packets.
Flow verification                     Uses ovs-ofctl to inspect installed rules and ping to observe traffic behaviour.

2.2 Network topology

The demonstrated topology is a single-switch Mininet topology with three hosts. The hosts are connected to
switch s1. The observed host addresses in the screenshots are h1 = 10.0.0.1, h2 = 10.0.0.2 and h3 = 10.0.0.3.

sudo mn --controller=ovsc --topo single,3
nodes
pingall

The pingall command checks reachability among Mininet hosts. In the earlier initial test, the result was 0% packet
loss. A later SDN test intentionally blocked traffic from 10.0.0.1 to 10.0.0.2.

3. DELIVERABLE 1 — IMPLEMENTATION
   
3.1 Agent operation

The agent is the sender in the monitoring application. It prepares a report with a host name and CPU/memory
values, converts the report into JSON bytes and sends it to the configured server IP address and UDP port. The
earlier simple agent example generated simulated values at regular intervals; the integrated agent allowed a CPU
value to be supplied through command-line arguments.

3.2 Integrated agent code

import json
import socket
import sys
if len(sys.argv) != 3:
print("Usage: python3 d1_integrated_agent.py laptop1 90")
sys.exit(1)
report = {
"host": sys.argv[1],
"cpu": float(sys.argv[2]),
SDN Socket Programming Project Report
SDN SOCKET PROGRAMMING MINI PROJECT | FINAL PROJECT REPORT
"memory": 50
}
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(
json.dumps(report).encode(),
("127.0.0.1", 5006)
)
client.close()
print("UDP report sent:", report)

3.3 Explanation of integrated agent

Code part                   | Explanation
import json, socket, sys      Loads JSON conversion, UDP networking and command-line argument modules.
len(sys.argv) != 3            Checks that the user supplied an agent name and CPU value.
sys.argv[1]                   Reads the host/agent name from the command line.
float(sys.argv[2])            Converts the CPU argument into a numeric value.
"memory": 50                  Adds a fixed memory value of 50 percent in this demonstration code.
socket(AF_INET, SOCK_DGRAM)   Creates an IPv4 UDP socket.
json.dumps(report).encode()   Converts the report dictionary into JSON bytes.
127.0.0.1:5006                Sends the report to port 5006 on the same machine. This loopback setup is a local integrated test.
client.close()                Closes the UDP socket after sending the report.

3.4 Server operation
The integrated server listens on its configured UDP port, receives datagrams, decodes the JSON report and
displays the host, CPU and memory values. When the CPU value crosses the configured threshold, the server
displays an alert and invokes the SDN action in the integrated demonstration. The supplied screenshot shows the
server listening on UDP port 5006 and receiving a report with CPU=90.0% and Memory=50.0%.

3.5 SDN flow rule
The flow-table evidence shows a rule with priority 200 matching IPv4 traffic from 10.0.0.1 to 10.0.0.2 and applying
actions=drop. This means packets matching that source and destination pair are discarded by the switch.
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
The flow table should be inspected while Mininet is running and switch s1 exists. The rule and ping test together
provide stronger evidence than a server print message alone.

4. DELIVERABLE 2 — EXTENDED MONITORING DEMONSTRATION
The supplied D2 screenshots show monitoring activity involving multiple Mininet hosts. The server output displays
reports from h2 and h3, including CPU and memory percentages, and shows alerts when high CPU or memory
values are detected. Another screenshot shows a server message indicating that a blocking rule was installed for
traffic from 10.0.0.1 to 10.0.0.2.

4.1 Additional report fields visible in the agent output
The supplied h2 agent screenshot displays a report containing host, cpu_percent, memory_percent,
process_count, network_tx_kbps, network_rx_kbps and timestamp. This indicates a richer monitoring report than
SDN Socket Programming Project Report
SDN SOCKET PROGRAMMING MINI PROJECT | FINAL PROJECT REPORT
the simple D1 example. The screenshot also shows a Network is unreachable error after some reports were sent.
This is documented as an observed connectivity issue in that particular run, not as a successful transmission.

4.2 D2 functional behaviour
• Agents send periodic reports containing host and resource information.
• The server receives reports from different hosts and prints their values.
• The server detects high CPU usage and displays a CPU alert.
• The server detects high memory usage and displays a memory alert.
• The server detects a host that has stopped sending reports in the shown monitoring output.
• The SDN server output indicates installation of a blocking rule for the selected h1-to-h2 traffic.

4.3 Threshold-based response
The screenshots show alerts at high CPU values, including values around or above 80%, and a high-memory alert at 88% or 94%. The exact threshold configuration should be confirmed from the final source code before submission. The server output also shows an alert when h2 stops sending reports.

5. TESTING AND RESULTS
   
5.1 Initial topology test
The Mininet topology was started with three hosts and one switch. The earlier pingall result was successful with 0% packet loss, indicating initial host connectivity before applying the blocking rule.

5.2 SDN blocking test
The h1-to-h2 ping test shows 3 packets transmitted, 0 received and 100% packet loss. The h2-to-h3 test shows 3 packets transmitted, 3 received and 0% packet loss. This is consistent with the displayed rule that drops traffic from 10.0.0.1 to 10.0.0.2 while another host pair remains reachable.

5.3 Flow-table verification
The ovs-ofctl output shows priority=200, source 10.0.0.1, destination 10.0.0.2 and actions=drop. The output also
shows packet counters, indicating that matching packets were counted by the rule.

5.4 D2 monitoring test
The supplied server screenshot shows reports from h2 and h3 with varying CPU and memory values. It includes
high-CPU alerts, a high-memory alert and a message that h2 stopped sending reports. These outputs
demonstrate monitoring and alert display in the shown run.

5.5 Test summary
Test                              Observed evidence                                              Result from supplied screenshot
Mininet topology creation         Hosts h1, h2, h3 and switch s1.                                Topology created.
                                  displayed.

Initial connectivity              Earlier pingall reported 0% packet loss                         Initial connectivity successful.

High CPU report                   Integrated server received                                      High CPU alert displayed.
                                  CPU=90.0%.                      
Flow rule                         priority=200; nw_src=10.0.0.1; nw_dst=10.0.0.2; actions=drop.   Drop rule visible in flow table.

h1 to h2 connectivity             3 transmitted, 0 received, 100% loss.                           Traffic blocked as expected for this rule.

h2 to h3 connectivity             3 transmitted, 3 received, 0% loss.                             Traffic remained reachable.

Multiple-host monitoring          Server output shows h2 and h3 reports                           Monitoring output observed.

SDN Socket Programming Project Report

and CPU/memory alerts.
Agent network issue                h2 screenshot ends with Network is unreachable.                Connectivity issue observed in that run.

6. LIMITATIONS AND OBSERVATIONS
   
• The integrated agent screenshot uses 127.0.0.1:5006 for a same-machine test. Loopback communication is
not the same as communication from a Mininet host to a server in another network namespace.
• Different screenshots show different UDP ports and server configurations. The final source files must be
checked so that each agent destination port matches the server bind port.
• The h2 agent screenshot records a Network is unreachable error after earlier reports were sent. This
indicates that the network path was not available for that later send attempt.
• Some D1 demonstration values are manually supplied or simulated; they should not be described as real
hardware measurements unless the final agent code actually collects system metrics.
• The report describes only the outputs visible in the supplied screenshots. Any further D2 performance
measurements should be added only after collecting actual latency, packet-loss and throughput data.

7. CONCLUSION
   
The project demonstrates the integration of UDP socket communication, system-resource reporting and SDN-
based traffic control in a Mininet environment. The D1 evidence shows the virtual topology, server reception of a
high-CPU report, installation and verification of an OpenFlow drop rule, and the corresponding connectivity
behaviour. The D2 evidence extends the monitoring demonstration to multiple hosts and additional resource
fields, with CPU, memory and missing-report alerts. The screenshots also identify a network-reachability issue in
one agent run, which should be considered during final testing. The project provides a foundation for further work
such as reliable multi-agent monitoring, recovery-based flow removal and measured performance comparison.

8. TEAM MEMBER DETAILS AND CONTRIBUTIONS
   
Member                  Name              SRN              Contribution
Member 1                Rohitsamartha B   PES1UG25AM321    Topology, agent and UDP report explanation.
Member 2                Sanvi S Shetty    PES1UG25AM352    Server-side report reception,threshold checking and alerts.
Member 3                Rohan R Sakhare   PES1UG25AM316    Mininet/Open vSwitch flow verification and testing.


APPENDIX A — OUTPUT SCREENSHOTS
The following screenshots are included as supplied. Captions describe the visible output; screenshots have not been recreated as text.

<img width="622" height="410" alt="image" src="https://github.com/user-attachments/assets/dd579ce0-b70b-4bdb-8160-83c452a95117" />




Figure A1. Integrated server receiving a high-CPU report on UDP port 5006.



<img width="1297" height="388" alt="Screenshot 2026-11-19 at 10 40 20 PM" src="https://github.com/user-attachments/assets/d97c260b-ea99-4a5e-b4c6-fae596977eb2" />




Figure A2. Mininet connectivity test: h1 to h2 is blocked while h2 to h3 succeeds.



<img width="619" height="401" alt="image" src="https://github.com/user-attachments/assets/b57f2600-115f-41f8-815f-07ad4978c9ee" />



Figure A3. Open vSwitch flow-table entry showing the priority-200 drop rule.



<img width="622" height="461" alt="image" src="https://github.com/user-attachments/assets/9f1a934a-0b81-4841-9fb2-12dddab282f8" />



Figure A4. Multi-host monitoring output with CPU/memory alerts and a stopped-agent message.




<img width="619" height="459" alt="image" src="https://github.com/user-attachments/assets/4b8528ef-213b-4822-9420-8708f80e5662" />



Figure A5. Agent report fields and the later Network is unreachable error in that run.




<img width="619" height="458" alt="image" src="https://github.com/user-attachments/assets/32c7b4ff-81df-4604-ad8b-adb23a020e4a" />



Figure A6. D2 monitoring server output showing reports, CPU/memory alerts and blocking action





<img width="663" height="411" alt="image" src="https://github.com/user-attachments/assets/ca5e9dae-bb57-4138-acb4-d24531d067ad" />



SDN Socket Programming Project Report

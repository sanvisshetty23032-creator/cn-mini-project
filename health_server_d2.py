
import json
import socket
import time
import subprocess

SERVER_IP = "10.0.0.1"
SERVER_PORT = 5005

CPU_LIMIT = 80
MEMORY_LIMIT = 85
AGENT_TIMEOUT_SECONDS = 6

SWITCH = "s1"
BLOCK_SOURCE = "10.0.0.1"
BLOCK_DESTINATION = "10.0.0.2"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))
sock.settimeout(1)

last_seen = {}
stale_alerted = set()
blocked = False

print(f"D2 Monitoring server listening on {SERVER_IP}:{SERVER_PORT}")

def install_flow_rule():
    global blocked

    if blocked:
        return

    command = [
        "ovs-ofctl", "-O", "OpenFlow13",
        "add-flow", SWITCH,
        f"priority=200,ip,nw_src={BLOCK_SOURCE},"
        f"nw_dst={BLOCK_DESTINATION},actions=drop"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            blocked = True
            print("SDN ACTION: Blocking rule installed!")
            print(f"Blocked traffic: {BLOCK_SOURCE} -> {BLOCK_DESTINATION}")
        else:
            print("SDN ERROR:", result.stderr.strip())

    except (OSError, subprocess.TimeoutExpired) as error:
        print("SDN ERROR:", error)

try:
    while True:
        try:
            data, address = sock.recvfrom(4096)
            report = json.loads(data.decode("utf-8"))

            host = str(report["host"])
            cpu = float(report["cpu_percent"])
            memory = float(report["memory_percent"])

            last_seen[host] = time.time()
            stale_alerted.discard(host)

            print(
                f"{host} from {address}: "
                f"CPU={cpu:.1f}% MEM={memory:.1f}%"
            )

            if cpu >= CPU_LIMIT:
                print(f"ALERT: High CPU on {host}: {cpu:.1f}%")
                install_flow_rule()

            if memory >= MEMORY_LIMIT:
                print(f"ALERT: High memory on {host}: {memory:.1f}%")

        except socket.timeout:
            pass

        except (ValueError, KeyError, TypeError,
                UnicodeDecodeError, json.JSONDecodeError) as error:
            print("Invalid report:", error)

        now = time.time()

        for host, last_time in list(last_seen.items()):
            if now - last_time > AGENT_TIMEOUT_SECONDS:
                if host not in stale_alerted:
                    print(f"ALERT: {host} stopped sending reports")
                    stale_alerted.add(host)

except KeyboardInterrupt:
    print("\nD2 Monitoring server stopped.")

finally:
    sock.close()


import json
import socket
import subprocess

PORT = 5010
THRESHOLD = 80

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", PORT))

print("Integrated server running on UDP port 5006")

try:
    while True:
        data, address = server.recvfrom(4096)
        try:
            report = json.loads(data.decode())
            host = report.get("host", "unknown")
            cpu = float(report.get("cpu", 0))
            memory = float(report.get("memory", 0))

            print(f"Report: {host}, CPU={cpu}%, Memory={memory}%")

            if cpu >= THRESHOLD:
                print("ALERT: High CPU detected")

                result = subprocess.run(
                    [
                        "ovs-ofctl", "-O", "OpenFlow13",
                        "add-flow", "s1",
                        "priority=200,ip,nw_src=10.0.0.1,"
                        "nw_dst=10.0.0.2,actions=drop"
                    ],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print("SDN ACTION: Rule installed to block h1 -> h2")
                else:
                    print("SDN ERROR:", result.stderr.strip())

        except (ValueError, json.JSONDecodeError) as error:
            print("Invalid report:", error)

except KeyboardInterrupt:
    print("Server stopped")
finally:
    server.close()

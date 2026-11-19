import json
import socket
import sys

if len(sys.argv) != 3:
    print("Usage: python3 d1_integrated_agent.py laptop1 90")
    sys.exit(1)

report = {
    "host": sys.argv[1],
    "cpu": float(sys.argv[2]),
    "memory": 50
}

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(
    json.dumps(report).encode(),
    ("127.0.0.1", 5010)
)
client.close()

print("UDP report sent:", report)

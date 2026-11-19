import socket
import json
import time
import random
import sys

SERVER_IP = "10.0.0.1"
SERVER_PORT = 5005
HOST_NAME = sys.argv[1] if len(sys.argv) > 1 else "host"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Health agent started: {HOST_NAME}")
print(f"Sending UDP reports to {SERVER_IP}:{SERVER_PORT}")

try:
    while True:
        # Simulated per-host statistics for the first demo
        report = {
            "host": HOST_NAME,
            "cpu_percent": random.randint(10, 100),
            "memory_percent": random.randint(20, 95),
            "process_count": random.randint(30, 150),
            "network_tx_kbps": random.randint(100, 2000),
            "network_rx_kbps": random.randint(100, 2000),
            "timestamp": time.time()
        }

        message = json.dumps(report).encode("utf-8")
        sock.sendto(message, (SERVER_IP, SERVER_PORT))

        print("Report sent:", report)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nAgent stopped.")

finally:
    sock.close()

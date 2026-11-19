
import json
import socket
import time

SERVER_IP = "10.0.0.1"
SERVER_PORT = 5005

CPU_LIMIT = 80
MEMORY_LIMIT = 85
AGENT_TIMEOUT_SECONDS = 6

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))
sock.settimeout(1)

last_seen = {}
stale_alerted = set()

print(f"Monitoring server listening on {SERVER_IP}:{SERVER_PORT}")

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
                f"CPU={cpu:.1f}% "
                f"MEM={memory:.1f}% "
                f"processes={report['process_count']} "
                f"TX={report['network_tx_kbps']} Kbps "
                f"RX={report['network_rx_kbps']} Kbps"
            )

            if cpu >= CPU_LIMIT:
                print(f"ALERT: high CPU on {host}: {cpu:.1f}%")

            if memory >= MEMORY_LIMIT:
                print(
                    f"ALERT: high memory on {host}: "
                    f"{memory:.1f}%"
                )

        except socket.timeout:
            pass
        except (
            ValueError,
            KeyError,
            TypeError,
            UnicodeDecodeError
        ) as exc:
            print("Invalid report:", exc)

        now = time.time()

        for host, last_time in list(last_seen.items()):
            if now - last_time > AGENT_TIMEOUT_SECONDS:
                if host not in stale_alerted:
                    print(
                        f"ALERT: {host} stopped sending reports"
                    )
                    stale_alerted.add(host)

except KeyboardInterrupt:
    print("\nMonitoring server stopped.")

finally:
    sock.close()

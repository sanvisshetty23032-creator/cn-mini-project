import socket, json, time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 5005))
s.settimeout(1)
last_seen = {}

print("Remote Health Monitoring Server Started")

try:
    while True:
        try:
            data, addr = s.recvfrom(4096)
            r = json.loads(data.decode())
            host = r["host"]
            last_seen[host] = time.time()

            print(f"{host} | CPU: {r['cpu']}% | Memory: {r['memory']}%")

            if r["cpu"] >= 80:
                print("ALERT: High CPU on", host)
            if r["memory"] >= 85:
                print("ALERT: High memory on", host)

        except socket.timeout:
            pass
        except (ValueError, KeyError, TypeError):
            print("Invalid report received")

        now = time.time()
        for host, last in list(last_seen.items()):
            if now - last > 6:
                print("ALERT: Agent stopped reporting:", host)
                del last_seen[host]

except KeyboardInterrupt:
    print("Server stopped")
finally:
    s.close()

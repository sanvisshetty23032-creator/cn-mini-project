import socket, json, random, time, sys

host = sys.argv[1] if len(sys.argv) > 1 else "agent"
target = ("10.0.0.1", 5005)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        report = {
            "host": host,
            "cpu": random.randint(10, 100),
            "memory": random.randint(20, 95)
        }
        s.sendto(json.dumps(report).encode(), target)
        print("Sent:", report)
        time.sleep(2)
except KeyboardInterrupt:
    print("Agent stopped")
finally:
    s.close()

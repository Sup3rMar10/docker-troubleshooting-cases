import signal
import sys
import time


def stop(signum, frame):
    print("got SIGTERM, shutting down cleanly", flush=True)
    sys.exit(0)


signal.signal(signal.SIGTERM, stop)
print("running", flush=True)
while True:
    time.sleep(1)

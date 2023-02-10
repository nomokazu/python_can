import subprocess
import time

while True:
    subprocess.run(["python3","virtual_simulation.py"])
    print("send")
    time.sleep(0.02)
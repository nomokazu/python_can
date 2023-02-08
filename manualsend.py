import subprocess
import time

while True:
    # STEERING
    # subprocess.run(["cansend", "slcan0", "102#01F00011110000F1"])
    # subprocess.run(["cansend", "slcan0", "102#01F0002000000000"])
    
    # BRAKE
    # subprocess.run(["cansend", "slcan0", "101#11F0002000000000"])

    #subprocess.run(["cansend", "slcan0", "105#0000000000000000"])
    subprocess.run(["cansend","slcan0","103#0001010200000000"])
    print("send")
    time.sleep(0.02)
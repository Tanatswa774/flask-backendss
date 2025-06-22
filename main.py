import time
import random
import json
import sys
import os
from adb_utils import take_screenshot, tap, swipe_map
from scanner import find_template

DEVICE = "127.0.0.1:21513"  # MEmu device port
USERNAME = sys.argv[1] if len(sys.argv) > 1 else "default"

def gather_resources():
    take_screenshot(DEVICE)

    try:
        nodes = find_template("screen.png", "templates/gem.png", threshold=0.83)

        # Save to user-specific file
        with open(f"gems_found_{USERNAME}.json", "w") as f:
            json.dump({"gems_found": len(nodes)}, f)

        if not nodes:
            print("[INFO] No gems found.")
        else:
            for (x, y) in nodes:
                print(f"[INFO] Found gem at ({x}, {y})")
                tap(DEVICE, x, y)
                time.sleep(3)
                tap(DEVICE, 800, 950)
                time.sleep(4)

    except Exception as e:
        print(f"[ERROR] {e}")
        with open(f"gems_found_{USERNAME}.json", "w") as f:
            json.dump({"gems_found": 0}, f)

def random_swipe():
    direction = random.choice(["left", "right", "up", "down"])
    print(f"[ACTION] Swiping {direction}")
    swipe_map(DEVICE, direction)
    time.sleep(2)

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)
    while True:
        gather_resources()
        random_swipe()
        time.sleep(5)

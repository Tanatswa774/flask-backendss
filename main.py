import time
import json
import sys
import os
from adb_utils import take_screenshot, tap, swipe_map, zoom_out
from scanner import find_template, is_march_active

DEVICE = "127.0.0.1:21503"
USERNAME = sys.argv[1] if len(sys.argv) > 1 else "default"
MAX_MARCHES = 2

active_marches = 0

# Grid navigation settings
grid_x, grid_y = 0, 0
grid_visited = set()
grid_max_x, grid_max_y = 10, 10  # Size of the exploration area
going_right = True

def gather_resources():
    global active_marches

    zoom_out(DEVICE)
    time.sleep(0.8)
    take_screenshot(DEVICE)

    try:
        nodes = find_template("screen.png", "templates/gem.png", threshold=0.83)
        gems_found = len(nodes)
        timestamp = int(time.time())

        with open(f"gems_found_{USERNAME}.json", "w") as f:
            json.dump({"gems_found": gems_found, "last_updated": timestamp}, f)

        if not nodes:
            print("[INFO] No gems found.")
            return False

        for (x, y) in nodes:
            if active_marches >= MAX_MARCHES:
                print("[INFO] Max marches reached.")
                break

            print(f"[INFO] Found gem at ({x}, {y})")
            tap(DEVICE, x, y)
            time.sleep(2)

            take_screenshot(DEVICE)
            if find_template("screen.png", "templates/gather_button.png", threshold=0.85):
                tap(DEVICE, 800, 950)
                active_marches += 1
                print(f"[INFO] Dispatched march #{active_marches}")
                time.sleep(3)
            else:
                print("[WARN] Gather button not detected.")
        return True

    except Exception as e:
        print(f"[ERROR] {e}")
        with open(f"gems_found_{USERNAME}.json", "w") as f:
            json.dump({"gems_found": 0, "last_updated": int(time.time())}, f)
        return False

def move_to_next_tile():
    global grid_x, grid_y, going_right, grid_visited

    current = (grid_x, grid_y)
    if current in grid_visited:
        print(f"[SKIP] Already visited tile {current}")
    else:
        print(f"[MOVE] Visiting tile {current}")
        grid_visited.add(current)

    # Swipe to simulate movement
    if going_right:
        swipe_map(DEVICE, "right")
        grid_x += 1
        if grid_x >= grid_max_x:
            going_right = False
            swipe_map(DEVICE, "down")
            grid_y += 1
    else:
        swipe_map(DEVICE, "left")
        grid_x -= 1
        if grid_x < 0:
            going_right = True
            swipe_map(DEVICE, "down")
            grid_y += 1

    time.sleep(1)

    if grid_y >= grid_max_y:
        print("[DONE] Reached edge of map grid. Resetting.")
        grid_x, grid_y = 0, 0
        grid_visited.clear()

def check_marches():
    global active_marches
    take_screenshot(DEVICE)
    if not is_march_active("screen.png"):
        if active_marches > 0:
            active_marches -= 1
            print(f"[INFO] One march has returned. Active marches: {active_marches}")

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)

    while True:
        check_marches()
        if active_marches < MAX_MARCHES:
            found = gather_resources()
            if not found:
                move_to_next_tile()
        else:
            print("[WAIT] All marches active. Waiting...")
            time.sleep(10)

import subprocess
import time

def take_screenshot(device_id):
    subprocess.run(["adb", "-s", device_id, "shell", "screencap", "-p", "/sdcard/screen.png"])
    subprocess.run(["adb", "-s", device_id, "pull", "/sdcard/screen.png", "screen.png"])

def tap(device_id, x, y):
    subprocess.run(["adb", "-s", device_id, "shell", "input", "tap", str(x), str(y)])

def swipe_map(device_id, direction):
    if direction == "left":
        subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe", "800", "500", "200", "500", "300"])
    elif direction == "right":
        subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe", "200", "500", "800", "500", "300"])
    elif direction == "up":
        subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe", "500", "800", "500", "200", "300"])
    elif direction == "down":
        subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe", "500", "200", "500", "800", "300"])

def zoom_out(device_id):
    print("[ACTION] Zooming out the map")
    for _ in range(3):
        subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe", "300", "500", "500", "500", "100"])
        subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe", "800", "500", "600", "500", "100"])
        time.sleep(0.5)

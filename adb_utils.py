import subprocess

def adb_exec(cmd, device=None):
    base = ['adb']
    if device:
        base += ['-s', device]
    full_cmd = base + cmd
    return subprocess.run(full_cmd, stdout=subprocess.PIPE).stdout.decode()

def take_screenshot(device, path="screen.png"):
    adb_exec(["shell", "screencap", "-p", "/sdcard/screen.png"], device)
    adb_exec(["pull", "/sdcard/screen.png", path], device)

def tap(device, x, y):
    adb_exec(["shell", "input", "tap", str(x), str(y)], device)

def swipe_map(device, direction="left"):
    if direction == "left":
        adb_exec(["shell", "input", "swipe", "800", "500", "200", "500", "300"], device)
    elif direction == "right":
        adb_exec(["shell", "input", "swipe", "200", "500", "800", "500", "300"], device)
    elif direction == "up":
        adb_exec(["shell", "input", "swipe", "500", "800", "500", "200", "300"], device)
    elif direction == "down":
        adb_exec(["shell", "input", "swipe", "500", "200", "500", "800", "300"], device)

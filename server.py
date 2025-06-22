from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import subprocess
import threading
import sys
import json
from typing import Optional, Dict

app = Flask(__name__)
CORS(app)

# Use a single user
USERNAME = "tanatswa"
bot_processes: Dict[str, Optional[subprocess.Popen]] = {USERNAME: None}
process_locks: Dict[str, threading.Lock] = {USERNAME: threading.Lock()}

@app.route("/start", methods=["POST"])
def start_bot():
    data = request.get_json()
    username = data.get("username")

    if username != USERNAME:
        return jsonify({"error": "Unauthorized"}), 403

    with process_locks[username]:
        if bot_processes[username] is not None and bot_processes[username].poll() is None:
            return jsonify({"status": "already running"}), 409

        try:
            bot_processes[username] = subprocess.Popen([sys.executable, "main.py", username])
            return jsonify({"status": "started"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/stop", methods=["POST"])
def stop_bot():
    data = request.get_json()
    username = data.get("username")

    if username != USERNAME:
        return jsonify({"error": "Unauthorized"}), 403

    with process_locks[username]:
        process = bot_processes.get(username)
        if process and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            bot_processes[username] = None
            return jsonify({"status": "stopped"})

        return jsonify({"status": "not running"}), 404

@app.route("/status", methods=["POST"])
def status():
    data = request.get_json()
    username = data.get("username")

    if username != USERNAME:
        return jsonify({"error": "Unauthorized"}), 403

    process = bot_processes.get(username)
    return jsonify({"running": process is not None and process.poll() is None})

@app.route("/gems", methods=["POST"])
def get_gem_count():
    data = request.get_json()
    username = data.get("username")

    if username != USERNAME:
        return jsonify({"error": "Unauthorized"}), 403

    filename = f"gems_found_{username}.json"
    try:
        with open(filename, "r") as f:
            return jsonify(json.load(f))
    except Exception:
        return jsonify({"gems_found": 0})

@app.route("/screenshot", methods=["GET"])
def screenshot():
    try:
        return send_file("screen.png", mimetype="image/png")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)

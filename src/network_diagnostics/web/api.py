#!/usr/bin/env python3

from flask import Flask, request, jsonify
import subprocess
import socket
import logging
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)

#####################
# Helper Functions  #
#####################

def do_ping(target, count=4):
    """
    Perform a ping on the target host for a specified count.
    Using Linux/WSL 'ping -c' syntax.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return {"output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr or "Ping failed."}

def do_traceroute(target):
    """
    Perform a traceroute on the target host using 'traceroute'.
    """
    try:
        result = subprocess.run(
            ["traceroute", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return {"output": result.stdout}
    except FileNotFoundError:
        return {"error": "'traceroute' command not found. Please install traceroute."}
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr or "Traceroute failed."}

def do_dns_lookup(domain):
    try:
        result = subprocess.run(
            ["nslookup", domain, "8.8.8.8"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return {"output": result.stdout}
    except FileNotFoundError:
        return {"error": "'nslookup' command not found. Please install dnsutils."}
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr or "DNS lookup failed."}


def do_port_scan(host, start_port, end_port):
    """
    Perform a simple TCP port scan on a range of ports.
    """
    open_ports = []
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Adjust timeout as needed
            result = s.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

#####################
# Flask Endpoints   #
#####################

@app.route("/ping", methods=["GET"])
def ping_endpoint():
    target = request.args.get("target")
    logging.info(f"Ping endpoint called with target={target}")
    count = request.args.get("count", 4, type=int)
    if not target:
        return jsonify({"error": "Missing 'target' parameter"}), 400

    result = do_ping(target, count)
    status_code = 200 if "output" in result else 400
    return jsonify(result), status_code

@app.route("/traceroute", methods=["GET"])
def traceroute_endpoint():
    target = request.args.get("target")
    if not target:
        return jsonify({"error": "Missing 'target' parameter"}), 400

    result = do_traceroute(target)
    status_code = 200 if "output" in result else 400
    return jsonify(result), status_code

@app.route("/dns", methods=["GET"])
def dns_endpoint():
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "Missing 'domain' parameter"}), 400

    result = do_dns_lookup(domain)
    status_code = 200 if "output" in result else 400
    return jsonify(result), status_code

@app.route("/scan", methods=["GET"])
def scan_endpoint():
    host = request.args.get("host")
    start_port = request.args.get("start", 1, type=int)
    end_port = request.args.get("end", 1024, type=int)
    if not host:
        return jsonify({"error": "Missing 'host' parameter"}), 400

    open_ports = do_port_scan(host, start_port, end_port)
    return jsonify({"open_ports": open_ports})

@app.route("/", methods=["GET"])
def index():
    return (
        "Network Diagnostics API\n"
        "Available endpoints:\n"
        " - /ping?target=<host>&count=<int>\n"
        " - /traceroute?target=<host>\n"
        " - /dns?domain=<domain>\n"
        " - /scan?host=<host>&start=<int>&end=<int>\n"
    )

if __name__ == "__main__":
    # Run on port 5001 to avoid clashing with other services
    app.run(host="0.0.0.0", port=5001)

#!/usr/bin/env python3

from flask import Flask, request, jsonify
import ipaddress
import logging
from flask_cors import CORS


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)

def calculate_subnet(ip, subnet):
    try:
        network = ipaddress.ip_network(f"{ip}/{subnet}", strict=False)
    except ValueError as e:
        return {"error": str(e)}
    
    return {
        "network": str(network),
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "number_of_hosts": network.num_addresses - 2  # Excludes network & broadcast addresses
    }

@app.route('/calculate', methods=['GET'])
def calculate():
    logging.info("Received /calculate request")
    ip = request.args.get("ip")
    subnet = request.args.get("subnet")
    
    if not ip or not subnet:
        return jsonify({"error": "Please provide 'ip' and 'subnet' parameters."}), 400
    
    try:
        subnet = int(subnet)
    except ValueError:
        return jsonify({"error": "'subnet' must be an integer."}), 400
    
    result = calculate_subnet(ip, subnet)
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

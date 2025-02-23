#!/usr/bin/env python3

import ipaddress
import argparse
import logging

logging.basicConfig(level=logging.INFO)


def calculate_subnet(ip, cidr):
    logging.info(f"Calculating subnet for IP={ip}, CIDR={cidr}")
    network = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)
    return {
        "network": str(network),
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "num_hosts": network.num_addresses - 2
    }

def main():
    parser = argparse.ArgumentParser(description="Subnetting Calculator CLI")
    parser.add_argument("ip", help="IP address, e.g., 192.168.1.0")
    parser.add_argument("subnet", help="Subnet mask in CIDR notation, e.g., 24", type=int)
    args = parser.parse_args()

    # Call the function and print the result for CLI usage
    result = calculate_subnet(args.ip, args.subnet)
    print(result)

if __name__ == "__main__":
    main()

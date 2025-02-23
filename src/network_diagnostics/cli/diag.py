#!/usr/bin/env python3

import subprocess
import argparse
import sys
import logging

def ping(target, count=4):
    logging.info(f"Ping called with target={target}, count={count}")
    """
    Perform a ping on the target host for a specified count.
    Assumes a Linux/WSL environment using 'ping -c'.
    """
    print(f"\n[PING] Pinging {target} with {count} packets:\n")
    try:
        subprocess.run(["ping", "-c", str(count), target], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ping failed: {e}")
        sys.exit(1)

def traceroute(target):
    """
    Perform a traceroute on the target host.
    Assumes a Linux environment using 'traceroute'.
    """
    print(f"\n[TRACEROUTE] Tracing route to {target}:\n")
    try:
        subprocess.run(["traceroute", target], check=True)
    except FileNotFoundError:
        print("Error: 'traceroute' command not found. Please install traceroute.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Traceroute failed: {e}")
        sys.exit(1)

def dns_lookup(domain):
    """
    Perform a DNS lookup using 'nslookup' on the given domain.
    """
    print(f"\n[DNS LOOKUP] Looking up {domain}:\n")
    try:
        subprocess.run(["nslookup", domain], check=True)
    except FileNotFoundError:
        print("Error: 'nslookup' command not found. Please install DNS utilities.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"DNS lookup failed: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Network Diagnostics CLI: ping, traceroute, and dns."
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    # Ping sub-command
    ping_parser = subparsers.add_parser("ping", help="Ping a target host")
    ping_parser.add_argument("target", help="Target hostname or IP")
    ping_parser.add_argument(
        "-c", "--count", default=4, type=int,
        help="Number of ping packets to send (default: 4)"
    )

    # Traceroute sub-command
    trace_parser = subparsers.add_parser("traceroute", help="Traceroute to a target host")
    trace_parser.add_argument("target", help="Target hostname or IP")

    # DNS sub-command
    dns_parser = subparsers.add_parser("dns", help="DNS lookup for a domain")
    dns_parser.add_argument("domain", help="Domain name to look up")

    args = parser.parse_args()

    if args.command == "ping":
        ping(args.target, args.count)
    elif args.command == "traceroute":
        traceroute(args.target)
    elif args.command == "dns":
        dns_lookup(args.domain)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

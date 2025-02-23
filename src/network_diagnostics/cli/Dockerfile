FROM python:3.10-slim

# Set a working directory inside the container
WORKDIR /app

# Copy your CLI script into the container
COPY diag.py /app/diag.py

# Make the script executable
RUN chmod +x /app/diag.py

# Install necessary networking tools
#   - iputils-ping provides the ping command
#   - traceroute for tracerouting
#   - dnsutils for nslookup
RUN apt-get update && apt-get install -y \
    iputils-ping \
    traceroute \
    dnsutils \
 && rm -rf /var/lib/apt/lists/*

# By setting the ENTRYPOINT to your script,
# you can pass subcommands/arguments directly to it.
ENTRYPOINT ["/app/diag.py"]

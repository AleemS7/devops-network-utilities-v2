FROM python:3.10-slim

WORKDIR /app

# Copy your Flask code
COPY api.py /app/api.py

# Install OS packages for ping/traceroute/dns
RUN apt-get update && apt-get install -y \
    iputils-ping \
    traceroute \
    dnsutils \
  && rm -rf /var/lib/apt/lists/*

# Now install Flask + flask-cors
RUN pip install flask flask-cors

EXPOSE 5001
ENTRYPOINT ["python", "/app/api.py"]

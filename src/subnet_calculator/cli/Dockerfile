FROM python:3.10-slim

WORKDIR /app

# Copy the subnet.py file from the new location
COPY subnet.py /app/subnet.py

RUN chmod +x /app/subnet.py

ENTRYPOINT ["/app/subnet.py"]

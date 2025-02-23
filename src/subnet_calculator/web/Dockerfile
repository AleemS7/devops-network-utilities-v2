FROM python:3.10-slim

WORKDIR /app

# Copy your Flask code
COPY web_subnet.py /app/web_subnet.py

# Install any OS packages (if needed) plus Flask + flask-cors
RUN apt-get update && apt-get install -y \
  # (add packages if you need them; if not, remove this line)
  && rm -rf /var/lib/apt/lists/*

RUN pip install flask flask-cors

EXPOSE 5000
ENTRYPOINT ["python", "/app/web_subnet.py"]


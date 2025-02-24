# DevOps Network Utilities Project

## Public Demo (Cloud Vantage)
[http://48.216.191.222/](http://48.216.191.222/)

## Introduction & Motivation
A containerized suite of network tools (subnet calculator, ping, traceroute, DNS, and port scanning) deployed on Azure Kubernetes Service (AKS). Each microservice is Docker-built—Python (Flask) for the backend services and a React frontend—and pushed to Azure Container Registry via a GitHub Actions CI pipeline. Terraform provisions the AKS cluster, and an Nginx Ingress routes traffic to the respective containerized services.

I started this project as a python execise to incorporate networking fundementals (subnetting, basic diagnostics). I then evolved it to learn DevOps concepts. I ended up learning Docker, Kubernetes, Azure, and how to orchestrate multiple microservices. The result is a cloud vantage networking toolkit that can also run locally if desired.

## Architecture & Tools

### Microservices:
- **Subnet Calculator (Python):** Calculates network/broadcast addresses and host counts.
- **Diagnostics (Python):** Runs ping, traceroute, DNS lookup, and port scans from inside the container/cluster.
- **Frontend (React):** Single-page app that calls these microservices via REST endpoints.

### Azure:
- **Azure Kubernetes Service (AKS):** Hosts the containers in separate pods.
- **Azure Container Registry (ACR):** Stores Docker images built by GitHub Actions.
- **Nginx Ingress:** Routes paths (/ping, /calculate, /dns, /scan, etc.) to the correct service.

### Infrastructure:
- **Terraform:** Provisions AKS, ACR, and resource groups in Azure.

### Pipeline:
- **GitHub Actions (CI)** builds and pushes images to ACR on each commit.  
  (Currently not fully deploying automatically, so it’s more CI than full CD.)

### Vantage:
The microservices run commands from within the cluster, so ping/traceroute/dns are from Azure’s perspective.

---

## Running Locally
You can run these tools on your local machine if you want the vantage from your own system:

### Clone this repo:
```console
git clone https://github.com/YourUser/devops-network-utilities.git
cd devops-network-utilities
```
### Docker Compose:
Check docker-compose.yml to see which ports map to your host. Then:
```console
docker-compose build
docker-compose up
```
Typically, the frontend might be at http://localhost:3000 (depending on how docker-compose.yml is set).
The subnet or diag containers might run on different local ports.

Note: If you want the CLI version, just go to src/subnet_calculator/cli/subnet.py or src/network_diagnostics/cli/diag.py and run them with Python. 
Because each environment can vary, you may need to tweak docker-compose.yml or your environment variables to match your local port mappings.

---

### Challenges & What I Learned
- **Network+ to Cloud:** Transitioning basic networking knowledge into a cloud environment taught me about vantage differences (local vs. container vs. AKS). Scanning from inside a container only checks connectivity from the cluster’s IP. This is useful for internal debugging server-side checks.
- **Docker & K8s:** Containerizing each microservice separately, then deploying them on AKS was eye-opening—especially dealing with path-based Ingress and rewriting issues.
- **CI Pipeline:** I set up GitHub Actions to build images automatically on each commit. Although it’s not a full CD pipeline yet, it showed me how to handle Docker builds, secrets for ACR, and version tagging.
- **Terraform:** Managing AKS, ACR, and resource groups with Terraform forced me to keep track of large state files and .gitignore them properly.
- **ICMP:** Some AKS setups block outbound ICMP, so I had to verify with a debug container (kubectl run debug). The ping and port scanner tool are still in progress and might have some errors.
- **Regex Path Rewrites:** I initially tried fancy regex in the new networking.k8s.io/v1 Ingress but learned it disallows them with pathType: Prefix. I simplified to direct endpoints like /ping.

---

### Next Steps
- **Terraform expansions:**
Currently provisioning AKS + ACR. Could also manage custom domains, SSL certificates, or advanced networking (like a custom VNET).
- **Security:**
Store secrets in Azure Key Vault. Add an auth layer for diagnostics if needed.
- **Automated Deployments:**
Extend GitHub Actions to do a kubectl apply or terraform apply upon each push, achieving fully automated DevOps.
- **Observability:**
Integrate Azure Monitor or a logging solution (e.g., ELK stack) to gather container logs and metrics.
- **Enhanced Tools:**
Fix ping and portscan issues. Add mtr, dig, or advanced port scanning with Nmap. Provide more robust error handling and reporting.

---

Thanks for reading - feel free to clone and adapt for your own environment. If you have any feedback or ideas on fixing ping or improving the toolset, feel free to message me!

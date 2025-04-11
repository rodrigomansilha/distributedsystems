# Minikube Tutorial: Client-Server Distributed System

This tutorial will guide you through setting up a client-server distributed system using Minikube, where:
- A group of server pods handle requests
- A group of client pods communicate with the servers
- Kubernetes manages service discovery and load balancing

## Prerequisites
- Minikube installed
- kubectl installed
- Docker installed

## Step 1: Start Minikube and Configure Docker
```bash
minikube start --driver=docker
eval $(minikube -p minikube docker-env)  # Use Minikube's Docker daemon
```

## Step 2: Create Minimal Python Docker Image

Create `Dockerfile.python-minimal`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask requests  # Install common packages

CMD ["python3"]
```

Build the image:
```bash
docker build -t python-minimal -f Dockerfile.python-minimal .
```

## Step 3: Create Application Dockerfile

Create `Dockerfile.app`:
```dockerfile
FROM python-minimal

# Clone your application code
RUN git clone https://github.com/yourusername/yourrepo.git /app
WORKDIR /app

# Example structure assumes:
# - server.py contains server code
# - client.py contains client code
#yourrepo/
#├── server.py
#├── client.py
#└── (other files)
```

Build the application:
```bash
docker build -t my-distributed-app -f Dockerfile.app .
```

## Step 4: Create Server Deployment

Create `server-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: server
spec:
  replicas: 3  # Three server instances
  selector:
    matchLabels:
      app: distributed-app
      role: server
  template:
    metadata:
      labels:
        app: distributed-app
        role: server
    spec:
      containers:
      - name: server
        image: my-distributed-app
        command: ["python3", "server.py"]
        ports:
        - containerPort: 8000

---
apiVersion: v1
kind: Service
metadata:
  name: server-service
spec:
  selector:
    app: distributed-app
    role: server
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
```

## Step 5: Create Client Deployment

Create `client-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: client
spec:
  replicas: 5  # Five client instances
  selector:
    matchLabels:
      app: distributed-app
      role: client
  template:
    metadata:
      labels:
        app: distributed-app
        role: client
    spec:
      containers:
      - name: client
        image: my-distributed-app
        command: ["python3", "client.py"]
        env:
        - name: SERVER_URL
          value: "http://server-service:8000"  # Kubernetes DNS name for servers
```

## Step 6: Deploy the System

```bash
kubectl apply -f server-deployment.yaml
kubectl apply -f client-deployment.yaml
```

## Step 7: Verify the Deployment

Check all components are running:
```bash
kubectl get pods
kubectl get services
```

View client logs (should show successful server communication):
```bash
kubectl logs -l role=client --tail=50
```

View server logs (should show incoming requests):
```bash
kubectl logs -l role=server --tail=50
```

## Step 8: Example Application Code

Create these files in your GitHub repository:

**server.py**:
```python
from flask import Flask
app = Flask(__name__)

request_count = 0

@app.route('/')
def hello():
    global request_count
    request_count += 1
    return f"Hello from server! Request count: {request_count}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**client.py**:
```python
import os
import requests
import time

SERVER_URL = os.getenv('SERVER_URL')

while True:
    try:
        response = requests.get(SERVER_URL)
        print(f"Client {os.getenv('HOSTNAME')} received: {response.text}")
    except Exception as e:
        print(f"Error contacting server: {e}")
    time.sleep(3)
```

## Step 9: Test the System

1. Watch client logs in real-time:
```bash
kubectl logs -l role=client -f
```

2. Scale the servers up or down:
```bash
kubectl scale deployment/server --replicas=5
```

3. Observe how clients automatically connect to all available servers

## Step 10: Clean Up

```bash
kubectl delete -f server-deployment.yaml
kubectl delete -f client-deployment.yaml
minikube stop
```

## Key Features of This Setup

1. **Automatic Service Discovery**: Clients find servers via `server-service` DNS name
2. **Load Balancing**: Kubernetes Service distributes traffic among server pods
3. **Scalability**: Easily adjust replicas for clients or servers
4. **Isolation**: Each component runs in its own container
5. **Centralized Logging**: View logs from all pods with label selectors

This gives you a complete, working client-server distributed system where:
- Clients automatically discover and communicate with servers
- You can scale each component independently
- Kubernetes handles all networking and service discovery

FROM python-minimal

# Clone your application code
RUN git clone git@github.com:rodrigomansilha/distributedsystems.git minikube-client-server/app
WORKDIR /app

# Example structure assumes:
# - server.py contains server code
# - client.py contains client code

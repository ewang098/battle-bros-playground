# Running the FastAPI App Locally with Minikube

Follow these steps to build, deploy, and access the FastAPI app inside your local Minikube Kubernetes cluster.

---

## Prerequisites

- Minikube installed and running
- Docker installed
- kubectl installed and configured

---

## Steps

### 1. Configure your shell to use Minikube's Docker daemon

This makes sure Docker builds the image **inside Minikube’s Docker environment**, so Kubernetes can find the image locally.

```bash
minikube start --driver=docker
eval $(minikube docker-env)
docker build -t fastapi-manage-a-bro:latest .
```

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

# Show all pods in the default namespace
kubectl get pods

# Show deployments
kubectl get deployments

# Show services
kubectl get services

# See rollout status of your deployment
kubectl rollout status deployment/fastapi-manage-a-bro-deployment

# View pod logs (replace POD_NAME with actual name)
kubectl logs POD_NAME

# Describe a pod (for detailed debugging info)
kubectl describe pod POD_NAME


```
# opens in web browser
minikube service fastapi-manage-a-bro
```

```
kubectl get pods
```

when making changes to python code, rebuild the image and then restart deployment

LOCALLY - can delete pod and it will restart with current built image

kubectl get pods -l app=postgres
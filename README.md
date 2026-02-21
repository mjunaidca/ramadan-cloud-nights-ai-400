# AI-400 Cloud Classes - Ramadan Coding Nights

## Table of Contents

- [Class 1: Kubernetes Communication Between Services](#class-1-kubernetes-communication-between-services)
  - [Project Structure](#project-structure)
  - [Running Locally](#running-locally)
  - [API Endpoints](#api-endpoints)
- [Challenge 1: Deploy Both Services in Kubernetes](#challenge-1-deploy-both-services-in-kubernetes)
  - [What You Need To Do](#what-you-need-to-do)
  - [Hints](#hints)
  - [Questions To Explore](#questions-to-explore)
  - [Bonus](#bonus)

---

## Class 1: Kubernetes Communication Between Services

In this class we built a simple **Task Manager** application with two services:

- **Backend** — FastAPI REST API that stores tasks in memory
- **Frontend** — A lightweight web UI that talks to the backend API

### Project Structure

```
live-code/
├── backend/
│   ├── main.py            # Task CRUD API
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/
│   ├── main.py            # Serves the web UI
│   ├── templates/
│   │   └── index.html     # Task manager page
│   ├── pyproject.toml
│   └── uv.lock
├── k8s.yaml
└── README.md
```

### Running Locally

```bash
# Terminal 1 - Backend
cd backend && uv run uvicorn main:app --port 8000

# Terminal 2 - Frontend
cd frontend && uv run uvicorn main:app --port 3000
```

Open `http://localhost:3000` to use the app.

### API Endpoints

| Method   | Endpoint        | Description       |
|----------|-----------------|-------------------|
| GET      | /tasks          | List all tasks    |
| GET      | /tasks/{id}     | Get a task        |
| POST     | /tasks          | Create a task     |
| PATCH    | /tasks/{id}     | Update a task     |
| DELETE   | /tasks/{id}     | Delete a task     |
| GET      | /docs           | Swagger UI        |
| GET      | /redoc          | ReDoc             |

---

## Challenge 1: Deploy Both Services in Kubernetes

Your goal is to deploy **both the frontend and backend** in Kubernetes and make them communicate with each other.

### What You Need To Do

1. **Build Docker images** for both frontend and backend
2. **Create Kubernetes manifests** (Deployment + Service) for each
3. **Make the frontend talk to the backend** inside the cluster

### Hints

- The frontend uses the `API_URL` environment variable to know where the backend is
- In Kubernetes, services can talk to each other using internal DNS
- The DNS format is: `http://<service-name>.<namespace>.svc.cluster.local:<port>`
- For services in the same namespace, just `http://<service-name>:<port>` works
- You will need a **ClusterIP** service for the backend (internal only)
- You will need a **NodePort** service for the frontend (external access)
- Pass `API_URL` to the frontend deployment using `env` in the container spec

### Questions To Explore

- What is the difference between ClusterIP, NodePort, and LoadBalancer?
- Why does the frontend need a NodePort but the backend only needs ClusterIP?
- What happens if the backend service name changes? How does the frontend know?
- How does Kubernetes DNS resolution work inside a pod?

### Bonus

- Add a `/health` endpoint to both services and configure readiness/liveness probes
- Try scaling the backend to 2 replicas — does the frontend still work? Why?
- What happens to tasks when a backend pod restarts?

Good luck and happy coding!

# 🚀 AI-Powered CI/CD Pipeline — Flask Todo App

A production-grade DevOps project showcasing a complete CI/CD pipeline with AI integration, container security scanning, Kubernetes deployment, and real-time monitoring.

---

## 📌 Project Overview

This project demonstrates an end-to-end DevOps workflow built around a simple Python Flask Todo application. The focus is entirely on the infrastructure and pipeline rather than the application itself.

---

## 🏗️ Architecture

```
Developer Push
      │
      ▼
┌─────────────────────────────────────────────┐
│              GitLab CI Pipeline             │
│                                             │
│  ┌─────────┐  ┌─────────┐  ┌───────────┐  │
│  │  Test   │─▶│  Build  │─▶│ Security  │  │
│  │ pytest  │  │ Docker  │  │  Trivy    │  │
│  │ 9 tests │  │  image  │  │  Scan     │  │
│  └─────────┘  └─────────┘  └───────────┘  │
│                                    │        │
│                             ┌──────▼──────┐ │
│                             │   Release   │ │
│                             │ AI Notes    │ │
│                             │ (Gemini)    │ │
│                             └─────────────┘ │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│           Kubernetes (Minikube)             │
│                                             │
│  ┌──────────────┐    ┌──────────────┐      │
│  │  todo-app    │    │  todo-app    │      │
│  │   Pod 1      │    │   Pod 2      │      │
│  └──────────────┘    └──────────────┘      │
│         │                                   │
│  ┌──────▼───────────────────────────┐      │
│  │         NodePort Service          │      │
│  └───────────────────────────────────┘      │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│         Monitoring Stack (Helm)             │
│                                             │
│   Prometheus ──▶ Grafana Dashboards        │
│   AlertManager                             │
│   Node Exporter                            │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Application | Python, Flask |
| Testing | pytest, pytest-cov |
| Containerization | Docker |
| CI/CD | GitLab CI |
| Security Scanning | Trivy (Aqua Security) |
| AI Integration | Google Gemini API |
| Container Orchestration | Kubernetes (Minikube) |
| Infrastructure as Code | Helm |
| Monitoring | Prometheus, Grafana, AlertManager |
| Container Registry | GitLab Container Registry |

---

## 📂 Project Structure

```
todo-app/
├── app.py                  # Flask REST API
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── release_notes.py        # AI-powered release notes generator
├── .gitlab-ci.yml          # CI/CD pipeline configuration
├── templates/
│   └── index.html          # Frontend UI
├── tests/
│   └── test_app.py         # Unit tests (9 tests)
└── k8s/
    ├── deployment.yaml     # Kubernetes Deployment
    └── service.yaml        # Kubernetes Service (NodePort)
```

---

## 🔄 CI/CD Pipeline Stages

### Stage 1 — Test
- Runs 9 unit tests using pytest
- Validates all API endpoints
- Generates coverage report

### Stage 2 — Build
- Builds Docker image
- Tags with Git commit SHA
- Pushes to GitLab Container Registry

### Stage 3 — Security
- Runs Trivy container vulnerability scan
- Checks for HIGH and CRITICAL CVEs
- Scans the freshly built image

### Stage 4 — Release (AI)
- Fetches last 10 git commits
- Sends to Google Gemini API
- Generates human-readable changelog grouped by Features, Bug Fixes, and Infrastructure changes
- Saves to `CHANGELOG.md`

---

## 🤖 AI Integration

The pipeline includes an AI-powered release notes generator (`release_notes.py`) that uses the **Google Gemini API** to automatically summarize git commits into structured, human-readable release notes on every push to main.

```
Git commits ──▶ Gemini API ──▶ Structured CHANGELOG.md
```

---

## ☸️ Kubernetes Deployment

The app is deployed on Kubernetes with:
- **2 replicas** for high availability
- **Liveness probe** on `/health` endpoint for auto-restart
- **Resource limits** (256Mi RAM, 200m CPU) per pod
- **NodePort service** for external access
- **ImagePullSecrets** for private registry authentication

---

## 📊 Monitoring

Full observability stack deployed via Helm (`kube-prometheus-stack`):
- **Prometheus** — scrapes metrics from all pods and nodes
- **Grafana** — pre-built Kubernetes dashboards for CPU, memory, and pod health
- **AlertManager** — alert routing and management
- **Node Exporter** — host-level metrics

### Access Grafana
```bash
kubectl --namespace monitoring port-forward svc/monitoring-grafana 3000:80
# Visit http://localhost:3000
# Username: admin
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.11+
- Docker
- kubectl
- Minikube
- Helm

### Run the app
```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

### Run tests
```bash
pytest tests/ -v --cov=app
```

### Run with Docker
```bash
docker build -t todo-app .
docker run -p 5000:5000 todo-app
```

### Deploy to Kubernetes
```bash
minikube start --driver=docker
kubectl apply -f k8s/
minikube service todo-app-service
```

### Deploy monitoring stack
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Web UI |
| GET | `/health` | Health check |
| GET | `/api/todos` | List all todos |
| POST | `/api/todos` | Create a todo |
| PATCH | `/api/todos/<id>` | Update a todo |
| DELETE | `/api/todos/<id>` | Delete a todo |

---

## 🎓 Author

**Jyotiraj Aditinandan Mahanta**  

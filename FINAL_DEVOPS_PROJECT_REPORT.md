# DevOps Project Report
**Course Code:** 25CIAEC59/25CYAEC59  
**Project Title:** End-to-End DevOps Pipeline: Automated CI/CD, Configuration Management, and Containerized Kubernetes Deployment with Autoscaling  
**Repository URL:** [https://github.com/spiderwen-2931/todo-api](https://github.com/spiderwen-2931/todo-api)  

---

## Executive Summary & Abstract
This project implements a complete, end-to-end continuous integration and continuous deployment (CI/CD) lifecycle for a modern cloud-native REST application. The pipeline spans two distinct but seamlessly integrated phases:
1. **Component 1 (CI/CD Pipeline):** Development of a high-performance TODO REST API in FastAPI, version control with branching workflows on Git/GitHub, automated linting and unit testing via Pytest, and continuous integration orchestration through Jenkins pipelines.
2. **Component 2 (Configuration Management & Deployment):** Infrastructure automation and configuration management using an Ansible role/playbook, container packaging with Docker, orchestrating zero-downtime deployment on Kubernetes, dynamic horizontal replica scaling, and self-healing resilience using Liveness and Readiness probes.

---

# COMPONENT 1: CI/CD Pipeline with Git & Jenkins (10 Marks)

## 1. Abstract
Component 1 establishes version control and automated validation mechanisms. Every commit pushed to the remote repository triggers a Jenkins CI pipeline that builds an isolated environment, runs code linting (PEP8), executes an automated test suite with coverage reporting, and verifies application build integrity.

## 2. Introduction
Modern DevOps practices mandate rapid feedback loops to catch regression bugs before deployment. By integrating Git branching models with Jenkins automation, team members can independently develop features and validate them before merging into production branches.

## 3. Implementation
### 3.1 Development Environment & Technologies
- **Programming Language:** Python 3.12
- **Framework:** FastAPI / Uvicorn (ASGI)
- **Data Validation:** Pydantic V2
- **Testing & Coverage:** Pytest, HTTPX (TestClient), Pytest-Cov
- **Code Quality / Linting:** Flake8
- **Version Control:** Git & GitHub
- **CI Server:** Jenkins 2.x LTS (Windows Service & Pipelines)

### 3.2 Application Architecture & Endpoints
The backend service exposes a RESTful interface with in-memory state handling:
- `GET /health` — Service health check endpoint
- `POST /todos/` — Create new task item (JSON schema validated)
- `GET /todos/` — Retrieve all active tasks
- `GET /todos/{id}` — Fetch specific task by unique identifier
- `PUT /todos/{id}` — Partial or full task update
- `DELETE /todos/{id}` — Delete task (HTTP 204 No Content)

### 3.3 CI Pipeline Workflow (`Jenkinsfile`)
The declarative Jenkins pipeline defines four automated stages:
1. **Checkout:** Automatically pulls the latest branch revision via Git SCM credentials.
2. **Environment Setup:** Creates a clean Python virtual environment (`.venv`) and installs project dependencies from `requirements.txt`.
3. **Lint:** Enforces code style with Flake8 to guarantee maintainability.
4. **Test:** Executes all 14 unit test cases with code coverage metrics using `pytest --cov=app`.
5. **Build Verification:** Executes smoke testing to confirm application module importability.

## 4. Chosen Enhancement & Rationale
- **Enhancement:** *Automated Multi-Stage Quality Gates in CI (Linting + Coverage Tests)*
- **Why Chosen:** Real-world CI pipelines do not simply package code; they act as quality gates. Incorporating linting (Flake8) prevents code decay, and running automated tests with code coverage ensures zero regressions before any artifact is approved for staging.

## 5. Results & Evidence (Screenshots to Insert)
> *[Insert your screenshots in the placeholders below]*

- **Figure 1.1:** Git branch and merge commit history (`git log --oneline --graph --all` or GitHub Network Graph showing feature branch merged into `main`).
- **Figure 1.2:** Jenkins Pipeline Stage View displaying all stages in **GREEN** (`Checkout`, `Setup Python Environment`, `Lint`, `Test`, `Build Verification`).
- **Figure 1.3:** Jenkins Build Console Output showing `14 passed` tests and `Finished: SUCCESS`.
- **Figure 1.4:** Local application testing / Swagger UI documentation at `http://localhost:8080/docs` or Postman endpoint execution.

## 6. Conclusion
Component 1 demonstrates a resilient automated testing pipeline. Code changes pushed to GitHub are automatically pulled, verified against 14 unit tests, and lint-checked without requiring manual developer intervention.

---

# COMPONENT 2: Configuration Management (Ansible) & Kubernetes Deployment (10 Marks)

## 1. Abstract
Component 2 transitions the application from continuous integration into immutable infrastructure deployment. The application host environment is configured automatically through modular Ansible playbooks, packaged into an optimized Docker container, and deployed onto a Kubernetes cluster with load balancing, horizontal pod scaling, and continuous health probes.

## 2. Introduction
Manual server administration causes configuration drift and deployment failures. Automating server configuration via Ansible provides idempotent execution, while Kubernetes provides declarative container orchestration, ensuring continuous availability, load distribution, and automated recovery.

## 3. Implementation
### 3.1 Ansible Configuration Management
An Ansible role structure (`app_setup`) was designed following industry best practices:
- **Inventory (`inventory`):** Declares local and remote target hosts.
- **Variables (`vars`):** Parameterizes settings such as application port (`app_port: 8000`) and deployment target directory (`app_dir: /opt/todo-api`).
- **Idempotent Tasks (`tasks/main.yml`):** Automatically installs runtime dependencies (`python3-pip`, `python3-venv`), creates application directories, synchronizes code assets, and sets up a dedicated virtual environment.
- **Event Handler (`handlers/main.yml`):** Restarts the uvicorn daemon only when application code changes are detected.

### 3.2 Containerization (Docker)
The `Dockerfile` employs an official `python:3.12-slim` base image to maintain a lightweight footprint:
- Dependencies are cached in intermediate layers.
- Application port 8000 is exposed.
- Uvicorn runs as the non-blocking production ASGI server.

### 3.3 Kubernetes Deployment & Service Architecture
- **Deployment Manifest (`k8s/deployment.yml`):** Manages 3 initial replicas of `todo-api:latest` with matching labels (`app: todo-api`).
- **Service Manifest (`k8s/service.yml`):** Provisions a `NodePort` service routing ingress traffic from external port 30080 to internal target port 8000 across active pods.

### 3.4 Scaling Demonstration
Dynamic horizontal scaling was executed via `kubectl scale deployment todo-api --replicas=5`. Kubernetes rapidly spun up 2 additional pods, updated endpoint slices, and distributed incoming requests across all 5 containers. Scaling back down to 2 replicas gracefully terminated redundant pods.

## 4. Chosen Enhancement & Rationale
- **Enhancement:** *Kubernetes Liveness and Readiness Probes*
- **Why Chosen:** Production containers often experience memory leaks, deadlocks, or delayed startup times. 
  - The **Readiness Probe** queries `GET /health` with a 5-second initial delay to guarantee the container does not receive traffic until the web server is fully initialized.
  - The **Liveness Probe** queries `GET /health` periodically (every 15 seconds); if the service deadlocks or fails to respond, Kubernetes automatically terminates and replaces the faulty pod, guaranteeing self-healing high availability.

## 5. Results & Evidence (Screenshots to Insert)
> *[Insert your screenshots in the placeholders below]*

- **Figure 2.1:** Ansible Playbook successful execution output (`PLAY RECAP: localhost: ok=... changed=... failed=0`).
- **Figure 2.2:** Docker container build output and local verification (`docker build` / `docker images`).
- **Figure 2.3:** Initial Kubernetes Deployment with 3 running pods (`kubectl get pods`).
- **Figure 2.4:** Kubernetes Service listing showing NodePort mapping (`kubectl get svc`).
- **Figure 2.5:** Scaling demonstration showing scale-up to 5 pods and scale-down to 2 pods (`kubectl get pods`).
- **Figure 2.6:** Evidence of Liveness and Readiness probes configured on pods (`kubectl describe pod <pod-name>`).
- **Figure 2.7:** Successful HTTP access to the live service in browser / curl showing `{"status":"ok","service":"todo-api"}`.

## 6. Conclusion
Component 2 completes the DevOps assembly line. Infrastructure is configured via codified Ansible playbooks, containerized for environmental consistency, and orchestrated on Kubernetes with automated health monitoring and dynamic elasticity.

---

## Resume Outcome Statements
- **Component 1:** *Automated CI build-and-test pipeline using Jenkins and GitHub webhooks, validating FastAPI endpoints with 14 unit tests, code coverage, and Flake8 linting on every push.*
- **Component 2:** *Configured automated server provisioning via Ansible roles and containerized deployment on Kubernetes with dynamic autoscaling (2-5 replicas) and self-healing Liveness/Readiness probes.*

---

## References
1. FastAPI Documentation: https://fastapi.tiangolo.com/
2. Jenkins Pipeline Documentation: https://www.jenkins.io/doc/book/pipeline/
3. Ansible Documentation & Galaxy: https://docs.ansible.com/
4. Kubernetes Concepts & Architecture: https://kubernetes.io/docs/concepts/
5. Docker Reference: https://docs.docker.com/

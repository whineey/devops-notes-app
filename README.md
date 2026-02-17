# DevOps Notes App

Simple full-stack notes application built with Flask and PostgreSQL,
containerized with Docker, deployed to Azure VM using Terraform,
and automated via CI/CD pipelines in GitHub Actions.

## Architecture

- Backend: Flask (Python)
- Database: PostgreSQL
- Reverse Proxy: Nginx
- Containerization: Docker & Docker Compose
- CI: GitHub Actions (build & push image to Docker Hub)
- CD: GitHub Actions (deploy over SSH to Azure VM)
- Infrastructure: Terraform (Azure VM provisioning)
- OS Provisioning: Cloud-init (Docker installation & setup)

## Features

- Add multi-line notes
- Mark notes as completed
- Delete notes
- Filter: All / Active / Completed
- Timestamp (formatted)
- Dockerized production-ready setup (Gunicorn + Nginx)

## CI Pipeline

Triggered on push to `main` branch (only changes in `/app`).

Steps:
1. Checkout code
2. Setup Docker Buildx
3. Login to Docker Hub
4. Build Docker image
5. Push image with:
   - `latest`
   - commit SHA tag

## CD Pipeline

Triggered after successful CI.

Steps:
1. SSH to Azure VM (key auth)
2. `docker compose pull`
3. `docker compose up -d`
4. Cleanup unused images

Deployment location on server:
 - /opt/notes-app

## Infrastructure

Provisioned using Terraform:

- Resource Group
- Virtual Network
- Subnet
- Network Security Group (SSH + HTTP)
- Public IP (static)
- Linux VM (Ubuntu Server)
- Cloud-init installs Docker and creates 'deploy' user with provided public SSH key

## Secrets Handling

Secrets are stored in GitHub Repository Secrets

## Production Deployment

Terraform:
 - `cd infrastructure`
 - `terraform init`
 - `terraform plan`
 - `terraform apply`

## Future Improvements

- HTTPS via Let's Encrypt
- Docker image vulnerability scanning
- Monitoring (Prometheus + Grafana)
- VM Hardening
- Move to container orchestrator (Kubernetes / Azure Container Apps)

## Purpose

This project demonstrates end-to-end DevOps workflow:

- Infrastructure as Code
- Containerization
- CI/CD automation
- Secure secret handling
- Cloud provisioning

---

Author: Adam
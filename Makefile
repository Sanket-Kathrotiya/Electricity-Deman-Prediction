# Variables
PYTHON=python
DOCKER=docker

# Default target
.PHONY: all
all: help

# Help target
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup           Install dependencies."
	@echo "  mlflow-server   Create mlflow local server "
	@echo "  prefect-login   Log in to Prefect Cloud."
	@echo "  create-pool     Create a Prefect work pool."
	@echo "  schedule        Schedule the workflow."
	@echo "  orchestrate     Run the Prefect orchestration."
	@echo "  deploy          Build and run the Docker container."
	@echo "  test            Run the test script for predictions."

# Install dependencies
.PHONY: setup
setup:
	pip install -r requirements.txt

# mlflow server
.PHONY: mlflow-server
mlflow-server:
	$(PYTHON)  -m mlflow server --backend-store-uri sqlite:///backend.db

# Prefect login
.PHONY: prefect-login
prefect-login:
	prefect cloud login

# Create Prefect work pool
.PHONY: create-pool
create-pool:
	prefect work-pool create my-managed-pool --type prefect:managed

# Schedule the workflow
.PHONY: schedule
schedule:
	$(PYTHON) 2-Orchestration/workflow_deployment.py

# Run the orchestration
.PHONY: orchestrate
orchestrate:
	$(PYTHON) 2-Orchestration/orchestrate.py

# Build and run the Docker container
.PHONY: deploy
deploy:
	cd 3_Deployment/web-service && \
	$(DOCKER) build -t nyc-electricity-demand-prediction-service:v1 . && \
	$(DOCKER) run --rm -p 9696:9696 nyc-electricity-demand-prediction-service:v1

# Run the test script
.PHONY: test
test:
	$(PYTHON) 3_Deployment/web-service/test.py

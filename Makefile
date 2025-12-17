.PHONY: all setup install test start stop clean lint lint-fix format

all: start

# Default shell
SHELL := /bin/bash

# Variables
VENV := backend/venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PID_FILE := .pids

# Setup virtual environment
setup:
	python3 -m venv $(VENV)
	@echo "Virtual environment created."

# Install all dependencies
install: setup
	$(PIP) install -r backend/requirements.txt
	cd frontend && npm install
	$(VENV)/bin/pre-commit install
	@echo "Dependencies installed."

# Run tests
test:
	cd backend && ../$(PYTHON) -m unittest discover tests
	@echo "Tests passed."

# Start services
start:
	@echo "Starting services..."
	@nohup $(VENV)/bin/uvicorn src.server:app --reload --port 8000 --app-dir backend > backend.log 2>&1 & echo $$! > $(PID_FILE).backend
	@cd frontend && nohup npm start > ../frontend.log 2>&1 & echo $$! > ../$(PID_FILE).frontend
	@echo "Backend running on http://localhost:8000 (PID: $$(cat $(PID_FILE).backend))"
	@echo "Frontend running on http://localhost:3000 (PID: $$(cat $(PID_FILE).frontend))"
	@echo "Logs: backend.log, frontend.log"

# Stop services
stop:
	@if [ -f $(PID_FILE).backend ]; then \
		kill $$(cat $(PID_FILE).backend) || true; \
		rm $(PID_FILE).backend; \
		echo "Backend stopped."; \
	else \
		echo "Backend not running."; \
	fi
	@if [ -f $(PID_FILE).frontend ]; then \
		kill $$(cat $(PID_FILE).frontend) || true; \
		rm $(PID_FILE).frontend; \
		echo "Frontend stopped."; \
	else \
		echo "Frontend not running."; \
	fi
	@pkill -f "uvicorn src.server:app" || true
	@pkill -f "react-scripts start" || true

# Clean up
clean:
	rm -rf $(VENV)
	rm -rf frontend/node_modules
	rm -rf frontend/build
	rm -f *.log
	rm -f $(PID_FILE).*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cleaned up environment."

# Lint - check code style without making changes
lint:
	@echo "Linting backend..."
	cd backend && ../$(VENV)/bin/flake8 src tests
	cd backend && ../$(VENV)/bin/mypy src --ignore-missing-imports
	cd backend && ../$(VENV)/bin/isort --check-only src tests
	cd backend && ../$(VENV)/bin/black --check src tests
	@echo "Linting frontend..."
	cd frontend && npm run lint
	cd frontend && npm run format:check
	@echo "All linting passed."

# Lint fix - automatically fix code style issues
lint-fix:
	@echo "Fixing backend code style..."
	cd backend && ../$(VENV)/bin/isort src tests
	cd backend && ../$(VENV)/bin/black src tests
	@echo "Fixing frontend code style..."
	cd frontend && npm run lint:fix
	cd frontend && npm run format
	@echo "Code style fixed."

# Format - alias for lint-fix
format: lint-fix

.PHONY: setup install test start stop clean

# Default shell
SHELL := /bin/bash

# Variables
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PID_FILE := .pids

# Setup virtual environment and install dependencies
setup:
	python3 -m venv $(VENV)
	@echo "Virtual environment created."

install: setup
	$(PIP) install -r requirements.txt
	cd ui && npm install
	@echo "Dependencies installed."

# Run tests
test:
	$(PYTHON) -m unittest discover tests
	@echo "Tests passed."

# Start services
start:
	@echo "Starting services..."
	@nohup $(VENV)/bin/uvicorn src.server:app --reload --port 8000 > backend.log 2>&1 & echo $$! > $(PID_FILE).backend
	@cd ui && nohup npm start > ../frontend.log 2>&1 & echo $$! > ../$(PID_FILE).frontend
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
	@# Also kill any lingering uvicorn or react scripts just in case
	@pkill -f "uvicorn src.server:app" || true
	@pkill -f "react-scripts start" || true

# Clean up
clean:
	rm -rf $(VENV)
	rm -rf ui/node_modules
	rm -f *.log
	rm -f $(PID_FILE).*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cleaned up environment."

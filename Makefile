# Environment name for Python virtual environment
ENV_NAME ?= venv

# Makefile targets
.PHONY: help create run clean

help:
	@echo "Makefile targets:"
	@echo "  create  - Create a Python virtual environment and install dependencies"
	@echo "  run     - Run the FastAPI application"
	@echo "  clean   - Remove the Python virtual environment"

create:
	python -m venv $(ENV_NAME)
	$(ENV_NAME)/Scripts/pip install --upgrade pip
	$(ENV_NAME)/Scripts/pip install -r requirements.txt
	@echo "Virtual environment '$(ENV_NAME)' created and dependencies installed."

run:
	$(ENV_NAME)/Scripts/uvicorn api.main:app --reload
	@echo "FastAPI application is running."

clean:
	rm -rf $(ENV_NAME)
	@echo "Virtual environment '$(ENV_NAME)' removed."
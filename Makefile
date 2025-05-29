# Mining Reliability Database
# Makefile for project automation

# Configuration
PYTHON = python3
PIP = pip3
PYTEST = pytest
BLACK = black

# Environment variables (can be overridden)
NEO4J_URI ?= bolt://localhost:7687
NEO4J_USER ?= neo4j
NEO4J_PASSWORD ?= password

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  setup      - Install dependencies"
	@echo "  schema     - Create database schema"
	@echo "  import     - Import all facility data"
	@echo "  reset      - Reset database (remove all data)"
	@echo "  clean      - Clean temporary files"
	@echo "  test       - Run tests"
	@echo "  format     - Format code with black"

.PHONY: setup
setup:
	$(PIP) install -r requirements.txt

.PHONY: dev-setup
dev-setup:
	$(PIP) install -e .

.PHONY: schema
schema:
	NEO4J_URI=$(NEO4J_URI) NEO4J_USER=$(NEO4J_USER) NEO4J_PASSWORD=$(NEO4J_PASSWORD) \
	$(PYTHON) scripts/create_schema.py

.PHONY: import
import:
	NEO4J_URI=$(NEO4J_URI) NEO4J_USER=$(NEO4J_USER) NEO4J_PASSWORD=$(NEO4J_PASSWORD) \
	$(PYTHON) scripts/import_data.py

.PHONY: import-facility
import-facility:
	@if [ -z "$(FACILITY)" ]; then \
		echo "Usage: make import-facility FACILITY=<facility_id>"; \
		exit 1; \
	fi
	NEO4J_URI=$(NEO4J_URI) NEO4J_USER=$(NEO4J_USER) NEO4J_PASSWORD=$(NEO4J_PASSWORD) \
	$(PYTHON) scripts/import_data.py --facility $(FACILITY)

.PHONY: reset
reset:
	NEO4J_URI=$(NEO4J_URI) NEO4J_USER=$(NEO4J_USER) NEO4J_PASSWORD=$(NEO4J_PASSWORD) \
	$(PYTHON) scripts/reset_db.py

.PHONY: reset-force
reset-force:
	NEO4J_URI=$(NEO4J_URI) NEO4J_USER=$(NEO4J_USER) NEO4J_PASSWORD=$(NEO4J_PASSWORD) \
	$(PYTHON) scripts/reset_db.py --force

.PHONY: clean
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} +
	find . -name "*.egg-info" -type d -exec rm -rf {} +
	find . -name "*.egg" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .eggs/

.PHONY: test
test:
	$(PYTEST) tests/

.PHONY: format
format:
	$(BLACK) mine_core/ scripts/ tests/

.PHONY: full-pipeline
full-pipeline: reset schema import test
	@echo "Full pipeline completed!"

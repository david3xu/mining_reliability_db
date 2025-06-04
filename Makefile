# Mining Reliability Database - Makefile
# Updated for unified configuration architecture

.PHONY: help setup schema import reset test clean install install-dev

help: ## Show available commands
	@echo "Mining Reliability Database Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Create environment configuration from template
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from template"; \
		echo "Edit .env with your configuration through unified environment.py gateway"; \
	else \
		echo ".env file already exists"; \
	fi

schema: ## Create database schema using unified configuration
	python scripts/setup/create_schema.py

import: ## Import all facility data using standardized patterns
	python scripts/setup/import_data.py

import-sample: ## Import sample facility data for testing
	python scripts/setup/import_data.py --facility sample

reset: ## Reset database data only (preserve schema)
	python scripts/setup/reset_db.py --force

reset-all: ## Reset database including schema constraints
	python scripts/setup/reset_db.py --drop-schema --force

test: ## Run complete test suite
	python -m pytest tests/ -v

test-coverage: ## Run tests with coverage report
	python -m pytest tests/ -v --cov=mine_core --cov-report=html

clean: ## Clean Python cache and build artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -f config_consistency_report.txt interface_compliance_report.txt interface_compliance_fixes.txt

install: ## Install core dependencies only
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev]"

install-full: ## Install all development and analysis dependencies
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

# Docker Neo4j Management - Updated patterns
docker-neo4j: ## Start Neo4j container with standard configuration
	docker run -d --name neo4j \
		-p 7474:7474 -p 7687:7687 \
		-e NEO4J_AUTH=neo4j/password \
		neo4j:latest
	@echo "Neo4j started. Browser: http://localhost:7474"
	@echo "Configure connection in .env file"

docker-start: ## Start existing Neo4j container
	docker start neo4j

docker-stop: ## Stop Neo4j container
	docker stop neo4j

docker-clean: ## Remove Neo4j container (deletes data)
	docker stop neo4j || true
	docker rm neo4j || true

docker-logs: ## View Neo4j container logs
	docker logs neo4j

# Development workflow shortcuts - Updated for unified architecture
dev-setup: setup install-dev docker-neo4j ## Complete development environment setup
	@echo "Development environment ready!"
	@echo "1. Edit .env file through unified configuration gateway"
	@echo "2. Run 'make schema' to create database schema"
	@echo "3. Run 'make import-sample' to load sample data"
	@echo "4. Access Neo4j browser: http://localhost:7474"

quick-start: setup schema import-sample ## Quick start with sample data
	@echo "Quick start complete!"
	@echo "Neo4j browser: http://localhost:7474"
	@echo "All configuration managed through environment.py gateway"

# Configuration validation
validate-config: ## Validate configuration setup
	@echo "Validating unified configuration..."
	python -c "from configs.environment import get_all_config; import json; print(json.dumps(get_all_config(), indent=2))"

validate-db: ## Test database connection
	@echo "Testing database connection..."
	python -c "from mine_core.database.db import get_database; db = get_database(); print('Database connection successful')"

# Data processing with environment overrides
import-large: ## Import data with optimized settings for large datasets
	BATCH_SIZE=10000 CONNECTION_TIMEOUT=60 python scripts/import_data.py

import-debug: ## Import data with debug logging
	LOG_LEVEL=DEBUG python scripts/import_data.py

# Schema management
schema-reset: reset-all schema ## Complete schema reset and recreation
	@echo "Schema completely reset and recreated"

# Performance operations
optimize-db: ## Create performance indexes
	python -c "from mine_core.database.db import get_database; get_database().optimize_performance()"

# Validation and integrity checks
validate-data: ## Run data integrity validation
	python -c "from mine_core.database.db import get_database; import json; print(json.dumps(get_database().validate_data_integrity(), indent=2))"

# Causal intelligence operations
analyze-causes: ## Generate causal intelligence summary
	python -c "from mine_core.database.db import get_database; import json; print(json.dumps(get_database().get_causal_intelligence_summary(), indent=2))"

# Code quality checks
lint: ## Run code quality checks
	black --check mine_core/ scripts/
	isort --check-only mine_core/ scripts/
	flake8 mine_core/ scripts/

format: ## Format code using black and isort
	black mine_core/ scripts/
	isort mine_core/ scripts/

type-check: ## Run type checking
	mypy mine_core/

# Documentation
docs: ## Generate documentation
	@echo "Documentation available in README.md"
	@echo "Architecture details in project_structure.md"

# Environment information
info: ## Show system information
	@echo "Python version: $(shell python --version)"
	@echo "Virtual environment: $(VIRTUAL_ENV)"
	@echo "Project directory: $(PWD)"
	@echo "Configuration status:"
	@make validate-config

# Security and cleanup
secure-clean: clean ## Secure cleanup including sensitive data
	find . -name "*.log" -delete
	find . -name ".env.*" -not -name ".env.example" -delete
	@echo "Secure cleanup completed"

# Consistency and Quality Assurance
validate-consistency: ## Run automated consistency validation
	python scripts/validate_consistency.py

check-interfaces: ## Check adapter interface compliance
	python scripts/check_interface_compliance.py

check-config-naming: ## Check configuration naming consistency
	python scripts/enforce_config_consistency.py

analyze-unused-functions: ## Analyze potentially unused functions
	python scripts/analyze_unused_functions.py

validate-architecture: ## Validate architecture compliance
	python dashboard/validation/architecture_validator.py

quality-check: validate-consistency check-interfaces check-config-naming analyze-unused-functions validate-architecture ## Run all quality checks

# Pre-commit setup
setup-pre-commit: ## Install and setup pre-commit hooks
	pip install pre-commit
	pre-commit install
	@echo "Pre-commit hooks installed successfully"

run-pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

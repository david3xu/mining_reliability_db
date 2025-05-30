# Mining Reliability Database - Makefile

.PHONY: help setup schema import reset test clean install install-dev install-full

help: ## Show available commands
	@echo "Mining Reliability Database Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Initial setup - copy environment template
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from template"; \
		echo "Edit .env with your configuration"; \
	else \
		echo ".env file already exists"; \
	fi

schema: ## Create database schema
	python scripts/create_schema.py

import: ## Import all facility data
	python scripts/import_data.py

reset: ## Reset database (data only)
	python scripts/reset_db.py --force

reset-all: ## Reset database including schema
	python scripts/reset_db.py --drop-schema --force

test: ## Run test suite
	python -m pytest tests/ -v

test-db: ## Run database tests only
	python -m pytest tests/test_database.py -v

test-pipelines: ## Run pipeline tests only
	python -m pytest tests/test_pipelines.py -v

clean: ## Clean Python cache files and test artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

install: ## Install core dependencies
	pip install -e .

install-dev: ## Install development tools (pytest, black, etc.)
	pip install -e ".[dev]"

install-full: ## Install all development dependencies (including ML, Azure, etc.)
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

docker-neo4j: ## Start Neo4j in Docker
	docker run -d --name neo4j \
		-p 7474:7474 -p 7687:7687 \
		-e NEO4J_AUTH=neo4j/password \
		neo4j:latest

docker-stop: ## Stop Neo4j Docker container
	docker stop neo4j

docker-start: ## Start existing Neo4j Docker container
	docker start neo4j

docker-clean: ## Remove Neo4j Docker container
	docker stop neo4j || true
	docker rm neo4j || true

# Development workflow shortcuts
dev-setup: setup install-dev docker-neo4j ## Complete development setup
	@echo "Development environment ready!"
	@echo "1. Edit .env file with your settings"
	@echo "2. Run 'make schema' to create database schema"
	@echo "3. Run 'make import' to load data"

quick-start: setup schema import-sample ## Quick start with sample data
	@echo "Quick start complete!"
	@echo "Neo4j browser: http://localhost:7474"

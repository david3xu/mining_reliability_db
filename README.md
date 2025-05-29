# Mining Reliability DB

A graph-based database system for tracking and analyzing mining operation incidents, root causes, and corrective actions.

## Overview

This project implements a Neo4j graph database to model complex relationships in mining incident data. It transforms raw reliability records into a structured data model following natural workflow progression:

```
Facility → ActionRequest → Problem → RootCause → ActionPlan → Verification
```

## Features

- Converts 41-field raw data into structured 12-entity model
- Tracks complete incident lifecycle from reporting to verification
- Captures relationships between incidents, causes, and resolutions
- Environment-driven configuration

## Quick Start

### 1. Prerequisites

- Python 3.10+
- Neo4j 4.4+
- Git

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd mining_reliability_db

# Create and activate virtual environment
python3.10 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (choose one):
make install        # Core dependencies only
make install-dev    # Core + development tools
make install-full   # All dependencies including ML/Azure tools
```

### 3. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your_password
```

### 4. Database Setup

```bash
# Start Neo4j (see Docker section below)
make schema
# or: python scripts/create_schema.py
```

### 5. Import Data

```bash
make import
# or: python scripts/import_data.py
```

## Docker Setup

### Start Neo4j

```bash
# Start Neo4j container
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest

# Check status
docker ps | grep neo4j

# View logs
docker logs neo4j
```

### Manage Neo4j Container

```bash
# Stop/Start
docker stop neo4j
docker start neo4j

# Remove (deletes data)
docker stop neo4j && docker rm neo4j
```

## Configuration

All configuration through environment variables:

| Variable       | Default               | Description          |
| -------------- | --------------------- | -------------------- |
| NEO4J_URI      | bolt://localhost:7687 | Neo4j connection URI |
| NEO4J_USER     | neo4j                 | Neo4j username       |
| NEO4J_PASSWORD | password              | Neo4j password       |
| DATA_DIR       | ./data/facility_data  | Raw data directory   |
| LOG_LEVEL      | INFO                  | Logging level        |

## Usage

### Create Database Schema

```bash
make schema
# or: python scripts/create_schema.py
```

### Import Facility Data

```bash
# Import all facilities
make import
# or: python scripts/import_data.py

# Import specific facility
make import-sample
# or: python scripts/import_data.py --facility sample
```

### Reset Database

```bash
# Reset data only
make reset
# or: python scripts/reset_db.py --force

# Reset data and schema
make reset-all
# or: python scripts/reset_db.py --drop-schema --force
```

### View All Commands

```bash
make help
```

### Custom Configuration

```bash
# Use custom Neo4j instance
python scripts/import_data.py \
  --uri bolt://custom:7687 \
  --user custom_user \
  --password custom_pass
```

## Development

### Installation Options

The project provides three installation options:

1. **Core Installation** (`make install`)

   - Installs only the essential dependencies
   - Suitable for basic usage

2. **Development Tools** (`make install-dev`)

   - Installs core dependencies + development tools
   - Includes pytest, black, flake8, mypy
   - Recommended for most developers

3. **Full Development** (`make install-full`)
   - Installs all possible dependencies
   - Includes ML, Azure, and other tools
   - Use only if you need specific tools

### Testing

Run the test suite:

```bash
# Run all tests
make test

# Run specific test files
make test-db
make test-pipelines
```

## Project Structure

```
mining_reliability_db/
├── configs/                # Configuration
│   ├── environment.py      # Environment loader
│   ├── model_schema.json   # Entity definitions
│   └── field_mappings.json # Field transformations
├── mine_core/              # Core business logic
│   ├── database/           # Database operations
│   ├── pipelines/          # ETL processes
│   └── entities/           # Data models
├── scripts/                # CLI tools
├── data/                   # Raw data files
└── tests/                  # Test suite
```

## Data Model

The system transforms raw incident records through a 12-entity model:

**Core Workflow**:

- **Facility**: Site locations
- **ActionRequest**: Incident reports
- **Problem**: Issue descriptions
- **RootCause**: Analysis results
- **ActionPlan**: Resolution steps
- **Verification**: Effectiveness validation

**Supporting Entities**:

- Department, Asset, Review, EquipmentStrategy, etc.

## Technologies

- **Neo4j**: Graph database (4.4+)
- **Python**: Core application (3.8+)
- **Pandas**: Data processing
- **JSON**: Configuration-driven transformations

## Development

### Adding New Data Sources

1. Create extractor in `mine_core/pipelines/`
2. Update field mappings in `configs/field_mappings.json`
3. Add entity definitions to `configs/model_schema.json`

### Environment Variables

All configuration through environment variables - no hardcoded values in source code.

## License

MIT License

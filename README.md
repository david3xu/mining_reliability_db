# Mining Reliability DB

A graph-based database system for tracking and analyzing mining operation incidents, root causes, and corrective actions with advanced causal intelligence capabilities.

## Overview

This system implements a Neo4j graph database to model complex relationships in mining incident data. It transforms raw reliability records into a structured 12-entity model following natural workflow progression:

```
Facility → ActionRequest → Problem → RootCause → ActionPlan → Verification
```

**Key Innovation**: Automated causal intelligence extraction that identifies primary and secondary root causes, enabling predictive maintenance and operational optimization.

## Features

- **Schema-Driven Architecture**: JSON configuration files define all data transformations
- **Causal Intelligence**: Automated extraction of root cause patterns for predictive insights
- **Dynamic Entity Labeling**: Self-organizing data structures based on operational characteristics
- **Unified Configuration Management**: Thread-safe, centralized configuration authority
- **Production-Ready**: Thread-safe operations with comprehensive error handling

## Quick Start

### Prerequisites

- Python 3.10+
- Neo4j 4.4+
- Git

### Installation

```bash
# Clone repository
git clone <repository-url>
cd mining_reliability_db

# Create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
make install-dev          # Development tools included
# or: pip install -e ".[dev]"
```

### Environment Configuration

```bash
# Create environment file
make setup
# or: cp .env.example .env

# Edit .env with your configuration
# All settings now managed through single configuration gateway
```

### Database Setup

```bash
# Start Neo4j (Docker method)
make docker-neo4j

# Create database schema
make schema
# or: python scripts/create_schema.py

# Import facility data
make import
# or: python scripts/import_data.py
```

## Architecture

### Configuration Authority

All system configuration flows through the unified `configs/environment.py` gateway:

```python
from configs.environment import get_db_config, get_batch_size, get_log_level
```

**No direct environment access** - all configuration through centralized authority.

### Validation Authority

All field validation handled by centralized `mine_core/shared/field_utils.py`:

```python
from mine_core.shared.field_utils import has_real_value, clean_label
```

**No local validation functions** - import from central authority only.

### Database Authority

Unified database interface through `mine_core/database/db.py`:

```python
from mine_core.database.db import get_database
```

**Single database interface** - no fragmented connection patterns.

## Environment Variables

### Database Configuration

```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

### Processing Parameters

```bash
BATCH_SIZE=5000
CONNECTION_TIMEOUT=30
MAX_RETRIES=3
```

### System Configuration

```bash
LOG_LEVEL=INFO
LOG_FILE=/path/to/logfile                    # Optional
DATA_DIR=./data/facility_data
ROOT_CAUSE_DELIMITERS=";,|,\n, - , / , and , & "
```

## Usage

### Schema Management

```bash
# Create schema
python scripts/create_schema.py

# Reset database (data only)
python scripts/reset_db.py --force

# Reset including schema
python scripts/reset_db.py --drop-schema --force
```

### Data Import

```bash
# Import all facilities
python scripts/import_data.py

# Import specific facility
python scripts/import_data.py --facility sample

# Custom configuration
python scripts/import_data.py \
  --uri bolt://custom:7687 \
  --user custom_user \
  --batch-size 1000
```

### Neo4j Browser Access

1. **Local Access**: http://localhost:7474
2. **Username**: neo4j
3. **Password**: password (or your configured password)

## Data Model

### Core Workflow Entities

- **Facility**: Mining operation sites
- **ActionRequest**: Incident reports with operational context
- **Problem**: Issue descriptions and requirements
- **RootCause**: Primary and secondary cause analysis
- **ActionPlan**: Resolution strategies and timelines
- **Verification**: Effectiveness validation and feedback

### Supporting Entities

- **Department**: Organizational responsibility tracking
- **Asset**: Equipment and resource involvement
- **Review**: Management oversight and approval
- **EquipmentStrategy**: Strategic maintenance implications

### Causal Intelligence Features

- **Primary Cause**: Direct root cause identification
- **Secondary Cause**: Systemic underlying factors
- **Evidence Correlation**: Supporting data relationships
- **Pattern Recognition**: Recurring issue identification

## Development

### Make Commands

```bash
make help              # Show all available commands
make install           # Core dependencies only
make install-dev       # Development tools included
make schema            # Create database schema
make import            # Import all facility data
make reset             # Reset database data
make reset-all         # Reset data and schema
make test              # Run test suite
make clean             # Remove cache files
```

### Docker Operations

```bash
make docker-neo4j      # Start Neo4j container
make docker-start      # Start existing container
make docker-stop       # Stop container
make docker-clean      # Remove container
```

### Custom Configuration

All configuration through environment variables - no hardcoded values:

```bash
# Override any parameter
BATCH_SIZE=10000 python scripts/import_data.py
LOG_LEVEL=DEBUG python scripts/create_schema.py
```

## Operational Intelligence

### Causal Analysis Queries

```cypher
// Find most frequent root causes
MATCH (rc:RootCause)
WHERE rc.root_cause IS NOT NULL
RETURN rc.root_cause, count(*) as frequency
ORDER BY frequency DESC
LIMIT 10

// Analyze causal patterns by facility
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)
RETURN f.facility_id, rc.root_cause, count(*) as incidents
ORDER BY incidents DESC
```

### Performance Analytics

```cypher
// Action plan effectiveness by category
MATCH (ar:ActionRequest)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
WHERE ar.categories IS NOT NULL AND v.is_action_plan_effective IS NOT NULL
RETURN ar.categories,
       count(*) as total_plans,
       count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) as effective_plans,
       toFloat(count(CASE WHEN v.is_action_plan_effective = true THEN 1 END)) / count(*) * 100 as effectiveness_rate
ORDER BY effectiveness_rate DESC
```

## Project Structure

```
mining_reliability_db/
├── configs/                   # Configuration authority
│   ├── environment.py         # Exclusive configuration gateway
│   ├── model_schema.json      # Entity definitions
│   └── field_mappings.json    # Field transformations
├── mine_core/                 # Business logic core
│   ├── shared/                # Centralized utilities
│   ├── database/              # Unified database interface
│   ├── pipelines/             # ETL processes
│   └── entities/              # Data models
├── scripts/                   # Standardized entry points
└── data/                      # Raw data storage
```

## Contributing

### Development Setup

```bash
# Complete development environment
make dev-setup

# Run tests
make test

# Code formatting
black mine_core/ scripts/
isort mine_core/ scripts/
```

### Architecture Principles

1. **Single Source of Truth**: All configuration through `environment.py`
2. **Centralized Validation**: All field validation through `field_utils.py`
3. **Unified Database Access**: All operations through `db.py`
4. **Schema-Driven Design**: Business logic externalized to JSON configuration

### Adding New Features

1. **Configuration**: Add to `environment.py` with environment variable support
2. **Validation**: Use existing `field_utils.py` functions or extend centrally
3. **Data Processing**: Follow ETL patterns in `pipelines/` directory
4. **Database Operations**: Extend unified `db.py` interface

## Troubleshooting

### Common Issues

**Import Errors**: Ensure virtual environment activated and dependencies installed

```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

**Database Connection**: Verify Neo4j running and environment variables set

```bash
# Check Neo4j status
docker ps | grep neo4j

# Test connection
python -c "from configs.environment import get_db_config; print(get_db_config())"
```

**Schema Errors**: Reset and recreate schema

```bash
python scripts/reset_db.py --drop-schema --force
python scripts/create_schema.py
```

### Performance Optimization

```bash
# Larger batch sizes for better performance
BATCH_SIZE=10000 python scripts/import_data.py

# Increase connection timeout for large datasets
CONNECTION_TIMEOUT=60 python scripts/import_data.py
```

## License

MIT License

## Support

For configuration issues, verify environment variables are properly set.
For data import problems, check log output with `LOG_LEVEL=DEBUG`.
For database connectivity, ensure Neo4j is running and accessible.

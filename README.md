# Mining Reliability Dashboard

Professional analytics platform for operational intelligence with clean Core → Adapter → Component architecture.

## Architecture

**Core Layer:** Business intelligence and data processing
**Adapter Layer:** Pure data access without business logic
**Component Layer:** UI rendering with single responsibilities

## Quick Start

**Requirements:** Python 3.9+, Neo4j 5.0+

```bash
# Clone and setup
git clone <repository>
cd mining-reliability-dashboard
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Start Neo4j database (choose one option)
docker-compose up -d neo4j    # Option 1: Docker Compose
# OR
make docker-neo4j             # Option 2: Direct Docker

# Setup database schema
make schema

# Import sample data (optional)
make import-sample

# Run dashboard
python dashboard/app.py
```

**Access:** http://localhost:8050

## Development Setup

**Complete development setup:**

```bash
make dev-setup    # Complete environment setup
make quick-start  # Quick start with sample data
```

**Available commands:**

```bash
make help  # Show all available commands
```

**Architecture Validation:**

```bash
make validate-architecture  # Validate architecture compliance
make validate-config       # Validate configuration setup
make validate-data         # Run data integrity validation
```

**Performance Analysis:**

```bash
python dashboard/validation/performance_profiler.py --report
```

**Integration Testing:**

```bash
python dashboard/validation/integration_tester.py --report
```

## Database Management

**Docker Setup Options:**

**Option 1: Docker Compose (Recommended):**
```bash
docker ps
docker-compose up -d neo4j     # Start Neo4j service
docker-compose down            # Stop all services
docker-compose logs neo4j      # View Neo4j logs
docker-compose stop neo4j      # Stop Neo4j only
```

**Option 2: Direct Docker Commands:**
```bash
make docker-neo4j   # Start new Neo4j container
make docker-start   # Start existing container
make docker-stop    # Stop container
make docker-logs    # View logs
make docker-clean   # Remove container (deletes data)
```

**Current Status Check:**
```bash
docker ps           # Check running containers
make validate-db    # Test database connection
```

**Schema Management:**

```bash
make schema         # Create database schema
make schema-reset   # Complete schema reset
make reset          # Reset data only
make reset-all      # Reset everything
```

**Data Import:**

```bash
make import         # Import all facility data
make import-sample  # Import sample data for testing
make import-large   # Optimized for large datasets
make import-debug   # Import with debug logging
```

## Structure

```
mine_core/          # Core business logic
dashboard/adapters/ # Pure data access layer
dashboard/components/ # UI rendering layer
configs/           # Configuration files
scripts/           # Database and utility scripts
```

## Compliance

- **MDC Architecture:** 100% compliant
- **Function Size:** Core ≤50, Adapter ≤20, Component ≤30 lines
- **Dependencies:** Core → Adapter → Component flow enforced
- **Configuration:** Schema-driven, zero hardcoding

## Performance

- **Response Time:** Sub-second for all operations
- **Architecture:** Clean separation eliminates redundancy
- **Monitoring:** Built-in performance profiling

## Features

- Portfolio analytics across operational facilities
- Workflow intelligence with stage analysis
- Data quality assessment and gap identification
- Facility-specific performance analysis
- Interactive navigation with real-time validation

## Configuration

All system behavior controlled through JSON configuration files in `configs/` directory. No hardcoded values in operational code.

**Key configuration files:**
- `model_schema.json` - Entity relationships and UI generation
- `field_mappings.json` - Data processing logic
- `dashboard_config.json` - UI settings and styling

## Testing

```bash
make test           # Run complete test suite
make test-coverage  # Run tests with coverage report
make lint           # Run code quality checks
make type-check     # Run type checking
```

## Production

**Docker deployment:**

```bash
docker-compose up -d
```

**Manual deployment:**

```bash
gunicorn dashboard.app:server --bind 0.0.0.0:8050
```

**Monitoring:** Performance and compliance validation tools included for production monitoring.

## Troubleshooting

**Common issues:**

- **Port conflicts:** Use `docker ps` to check existing containers
- **Database connection:** Run `make validate-db` to test connection
- **Performance issues:** Run `make validate-architecture --report`

**Getting help:**

```bash
make info           # Show system information
make help          # Show all available commands
```

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

# Run dashboard
python dashboard/app.py
```

**Access:** http://localhost:8050

## Development

**Architecture Validation:**

```bash
python dashboard/validation/architecture_validator.py --report
```

**Performance Analysis:**

```bash
python dashboard/validation/performance_profiler.py --report
```

**Integration Testing:**

```bash
python dashboard/validation/integration_tester.py --report
```

## Structure

```
mine_core/          # Core business logic
dashboard/adapters/ # Pure data access layer
dashboard/components/ # UI rendering layer
configs/           # Configuration files
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

## Production

```bash
# Docker deployment
docker-compose up -d

# Manual deployment
gunicorn dashboard.app:server --bind 0.0.0.0:8050
```

**Monitoring:** Performance and compliance validation tools included for production monitoring.

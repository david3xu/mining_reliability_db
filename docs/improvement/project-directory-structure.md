# Mining Reliability Database - Complete Directory Structure

```
mining_reliability_db/
├── .env.example                    # Environment configuration template
├── .gitignore                      # Git exclusion patterns
├── pyproject.toml                  # Project metadata and dependencies
├── requirements-dev.txt            # Additional development dependencies
├── LICENSE                         # MIT License
├── README.md                       # Project overview and setup
├── CHANGELOG.md                    # Version history and changes
├── Makefile                        # Build and management commands
│
├── configs/                        # Configuration layer
│   ├── __init__.py                 # Config package init
│   ├── environment.py              # [UPDATED] Consolidated config loader
│   ├── model_schema.json           # Entity definitions & relationships
│   └── field_mappings.json         # Field transformation mappings
│
├── mine_core/                      # Core business logic
│   ├── __init__.py                 # Core package init
│   │
│   ├── shared/                     # [NEW] Shared utilities
│   │   ├── __init__.py
│   │   ├── common.py               # [NEW] Common functions (path, logging, error handling)
│   │   └── constants.py            # [NEW] Centralized constants
│   │
│   ├── database/                   # Database operations
│   │   ├── __init__.py             # Database package exports
│   │   ├── db.py                   # [UPDATED] Unified database interface
│   │   └── queries.py              # Database query operations
│   │
│   ├── entities/                   # Data entities
│   │   ├── __init__.py             # Entity package exports
│   │   └── definitions.py          # Schema-driven entity definitions
│   │
│   ├── pipelines/                  # ETL processes
│   │   ├── __init__.py             # Pipeline package exports
│   │   ├── extractor.py            # Data extraction from JSON files
│   │   ├── transformer.py          # [UPDATED] Schema-driven data transformation
│   │   └── loader.py               # [UPDATED] Schema-driven database loading
│   │
│   └── helpers/                    # Helper utilities
│       ├── __init__.py             # Helper package exports
│       └── log_manager.py          # Logging utilities
│
├── scripts/                        # Command-line tools
│   ├── create_schema.py            # [UPDATED] Schema creation script
│   ├── import_data.py              # [UPDATED] Data import script
│   └── reset_db.py                 # [UPDATED] Database reset script
│
├── data/                           # Data storage
│   └── facility_data/              # Raw facility data files
│       ├── sample.json             # Sample data file
│       └── *.json                  # Additional facility data files
│
├── tests/                          # Test suite
│   ├── __init__.py                 # Test package init
│   ├── test_database.py            # Database operation tests
│   └── test_pipelines.py           # ETL pipeline tests
│
├── docs/                           # Documentation
│   ├── project_structure.md        # Project structure overview
│   ├── data-exploration-journey.md # Data analysis journey
│   ├── field-mapping-final.md      # Field mapping documentation
│   └── conceptual-erd-final.md     # Entity relationship documentation
│
└── .venv/                          # Virtual environment (git-ignored)
```

## Key Changes from Original Structure

### **Files Added**
- `mine_core/shared/common.py` - Shared utilities for path setup, logging, error handling
- `mine_core/shared/constants.py` - Centralized constants (batch sizes, entity order, etc.)

### **Files Updated**
- `configs/environment.py` - Consolidated configuration access with caching
- `mine_core/database/db.py` - Unified database interface with schema integration
- `mine_core/pipelines/loader.py` - Schema-driven loading with no hardcoded values
- `mine_core/pipelines/transformer.py` - Schema-driven transformation logic
- `scripts/create_schema.py` - Standardized setup and error handling
- `scripts/import_data.py` - Standardized setup and logging
- `scripts/reset_db.py` - Standardized setup with improved batch operations

### **Files Removed**
- `mine_core/database/connection.py` - Redundant database wrapper
- `mine_core/helpers/schema_validator.py` - Functionality merged into database module

## Directory Purpose Summary

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `configs/` | Configuration management | Schema, mappings, environment settings |
| `mine_core/shared/` | Common utilities | Constants, shared functions |
| `mine_core/database/` | Neo4j operations | Database interface, queries |
| `mine_core/pipelines/` | ETL processes | Extract, transform, load operations |
| `scripts/` | CLI tools | Database management commands |
| `data/` | Raw data storage | JSON facility data files |
| `tests/` | Test suite | Unit and integration tests |
| `docs/` | Documentation | Design docs, field mappings |

## Extension Points

**New Data Sources**: Add extractors to `mine_core/pipelines/`
**Custom Analytics**: Extend `mine_core/database/queries.py`
**Dashboard Integration**: Build on existing query interface
**Configuration Changes**: Modify JSON files in `configs/`
**Additional Utilities**: Extend `mine_core/shared/`

This structure provides clear separation of concerns with standardized patterns for extension and maintenance.
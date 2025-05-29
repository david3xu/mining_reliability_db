# Mining Reliability DB: Project Structure

## Directory Organization

```
mining_reliability_db/
├── .env.example                # Environment configuration template
├── .gitignore                  # Git exclusion patterns
├── pyproject.toml              # Project metadata and dependencies
├── requirements-dev.txt        # Additional development dependencies
├── LICENSE                     # MIT License text
├── CHANGELOG.md                # Version history and changes
├── configs/                    # Configuration files
│   ├── environment.py          # Simple environment variable loader
│   ├── model_schema.json       # Neo4j schema definition
│   └── field_mappings.json     # Field transformation mappings
├── data/                       # Data storage
│   └── facility_data/          # Raw facility data files
├── docs/                       # Documentation
├── mine_core/                  # Core package
│   ├── __init__.py
│   ├── database/               # Database operations
│   │   ├── __init__.py
│   │   ├── connection.py       # Compatibility wrapper
│   │   ├── db.py               # Unified database interface
│   │   └── queries.py          # Database query operations
│   ├── entities/               # Data entities
│   │   ├── __init__.py
│   │   └── definitions.py      # Entity structure definitions
│   ├── pipelines/              # Data processing
│   │   ├── __init__.py
│   │   ├── extractor.py        # Data extraction
│   │   ├── transformer.py      # Data transformation
│   │   └── loader.py           # Database loading
│   └── helpers/                # Helper functions
│       ├── __init__.py
│       └── log_manager.py      # Logging utilities
├── scripts/                    # Command-line scripts
│   ├── create_schema.py        # Schema creation
│   ├── import_data.py          # Data import
│   └── reset_db.py            # Database reset
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_database.py       # Database tests
│   └── test_pipelines.py      # Pipeline tests
└── .venv/                      # Virtual environment (git-ignored)
```

## Key Files

### Configuration

- `pyproject.toml`: Project metadata, dependencies, and build configuration
- `requirements-dev.txt`: Additional development dependencies
- `.env.example`: Template for environment variables
- `configs/`: Configuration files for database schema and field mappings

### Core Package

- `mine_core/`: Main package containing all business logic
  - `database/`: Neo4j database operations
  - `entities/`: Data model definitions
  - `pipelines/`: ETL process implementation
  - `helpers/`: Utility functions

### Scripts

- `scripts/`: Command-line tools for database management
  - `create_schema.py`: Creates Neo4j schema
  - `import_data.py`: Imports facility data
  - `reset_db.py`: Resets database state

### Tests

- `tests/`: Test suite
  - `test_database.py`: Database operation tests
  - `test_pipelines.py`: ETL pipeline tests

### Documentation

- `docs/`: Project documentation
- `README.md`: Project overview and setup instructions
- `CHANGELOG.md`: Version history and changes

## Development Setup

1. Create virtual environment:

   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   # Core dependencies
   pip install -e .

   # Development tools
   pip install -e ".[dev]"

   # Additional development dependencies
   pip install -r requirements-dev.txt
   ```

3. Configure environment:

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Initialize database:
   ```bash
   make schema
   ```

## Build and Test

- Run tests: `make test`
- Clean build artifacts: `make clean`
- Install package: `pip install -e .`

## Component Relationships

### Data Flow

1. **Raw Data** → Raw facility data files in JSON format
2. **Extraction** → `extractor.py` reads raw data files
3. **Transformation** → `transformer.py` converts using field mappings from JSON config
4. **Loading** → `loader.py` imports to Neo4j through unified database interface
5. **Query/Analysis** → Database operations through single `db.py` interface

### Core Components

- **Configuration**: Simple environment variable loading through `environment.py`
- **Entity Definitions**: Entity structures matching the 12-entity data model
- **Data Pipelines**: Extract-Transform-Load process with JSON-driven field mappings
- **Database Layer**: Unified interface (`db.py`) with compatibility wrapper
- **CLI Scripts**: Command-line entry points with clean business logic separation

## Refactored Architecture

### Database Interface Consolidation

```
Before: Multiple connection patterns
├── connection.py (DatabaseConnection class)
├── loader.py (direct Neo4j calls)
└── queries.py (separate connection)

After: Unified interface
├── db.py (single Database class)
├── connection.py (compatibility wrapper)
├── loader.py (uses unified interface)
└── queries.py (uses unified interface)
```

### Configuration Simplification

```
Before: Complex configuration system
└── settings.py (50+ lines, nested logic)

After: Environment-driven configuration
├── environment.py (simple functions)
├── .env.example (configuration template)
└── JSON files (schema and mappings)
```

### Script Architecture

```
Before: Mixed CLI and business logic
After: Clean separation
├── Argument parsing in scripts
├── Business logic in core modules
└── Environment-based configuration
```

## Design Principles

1. **Separation of concerns**: Each module has a specific responsibility
2. **Environment-driven configuration**: All settings through environment variables
3. **Unified database interface**: Single point for all Neo4j operations
4. **JSON-driven transformation**: Field mappings externalized to configuration
5. **Backward compatibility**: Legacy interfaces preserved during transition

## Naming Conventions

- **Packages**: Lowercase with underscores (snake_case)
- **Modules**: Descriptive of function, not implementation
- **Functions**: Action verbs that describe purpose
- **Variables**: Descriptive nouns that indicate content
- **Classes**: CapitalizedWords (PascalCase)

## Extension Points

The simplified architecture allows for future extensions:

1. Additional entity types can be added to `entities/definitions.py`
2. New data sources supported by creating extractors
3. Alternative databases integrated through the unified database interface
4. Field mappings modified through JSON configuration files
5. Environment variables added through `environment.py` functions

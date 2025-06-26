# Search Algorithms Only Branch

This branch is specifically focused on preserving and maintaining only the search algorithm features from the mining reliability database project.

## Preserved Components

### 1. Core Search Algorithms

- **Graph Search Component** (`dashboard/components/graph_search.py`)

  - Comprehensive Neo4j graph exploration
  - Multi-dimensional search capabilities
  - Results visualization and processing

- **Cypher Search Interface** (`dashboard/components/cypher_search.py`)
  - Advanced Cypher query interface
  - Query validation and safety framework
  - Template-based query system

### 2. Search Configurations

- **Graph Search Config** (`configs/graph_search_config.json`)

  - Pre-configured search queries for different use cases
  - Equipment patterns, temporal analysis, solution effectiveness

- **Cypher Search Config** (`configs/cypher_search_config.json`)
  - Safety framework settings
  - Query templates and examples
  - Validation rules

### 3. Pre-defined Search Queries (`configs/queries/`)

- Stakeholder-focused queries (who_can_help_me, what_should_i_check_first, etc.)
- Root cause analysis queries
- Solution effectiveness queries
- Investigation approach queries

### 4. Core Analytics (`mine_core/analytics/`)

- Pattern discovery algorithms
- Workflow analysis capabilities
- Cross-facility intelligence extraction

### 5. Database Layer (Minimal)

- Neo4j connectivity for search operations
- Data adapters specifically for search functionality
- Configuration management

## Removed Components

- Full dashboard application (keeping only search components)
- Data ingestion pipelines
- Non-search related utilities
- Comprehensive project documentation (keeping only search-related docs)
- Testing infrastructure (keeping only search-related tests)

## Usage

This branch can be used as a standalone search algorithm library or integrated into other projects that need sophisticated graph-based search capabilities for mining reliability data.

## Key Features Preserved

1. **Multi-dimensional Graph Search**: Advanced Neo4j pattern matching
2. **Safety-First Cypher Interface**: Validated query execution
3. **Template-Based Queries**: Pre-built queries for common use cases
4. **Cross-Facility Intelligence**: Pattern discovery across multiple facilities
5. **Solution Effectiveness Tracking**: Evidence-based solution ranking
6. **Stakeholder Query System**: Role-based information retrieval

## Project Structure After Cleanup

```
mining-reliability-search/
├── 📄 README.md                     # Search-focused documentation
├── 📄 setup.py                      # Search algorithm package configuration
├── 📄 requirements.txt               # Minimal search dependencies
├── 📄 LICENSE                       # Project license
├── 📄 Makefile                      # Build and maintenance commands
├── 📄 pyproject.toml                # Python project configuration
├── 📄 .env.example                  # Environment configuration template
│
├── 🔍 dashboard/                     # Search Interface Layer
│   ├── 📄 __init__.py
│   ├── 📄 app.py                    # Minimal app with search routes only
│   ├── 🔧 adapters/                 # Data connectivity
│   │   ├── 📄 __init__.py
│   │   ├── 📄 data_adapter.py       # Database connectivity for search
│   │   ├── 📄 config_adapter.py     # Configuration management
│   │   └── 📄 interfaces.py         # Interface definitions
│   └── 🎨 components/               # Search Components Only
│       ├── 📄 __init__.py
│       ├── 🔍 graph_search.py       # Multi-dimensional graph search (1,087 lines)
│       ├── 🛡️ cypher_search.py      # Safe Cypher interface (531 lines)
│       └── 📄 layout_template.py    # UI foundation
│
├── 🧠 mine_core/                     # Core Search Engine
│   ├── 📄 __init__.py
│   ├── 🔬 analytics/                # Pattern Discovery Engine
│   │   ├── 📄 __init__.py
│   │   ├── 📊 pattern_discovery.py  # Cross-facility pattern analysis (498 lines)
│   │   └── ⚡ workflow_analyzer.py  # Workflow pattern search
│   ├── 🗄️ database/                # Database Layer
│   │   ├── 📄 __init__.py
│   │   ├── 🔗 db.py                # Neo4j connectivity
│   │   ├── 🎯 query_manager.py     # Query execution hub (738 lines)
│   │   └── 📋 queries.py           # Pre-built query library
│   ├── 🤝 shared/                  # Shared Utilities
│   │   ├── 📄 __init__.py
│   │   ├── 🔧 common.py            # Common functions
│   │   ├── 🔄 schema_type_converter.py # Schema utilities
│   │   └── 🔍 field_resolver.py    # Field resolution
│   └── 🆘 helpers/                 # Support Infrastructure
│       ├── 📄 __init__.py
│       └── 📝 log_manager.py       # Logging infrastructure
│
├── ⚙️ configs/                      # Search Configurations
│   ├── 📄 __init__.py
│   ├── 📄 environment.py           # Environment management
│   ├── 🔍 graph_search_config.json # Search query templates (130 lines)
│   ├── 🛡️ cypher_search_config.json # Safety framework settings
│   ├── 🎯 cypher_search_config_simple.json # Basic query templates
│   ├── 📊 system_constants.json    # System constants
│   ├── 🗄️ model_schema.json       # Database schema
│   └── 📁 queries/                 # Pre-built Query Library
│       ├── 👥 who_can_help_me.cypher
│       ├── 🔍 what_should_i_check_first.cypher
│       ├── ✅ proven_solutions.cypher
│       ├── 🎯 effective_actions.cypher
│       ├── 🔬 diagnostic_experts.cypher
│       ├── 📈 investigation_approaches.cypher
│       ├── 🔧 how_do_i_fix_it.cypher
│       ├── ❓ why_did_this_happen.cypher
│       ├── 🔍 potential_root_causes.cypher
│       ├── ⏱️ repair_timelines.cypher
│       ├── 👨‍💼 expert_departments.cypher
│       ├── 📋 prioritized_investigation_steps.cypher
│       ├── 🔍 how_do_i_figure_out_whats_wrong.cypher
│       └── 🐛 effective_actions_debug.cypher
│
├── 🛠️ utils/                       # Essential Utilities
│   ├── 📄 __init__.py
│   └── 📝 json_recorder.py         # Result logging utility
│
├── 🧪 tests/                       # Search-Focused Testing
│   ├── 🔬 unit/                    # Unit Tests
│   │   ├── 🔍 search/              # Search algorithm tests
│   │   ├── 📊 analytics/           # Pattern discovery tests
│   │   └── 🗄️ database/           # Database connectivity tests
│   ├── 🔗 integration/             # Integration Tests
│   │   └── 🔍 search_integration/  # End-to-end search tests
│   └── ⚡ performance/             # Performance Tests
│       └── 🔍 search_performance/  # Search algorithm benchmarks
│
├── 📊 data/                        # Minimal Sample Data
│   └── 🧪 sample_data/            # Test datasets for algorithm validation
│
├── 📚 docs/                        # Search Documentation
│   ├── 📄 NEO4J_COMMAND_LINE_GUIDE.md
│   ├── 📊 neo4j-graph-analysis/    # Graph database benefits
│   ├── ❓ ground-truth-questions/  # Validation questions
│   └── 📋 SEARCH_BRANCH_CLEANUP_PLAN.md # Transformation documentation
│
└── 🔧 scripts/                     # Essential Scripts
    ├── 🧪 test_comprehensive_graph_search.py # Search testing
    └── 🔍 analyze_unused_functions.py # Code analysis
```

### Key Structural Changes

- **📉 Size Reduction**: ~70-80% reduction from original codebase
- **🎯 Focused Architecture**: Only search-related components preserved
- **🔗 Clean Dependencies**: Minimal, search-focused package requirements
- **📚 Targeted Documentation**: Search algorithm focus
- **🧪 Relevant Testing**: Search and analytics testing only

### Component Highlights

- **🔍 Graph Search (1,087 lines)**: Primary search interface with Neo4j integration
- **🛡️ Cypher Search (531 lines)**: Advanced query interface with safety validation
- **📊 Pattern Discovery (498 lines)**: Cross-facility intelligence algorithms
- **🎯 Query Manager (738 lines)**: Centralized database operations
- **⚙️ 14 Query Templates**: Stakeholder-focused pre-built queries
- **🔍 Search Configurations**: Comprehensive search behavior settings

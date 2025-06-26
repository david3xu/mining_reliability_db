# Mining Reliability Database - Project Structure & Workflow

## Overview

This document provides a visual representation of the project structure and workflow for the **search-algorithms-only** branch of the mining reliability database. This branch focuses exclusively on search algorithms and analytics, with all non-search components removed.

## Directory Structure Diagram

**(Based on actual project tree - 31 directories, 99 files)**

```
mining_reliability_db/
├── 📋 configs/                          # Configuration files
│   ├── __init__.py                     # Configuration package init
│   ├── environment.py                   # Environment configuration
│   ├── graph_search_config.json         # Graph search configurations
│   ├── cypher_search_config.json        # Cypher search configurations
│   ├── cypher_search_config_simple.json # Simplified cypher search
│   ├── model_schema.json                # Data model schema
│   ├── system_constants.json            # System constants
│   └── queries/                         # Pre-built query templates (14 files)
│       ├── diagnostic_experts.cypher    # Diagnostic expertise
│       ├── effective_actions.cypher     # Working solutions
│       ├── effective_actions_debug.cypher # Debug actions
│       ├── expert_departments.cypher    # Department expertise
│       ├── how_do_i_figure_out_whats_wrong.cypher # Diagnostic guidance
│       ├── how_do_i_fix_it.cypher       # Repair guidance
│       ├── investigation_approaches.cypher # Investigation methods
│       ├── potential_root_causes.cypher # Likely causes
│       ├── prioritized_investigation_steps.cypher # Step-by-step guidance
│       ├── proven_solutions.cypher      # Verified solutions
│       ├── repair_timelines.cypher      # Repair estimates
│       ├── what_should_i_check_first.cypher # Investigation priorities
│       ├── who_can_help_me.cypher       # Expert finding
│       └── why_did_this_happen.cypher   # Root cause analysis
│
├── 🎯 dashboard/                        # Web application interface
│   ├── __init__.py                     # Dashboard package init
│   ├── app.py                          # Main application entry point
│   ├── adapters/                       # Data access layer
│   │   ├── __init__.py                 # Adapter exports
│   │   ├── data_adapter.py             # Database queries & comprehensive search
│   │   ├── config_adapter.py           # Configuration loading
│   │   └── interfaces.py               # Interface definitions
│   ├── components/                     # UI components
│   │   ├── __init__.py                 # Component exports
│   │   ├── graph_search.py             # Graph search interface
│   │   ├── cypher_search.py            # Cypher query interface
│   │   ├── layout_template.py          # UI layout templates
│   │   └── micro/                      # Micro components
│   │       └── __init__.py             # Micro component exports
│   └── utils/                          # Dashboard utilities
│       ├── __init__.py                 # Utils exports
│       ├── data_transformers.py        # Data transformation utilities
│       ├── styling.py                  # Styling utilities
│       └── url_builders.py             # URL building utilities
│
├── 🔍 mine_core/                       # Core business logic
│   ├── __init__.py                     # Core package init
│   ├── analytics/                      # Analytics modules
│   │   ├── __init__.py                 # Analytics exports
│   │   ├── pattern_discovery.py       # Pattern analysis
│   │   └── workflow_analyzer.py        # Workflow analysis
│   ├── database/                       # Database layer
│   │   ├── __init__.py                 # Database exports
│   │   ├── db.py                       # Database connection
│   │   ├── queries.py                  # Base query definitions
│   │   └── query_manager.py            # Query execution
│   ├── helpers/                        # Helper modules
│   │   ├── __init__.py                 # Helper exports
│   │   └── log_manager.py              # Logging utilities
│   ├── shared/                         # Shared utilities
│   │   ├── __init__.py                 # Shared exports
│   │   ├── common.py                   # Common utilities
│   │   ├── field_resolver.py           # Field resolution
│   │   ├── field_utils.py              # Field utilities
│   │   └── schema_type_converter.py    # Type conversion
│   └── utils/                          # Core utilities
│       └── constants.py                # Core constants
│
├── 🛠️ utils/                           # Utility modules
│   ├── __init__.py                     # Utils package init
│   └── json_recorder.py               # JSON recording utilities
│
├── 📊 data/                            # Data directories
│   ├── sample_data/                    # Sample/test data
│   │   ├── fab16f86-faa9-44d9-b9d7-cfbbb47061da_sample.json
│   │   ├── mining_maintenance_nested_sample.json
│   │   ├── sample_5_fab16f86-faa9-44d9-b9d7-cfbbb47061da_sample.json
│   │   └── test_incremental_fab16f86_sample.json
│   └── search_results/                 # Search result exports
│       ├── search_20250627_070523_A_leak_was_discovered.json
│       ├── search_20250627_070540_A_leak.json
│       ├── search_20250627_070543_A_leak.json
│       ├── search_20250627_070544_A_leak.json
│       └── search_20250627_070546_A_leak.json
│
├── 📚 docs/                            # Documentation
│   ├── COMPREHENSIVE_SEARCH_IMPLEMENTATION.md # Search implementation guide
│   ├── NEO4J_COMMAND_LINE_GUIDE.md     # Neo4j CLI guide
│   ├── PROJECT_STRUCTURE_WORKFLOW.md   # This document
│   ├── PROJECT_STRUCTURE_WORKFLOW_ACCURATE.md # Accurate structure doc
│   ├── SEARCH_BRANCH_CLEANUP_PLAN.md   # Cleanup strategy
│   ├── ground-truth-questions/         # Question analysis documentation
│   │   ├── comprehensive-dimensional-analysis.md
│   │   ├── dimensional-question-framework.md
│   │   ├── dimensions-table.md
│   │   ├── question-generation-config.json
│   │   ├── question-templates-by-level.md
│   │   ├── raw-data-dimensional-analysis.md
│   │   ├── stakeholder-focused-questions.md
│   │   └── using-queries.md
│   └── neo4j-graph-analysis/           # Neo4j analysis documentation
│       └── benifits-of-neo4j-vs-eda.md
│
├── 🧪 scripts/                         # Utility scripts
│   ├── analyze_unused_functions.py     # Code analysis scripts
│   ├── README_facility_splitter.md     # Script documentation
│   ├── test_neo4j_curl.sh             # Neo4j connection test
│   ├── deployment/                     # Deployment scripts (empty)
│   ├── queries/                        # Query scripts
│   │   ├── priority_analysis.sh        # Priority analysis
│   │   ├── query.sh                    # Query execution
│   │   └── README.md                   # Query script documentation
│   └── validation/                     # Validation scripts (empty)
│
├──  tests/                           # Test structure (directories only)
│   ├── integration/                    # Integration tests
│   ├── performance/                    # Performance tests
│   └── unit/                           # Unit tests
│       ├── test_adapters/              # Adapter tests
│       ├── test_components/            # Component tests
│       └── test_core/                  # Core tests
│
├── 📄 Root Project Files               # Root-level project files
│   ├── README.md                       # Project overview and setup
│   ├── CHANGELOG.md                    # Version history and changes
│   ├── LICENSE                         # Project license
│   ├── requirements.txt                # Main Python dependencies
│   ├── requirements-dev.txt            # Development dependencies
│   ├── setup.py                        # Package setup and installation
│   ├── pyproject.toml                  # Modern Python project configuration
│   ├── Makefile                        # Build automation commands
│   ├── docker-compose.yml              # Docker services configuration
│   ├── connect_devcontainer.sh         # Development container setup
│   ├── cleanup_for_search_branch.sh    # Branch cleanup script
│   └── SEARCH_ALGORITHMS_BRANCH.md     # Search branch documentation
│
└── � Validation & Testing Scripts     # Quality assurance
    ├── verify_comprehensive_search.py  # Search functionality verification
    ├── quick_validation.py             # Quick component tests
    ├── final_validation.py             # Complete system validation
    ├── plan_completion_check.py        # Cleanup verification
    └── test_imports.py                 # Import validation tests
```

## Project Workflow Diagram

### High-Level Architecture Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MINING RELIABILITY DATABASE                        │
│                              Search-Algorithms-Only                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │   Graph Search  │  │  Cypher Search  │  │  Layout Engine  │            │
│  │  (graph_search) │  │ (cypher_search) │  │(layout_template)│            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                      dashboard/components/                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ADAPTER LAYER                                      │
│  ┌─────────────────────────────────────┐  ┌─────────────────────────────────┐│
│  │         DATA ADAPTER                │  │        CONFIG ADAPTER           ││
│  │                                     │  │                                 ││
│  │ • execute_comprehensive_graph_search│  │ • get_graph_search_config       ││
│  │ • execute_organized_comprehensive   │  │ • get_cypher_search_config      ││
│  │ • _execute_query_templates          │  │ • load configurations           ││
│  │ • _execute_single_template          │  │                                 ││
│  │ • execute_cypher_query              │  │                                 ││
│  └─────────────────────────────────────┘  └─────────────────────────────────┘│
│                      dashboard/adapters/                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        COMPREHENSIVE SEARCH ENGINE                           │
│                                                                               │
│  Phase 1: Query Templates (14 templates)                                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │ configs/queries/*.cypher → Filter Replacement → Execute                 │ │
│  │ • why_did_this_happen.cypher    • effective_actions.cypher             │ │
│  │ • proven_solutions.cypher       • who_can_help_me.cypher               │ │
│  │ • potential_root_causes.cypher  • how_do_i_fix_it.cypher               │ │
│  │ • And 8 more templates...                                              │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                     │
│  Phase 2: Configuration Searches (7+ categories)                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │ configs/graph_search_config.json → Parameter Injection → Execute       │ │
│  │ • direct_field_matches          • temporal_patterns                    │ │
│  │ • equipment_patterns            • recurring_sequences                  │ │
│  │ • causal_chains                 • solution_effectiveness               │ │
│  │ • cross_facility_patterns                                              │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                     │
│  Phase 3: Comprehensive Single Queries (3 queries)                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │ • comprehensive_incident_search  • equipment_facility_network          │ │
│  │ • solution_effectiveness_graph                                         │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                     │
│  Phase 4: Result Processing                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │ Deduplication → Limit Results → Categorize → Create Summary            │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CORE BUSINESS LAYER                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │   ANALYTICS     │  │    DATABASE     │  │     SHARED      │            │
│  │                 │  │                 │  │                 │            │
│  │ • Pattern       │  │ • Query Manager │  │ • Common Utils  │            │
│  │   Discovery     │  │ • DB Connection │  │ • Type Convert  │            │
│  │ • Workflow      │  │ • Base Queries  │  │ • Field Resolve │            │
│  │   Analyzer      │  │                 │  │                 │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│                               mine_core/                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA STORAGE LAYER                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                           NEO4J GRAPH DATABASE                           │ │
│  │                                                                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │ │
│  │  │ActionRequest│  │   Problem   │  │  RootCause  │  │ ActionPlan  │    │ │
│  │  │             │  │             │  │             │  │             │    │ │
│  │  │ ├─BELONGS_TO─┼──┼─IDENTIFIED─┼──┼──ANALYZES──┼──┼──RESOLVES──→│    │ │
│  │  │             │  │    _IN      │  │             │  │             │    │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │ │
│  │         │                                                   │           │ │
│  │         ▼                                                   ▼           │ │
│  │  ┌─────────────┐                                    ┌─────────────┐    │ │
│  │  │  Facility   │                                    │Verification │    │ │
│  │  │             │                                    │             │    │ │
│  │  └─────────────┘                                    └─────────────┘    │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Search Workflow Detail

### Comprehensive Search Process

```
User Search Query: "motor failure"
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   SEARCH ORCHESTRATION                      │
│                                                             │
│  execute_comprehensive_graph_search("motor failure")       │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                     PHASE 1: TEMPLATES                     │
│                                                             │
│  For each .cypher file in configs/queries/:                │
│  1. Load template content                                   │
│  2. Replace {filter_clause} with search parameters         │
│  3. Execute query: toLower(p.what_happened) CONTAINS       │
│     toLower('motor failure') OR ...                        │
│  4. Tag results with: search_category="template_query"     │
│                                                             │
│  Results: ~15-20 results per template × 14 templates       │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                 PHASE 2: CONFIGURATIONS                    │
│                                                             │
│  For each category in graph_search_config.json:            │
│  1. direct_field_matches (3 sub-queries)                   │
│  2. equipment_patterns (3 sub-queries)                     │
│  3. causal_chains (2 sub-queries)                          │
│  4. cross_facility_patterns (2 sub-queries)                │
│  5. temporal_patterns (3 sub-queries)                      │
│  6. recurring_sequences (2 sub-queries)                    │
│  7. solution_effectiveness (1 sub-query)                   │
│                                                             │
│  Execute with parameters: {search_term: "motor failure"}   │
│  Tag results with: search_category, search_subcategory     │
│                                                             │
│  Results: ~10-15 results per category × 7 categories       │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 3: COMPREHENSIVE                      │
│                                                             │
│  Execute 3 broad analysis queries:                         │
│  1. comprehensive_incident_search                          │
│  2. equipment_facility_network                             │
│  3. solution_effectiveness_graph                           │
│                                                             │
│  Results: ~20-30 results per query × 3 queries            │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   PHASE 4: PROCESSING                      │
│                                                             │
│  1. Combine all results (~300-400 raw results)             │
│  2. Remove duplicates by incident ID                       │
│  3. Limit to top 100 for performance                       │
│  4. Categorize by search type                              │
│  5. Create comprehensive summary                           │
│                                                             │
│  Final Result: {                                           │
│    nodes: [...],                                           │
│    summary: "Found X results for 'motor failure'",        │
│    search_metadata: { categories: {...} }                 │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                          │
│                                                             │
│  Display comprehensive results with:                       │
│  • Result summary and counts                               │
│  • Category breakdown                                      │
│  • Individual result details                               │
│  • Source query identification                             │
└─────────────────────────────────────────────────────────────┘
```

## Component Interaction Flow

```
dashboard/app.py
    │
    ├─ Initializes Dash application
    ├─ Sets up routing for search interfaces
    │
    ▼
dashboard/components/
    │
    ├─ graph_search.py → Creates graph search UI
    ├─ cypher_search.py → Creates cypher query UI
    ├─ layout_template.py → Provides UI templates
    │
    ▼
dashboard/adapters/
    │
    ├─ data_adapter.py → execute_comprehensive_graph_search()
    │   │
    │   ├─ _execute_query_templates() → Load & execute .cypher files
    │   ├─ _execute_single_template() → Individual template execution
    │   └─ execute_organized_comprehensive_search() → Categorized results
    │
    ├─ config_adapter.py → Load JSON configurations
    │   │
    │   ├─ get_graph_search_config() → graph_search_config.json
    │   └─ get_cypher_search_config() → cypher_search_config.json
    │
    ▼
mine_core/database/
    │
    ├─ query_manager.py → execute_cypher_query()
    ├─ db.py → Neo4j connection management
    └─ queries.py → Base query definitions
    │
    ▼
mine_core/analytics/
    │
    ├─ pattern_discovery.py → Pattern analysis algorithms
    └─ workflow_analyzer.py → Workflow analysis tools
    │
    ▼
Neo4j Graph Database
    │
    └─ ActionRequest ↔ Problem ↔ RootCause ↔ ActionPlan ↔ Verification
       ↓
       Facility
```

## Key Features

### 🔍 **Comprehensive Search**

- **24+ Search Methods Combined** - All query templates + configuration searches + comprehensive queries
- **Single Unified Interface** - One search executes all methods
- **Intelligent Deduplication** - Removes duplicate incidents while preserving insights
- **Performance Optimized** - Results limited and processed efficiently

### 🏗️ **Modular Architecture**

- **Clean Separation** - UI, Adapters, Core Logic, Database layers
- **Search-Only Focus** - All non-search components removed
- **Configuration-Driven** - Search behavior controlled by JSON configs and .cypher templates

### 📊 **Result Organization**

- **Category-Based** - Results organized by search method type
- **Rich Metadata** - Detailed statistics and source identification
- **Flexible Output** - Both comprehensive and organized result formats

### 🛠️ **Developer-Friendly**

- **Single Entry Point** - Only one app.py file
- **Clean Interfaces** - Well-defined adapter interfaces
- **Comprehensive Documentation** - Full workflow and structure docs
- **Easy Testing** - Verification scripts for all components

---

_This document serves as the definitive guide to understanding the search-algorithms-only branch structure and workflow. All components work together to provide a comprehensive search experience that leverages every available search method in the system._

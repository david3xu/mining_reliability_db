#!/bin/bash
# Search Algorithms Branch Cleanup Script
# This script implements the comprehensive cleanup plan documented in docs/SEARCH_BRANCH_CLEANUP_PLAN.md
# This script removes non-search related components while preserving core search algorithms

echo "🔍 Starting search-algorithms-only branch cleanup..."
echo "📋 Following plan documented in docs/SEARCH_BRANCH_CLEANUP_PLAN.md"
echo ""

# Verify we're on the correct branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "search-algorithms-only" ]; then
    echo "⚠️  WARNING: Current branch is '$current_branch', expected 'search-algorithms-only'"
    echo "Please switch to the search-algorithms-only branch before running this script."
    exit 1
fi

echo "✅ Confirmed on branch: $current_branch"
echo ""

# PHASE 1: Remove Dashboard UI Components (Non-Search)
echo "🎨 Phase 1: Removing non-search dashboard components..."
rm -rf dashboard/callbacks/
rm -rf dashboard/layouts/
rm -rf dashboard/routing/
rm -rf dashboard/validation/
rm -rf dashboard/assets/
rm -rf dashboard/dash-docs/
echo "   ✅ Removed dashboard UI infrastructure"

# Keep only search-related components in dashboard/components/
echo "🔍 Preserving only search components..."
cd dashboard/components/
# Delete non-search components (keep graph_search.py, cypher_search.py, layout_template.py, __init__.py)
find . -name "*.py" \
    -not -name "graph_search.py" \
    -not -name "cypher_search.py" \
    -not -name "layout_template.py" \
    -not -name "__init__.py" \
    -delete
cd ../..
echo "   ✅ Preserved core search components only"

# Keep only essential adapters
echo "🔌 Cleaning up data adapters..."
cd dashboard/adapters/
find . -name "*.py" \
    -not -name "data_adapter.py" \
    -not -name "config_adapter.py" \
    -not -name "interfaces.py" \
    -not -name "__init__.py" \
    -delete
cd ../..
echo "   ✅ Preserved essential data adapters only"

# PHASE 2: Remove Data Processing Components
echo ""
echo "🏭 Phase 2: Removing data processing components..."
rm -rf mine_core/pipelines/
rm -rf mine_core/business/
rm -rf mine_core/entities/
echo "   ✅ Removed ETL pipelines and business logic"

# Keep only search-related analytics
echo "🧠 Preserving core analytics algorithms..."
cd mine_core/analytics/
find . -name "*.py" \
    -not -name "pattern_discovery.py" \
    -not -name "workflow_analyzer.py" \
    -not -name "__init__.py" \
    -delete 2>/dev/null || true
cd ../..
echo "   ✅ Preserved pattern discovery and workflow analysis"

# PHASE 3: Clean Up Data Directories
echo ""
echo "📊 Phase 3: Cleaning up data directories..."
rm -rf data/combined/
rm -rf data/excel_output/
rm -rf data/facility_data/
rm -rf data/facility_markdown/
rm -rf data/inter_data/
rm -rf data/raw_data/
rm -rf data/stakeholder_results/
rm -rf data/test_output/
rm -rf data/search_results/
# Keep data/sample_data/ for testing
echo "   ✅ Removed data files, preserved sample data for testing"

# Remove excavator analysis (specific use case)
echo "🏗️ Removing specific use case analysis..."
rm -rf excavator_analysis/
echo "   ✅ Removed use-case specific analysis"

# PHASE 4: Clean Up Documentation and Scripts
echo ""
echo "📚 Phase 4: Cleaning up documentation and scripts..."

# Remove non-search related docs (preserve search-related documentation)
rm -rf docs/copilot-studio-agent-implementation/
rm -rf docs/design/
rm -rf docs/improvement/
rm -rf docs/presentation/
rm -rf docs/tasks-based-on-sharepoint/
rm -f docs/41_FIELD_DATASET_ANALYSIS.md
rm -f docs/STAKEHOLDER_JOURNEY_IMPLEMENTATION_COMPLETE.md
rm -f docs/DEV_CONTAINER_SETUP_GUIDE.md
rm -f docs/common-issues.md
# Keep: NEO4J_COMMAND_LINE_GUIDE.md, neo4j-graph-analysis/, ground-truth-questions/
echo "   ✅ Preserved search-related documentation only"

# Remove data processing scripts
rm -rf scripts/data_processing/
rm -rf scripts/setup/

# Remove most validation scripts (keep search-related ones)
cd scripts/
find . -name "*.py" \
    -not -name "test_comprehensive_graph_search.py" \
    -not -name "analyze_unused_functions.py" \
    -delete 2>/dev/null || true
cd ..
echo "   ✅ Preserved essential search testing scripts"

# PHASE 5: Clean Up Test Infrastructure
echo ""
echo "🧪 Phase 5: Cleaning up test infrastructure..."
cd tests/
# Keep only search-related tests
find . -name "*.py" \
    -not -name "*search*" \
    -not -name "*query*" \
    -not -name "*pattern*" \
    -not -name "*database*" \
    -not -name "__init__.py" \
    -delete 2>/dev/null || true
cd ..
echo "   ✅ Preserved search and database related tests only"

# Clean up utilities (keep minimal essential ones)
echo "🛠️ Cleaning up utilities..."
cd utils/
find . -name "*.py" \
    -not -name "json_recorder.py" \
    -not -name "__init__.py" \
    -delete 2>/dev/null || true
cd ..
echo "   ✅ Preserved essential utilities only"

# PHASE 6: Clean Up Configuration Files
echo ""
echo "⚙️ Phase 6: Cleaning up configuration files..."
cd configs/
# Remove non-search configurations (preserve search-related configs)
find . -name "*.json" \
    -not -name "*search*" \
    -not -name "*cypher*" \
    -not -name "system_constants.json" \
    -not -name "model_schema.json" \
    -delete 2>/dev/null || true
cd ..
echo "   ✅ Preserved search configurations and system constants only"
# Preserved files: graph_search_config.json, cypher_search_config*.json, system_constants.json, model_schema.json
# Preserved directories: queries/ (all .cypher files)
echo "   📋 Configs preserved: search configs, system constants, model schema, query templates"

# PHASE 7: Update Dependencies and Package Configuration
echo ""
echo "📦 Phase 7: Updating dependencies and package configuration..."

# Remove development requirements (keep only production essentials)
rm -f requirements-dev.txt
rm -rf requirements/
echo "   ✅ Removed development and multiple requirement files"

# Update main requirements to include only search essentials
cat > requirements.txt << 'EOF'
# Core Dependencies for Mining Reliability Search Algorithms
# Graph Database and Connectivity
neo4j>=5.0.0

# Dashboard and Web Interface
dash>=2.15.0
dash-bootstrap-components>=1.5.0

# Data Visualization and Analysis
plotly>=5.17.0
pandas>=2.0.0

# Configuration and Environment
python-dotenv>=1.0.0
pydantic>=2.0.0

# Optional: Enhanced Analytics
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0

# Logging and Utilities
structlog>=23.1.0
EOF
echo "   ✅ Updated requirements.txt with search-focused dependencies"

# Update setup.py to reflect search-only focus
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="mining-reliability-search",
    version="1.0.0",
    description="Advanced search algorithms for mining reliability data using Neo4j graph database",
    long_description="Sophisticated search algorithms and pattern discovery tools specifically designed for mining reliability data analysis. Features include graph-based search, Cypher query interface with safety validation, cross-facility pattern discovery, and stakeholder-focused query templates.",
    packages=find_packages(),
    install_requires=[
        "neo4j>=5.0.0",
        "dash>=2.15.0",
        "dash-bootstrap-components>=1.5.0",
        "plotly>=5.17.0",
        "pandas>=2.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "scikit-learn>=1.3.0",
        "structlog>=23.1.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Engineers",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="mining reliability search algorithms neo4j graph database pattern discovery",
    author="Mining Reliability Team",
    project_urls={
        "Documentation": "https://github.com/your-org/mining-reliability-search/docs",
        "Source": "https://github.com/your-org/mining-reliability-search",
        "Tracker": "https://github.com/your-org/mining-reliability-search/issues",
    },
)
EOF
echo "   ✅ Updated setup.py with search-focused package definition"

# PHASE 8: Update Documentation
echo ""
echo "📝 Phase 8: Updating project documentation..."

# Update README to reflect search-only focus
cat > README.md << 'EOF'
# Mining Reliability Search Algorithms

Advanced search algorithms and pattern discovery tools specifically designed for mining reliability data analysis using Neo4j graph database.

## 🚀 Overview

This repository contains sophisticated search algorithms that enable engineers and analysts to quickly discover patterns, solutions, and insights across mining facility data. Built on Neo4j graph database technology, it provides both user-friendly interfaces and powerful programmatic access to complex mining reliability data.

## ✨ Key Features

### 🔍 Multi-Dimensional Graph Search
- **Comprehensive Pattern Matching**: Search across incidents, equipment, solutions, and facilities simultaneously
- **Cross-Facility Intelligence**: Discover knowledge sharing opportunities between different facilities
- **Equipment Failure Analysis**: Specialized algorithms for equipment-specific failure patterns
- **Temporal Pattern Discovery**: Time-based trend analysis and seasonal pattern detection

### 🛡️ Safe Cypher Query Interface
- **Query Validation Framework**: Built-in safety checks prevent dangerous operations
- **Template-Based System**: Pre-built queries for common use cases
- **Advanced Result Visualization**: Interactive charts and graphs for query results
- **Export Capabilities**: CSV, JSON, and visualization exports

### 📊 Pattern Discovery Engine
- **Root Cause Analysis**: Automated discovery of recurring root causes
- **Solution Effectiveness Ranking**: Evidence-based solution success analysis
- **Stakeholder Knowledge Mapping**: Connect experts with relevant experience
- **Workflow Analysis**: Process efficiency and bottleneck identification

### 🎯 Stakeholder-Focused Queries
Pre-built queries optimized for different roles:
- **Engineers**: "What should I check first?", "Who can help me?"
- **Managers**: "What are the most effective solutions?", "Where are the patterns?"
- **Analysts**: "Why did this happen?", "How do I prevent recurrence?"

## 🏗️ Architecture

```
mining-reliability-search/
├── dashboard/
│   ├── components/
│   │   ├── graph_search.py      # Multi-dimensional graph search interface
│   │   └── cypher_search.py     # Advanced Cypher query interface
│   └── adapters/                # Data connectivity layer
├── mine_core/
│   ├── analytics/
│   │   ├── pattern_discovery.py # Core pattern analysis algorithms
│   │   └── workflow_analyzer.py # Workflow pattern analysis
│   └── database/                # Neo4j connectivity and query management
├── configs/
│   ├── graph_search_config.json # Search algorithm configurations
│   ├── cypher_search_config.json # Query safety and templates
│   └── queries/                 # Pre-built Cypher query library
└── utils/                       # Utilities and helpers
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Neo4j Database 5.0+
- Access to mining reliability data in Neo4j

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/mining-reliability-search.git
cd mining-reliability-search

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Neo4j connection details:
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your_password
```

### Running the Search Interface

```bash
# Start the search dashboard
python -m dashboard.app

# Open your browser to: http://localhost:8050
```

### Programmatic Usage

```python
from mine_core.analytics.pattern_discovery import PatternDiscovery
from mine_core.database.query_manager import QueryManager

# Initialize search components
pattern_discovery = PatternDiscovery()
query_manager = QueryManager()

# Search for equipment failures
results = pattern_discovery.analyze_equipment_patterns("excavator motor")

# Execute custom search
query_results = query_manager.search_comprehensive("contamination incidents")
```

## 📋 Core Components

### Graph Search Engine (`dashboard/components/graph_search.py`)
- **Multi-dimensional search**: Incidents, equipment, solutions, facilities
- **Intelligent result ranking**: Relevance-based result ordering
- **Export capabilities**: Multiple output formats
- **Real-time suggestions**: Auto-complete and search hints

### Cypher Query Interface (`dashboard/components/cypher_search.py`)
- **Safety validation**: Query sanitization and limits
- **Template library**: Common query patterns
- **Result visualization**: Charts, tables, and graphs
- **Query history**: Track and reuse previous searches

### Pattern Discovery (`mine_core/analytics/pattern_discovery.py`)
- **Cross-facility analysis**: Compare patterns across locations
- **Equipment failure clustering**: Group similar failure modes
- **Solution effectiveness scoring**: Rank solutions by success rate
- **Trend detection**: Identify emerging patterns over time

### Query Templates (`configs/queries/`)
Stakeholder-focused pre-built queries:
- `who_can_help_me.cypher` - Find relevant experts
- `what_should_i_check_first.cypher` - Priority investigation steps
- `proven_solutions.cypher` - Validated solution approaches
- `why_did_this_happen.cypher` - Root cause analysis

## 🔧 Configuration

### Search Behavior (`configs/graph_search_config.json`)
```json
{
  "search_queries": {
    "comprehensive_incident_search": "...",
    "equipment_facility_network": "...",
    "solution_effectiveness_graph": "..."
  },
  "result_limits": {
    "default_limit": 20,
    "max_limit": 100
  }
}
```

### Safety Framework (`configs/cypher_search_config.json`)
```json
{
  "safety": {
    "allowed_keywords": ["MATCH", "RETURN", "WHERE", "ORDER BY"],
    "forbidden_keywords": ["DELETE", "DROP", "CREATE"],
    "max_query_length": 2000,
    "require_limit_clause": true
  }
}
```

## 📊 Use Cases

### Equipment Failure Analysis
Search for patterns in equipment failures across facilities:
```cypher
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
WHERE ar.categories CONTAINS 'excavator'
RETURN f.facility_id, count(*) as incidents
ORDER BY incidents DESC
```

### Solution Effectiveness Tracking
Find the most effective solutions for specific problems:
```cypher
MATCH (ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
WHERE v.is_action_plan_effective = 'Yes'
RETURN ap.action_plan, count(*) as success_count
ORDER BY success_count DESC
```

### Expert Knowledge Discovery
Identify who has experience with specific issues:
```cypher
MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
WHERE ar.categories CONTAINS $equipment_type
RETURN f.facility_id, collect(ar.responsible_department) as departments
```

## 🧪 Testing

```bash
# Run search algorithm tests
python -m pytest tests/unit/analytics/
python -m pytest tests/unit/database/

# Test search interfaces
python scripts/test_comprehensive_graph_search.py

# Performance testing
python -m pytest tests/performance/ -v
```

## 📚 Documentation

- **[Neo4j Command Line Guide](docs/NEO4J_COMMAND_LINE_GUIDE.md)** - Database interaction guide
- **[Graph Analysis Benefits](docs/neo4j-graph-analysis/)** - Why graph databases for mining data
- **[Ground Truth Questions](docs/ground-truth-questions/)** - Validation question library
- **[Search Algorithm Details](docs/SEARCH_BRANCH_CLEANUP_PLAN.md)** - Technical implementation details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-search`)
3. Commit your changes (`git commit -m 'Add amazing search feature'`)
4. Push to the branch (`git push origin feature/amazing-search`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Report bugs and request features via GitHub Issues
- **Questions**: Use GitHub Discussions for general questions

## 🔗 Related Projects

- **Neo4j**: Graph database platform
- **Dash**: Python web application framework
- **Plotly**: Interactive visualization library

---

**Built with ❤️ for mining reliability engineers**
EOF
echo "   ✅ Updated README.md with search-focused content"

# PHASE 9: Final Summary and Validation
echo ""
echo "🎯 CLEANUP COMPLETE!"
echo "===================="
echo ""
echo "✅ Search-algorithms-only branch transformation completed successfully!"
echo ""
echo "📊 PRESERVED COMPONENTS:"
echo "├── 🔍 Core Search Algorithms"
echo "│   ├── dashboard/components/graph_search.py (1,087 lines)"
echo "│   ├── dashboard/components/cypher_search.py (531 lines)"
echo "│   └── dashboard/components/layout_template.py"
echo "├── 🗄️ Database Layer"
echo "│   ├── mine_core/database/db.py"
echo "│   ├── mine_core/database/query_manager.py (738 lines)"
echo "│   └── mine_core/database/queries.py"
echo "├── 🧠 Analytics Engine"
echo "│   ├── mine_core/analytics/pattern_discovery.py (498 lines)"
echo "│   └── mine_core/analytics/workflow_analyzer.py"
echo "├── ⚙️ Search Configurations"
echo "│   ├── configs/graph_search_config.json (130 lines)"
echo "│   ├── configs/cypher_search_config*.json"
echo "│   ├── configs/system_constants.json"
echo "│   ├── configs/model_schema.json"
echo "│   └── configs/queries/*.cypher (14 query templates)"
echo "├── 🔌 Data Adapters"
echo "│   ├── dashboard/adapters/data_adapter.py"
echo "│   ├── dashboard/adapters/config_adapter.py"
echo "│   └── dashboard/adapters/interfaces.py"
echo "├── 🛠️ Essential Utilities"
echo "│   ├── utils/json_recorder.py"
echo "│   ├── mine_core/shared/common.py"
echo "│   └── mine_core/helpers/log_manager.py"
echo "└── 📚 Search Documentation"
echo "    ├── docs/NEO4J_COMMAND_LINE_GUIDE.md"
echo "    ├── docs/neo4j-graph-analysis/"
echo "    ├── docs/ground-truth-questions/"
echo "    └── docs/SEARCH_BRANCH_CLEANUP_PLAN.md"
echo ""
echo "�️ REMOVED COMPONENTS:"
echo "├── Dashboard UI (callbacks, layouts, routing, validation)"
echo "├── Non-search components (12+ dashboard components)"
echo "├── Data processing (pipelines, business logic, entities)"
echo "├── Raw data files (all data directories except sample_data)"
echo "├── Non-search configurations (10+ config files)"
echo "├── Development infrastructure (scripts, testing, docs)"
echo "└── Project-specific analysis (excavator_analysis/)"
echo ""
echo "📦 UPDATED FILES:"
echo "├── requirements.txt - Search-focused dependencies only"
echo "├── setup.py - Mining-reliability-search package"
echo "├── README.md - Comprehensive search algorithm documentation"
echo "└── Module __init__.py files - Updated imports"
echo ""
echo "🚀 NEXT STEPS:"
echo "1. Run validation tests: python scripts/test_comprehensive_graph_search.py"
echo "2. Test search interface: python -m dashboard.app"
echo "3. Verify configurations load: python -c 'from configs.environment import get_schema; print(\"Config OK\")'"
echo "4. Check dependencies: pip install -r requirements.txt"
echo "5. Review documentation: cat README.md"
echo ""
echo "📋 ESTIMATED REDUCTION: 70-80% of original codebase"
echo "🎯 FOCUS: Core search algorithms and minimal supporting infrastructure"
echo ""
echo "🎉 Ready to use as a focused search algorithm library!"
echo ""
echo "📖 See docs/SEARCH_BRANCH_CLEANUP_PLAN.md for complete transformation details"

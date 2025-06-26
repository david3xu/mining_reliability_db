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

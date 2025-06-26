# Search Algorithms Branch - Cleanup Plan

## Overview

This document outlines the comprehensive plan for transforming the mining reliability database repository into a focused search-algorithms-only branch. The goal is to preserve core search functionality while removing non-essential components.

## Branch Strategy

- **Source Branch**: `main` (current comprehensive mining reliability system)
- **Target Branch**: `search-algorithms-only`
- **Purpose**: Create a focused repository containing only search algorithms and related infrastructure

---

## 📋 DETAILED CLEANUP PLAN

### 🔍 CORE SEARCH COMPONENTS - PRESERVE

| Component                  | Path                                      | Action     | Size        | Justification                                             |
| -------------------------- | ----------------------------------------- | ---------- | ----------- | --------------------------------------------------------- |
| **Graph Search Engine**    | `dashboard/components/graph_search.py`    | **KEEP**   | 1,087 lines | Primary graph search functionality with Neo4j integration |
| **Cypher Query Interface** | `dashboard/components/cypher_search.py`   | **KEEP**   | 531 lines   | Advanced query interface with safety validation framework |
| **Layout Template**        | `dashboard/components/layout_template.py` | **KEEP**   | TBD         | UI foundation required by search components               |
| **Component Init**         | `dashboard/components/__init__.py`        | **MODIFY** | Small       | Update imports to only include search components          |

### 🔌 DATA ACCESS LAYER - PRESERVE

| Component              | Path                                   | Action   | Size      | Justification                                   |
| ---------------------- | -------------------------------------- | -------- | --------- | ----------------------------------------------- |
| **Database Core**      | `mine_core/database/db.py`             | **KEEP** | TBD       | Essential Neo4j connectivity                    |
| **Query Manager**      | `mine_core/database/query_manager.py`  | **KEEP** | 738 lines | Centralized query execution and result handling |
| **Database Queries**   | `mine_core/database/queries.py`        | **KEEP** | TBD       | Pre-built search query library                  |
| **Data Adapter**       | `dashboard/adapters/data_adapter.py`   | **KEEP** | TBD       | Database connectivity for search operations     |
| **Config Adapter**     | `dashboard/adapters/config_adapter.py` | **KEEP** | TBD       | Configuration management for search             |
| **Adapter Interfaces** | `dashboard/adapters/interfaces.py`     | **KEEP** | TBD       | Interface definitions used by search components |

### 🧠 ANALYTICS ENGINE - PRESERVE

| Component             | Path                                       | Action     | Size      | Justification                                                |
| --------------------- | ------------------------------------------ | ---------- | --------- | ------------------------------------------------------------ |
| **Pattern Discovery** | `mine_core/analytics/pattern_discovery.py` | **KEEP**   | 498 lines | Core pattern analysis algorithms for cross-facility insights |
| **Workflow Analyzer** | `mine_core/analytics/workflow_analyzer.py` | **KEEP**   | TBD       | Workflow pattern search and analysis                         |
| **Analytics Init**    | `mine_core/analytics/__init__.py`          | **MODIFY** | Small     | Update imports for remaining analytics modules               |

### ⚙️ CONFIGURATION FILES - PRESERVE

| File                     | Path                                       | Action       | Size      | Justification                                  |
| ------------------------ | ------------------------------------------ | ------------ | --------- | ---------------------------------------------- |
| **Graph Search Config**  | `configs/graph_search_config.json`         | **KEEP**     | 130 lines | Core search query templates and configurations |
| **Cypher Search Config** | `configs/cypher_search_config.json`        | **KEEP**     | TBD       | Safety framework and query validation rules    |
| **Cypher Simple Config** | `configs/cypher_search_config_simple.json` | **KEEP**     | TBD       | Simplified query templates for basic searches  |
| **System Constants**     | `configs/system_constants.json`            | **KEEP**     | TBD       | System-wide constants used by search           |
| **Model Schema**         | `configs/model_schema.json`                | **KEEP**     | TBD       | Database schema definitions for search         |
| **Environment Config**   | `configs/environment.py`                   | **KEEP**     | TBD       | Environment and configuration management       |
| **Query Templates**      | `configs/queries/*.cypher`                 | **KEEP ALL** | 14 files  | Pre-built Cypher queries for stakeholder needs |

### 🛠️ UTILITIES - PRESERVE MINIMAL

| Component            | Path                                        | Action   | Size | Justification                                |
| -------------------- | ------------------------------------------- | -------- | ---- | -------------------------------------------- |
| **JSON Recorder**    | `utils/json_recorder.py`                    | **KEEP** | TBD  | Used by search components for result logging |
| **Common Utilities** | `mine_core/shared/common.py`                | **KEEP** | TBD  | Common functions used by search algorithms   |
| **Log Manager**      | `mine_core/helpers/log_manager.py`          | **KEEP** | TBD  | Logging infrastructure for search operations |
| **Schema Converter** | `mine_core/shared/schema_type_converter.py` | **KEEP** | TBD  | Schema utilities for search                  |
| **Field Resolver**   | `mine_core/shared/field_resolver.py`        | **KEEP** | TBD  | Field resolution for search queries          |

### 🎯 APPLICATION ENTRY POINT - MODIFY

| Component            | Path                    | Action     | Modification Required                                   |
| -------------------- | ----------------------- | ---------- | ------------------------------------------------------- |
| **Main Application** | `dashboard/app.py`      | **MODIFY** | Remove all routes except graph search and cypher search |
| **Dashboard Init**   | `dashboard/__init__.py` | **MODIFY** | Update imports for remaining components                 |
| **Mine Core Init**   | `mine_core/__init__.py` | **MODIFY** | Update imports for remaining modules                    |

---

## 🗑️ COMPONENTS TO DELETE

### 🎨 UI COMPONENTS - DELETE

| Category                 | Files/Directories       | Reason for Removal                          |
| ------------------------ | ----------------------- | ------------------------------------------- |
| **Dashboard Callbacks**  | `dashboard/callbacks/`  | Non-search UI interaction logic             |
| **Dashboard Layouts**    | `dashboard/layouts/`    | Complex multi-page UI layouts               |
| **Dashboard Routing**    | `dashboard/routing/`    | Multi-page navigation system                |
| **Dashboard Validation** | `dashboard/validation/` | UI validation not core to search algorithms |
| **Dashboard Assets**     | `dashboard/assets/`     | UI styling and static assets                |
| **Dashboard Docs**       | `dashboard/dash-docs/`  | Dashboard-specific documentation            |

### 🖼️ NON-SEARCH COMPONENTS - DELETE

| Component                | Path                                                   | Reason for Removal                |
| ------------------------ | ------------------------------------------------------ | --------------------------------- |
| **Facility Detail UI**   | `dashboard/components/facility_detail.py`              | Facility-specific visualization   |
| **Graph Visualizer**     | `dashboard/components/graph_visualizer.py`             | General graph visualization UI    |
| **Tab Navigation**       | `dashboard/components/tab_navigation.py`               | UI navigation components          |
| **Workflow Analysis UI** | `dashboard/components/workflow_analysis.py`            | Workflow-specific UI              |
| **Data Quality UI**      | `dashboard/components/data_quality.py`                 | Data quality visualization        |
| **Interactive Elements** | `dashboard/components/interactive_elements.py`         | General UI interactive components |
| **Portfolio Overview**   | `dashboard/components/portfolio_overview.py`           | Portfolio management UI           |
| **Case Study UI**        | `dashboard/components/solution_sequence_case_study.py` | Case study visualization          |
| **Incident Search UI**   | `dashboard/components/incident_search.py`              | Incident-specific search UI       |
| **Stakeholder UI**       | `dashboard/components/stakeholder_essentials.py`       | Stakeholder management UI         |

### 🏭 DATA PROCESSING - DELETE

| Category                    | Path                                             | Reason for Removal                    |
| --------------------------- | ------------------------------------------------ | ------------------------------------- |
| **ETL Pipelines**           | `mine_core/pipelines/`                           | Data processing not search algorithms |
| **Business Logic**          | `mine_core/business/`                            | Business rules not search focused     |
| **Entity Management**       | `mine_core/entities/`                            | Entity CRUD operations not search     |
| **Data Processing Scripts** | `scripts/data_processing/`                       | Data transformation scripts           |
| **Facility Adapters**       | `dashboard/adapters/facility_adapter.py`         | Facility-specific data handling       |
| **Workflow Adapters**       | `dashboard/adapters/workflow_adapter.py`         | Workflow-specific data handling       |
| **JSON Export Adapter**     | `dashboard/adapters/data_adapter_json_export.py` | Data export functionality             |

### 📊 DATA STORAGE - DELETE

| Category                | Path                        | Reason for Removal                          |
| ----------------------- | --------------------------- | ------------------------------------------- |
| **Raw Data**            | `data/raw_data/`            | Actual data files not needed for algorithms |
| **Combined Data**       | `data/combined/`            | Processed data not needed                   |
| **Intermediate Data**   | `data/inter_data/`          | Processing intermediates not needed         |
| **Excel Outputs**       | `data/excel_output/`        | Export formats not needed                   |
| **Facility Data**       | `data/facility_data/`       | Facility-specific data files                |
| **Facility Markdown**   | `data/facility_markdown/`   | Documentation files                         |
| **Test Output**         | `data/test_output/`         | Test result files                           |
| **Stakeholder Results** | `data/stakeholder_results/` | Result files not algorithms                 |
| **Search Results**      | `data/search_results/`      | Cached search results                       |

### ⚙️ NON-SEARCH CONFIGS - DELETE

| File                                           | Reason for Removal                                 |
| ---------------------------------------------- | -------------------------------------------------- |
| `configs/dashboard_config.json`                | Dashboard UI configuration                         |
| `configs/dashboard_styling.json`               | UI styling configuration                           |
| `configs/dashboard_charts.json`                | Chart visualization config                         |
| `configs/field_mappings.json`                  | Data field mapping not search                      |
| `configs/field_analysis.json`                  | Field analysis not search algorithms               |
| `configs/field_category_display_mapping.json`  | UI display mapping                                 |
| `configs/maintenance_records_config.json`      | Records management config                          |
| `configs/stakeholder_intelligence_config.json` | Stakeholder management config                      |
| `configs/stakeholder_essential_queries.json`   | Move relevant queries to search configs            |
| `configs/entity_classification.json`           | Entity management config                           |
| `configs/entity_connections.json`              | Entity relationship config (unless used by search) |
| `configs/workflow_stages.json`                 | Workflow management config                         |
| `configs/case_study_schema.json`               | Case study specific schema                         |
| `configs/symptom_classification_config.json`   | Symptom management config                          |

### 🧪 NON-SEARCH SCRIPTS - DELETE

| Script                                       | Reason for Removal            |
| -------------------------------------------- | ----------------------------- |
| `scripts/validate_phase1_core_foundation.py` | Project validation not search |
| `scripts/validate_dashboard_architecture.py` | Dashboard validation          |
| `scripts/fix_raw_data.py`                    | Data fixing not algorithms    |
| `scripts/check_interface_compliance.py`      | Interface validation          |
| `scripts/validate_consistency.py`            | Data consistency checking     |
| `scripts/enforce_config_consistency.py`      | Config management             |
| `scripts/setup/`                             | Database setup scripts        |
| All other scripts except search-related      | Various non-search utilities  |

### 📚 NON-SEARCH DOCUMENTATION - DELETE

| Documentation                                         | Reason for Removal              |
| ----------------------------------------------------- | ------------------------------- |
| `docs/41_FIELD_DATASET_ANALYSIS.md`                   | Dataset analysis not algorithms |
| `docs/common-issues.md`                               | General troubleshooting         |
| `docs/DEV_CONTAINER_SETUP_GUIDE.md`                   | Development setup               |
| `docs/STAKEHOLDER_JOURNEY_IMPLEMENTATION_COMPLETE.md` | Implementation documentation    |
| `docs/copilot-studio-agent-implementation/`           | AI agent implementation         |
| `docs/design/`                                        | System design documentation     |
| `docs/improvement/`                                   | Improvement suggestions         |
| `docs/presentation/`                                  | Presentation materials          |
| `docs/tasks-based-on-sharepoint/`                     | Task management docs            |

### 🏗️ PROJECT STRUCTURE - DELETE

| Component              | Reason for Removal                    |
| ---------------------- | ------------------------------------- |
| `excavator_analysis/`  | Specific use case analysis            |
| `requirements/`        | Multiple requirement files not needed |
| `requirements-dev.txt` | Development dependencies              |

---

## 📝 FILES TO MODIFY

### 🔧 Core Application Files

| File                   | Modifications Required                                                                                                                                                                                                                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`dashboard/app.py`** | • Remove all routes except graph search and cypher search<br>• Remove imports for deleted components<br>• Simplify app initialization<br>• Keep only search-related callbacks                                                                                                              |
| **`setup.py`**         | • Update package name to "mining-reliability-search"<br>• Update description to focus on search algorithms<br>• Remove dependencies for deleted components<br>• Update classifiers                                                                                                         |
| **`requirements.txt`** | • Keep only search-essential packages:<br>&nbsp;&nbsp;- neo4j>=5.0.0<br>&nbsp;&nbsp;- dash>=2.15.0<br>&nbsp;&nbsp;- dash-bootstrap-components>=1.5.0<br>&nbsp;&nbsp;- plotly>=5.17.0<br>&nbsp;&nbsp;- pandas>=2.0.0<br>&nbsp;&nbsp;- python-dotenv>=1.0.0<br>&nbsp;&nbsp;- pydantic>=2.0.0 |
| **`README.md`**        | • Rewrite to focus on search algorithms<br>• Update quick start guide<br>• List preserved components<br>• Update usage examples                                                                                                                                                            |

### 🔗 Module Initialization Files

| File                                   | Modifications Required                                        |
| -------------------------------------- | ------------------------------------------------------------- |
| **`dashboard/__init__.py`**            | • Update imports to only include remaining components         |
| **`dashboard/components/__init__.py`** | • Import only graph_search and cypher_search                  |
| **`dashboard/adapters/__init__.py`**   | • Import only data_adapter, config_adapter, interfaces        |
| **`mine_core/__init__.py`**            | • Update imports for remaining database and analytics modules |
| **`mine_core/analytics/__init__.py`**  | • Import only pattern_discovery and workflow_analyzer         |
| **`mine_core/database/__init__.py`**   | • Keep all current imports (core database functionality)      |

---

## 🧪 TESTING STRATEGY

### ✅ Tests to Keep

| Test Category                | Path                         | Action                       |
| ---------------------------- | ---------------------------- | ---------------------------- |
| **Search Integration Tests** | `tests/integration/*search*` | Keep and maintain            |
| **Search Unit Tests**        | `tests/unit/*search*`        | Keep and maintain            |
| **Query Tests**              | `tests/unit/*query*`         | Keep and maintain            |
| **Database Tests**           | `tests/unit/database/`       | Keep essential tests         |
| **Analytics Tests**          | `tests/unit/analytics/`      | Keep pattern discovery tests |

### 🗑️ Tests to Remove

| Test Category             | Reason for Removal             |
| ------------------------- | ------------------------------ |
| **UI Component Tests**    | Testing deleted UI components  |
| **Data Processing Tests** | Testing deleted ETL pipelines  |
| **Business Logic Tests**  | Testing deleted business rules |
| **Integration Tests**     | Testing deleted integrations   |

---

## 📊 SAMPLE DATA STRATEGY

### 📁 Data to Keep (Minimal)

| Directory               | Purpose                                     | Action               |
| ----------------------- | ------------------------------------------- | -------------------- |
| **`data/sample_data/`** | Small dataset for testing search algorithms | Keep minimal samples |

### 🗑️ Data to Remove

| Directory                  | Reason for Removal                                    |
| -------------------------- | ----------------------------------------------------- |
| All other data directories | Large datasets not needed for algorithm demonstration |

---

## 🚀 VALIDATION PLAN

### ✅ Post-Cleanup Validation Steps

1. **Dependency Check**: Ensure all imports resolve correctly
2. **Search Functionality**: Test graph search and cypher search components
3. **Configuration Loading**: Verify all config files load properly
4. **Database Connectivity**: Test Neo4j connection and query execution
5. **Pattern Discovery**: Test analytics algorithms
6. **Documentation**: Verify README and documentation accuracy

### 📋 Success Criteria

- [ ] Application starts without errors
- [ ] Graph search interface loads and functions
- [ ] Cypher search interface loads with safety validation
- [ ] Pre-defined queries execute successfully
- [ ] Pattern discovery algorithms run without errors
- [ ] All configuration files load correctly
- [ ] Dependencies are minimal and focused
- [ ] Documentation accurately reflects preserved functionality

---

## 📈 EXPECTED OUTCOMES

### 📉 Repository Size Reduction

- **Estimated reduction**: 70-80% of current codebase
- **Focus**: Core search algorithms and minimal supporting infrastructure
- **Benefits**: Easier maintenance, clearer purpose, faster onboarding

### 🎯 Preserved Functionality

- Full graph search capabilities
- Advanced Cypher query interface with safety framework
- Pattern discovery across facilities
- Pre-built query templates for common use cases
- Configuration-driven search behavior

### 🔄 Reusability

- Can be integrated into other mining reliability projects
- Standalone search algorithm library
- Clear API for search operations
- Well-documented search configurations

---

## 📋 EXECUTION CHECKLIST

- [ ] Create search-algorithms-only branch
- [ ] Execute cleanup script (to be created)
- [ ] Modify remaining files per plan
- [ ] Update documentation
- [ ] Test all preserved functionality
- [ ] Validate configuration loading
- [ ] Update README with new focus
- [ ] Create final validation report

## 📅 Timeline

- **Planning**: Complete ✅
- **Script Creation**: Next step
- **Execution**: After script validation
- **Testing**: After cleanup completion
- **Documentation**: Final step

---

_This plan ensures a systematic transformation while preserving all essential search algorithm functionality._

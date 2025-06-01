---
applyTo: "**"
---

# Mining Reliability Database - Neo4j Dashboard Project Instructions

## High-Level Rules

- **Keep it simple**: Basic, direct, and straightforward solutions only
- **No complexity**: Avoid unnecessary features, over-engineering, or complex patterns
- **Lightweight approach**: Minimal code, minimal dependencies, maximum efficiency
- **Professional simplicity**: Clean, readable, maintainable code without bells and whistles
- **Data-driven everything**: All configurations, schemas, and logic must be dynamic and driven by data/config files
- **No hardcoding**: Never use static or hardcoded values - always reference configs, schemas, or database
- **Concise communication**: Explanations should be brief, clear, and easy to understand
- **Real codebase focus**: All suggestions must be based on actual project structure and existing code
- **Evolution-aware**: This project grows and changes over time - always check current codebase before making assumptions

## Project Evolution & Dynamic Nature

This project is **actively evolving** with continuous improvements and additions:

- **Check existing code first**: Always examine current files before suggesting new implementations
- **Extend, don't replace**: Build upon existing patterns and structures rather than recreating
- **Schema evolution**: Configurations and schemas change over time - reference latest versions
- **Incremental enhancement**: Add features that complement existing functionality
- **Backward compatibility**: Maintain compatibility with existing data and workflows
- **Document changes**: Update relevant configs when adding new features or data structures

## Project Overview

This is an **operational reliability intelligence** system using Neo4j as the graph database and Dash for the dashboard interface. The system tracks incident workflows, problem analysis, and action verification across mining facilities - focusing on **incident workflow intelligence** rather than traditional maintenance management.

## Architecture & Technology Stack

- **Database**: Neo4j graph database
- **Backend**: Python with neo4j driver
- **Dashboard**: Plotly Dash with navigation hub design
- **Data Processing**: Pandas, custom pipelines in `mine_core`
- **Configuration**: JSON-based configs in `configs/` directory
- **Core Pattern**: Adapter-driven architecture with data transformers

## Coding Standards

### Python Code Style

- Follow PEP 8 standards
- Use type hints for function parameters and return values
- Use descriptive variable names that reflect the mining domain
- Keep functions focused and under 50 lines when possible
- Use docstrings for all public functions and classes
- **No unnecessary complexity**: Write the simplest solution that works
- **Reference configs**: Always use `configs/` files instead of hardcoded values

### File Organization

- Place dashboard components in `dashboard/components/`
- Put data processing logic in `mine_core/` modules
- Store configurations in `configs/` directory
- Keep database schemas and scripts in `scripts/`
- **Actual structure**: Use `dashboard/adapters/interaction_handlers.py` for callbacks
- **Follow existing patterns**: Study current file structure before adding new modules
- **Maintain consistency**: Use established naming conventions and organization

## Core Architectural Patterns

### Data Flow Architecture

```
mine_core.database.queries → dashboard.adapters → utils.data_transformers → components
```

### Schema-Driven Development

- `field_mappings.json` drives data processing logic
- `model_schema.json` defines entity relationships and UI generation
- All interfaces dynamically generated from schema definitions
- No hardcoded field names or static configurations

### Data Adapter Pattern

- `get_data_adapter()` singleton access for mine_core integration
- Single point data access with caching and validation
- Adapter layer handles all database interactions

### Error Handling Standard

- Use `handle_error(logger, e, context)` pattern throughout codebase
- Consistent logging with specific context information
- Graceful degradation for data quality issues

### Neo4j Best Practices

- Use parameterized queries to prevent injection
- Follow graph modeling best practices (nodes for entities, relationships for connections)
- Use meaningful node labels and relationship types
- Index frequently queried properties

### Dashboard Development

- Use modular component structure in `dashboard/components/`
- Implement interaction handlers in `dashboard/adapters/interaction_handlers.py`
- Follow the layout template pattern in `dashboard/layouts/`
- Ensure responsive design for different screen sizes
- **Navigation hub design**: Clean home page with metric cards → dedicated analysis pages
- **Schema-driven UI**: Use `configs/model_schema.json` to build dynamic interfaces
- **Config-driven styling**: Reference `configs/dashboard_config.json` for all UI settings

## Dashboard Design Philosophy

### Navigation Architecture

- **Home Page**: Interactive metric cards only (clean, focused)
- **Analysis Pages**: Dedicated chart/table focus (single purpose views)
- **Facility Pages**: Individual facility drill-down with routing
- **Multi-tab Support**: Portfolio/Quality/Workflow analysis views

### Click-Based Exploration

- Metric cards navigate to dedicated pages (`/historical-records`, `/facilities-distribution`)
- Professional routing patterns with URL-based navigation
- Clean separation between overview and detailed analysis
- Enterprise-style navigation hub rather than traditional dashboard

### URL Navigation Structure

- `/` - Clean metric cards home page
- `/historical-records` - Timeline analysis focus
- `/facilities-distribution` - Pie chart analysis
- `/data-types-distribution` - Bar chart analysis
- `/facility/facility-name` - Individual facility drill-down

### Standardized Layout System

- `layout_template.py` provides consistent grid structure
- `create_standard_layout()` for all analysis pages
- Metric cards, main grid, summary sections pattern

## Domain Knowledge

### Incident Workflow Intelligence Context

- **Facilities**: Mining sites with operational reliability tracking
- **ActionRequest**: Incident reporting and tracking system
- **Problem**: Problem definition and analysis workflows
- **RootCause**: Causal analysis and investigation processes
- **ActionPlan**: Resolution planning and execution tracking
- **Verification**: Effectiveness verification and closure processes

### Key Entities (Incident Workflow Focus)

1. **ActionRequest**: Incident reporting and initial tracking
2. **Problem**: Problem definition and analysis workflows
3. **RootCause**: Causal analysis and investigation
4. **ActionPlan**: Resolution planning and execution records
5. **Verification**: Effectiveness verification and closure tracking

### Data Flow

1. Raw incident data ingestion from mining systems
2. Processing through `mine_core.pipelines` for workflow intelligence
3. Storage in Neo4j graph structure (incident relationships)
4. Visualization through navigation hub dashboard

## Development Preferences

### When Working with Data

- Always validate data integrity before processing
- Use the field mappings in `configs/field_mappings.json`
- Handle missing or malformed data gracefully
- Log data quality issues for monitoring
- **Dynamic processing**: Base all data logic on schema definitions, never hardcode field names
- **Config-driven validation**: Use schema files to define validation rules

### Dashboard Features

- Prioritize performance for large datasets
- Implement proper error handling and user feedback
- Use caching where appropriate
- Provide interactive filtering and drill-down capabilities

### Code Quality

- Write unit tests for core business logic
- Use the existing test structure in `tests/`
- Handle exceptions appropriately with meaningful error messages
- Document complex algorithms and business rules
- **Simplicity first**: Choose the most straightforward implementation
- **Config-based testing**: Use config files to drive test scenarios, avoid hardcoded test data

## File Structure Conventions

- `dashboard/app.py`: Main Dash application entry point
- `dashboard/components/`: Reusable UI components
- `dashboard/adapters/interaction_handlers.py`: Interactive behavior handlers (not callbacks/)
- `mine_core/database/`: Neo4j connection and query logic
- `mine_core/entities/`: Business object models
- `configs/`: JSON configuration files
- `dashboard/utils/data_transformers.py`: Data transformation layer

## Common Tasks

- When adding new visualizations, create components in `dashboard/components/`
- For new data processing, extend pipelines in `mine_core/pipelines/`
- Database schema changes should update `scripts/create_schema.py`
- New configurations go in `configs/` with appropriate JSON structure
- **Before implementing**: Check if similar functionality already exists
- **Integration approach**: Ensure new features work with existing data flows
- **Config updates**: Update field mappings and schemas when adding new data types
- **Use error handling**: Apply `handle_error(logger, e, context)` for all exception handling
- **Follow URL patterns**: Use `/analysis-type` structure for dedicated analysis pages
- **Apply layout template**: Use `create_standard_layout()` template for new analysis pages

## Dynamic Adaptation Guidelines

- **Scan workspace**: Always explore current codebase structure before suggesting changes
- **Check latest configs**: Reference most recent versions of schema and mapping files
- **Extend existing**: Build upon current implementations rather than starting from scratch
- **Version awareness**: Consider that data structures and APIs may have evolved
- **Test integration**: Ensure new code works with existing pipelines and components
- **Update documentation**: Reflect changes in relevant config files and comments

## Performance Considerations

- Use efficient Cypher queries for Neo4j
- Implement pagination for large result sets
- Cache frequently accessed data
- Optimize dashboard callback performance

## Security & Data Handling

- Sanitize all user inputs
- Use parameterized database queries
- Respect data privacy for mining operational information
- Implement proper error handling without exposing sensitive details

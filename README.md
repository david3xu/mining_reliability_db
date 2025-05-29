# Mining Reliability DB

A graph-based database system for tracking and analyzing mining operation incidents, root causes, and corrective actions.

## Overview

This project implements a Neo4j graph database to model the complex relationships in mining incident data. It transforms raw reliability records into a structured data model that follows the natural workflow of incident management:

```
Facility → ActionRequest → Problem → RootCause → ActionPlan → Verification
```

## Features

- Converts 41-field raw data into a structured 12-entity model
- Tracks complete incident lifecycle from reporting to verification
- Captures relationships between incidents, causes, and resolutions
- Supports pattern analysis for recurring issues
- Maintains financial impact metrics

## Installation

1. Install Neo4j (4.4+) and Python (3.8+)
2. Clone this repository
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   Or for development:
   ```
   pip install -e .
   ```
4. Configure Neo4j connection in environment variables or settings file

## Docker Commands

```bash
# Start Neo4j
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest

# Check status
docker ps | grep neo4j

# View logs
docker logs neo4j

# Stop/Start
docker stop neo4j
docker start neo4j

# Remove (deletes data)
docker stop neo4j && docker rm neo4j
```

## Usage

1. Create database schema:

   ```
   make schema
   ```

2. Import data:

   ```
   make import
   ```

3. Run analysis queries or web interface:
   ```
   make web
   ```

## Project Structure

See [project_structure.md](project_structure.md) for detailed organization.

## Development

This project follows standard Python development practices:

- Uses `pyproject.toml` for package configuration
- Provides a Makefile for common operations
- Includes automated tests in the `tests/` directory

## Technologies

- Neo4j graph database
- Python 3.8+
- Pandas for data processing
- Matplotlib/Seaborn for visualization
- Dash (optional) for web interface

## License

[MIT License](LICENSE)

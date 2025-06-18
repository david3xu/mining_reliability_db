# Neo4j Command Line Interaction Guide

This guide provides comprehensive instructions for interacting with Neo4j using command line tools for the Mining Reliability Database project.

## Table of Contents

- [Database Connection](#database-connection)
- [Docker Management](#docker-management)
- [Cypher Shell Commands](#cypher-shell-commands)
- [Database Administration](#database-administration)
- [Data Import/Export](#data-importexport)
- [Monitoring and Debugging](#monitoring-and-debugging)
- [Project-Specific Commands](#project-specific-commands)

## Database Connection

### Authentication Credentials

```bash
# Project credentials
Username: neo4j
Password: mining123
URI: bolt://localhost:7687
Browser: http://localhost:7474
```

### Connection Methods

#### 1. Python Test Connection

```bash
cd /home/291928k/uwa/alcoa/mining_reliability_db
python test_connection.py
```

#### 2. Direct Cypher Shell Access

```bash
# Connect to Neo4j container directly
docker exec -it mining-neo4j cypher-shell -u neo4j -p mining123

# Alternative with database specification
docker exec -it mining-neo4j cypher-shell -u neo4j -p mining123 -d mining_reliability
```

#### 3. One-liner Query Execution

```bash
# Execute single query
docker exec mining-neo4j cypher-shell -u neo4j -p mining123 "MATCH (n) RETURN count(n);"

# Execute query with output formatting
docker exec mining-neo4j cypher-shell -u neo4j -p mining123 --format verbose "SHOW DATABASES;"
```

## Docker Management

### Container Operations

```bash
# Start Neo4j using docker-compose
docker compose up -d neo4j

# Start using Makefile
make docker-neo4j

# Check container status
docker ps | grep neo4j

# View container logs
docker compose logs neo4j --tail 20

# Follow logs in real-time
docker compose logs neo4j --follow

# Restart container
docker compose restart neo4j

# Stop container
docker compose stop neo4j

# Remove container and data (destructive)
make docker-clean
```

### Container Inspection

```bash
# Get container details
docker inspect mining-neo4j

# Check resource usage
docker stats mining-neo4j

# Access container shell
docker exec -it mining-neo4j bash
```

## Cypher Shell Commands

### Basic Operations

```cypher
-- Check connection
CALL db.ping();

-- Show database info
CALL dbms.components();

-- Show current database
:use system;
SHOW DATABASES;

-- Switch database
:use mining_reliability;

-- Show constraints
SHOW CONSTRAINTS;

-- Show indexes
SHOW INDEXES;
```

### Data Queries

```cypher
-- Count all nodes
MATCH (n) RETURN count(n);

-- Count all relationships
MATCH ()-[r]-() RETURN count(r);

-- Show node labels
CALL db.labels();

-- Show relationship types
CALL db.relationshipTypes();

-- Show schema
CALL db.schema.visualization();

-- Get sample nodes by label
MATCH (n:Facility) RETURN n LIMIT 5;
```

### Database Statistics

```cypher
-- Get database statistics
CALL apoc.meta.stats();

-- Get detailed schema information
CALL apoc.meta.schema();

-- Check database size
CALL apoc.monitor.store();

-- Show running queries
CALL dbms.listQueries();
```

## Database Administration

### Schema Management

```bash
# Create schema using project script
python scripts/setup/create_schema.py

# Reset database completely
make reset-all

# Reset data only (preserve schema)
make reset

# Validate database
make validate-db
```

### Constraint Operations

```cypher
-- Create unique constraint
CREATE CONSTRAINT constraint_facility_id FOR (f:Facility) REQUIRE f.facility_id IS UNIQUE;

-- Drop constraint
DROP CONSTRAINT constraint_facility_id;

-- Show all constraints
SHOW CONSTRAINTS;
```

### Index Operations

```cypher
-- Create index
CREATE INDEX index_incident_date FOR (i:Incident) ON (i.date);

-- Drop index
DROP INDEX index_incident_date;

-- Show all indexes
SHOW INDEXES;
```

## Data Import/Export

### Project Data Import

```bash
# Import all facility data
python scripts/setup/import_data.py

# Import specific facility
python scripts/setup/import_data.py --facility sample

# Import with debug logging
LOG_LEVEL=DEBUG python scripts/setup/import_data.py
```

### CSV Import via Cypher

```cypher
-- Import CSV data
LOAD CSV WITH HEADERS FROM 'file:///var/lib/neo4j/import/facilities.csv' AS row
CREATE (f:Facility {
    facility_id: row.facility_id,
    name: row.name,
    location: row.location
});

-- Import with periodic commit
:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM 'file:///import/large_dataset.csv' AS row
CREATE (n:Node {property: row.value});
```

### Data Export

```cypher
-- Export to CSV
CALL apoc.export.csv.all("/var/lib/neo4j/import/export.csv", {});

-- Export specific nodes
CALL apoc.export.csv.query(
    "MATCH (f:Facility) RETURN f.facility_id, f.name",
    "/var/lib/neo4j/import/facilities_export.csv",
    {}
);
```

## Monitoring and Debugging

### Performance Monitoring

```cypher
-- Show slow queries
CALL dbms.listQueries()
YIELD query, elapsedTimeMillis
WHERE elapsedTimeMillis > 1000
RETURN query, elapsedTimeMillis;

-- Profile query performance
PROFILE MATCH (n:Facility)-[r]->(m) RETURN count(*);

-- Explain query execution plan
EXPLAIN MATCH (n:Facility) WHERE n.name = 'Sample' RETURN n;
```

### System Information

```cypher
-- Check system configuration
CALL dbms.listConfig() YIELD name, value
WHERE name CONTAINS 'memory'
RETURN name, value;

-- Check available procedures
CALL dbms.procedures() YIELD name, signature
WHERE name CONTAINS 'apoc'
RETURN name, signature LIMIT 10;

-- Check running transactions
CALL dbms.listTransactions();
```

### Log Analysis

```bash
# View recent logs
docker exec mining-neo4j tail -f /logs/neo4j.log

# Search for errors
docker exec mining-neo4j grep "ERROR" /logs/neo4j.log

# View query logs
docker exec mining-neo4j tail -f /logs/query.log
```

## Project-Specific Commands

### Mining Reliability Database Operations

```bash
# Complete development setup
make dev-setup

# Quick start with sample data
make quick-start

# Validate configuration
make validate-config

# Analyze causal intelligence
make analyze-causes

# Check data integrity
make validate-data

# Run quality checks
make quality-check
```

### Schema Validation

```cypher
-- Check for mining-specific entities
MATCH (f:Facility) RETURN f.facility_id, f.name;
MATCH (i:Incident) RETURN i.incident_id, i.description LIMIT 5;
MATCH (e:Equipment) RETURN e.equipment_id, e.type LIMIT 5;

-- Validate relationships
MATCH (f:Facility)-[r]->(e:Equipment) RETURN type(r), count(*);
MATCH (i:Incident)-[r]->(c:RootCause) RETURN type(r), count(*);
```

### Troubleshooting Commands

```bash
# Test connection
python -c "from mine_core.database.db import get_database; db = get_database(); print('Connected successfully')"

# Check environment configuration
python -c "from configs.environment import get_all_config; import json; print(json.dumps(get_all_config(), indent=2))"

# Verify Neo4j service health
curl -I http://localhost:7474

# Check port availability
netstat -tuln | grep 7474
netstat -tuln | grep 7687
```

## Useful Aliases and Shortcuts

Add these to your `.bashrc` or `.zshrc` for quick access:

```bash
# Neo4j aliases
alias neo4j-connect="docker exec -it mining-neo4j cypher-shell -u neo4j -p mining123"
alias neo4j-logs="docker compose logs neo4j --tail 50"
alias neo4j-restart="docker compose restart neo4j"
alias neo4j-status="docker ps | grep neo4j"

# Project aliases
alias mining-reset="cd /home/291928k/uwa/alcoa/mining_reliability_db && make reset-all"
alias mining-test="cd /home/291928k/uwa/alcoa/mining_reliability_db && python test_connection.py"
alias mining-schema="cd /home/291928k/uwa/alcoa/mining_reliability_db && make schema"
```

## Common Error Solutions

### Authentication Failed

```bash
# Reset Neo4j data volume
docker compose down
docker volume rm mining_reliability_db_neo4j_data
docker compose up -d neo4j
```

### Port Already in Use

```bash
# Find and stop conflicting processes
docker ps | grep :7474
docker ps | grep :7687
docker stop <container_id>
```

### Connection Refused

```bash
# Check if Neo4j is running
docker compose ps neo4j
docker compose logs neo4j

# Restart if needed
docker compose restart neo4j
```

## Best Practices

1. **Always use transactions** for data modifications
2. **Index frequently queried properties** for performance
3. **Use EXPLAIN/PROFILE** to optimize queries
4. **Regular backups** before major changes
5. **Monitor memory usage** for large datasets
6. **Use APOC procedures** for advanced operations
7. **Batch large imports** with PERIODIC COMMIT

## References

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Cypher Query Language](https://neo4j.com/docs/cypher-manual/current/)
- [APOC Procedures](https://neo4j.com/labs/apoc/)
- [Docker Compose Neo4j](https://neo4j.com/developer/docker-run-neo4j/)

---

**Created**: June 17, 2025
**Project**: Mining Reliability Database
**Environment**: Docker Compose + Neo4j 5.13 Community

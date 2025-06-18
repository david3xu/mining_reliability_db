# Dev Container Setup & Troubleshooting Guide

## Overview

This document records the complete solution for setting up a dev container for the Mining Reliability Database project when the standard VS Code "Reopen in Container" functionality fails.

## Problem Summary

- User was unable to open the project in a dev container through VS Code's standard interface
- VS Code dev container commands were failing
- Needed to set up the development environment manually using command line tools

## Environment Details

- **OS**: Linux (Ubuntu-based)
- **Docker**: Version 28.0.1
- **Docker Compose**: V2.33.1
- **VS Code Extension**: Dev Containers (ms-azuretools.vscode-containers)
- **Project**: Mining Reliability Database with Python 3.12, Neo4j, and Dash

## Root Cause Analysis

1. **Dev Container Configuration Issues**:

   - Original devcontainer.json used Python 3.11 instead of 3.12
   - Outdated Python linting settings causing conflicts
   - Used deprecated `docker-compose` instead of `docker compose` command

2. **VS Code Command Issues**:
   - Standard VS Code dev container commands were not responding
   - Required manual CLI-based approach

## Complete Solution

### Step 1: Fix Dev Container Configuration

**File: `.devcontainer/devcontainer.json`**

**Issues Fixed:**

```json
// BEFORE (problematic)
{
    "image": "mcr.microsoft.com/devcontainers/python:3.11",
    "postCreateCommand": "pip install -e .[dev] && docker-compose up -d neo4j",
    "settings": {
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.linting.flake8Enabled": true,
        "python.formatting.provider": "black"
    }
}

// AFTER (fixed)
{
    "image": "mcr.microsoft.com/devcontainers/python:3.12",
    "postCreateCommand": "pip install -e .[dev] && docker compose up -d neo4j",
    "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.testing.pytestEnabled": true,
        "python.testing.pytestArgs": ["tests"]
    }
}
```

### Step 2: Install Dev Containers CLI

```bash
npm install -g @devcontainers/cli
```

### Step 3: Build Dev Container Manually

```bash
# Build the container with detailed logging
devcontainer build --workspace-folder . --log-level trace

# Start the container
devcontainer up --workspace-folder .
```

### Step 4: Set Up Supporting Services

```bash
# Stop any conflicting Neo4j instances
docker stop neo4j && docker rm neo4j

# Remove old data to reset passwords
docker compose down && docker volume rm mining_reliability_db_neo4j_data

# Start fresh Neo4j instance
docker compose up -d neo4j
```

### Step 5: Fix Environment Configuration

**File: `.env`**

```env
# Update Neo4j password to match docker-compose.yml
NEO4J_PASSWORD=mining123  # Changed from 'password'
```

### Step 6: Create Connection Helper Script

**File: `connect_devcontainer.sh`**

```bash
#!/bin/bash
echo "🔍 Dev Container Setup Instructions"
echo "=================================="
echo "Option 1: Using VS Code Command Palette"
echo "1. Press Ctrl+Shift+P"
echo "2. Type 'Dev Containers: Attach to Running Container'"
echo "3. Select the container: vsc-mining_reliability_db-..."
```

## Connection Methods

### Method 1: VS Code Command Palette (Recommended)

1. Press `Ctrl+Shift+P` (Linux/Windows) or `Cmd+Shift+P` (Mac)
2. Type: `Dev Containers: Attach to Running Container`
3. Select container starting with: `vsc-mining_reliability_db-`

### Method 2: VS Code Remote Explorer

1. Open Remote Explorer sidebar in VS Code
2. Navigate to "Dev Containers" section
3. Find running container and click "Attach in New Window"

### Method 3: Manual Container Access

```bash
# Find container ID
docker ps | grep mining_reliability_db

# Access container directly
docker exec -it <container_id> /bin/bash
```

## Verification Steps

### Test Connection Script

**File: `test_connection.py`**

```python
#!/usr/bin/env python3
"""Test script to verify Neo4j connection and dashboard dependencies"""

from dotenv import load_dotenv
from neo4j import GraphDatabase
import os

def test_neo4j_connection():
    load_dotenv()
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'mining123')

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j!' AS message")
            record = result.single()
            print(f"✅ Connection successful: {record['message']}")
        driver.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_dashboard_imports():
    try:
        import dash, plotly, pandas
        print("✅ All dashboard dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Mining Reliability Database Setup")
    deps_ok = test_dashboard_imports()
    neo4j_ok = test_neo4j_connection()

    if deps_ok and neo4j_ok:
        print("🎉 All tests passed! Your environment is ready.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
```

### Run Tests

```bash
# Inside dev container
cd /workspaces/mining_reliability_db
python test_connection.py
```

## Service URLs

| Service       | URL                   | Credentials     |
| ------------- | --------------------- | --------------- |
| Neo4j Browser | http://localhost:7474 | neo4j/mining123 |
| Dashboard     | http://localhost:8050 | N/A             |
| Neo4j Bolt    | bolt://localhost:7687 | neo4j/mining123 |

## Common Issues & Solutions

### Issue 1: Port Conflicts

**Symptom**: `port is already allocated` error
**Solution**:

```bash
docker stop $(docker ps -q --filter "publish=7474")
docker stop $(docker ps -q --filter "publish=7687")
```

### Issue 2: Authentication Failures

**Symptom**: Neo4j authentication errors
**Solution**: Reset Neo4j data volume

```bash
docker compose down
docker volume rm mining_reliability_db_neo4j_data
docker compose up -d neo4j
```

### Issue 3: Python Import Errors

**Symptom**: Cannot import dashboard dependencies
**Solution**: Reinstall in dev container

```bash
pip install -e .[dev]
pip install dash plotly pandas neo4j
```

### Issue 4: VS Code Commands Not Working

**Symptom**: Dev container commands fail in VS Code
**Solution**: Use CLI approach

```bash
devcontainer up --workspace-folder .
# Then use "Attach to Running Container" in VS Code
```

## File Structure

```
.devcontainer/
├── devcontainer.json          # Fixed configuration
.vscode/
├── settings.json             # VS Code workspace settings
├── .env                      # Environment variables (fixed passwords)
├── docker-compose.yml        # Service definitions
├── test_connection.py        # Verification script
├── connect_devcontainer.sh   # Helper script
└── start_dashboard.py        # Dashboard startup script
```

## Environment Variables

```env
# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=mining123
NEO4J_DATABASE=mining_reliability

# Dashboard Configuration
DASHBOARD_HOST=127.0.0.1
DASHBOARD_PORT=8050
DASHBOARD_DEBUG=True
```

## Dependencies Installed

- **Core**: Python 3.12, pip, setuptools
- **Dashboard**: dash==2.14.1, plotly==5.17.0, pandas==2.1.3
- **Database**: neo4j (latest compatible version)
- **Development**: pytest, black, flake8, mypy
- **VS Code Extensions**: Python, Pylint, Black Formatter, Jupyter

## Success Indicators

✅ Dev container builds without errors
✅ Container starts and remains running
✅ Neo4j database accessible on ports 7474/7687
✅ Python dependencies import successfully
✅ VS Code can attach to running container
✅ Test connection script passes all checks

## Alternative Approach

If dev container still fails, the project can be run locally using:

1. Python virtual environment (`.venv`)
2. Docker Compose for Neo4j only
3. Manual dependency installation

This approach was successfully implemented as a fallback solution.

---

**Document Created**: June 17, 2025
**Last Updated**: June 17, 2025
**Status**: Verified Working Solution

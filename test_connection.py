#!/usr/bin/env python3
"""
Test script to verify Neo4j connection and basic dashboard functionality
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from neo4j import GraphDatabase

def test_neo4j_connection():
    """Test connection to Neo4j database"""
    load_dotenv()

    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'mining123')

    print(f"Testing connection to {uri}")
    print(f"User: {user}")

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))

        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j!' AS message")
            record = result.single()
            print(f"✅ Connection successful: {record['message']}")

            # Test database info
            result = session.run("CALL dbms.components() YIELD name, versions, edition")
            for record in result:
                print(f"Database: {record['name']} {record['versions'][0]} ({record['edition']})")

        driver.close()
        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_dashboard_imports():
    """Test if dashboard modules can be imported"""
    try:
        import dash
        import dash_bootstrap_components as dbc
        import plotly
        import pandas
        print("✅ All dashboard dependencies imported successfully")
        print(f"- Dash: {dash.__version__}")
        print(f"- Dash Bootstrap Components: {dbc.__version__}")
        print(f"- Plotly: {plotly.__version__}")
        print(f"- Pandas: {pandas.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Mining Reliability Database Setup")
    print("=" * 50)

    print("\n1. Testing Python dependencies...")
    deps_ok = test_dashboard_imports()

    print("\n2. Testing Neo4j connection...")
    neo4j_ok = test_neo4j_connection()

    print("\n" + "=" * 50)
    if deps_ok and neo4j_ok:
        print("🎉 All tests passed! Your environment is ready.")
        print("\nNext steps:")
        print("- Access Neo4j Browser at: http://localhost:7474")
        print("- Run the dashboard with: python dashboard/app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

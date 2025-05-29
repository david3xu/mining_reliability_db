#!/usr/bin/env python3
"""
Debug Neo4j Database Contents
Investigate what's actually stored in the database.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mine_core.database.db import Database
from configs.environment import get_db_config

def debug_database():
    """Debug database contents in detail"""

    config = get_db_config()
    db = Database(
        uri=config['uri'],
        user=config['user'],
        password=config['password']
    )

    print("=== Neo4j Database Debug Analysis ===\n")

    try:
        # Look at all nodes with all their properties
        print("1. All Nodes with Properties...")
        all_nodes = db.execute_query("""
            MATCH (n)
            RETURN labels(n) as labels, properties(n) as props
            ORDER BY labels(n)[0]
        """)

        for i, node in enumerate(all_nodes):
            print(f"   Node {i+1}: {node['labels']} -> {node['props']}")
            if i > 20:  # Limit output
                print(f"   ... and {len(all_nodes) - i - 1} more nodes")
                break

        print()

        # Look at ActionRequest nodes specifically
        print("2. ActionRequest Nodes Detail...")
        ar_nodes = db.execute_query("""
            MATCH (ar:ActionRequest)
            RETURN properties(ar) as props
        """)

        for i, ar in enumerate(ar_nodes):
            print(f"   ActionRequest {i+1}: {ar['props']}")

        print()

        # Look at relationships
        print("3. Relationship Details...")
        relationships = db.execute_query("""
            MATCH (a)-[r]->(b)
            RETURN labels(a)[0] as from_type, type(r) as rel_type, labels(b)[0] as to_type,
                   properties(a) as from_props, properties(b) as to_props
        """)

        for i, rel in enumerate(relationships):
            print(f"   Relationship {i+1}:")
            print(f"     {rel['from_type']} -> {rel['rel_type']} -> {rel['to_type']}")
            print(f"     From: {rel['from_props']}")
            print(f"     To: {rel['to_props']}")
            print()

        # Check for constraint violations or issues
        print("4. Schema Constraints...")
        constraints = db.execute_query("CALL db.constraints() YIELD description RETURN description")
        for constraint in constraints:
            print(f"   - {constraint['description']}")

        print()

        # Look for any nodes that actually have proper IDs
        print("5. Nodes with Valid Data...")
        valid_nodes = db.execute_query("""
            MATCH (n)
            WHERE EXISTS(n.action_request_number) OR EXISTS(n.problem_id) OR EXISTS(n.asset_numbers)
            RETURN labels(n)[0] as type, properties(n) as props
        """)

        if valid_nodes:
            print(f"   Found {len(valid_nodes)} nodes with actual data:")
            for node in valid_nodes:
                print(f"   - {node['type']}: {node['props']}")
        else:
            print("   No nodes found with actual data properties")

        print()

    except Exception as e:
        print(f"Error during debug: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    debug_database()

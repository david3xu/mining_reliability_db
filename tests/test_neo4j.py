#!/usr/bin/env python3
"""
Quick Neo4j connection test and data exploration
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mine_core.database.db import get_database

def test_connection():
    """Test Neo4j connection and explore data"""
    print("Testing Neo4j connection...")

    try:
        db = get_database()

        # Test connection
        print("✅ Neo4j connection successful!")

        # Get all node labels
        print("\n📊 Node types in database:")
        result = db.execute_query("CALL db.labels()")
        for record in result:
            print(f"  - {record['label']}")

        # Count all nodes
        print("\n🔢 Total node count:")
        result = db.execute_query("MATCH (n) RETURN count(n) as total")
        for record in result:
            print(f"  Total nodes: {record['total']}")

        # Count nodes by type
        print("\n📈 Nodes by type:")
        labels_result = db.execute_query("CALL db.labels()")
        for label_record in labels_result:
            label = label_record['label']
            count_result = db.execute_query(f"MATCH (n:{label}) RETURN count(n) as count")
            for count_record in count_result:
                print(f"  {label}: {count_record['count']}")

        # Show relationship types
        print("\n🔗 Relationship types:")
        result = db.execute_query("CALL db.relationshipTypes()")
        for record in result:
            print(f"  - {record['relationshipType']}")

        # Show sample facility data
        print("\n🏭 Sample facility data:")
        result = db.execute_query("""
            MATCH (f:Facility)
            RETURN f.facility_id, f.facility_name
            LIMIT 5
        """)
        for record in result:
            print(f"  Facility: {record['f.facility_id']} - {record.get('f.facility_name', 'N/A')}")

        # Show sample workflow chain
        print("\n⛓️ Sample workflow chain:")
        result = db.execute_query("""
            MATCH (f:Facility)<-[:BELONGS_TO]-(ar:ActionRequest)
                  <-[:IDENTIFIED_IN]-(p:Problem)
                  <-[:ANALYZES]-(rc:RootCause)
                  <-[:RESOLVES]-(ap:ActionPlan)
            RETURN f.facility_id, ar.action_request_number,
                   p.what_happened, rc.root_cause, ap.action_plan
            LIMIT 3
        """)
        for record in result:
            print(f"  🏭 {record['f.facility_id']} → AR: {record['ar.action_request_number']}")
            print(f"    Problem: {record['p.what_happened'][:50]}...")
            print(f"    Root Cause: {record['rc.root_cause'][:50]}...")
            print(f"    Action Plan: {record['ap.action_plan'][:50]}...")
            print()

        db.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()

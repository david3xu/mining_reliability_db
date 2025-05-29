#!/usr/bin/env python3
"""
Fix Neo4j Database Issues
1. Add missing base 'id' field to all data nodes
2. Delete schema template nodes
3. Recreate relationships between actual data nodes
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mine_core.database.db import Database
from configs.environment import get_db_config

def fix_database():
    """Fix the database issues"""

    print("Starting database fix...")

    try:
        config = get_db_config()
        db = Database(
            uri=config['uri'],
            user=config['user'],
            password=config['password']
        )
        print("✓ Connected to database")
    except Exception as e:
        print(f"✗ Error connecting: {e}")
        return

    print("=== Neo4j Database Fix ===\n")

    try:
        # Step 1: Add missing base 'id' field to all data nodes
        print("1. Adding missing 'id' field to data nodes...")

        entity_mappings = {
            'ActionRequest': 'actionrequest_id',
            'Problem': 'problem_id',
            'RootCause': 'rootcause_id',
            'ActionPlan': 'actionplan_id',
            'Verification': 'verification_id',
            'Department': 'department_id',
            'Asset': 'asset_id',
            'RecurringStatus': 'recurringstatus_id',
            'AmountOfLoss': 'amountofloss_id',
            'Review': 'review_id',
            'EquipmentStrategy': 'equipmentstrategy_id',
            'Facility': 'facility_id'
        }

        for entity_type, id_field in entity_mappings.items():
            # Update nodes that have the specific ID field but missing base 'id'
            query = f"""
            MATCH (n:{entity_type})
            WHERE n.{id_field} IS NOT NULL AND (n.id IS NULL OR n.id = "")
            SET n.id = n.{id_field}
            RETURN count(n) as updated
            """

            result = db.execute_query(query)
            count = result[0]['updated'] if result else 0
            if count > 0:
                print(f"   ✓ Updated {count} {entity_type} nodes with base 'id' field")

        print()

        # Step 2: Delete schema template nodes
        print("2. Removing schema template nodes...")

        # First delete relationships involving template nodes
        template_rels = db.execute_query("""
            MATCH (a:_SchemaTemplate)-[r]-(b)
            DELETE r
            RETURN count(r) as deleted_rels
        """)

        rel_count = template_rels[0]['deleted_rels'] if template_rels else 0
        if rel_count > 0:
            print(f"   ✓ Deleted {rel_count} relationships involving template nodes")

        # Then delete template nodes
        template_nodes = db.execute_query("""
            MATCH (n:_SchemaTemplate)
            DELETE n
            RETURN count(n) as deleted_nodes
        """)

        node_count = template_nodes[0]['deleted_nodes'] if template_nodes else 0
        if node_count > 0:
            print(f"   ✓ Deleted {node_count} schema template nodes")

        print()

        # Step 3: Create relationships between actual data nodes
        print("3. Creating relationships between actual data nodes...")

        relationships = [
            # Main workflow chain - CORRECTED DIRECTIONS
            ('ActionRequest', 'facility_id', 'BELONGS_TO', 'Facility', 'facility_id'),
            ('Problem', 'actionrequest_id', 'IDENTIFIED_IN', 'ActionRequest', 'actionrequest_id'),
            ('RootCause', 'problem_id', 'ANALYZES', 'Problem', 'problem_id'),
            ('ActionPlan', 'rootcause_id', 'RESOLVES', 'RootCause', 'rootcause_id'),
            ('Verification', 'actionplan_id', 'VALIDATES', 'ActionPlan', 'actionplan_id'),

            # Support entity relationships - CORRECTED DIRECTIONS
            ('Asset', 'problem_id', 'INVOLVED_IN', 'Problem', 'problem_id'),
            ('AmountOfLoss', 'problem_id', 'QUANTIFIES', 'Problem', 'problem_id'),
            ('RecurringStatus', 'problem_id', 'CLASSIFIES', 'Problem', 'problem_id'),
            ('Department', 'actionrequest_id', 'ASSIGNED_TO', 'ActionRequest', 'actionrequest_id'),
            ('Review', 'actionplan_id', 'EVALUATES', 'ActionPlan', 'actionplan_id'),
            ('EquipmentStrategy', 'actionplan_id', 'MODIFIES', 'ActionPlan', 'actionplan_id')
        ]

        for from_type, from_field, rel_type, to_type, to_field in relationships:
            query = f"""
            MATCH (from:{from_type}), (to:{to_type})
            WHERE from.{from_field} IS NOT NULL AND to.{to_field} IS NOT NULL
                  AND from.{from_field} = to.{to_field}
                  AND NOT (from)-[:{rel_type}]->(to)
            CREATE (from)-[:{rel_type}]->(to)
            RETURN count(*) as created
            """

            result = db.execute_query(query)
            count = result[0]['created'] if result else 0
            if count > 0:
                print(f"   ✓ Created {count} {from_type}-[{rel_type}]->{to_type} relationships")

        print()

        # Step 4: Verify the fixes
        print("4. Verification...")

        # Check nodes with missing IDs
        missing_ids = db.execute_query("""
            MATCH (n)
            WHERE n.id IS NULL OR n.id = ""
            RETURN labels(n)[0] as type, count(n) as count
            ORDER BY type
        """)

        if missing_ids:
            print("   Nodes still missing 'id' field:")
            for record in missing_ids:
                print(f"   - {record['type']}: {record['count']}")
        else:
            print("   ✓ All nodes now have valid 'id' field")

        # Check relationships
        rel_stats = db.execute_query("""
            MATCH ()-[r]->()
            RETURN type(r) as rel_type, count(r) as count
            ORDER BY count DESC
        """)

        print("   Relationship counts after fix:")
        for rel in rel_stats:
            print(f"   - {rel['rel_type']}: {rel['count']}")

        # Test a sample workflow chain
        workflow_test = db.execute_query("""
            MATCH (f:Facility)-[:BELONGS_TO]->(ar:ActionRequest)-[:IDENTIFIED_IN]->(p:Problem)
                  -[:ANALYZES]->(rc:RootCause)-[:RESOLVES]->(ap:ActionPlan)
            RETURN f.facility_name, ar.action_request_number, p.what_happened,
                   rc.root_cause, ap.action_plan
            LIMIT 1
        """)

        if workflow_test:
            print(f"   ✓ Workflow chain test successful: {len(workflow_test)} complete chains found")
        else:
            print("   ⚠️  Workflow chain test failed - no complete chains found")

        print()
        print("=== Database Fix Complete ===")

    except Exception as e:
        print(f"Error during fix: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    fix_database()

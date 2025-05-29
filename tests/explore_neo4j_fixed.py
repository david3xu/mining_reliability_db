#!/usr/bin/env python3
"""
Enhanced Neo4j Database Explorer with Fixed Queries
Corrects property names and investigates data quality issues.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print(f"Project root: {project_root}")
print(f"Python path: {sys.path[:3]}")

try:
    from mine_core.database.db import Database
    print("Successfully imported Database")
except ImportError as e:
    print(f"Error importing Database: {e}")

try:
    from configs.environment import get_db_config
    print("Successfully imported get_db_config")
except ImportError as e:
    print(f"Error importing get_db_config: {e}")
    sys.exit(1)

def explore_database():
    """Explore the Neo4j database with corrected queries"""

    print("Starting exploration script...")

    # Get database configuration
    try:
        config = get_db_config()
        print(f"Database config: {config['uri']}")
    except Exception as e:
        print(f"Error getting config: {e}")
        return

    # Initialize database connection
    try:
        db = Database(
            uri=config['uri'],
            user=config['user'],
            password=config['password']
        )
        print("Database connection initialized")
    except Exception as e:
        print(f"Error initializing database: {e}")
        return

    print("=== Mining Reliability Database Exploration (Fixed) ===\n")

    try:
        # Test connection
        print("1. Testing Database Connection...")
        result = db.execute_query("RETURN 1 as test")
        print(f"   ✓ Connection successful: {result}")
        print()

        # Get database overview
        print("2. Database Overview...")
        stats = db.execute_query("""
            MATCH (n)
            RETURN labels(n)[0] as NodeType, count(n) as Count
            ORDER BY Count DESC
        """)
        print("   Node counts by type:")
        for record in stats:
            print(f"   - {record['NodeType']}: {record['Count']}")
        print()

        # Get relationship overview
        print("3. Relationship Overview...")
        rels = db.execute_query("""
            MATCH ()-[r]->()
            RETURN type(r) as RelType, count(r) as Count
            ORDER BY Count DESC
        """)
        print("   Relationship counts by type:")
        for record in rels:
            print(f"   - {record['RelType']}: {record['Count']}")
        print()

        # Check for missing IDs - detailed analysis
        print("4. Data Quality Check - Missing ID Fields...")
        entity_types = ['ActionRequest', 'Problem', 'RootCause', 'ActionPlan',
                       'Verification', 'Department', 'Asset', 'RecurringStatus',
                       'AmountOfLoss', 'Review', 'EquipmentStrategy', 'Facility']

        for entity_type in entity_types:
            # Check for nodes with missing ID fields
            missing_ids = db.execute_query(f"""
                MATCH (n:{entity_type})
                WHERE n.id IS NULL OR n.id = ""
                RETURN count(n) as missing_count
            """)

            if missing_ids and missing_ids[0]['missing_count'] > 0:
                print(f"   ⚠️  {entity_type}: {missing_ids[0]['missing_count']} nodes with missing base 'id' field")

                # Get example of problematic nodes
                examples = db.execute_query(f"""
                    MATCH (n:{entity_type})
                    WHERE n.id IS NULL OR n.id = ""
                    RETURN properties(n) as props
                    LIMIT 1
                """)
                if examples:
                    print(f"       Example properties: {examples[0]['props']}")
            else:
                print(f"   ✓ {entity_type}: All nodes have valid 'id' field")

        print()

        # Test Problem->RootCause chain
        print("5. Testing Problem-RootCause Relationships...")
        problem_chains = db.execute_query("""
            MATCH (p:Problem)-[r:ANALYZES]->(rc:RootCause)
            RETURN p.problem_id as problem_id, rc.cause_id as cause_id, rc.root_cause as root_cause
            ORDER BY p.problem_id
        """)

        if problem_chains:
            print(f"   ✓ Found {len(problem_chains)} Problem->RootCause relationships:")
            for chain in problem_chains:
                print(f"   - Problem {chain['problem_id']} -> RootCause {chain['cause_id']}: {chain['root_cause']}")
        else:
            print("   ⚠️  No Problem->RootCause relationships found")

            # Debug: Check what relationships exist from Problems
            problem_debug = db.execute_query("""
                MATCH (p:Problem)-[r]->(n)
                RETURN p.problem_id, type(r) as rel_type, labels(n)[0] as target_type, count(*) as count
            """)
            print("   Debug - Relationships from Problems:")
            for debug in problem_debug:
                print(f"   - Problem {debug['p.problem_id']} -> {debug['rel_type']} -> {debug['target_type']}: {debug['count']}")

        print()

        # Test Asset data with correct field names
        print("6. Testing Asset Data (Corrected Field Names)...")
        assets = db.execute_query("""
            MATCH (a:Asset)
            RETURN a.asset_id, a.asset_numbers, a.asset_activity_numbers, a.problem_id
            ORDER BY a.asset_id
        """)

        if assets:
            print(f"   ✓ Found {len(assets)} Asset records:")
            for asset in assets:
                print(f"   - Asset {asset['a.asset_id']}: Numbers={asset['a.asset_numbers']}, Activity={asset['a.asset_activity_numbers']}, Problem={asset['a.problem_id']}")
        else:
            print("   ⚠️  No Asset records found")

        print()

        # Test ActionRequest analysis
        print("7. Testing ActionRequest Analysis...")
        action_requests = db.execute_query("""
            MATCH (ar:ActionRequest)
            RETURN ar.action_request_id, ar.action_request_number, ar.title, ar.stage
            ORDER BY ar.action_request_id
        """)

        if action_requests:
            print(f"   ✓ Found {len(action_requests)} ActionRequest records:")
            for ar in action_requests:
                print(f"   - {ar['ar.action_request_id']}: {ar['ar.action_request_number']} - {ar['ar.title']} ({ar['ar.stage']})")
        else:
            print("   ⚠️  No ActionRequest records found")

        print()

        # Test complete workflow chain
        print("8. Testing Complete Workflow Chain...")
        workflow = db.execute_query("""
            MATCH (f:Facility)-[:BELONGS_TO]->(ar:ActionRequest)-[:IDENTIFIED_IN]->(p:Problem)
                  -[:ANALYZES]->(rc:RootCause)-[:RESOLVES]->(ap:ActionPlan)
            RETURN f.facility_name, ar.action_request_number, p.what_happened,
                   rc.root_cause, ap.action_plan
            LIMIT 5
        """)

        if workflow:
            print(f"   ✓ Found {len(workflow)} complete workflow chains:")
            for w in workflow:
                print(f"   - Facility: {w['f.facility_name']}")
                print(f"     Request: {w['ar.action_request_number']}")
                print(f"     Problem: {w['p.what_happened'][:50]}...")
                print(f"     Root Cause: {w['rc.root_cause']}")
                print(f"     Action Plan: {w['ap.action_plan'][:50]}...")
                print()
        else:
            print("   ⚠️  No complete workflow chains found")

            # Debug each step
            print("   Debug - Step by step analysis:")
            steps = [
                ("Facility->ActionRequest", "MATCH (f:Facility)-[:BELONGS_TO]->(ar:ActionRequest) RETURN count(*) as count"),
                ("ActionRequest->Problem", "MATCH (ar:ActionRequest)-[:IDENTIFIED_IN]->(p:Problem) RETURN count(*) as count"),
                ("Problem->RootCause", "MATCH (p:Problem)-[:ANALYZES]->(rc:RootCause) RETURN count(*) as count"),
                ("RootCause->ActionPlan", "MATCH (rc:RootCause)-[:RESOLVES]->(ap:ActionPlan) RETURN count(*) as count")
            ]

            for step_name, query in steps:
                result = db.execute_query(query)
                count = result[0]['count'] if result else 0
                print(f"   - {step_name}: {count} relationships")

        print()

        # Check for orphaned nodes
        print("9. Orphaned Node Analysis...")
        orphan_queries = [
            ("ActionRequest without Facility", "MATCH (ar:ActionRequest) WHERE NOT ()-[:BELONGS_TO]->(ar) RETURN count(ar) as count"),
            ("Problem without ActionRequest", "MATCH (p:Problem) WHERE NOT ()-[:IDENTIFIED_IN]->(p) RETURN count(p) as count"),
            ("RootCause without Problem", "MATCH (rc:RootCause) WHERE NOT ()-[:ANALYZES]->(rc) RETURN count(rc) as count"),
            ("ActionPlan without RootCause", "MATCH (ap:ActionPlan) WHERE NOT ()-[:RESOLVES]->(ap) RETURN count(ap) as count")
        ]

        for check_name, query in orphan_queries:
            result = db.execute_query(query)
            count = result[0]['count'] if result else 0
            if count > 0:
                print(f"   ⚠️  {check_name}: {count} orphaned nodes")
            else:
                print(f"   ✓ {check_name}: No orphaned nodes")

        print()
        print("=== Exploration Complete ===")

    except Exception as e:
        print(f"Error during exploration: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    explore_database()

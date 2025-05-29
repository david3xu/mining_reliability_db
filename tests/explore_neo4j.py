#!/usr/bin/env python3
"""
Enhanced Neo4j data exploration script
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mine_core.database.db import get_database

def explore_database():
    """Comprehensive database exploration"""
    print("🔍 Exploring Neo4j Mining Reliability Database...")

    try:
        db = get_database()
        print("✅ Connected successfully!")

        # 1. Basic statistics
        print("\n📊 DATABASE OVERVIEW")
        print("=" * 40)

        # Node counts
        result = db.execute_query("MATCH (n) RETURN count(n) as total")
        total_nodes = list(result)[0]['total']
        print(f"Total nodes: {total_nodes:,}")

        # Relationship counts
        result = db.execute_query("MATCH ()-[r]->() RETURN count(r) as total")
        total_rels = list(result)[0]['total']
        print(f"Total relationships: {total_rels:,}")        # 2. Node type distribution
        print("\n📈 NODE TYPE DISTRIBUTION")
        print("=" * 40)

        # Get all labels and count nodes for each
        labels_result = db.execute_query("CALL db.labels()")
        records = []
        for label_record in labels_result:
            label = label_record['label']
            count_result = db.execute_query(f"MATCH (n:`{label}`) RETURN count(n) as count")
            count = list(count_result)[0]['count']
            records.append({'label': label, 'count': count})
        records.sort(key=lambda x: x['count'], reverse=True)

        for record in records:
            print(f"  {record['label']:<20} {record['count']:>6,}")

        # 3. Relationship patterns
        print("\n🔗 RELATIONSHIP PATTERNS")
        print("=" * 40)
        result = db.execute_query("""
            MATCH (a)-[r]->(b)
            RETURN labels(a)[0] as from_type, type(r) as rel_type,
                   labels(b)[0] as to_type, count(*) as count
            ORDER BY count DESC
            LIMIT 15
        """)

        for record in result:
            from_type = record['from_type'] or 'Unknown'
            to_type = record['to_type'] or 'Unknown'
            print(f"  {from_type} --{record['rel_type']}--> {to_type} ({record['count']:,})")

        # 4. Sample facility data
        print("\n🏭 FACILITY OVERVIEW")
        print("=" * 40)
        result = db.execute_query("""
            MATCH (f:Facility)
            WHERE f.facility_id IS NOT NULL
            RETURN f.facility_id, f.facility_name
            LIMIT 10
        """)

        facilities = list(result)
        if facilities:
            for record in facilities:
                name = record.get('f.facility_name', 'Unnamed')
                print(f"  📍 {record['f.facility_id']}: {name}")
        else:
            print("  No facilities with valid IDs found")

        # 5. Action Request analysis
        print("\n📋 ACTION REQUEST ANALYSIS")
        print("=" * 40)
        result = db.execute_query("""
            MATCH (ar:ActionRequest)
            WHERE ar.action_request_id IS NOT NULL
            OPTIONAL MATCH (ar)-[:HAS_ACTION_PLAN]->(ap:ActionPlan)
            RETURN ar.action_request_id, ar.action_request_number,
                   count(ap) as action_plans
            ORDER BY ar.action_request_id
            LIMIT 5
        """)

        for record in result:
            ar_num = record.get('ar.action_request_number', 'N/A')
            plans = record['action_plans']
            print(f"  📝 AR-{record['ar.action_request_id']} (#{ar_num}): {plans} action plan(s)")

        # 6. Problem-RootCause chains
        print("\n🔍 PROBLEM ANALYSIS CHAINS")
        print("=" * 40)
        result = db.execute_query("""
            MATCH (p:Problem)<-[:ANALYZES]-(rc:RootCause)
            WHERE p.problem_id IS NOT NULL AND rc.rootcause_id IS NOT NULL
            RETURN p.problem_id,
                   substring(coalesce(p.what_happened, 'Unknown problem'), 0, 50) as problem_desc,
                   rc.rootcause_id,
                   substring(coalesce(rc.root_cause, 'Unknown cause'), 0, 50) as cause_desc
            LIMIT 5
        """)

        chains = list(result)
        if chains:
            for record in chains:
                print(f"  🚨 Problem {record['p.problem_id']}: {record['problem_desc']}...")
                print(f"     → Root Cause {record['rc.rootcause_id']}: {record['cause_desc']}...")
                print()
        else:
            print("  No problem-rootcause chains found")

        # 7. Asset relationships
        print("\n⚙️ ASSET MANAGEMENT")
        print("=" * 40)
        result = db.execute_query("""
            MATCH (a:Asset)-[r]->(target)
            WHERE a.asset_id IS NOT NULL
            RETURN a.asset_id,
                   substring(coalesce(a.asset_numbers, 'Unknown asset'), 0, 30) as asset_numbers,
                   type(r) as relationship,
                   labels(target)[0] as target_type,
                   count(*) as count
            ORDER BY count DESC
            LIMIT 10
        """)

        for record in result:
            asset_numbers = record['asset_numbers']
            print(f"  🔧 Asset {record['a.asset_id']} ({asset_numbers}) --{record['relationship']}--> {record['target_type']} ({record['count']})")

        # 8. Data quality check
        print("\n✅ DATA QUALITY CHECK")
        print("=" * 40)

        # Check for nodes with missing IDs
        result = db.execute_query("""
            CALL db.labels() YIELD label
            RETURN label
        """)

        for label_record in result:
            label = label_record['label']
            if label == '_SchemaTemplate':
                continue

            # Check for null IDs
            id_field = f"{label.lower()}_id"
            null_count_result = db.execute_query(f"""
                MATCH (n:`{label}`)
                WHERE n.`{id_field}` IS NULL OR n.`{id_field}` = ''
                RETURN count(n) as null_count
            """)
            null_count = list(null_count_result)[0]['null_count']

            if null_count > 0:
                print(f"  ⚠️  {label}: {null_count} nodes with missing {id_field}")

        db.close()
        print("\n🎉 Database exploration complete!")

    except Exception as e:
        print(f"❌ Error during exploration: {e}")
        import traceback
        traceback.print_exc()

def interactive_query():
    """Allow custom Cypher queries"""
    print("\n🔧 INTERACTIVE QUERY MODE")
    print("=" * 40)
    print("Enter Cypher queries (type 'exit' to quit):")

    db = get_database()

    while True:
        try:
            query = input("\nCypher> ").strip()
            if query.lower() in ['exit', 'quit', 'q']:
                break

            if not query:
                continue

            result = db.execute_query(query)
            records = list(result)

            if records:
                print(f"\n📊 Results ({len(records)} records):")
                for i, record in enumerate(records[:10]):  # Limit to first 10
                    print(f"  {i+1}. {dict(record)}")
                if len(records) > 10:
                    print(f"  ... ({len(records) - 10} more records)")
            else:
                print("✅ Query executed successfully (no results)")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

    db.close()
    print("👋 Goodbye!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_query()
    else:
        explore_database()
        print("\n💡 Tip: Run with --interactive flag for custom queries!")

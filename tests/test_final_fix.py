#!/usr/bin/env python3
"""
Test the final fix for null records in grouping
"""
import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.database.db import get_database

def test_final_fix():
    print("Testing final null filtering fix...")

    db = get_database()

    # Load and test the actual query file content
    with open('/home/291928k/uwa/alcoa/mining_reliability_db/configs/queries/potential_root_causes.cypher', 'r') as f:
        query_template = f.read()

    # Replace the filter clause placeholder
    query = query_template.replace('{filter_clause}', "toLower(p.what_happened) CONTAINS toLower('contamination')")

    results = db.execute_query(query)

    print(f"Total results: {len(results)}")

    # Check for null records
    null_records = []
    for i, record in enumerate(results):
        if (record.get('incident_id') is None or
            record.get('facility') is None or
            record.get('problem_description') is None or
            record.get('proven_solution') is None):
            null_records.append(i)

    if len(null_records) == 0:
        print("✅ SUCCESS: No null records found!")
    else:
        print(f"❌ FAIL: Found {len(null_records)} null records at positions: {null_records}")

    # Show sample results
    print("\nSample results:")
    for i, record in enumerate(results[:3]):
        print(f"Record {i+1}:")
        print(f"  incident_id: {record.get('incident_id')}")
        print(f"  facility: {record.get('facility', 'N/A')[:30]}...")
        print(f"  problem_description: {record.get('problem_description', 'N/A')[:60]}...")
        print(f"  proven_solution: {record.get('proven_solution', 'N/A')[:60]}...")
        print(f"  frequency: {record.get('frequency')}")
        print()

if __name__ == "__main__":
    test_final_fix()

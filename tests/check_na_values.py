#!/usr/bin/env python3
"""
Detailed test to show full data values without truncation
"""
import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.database.db import get_database

def test_full_data_display():
    print("Testing to show FULL data values (no truncation)...")

    db = get_database()

    # Load and test the actual query file content
    with open('/home/291928k/uwa/alcoa/mining_reliability_db/configs/queries/potential_root_causes.cypher', 'r') as f:
        query_template = f.read()

    # Replace the filter clause placeholder
    query = query_template.replace('{filter_clause}', "toLower(p.what_happened) CONTAINS toLower('contamination')")

    results = db.execute_query(query)

    print(f"Total results: {len(results)}")

    # Check for actual N/A or null values in the data
    na_count = 0
    null_count = 0

    for record in results:
        # Check for actual N/A strings in the data
        for field in ['incident_id', 'facility', 'problem_description', 'proven_solution']:
            value = record.get(field)
            if value == 'N/A':
                na_count += 1
                print(f"Found actual N/A in field {field}")
            if value is None:
                null_count += 1
                print(f"Found null in field {field}")

    print(f"\nData Quality Analysis:")
    print(f"  Actual 'N/A' strings in data: {na_count}")
    print(f"  Actual null values: {null_count}")
    print(f"  Status: {'✅ CLEAN DATA' if na_count == 0 and null_count == 0 else '❌ DATA ISSUES'}")

    # Show FULL results without truncation
    print(f"\n=== FULL SAMPLE RESULTS (No Truncation) ===")
    for i, record in enumerate(results[:2]):
        print(f"\n--- Record {i+1} ---")
        print(f"Incident ID: '{record.get('incident_id')}'")
        print(f"Facility: '{record.get('facility')}'")
        print(f"Problem Description: '{record.get('problem_description')}'")
        print(f"Proven Solution: '{record.get('proven_solution')}'")
        print(f"Frequency: {record.get('frequency')}")

if __name__ == "__main__":
    test_full_data_display()

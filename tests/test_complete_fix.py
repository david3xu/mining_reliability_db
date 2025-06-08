#!/usr/bin/env python3
"""
Complete test for the incident root cause investigation fix
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.database.db import get_database

def test_complete_fix():
    """Test the complete fix for field mapping and null filtering"""
    print("="*80)
    print("COMPLETE INCIDENT ROOT CAUSE INVESTIGATION FIX TEST")
    print("="*80)

    try:
        db_connection = get_database()
        print("✅ Database connection established")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return

    # Test 1: Check the corrected query with proper field names and null filtering
    print("\n1. Testing corrected query from actual file...")

    # Load the actual query file
    try:
        with open('/home/291928k/uwa/alcoa/mining_reliability_db/configs/queries/potential_root_causes.cypher', 'r') as f:
            query_template = f.read()

        # Replace the filter clause placeholder
        corrected_query = query_template.replace('{filter_clause}', "toLower(p.what_happened) CONTAINS toLower('contamination')")

    except Exception as e:
        print(f"❌ Error reading query file: {e}")
        return

    try:
        results = db_connection.execute_query(corrected_query)
        print(f"✅ Found {len(results)} records")

        # Check for null records
        null_count = 0
        for record in results:
            if (record.get('incident_id') is None or
                record.get('facility') is None or
                record.get('problem_description') is None or
                record.get('proven_solution') is None):
                null_count += 1

        if null_count == 0:
            print("✅ No null records found - null filtering working correctly")
        else:
            print(f"❌ Found {null_count} records with null values")

        # Check field names
        if results:
            expected_fields = ['incident_id', 'facility', 'problem_description', 'proven_solution']
            actual_fields = list(results[0].keys())

            field_check = all(field in actual_fields for field in expected_fields)
            if field_check:
                print("✅ All expected field names present - field mapping working correctly")
                print(f"   Fields: {expected_fields}")
            else:
                print(f"❌ Field mapping issue - expected {expected_fields}, got {actual_fields}")

        # Display sample results
        print("\nSample results:")
        for i, record in enumerate(results[:3]):
            print(f"Record {i+1}:")
            print(f"  incident_id: {record.get('incident_id')}")
            print(f"  facility: {record.get('facility')}")
            print(f"  problem_description: {record.get('problem_description', 'N/A')[:100]}...")
            print(f"  proven_solution: {record.get('proven_solution', 'N/A')[:100]}...")
            print()

    except Exception as e:
        print(f"❌ Error executing corrected query: {e}")

    # Test 2: Test the actual query file content
    print("\n2. Testing actual query file content...")
    try:
        with open('/home/291928k/uwa/alcoa/mining_reliability_db/configs/queries/potential_root_causes.cypher', 'r') as f:
            query_content = f.read()

        # Check for correct field mappings in file
        if 'problem_description' in query_content and 'proven_solution' in query_content:
            print("✅ Query file has correct field mappings")
        else:
            print("❌ Query file still has incorrect field mappings")

        # Check for null filtering in file
        null_checks = ['ar.action_request_number IS NOT NULL',
                      'f.facility_id IS NOT NULL',
                      'p.what_happened IS NOT NULL',
                      'rc.root_cause IS NOT NULL']

        null_filtering_ok = all(check in query_content for check in null_checks)
        if null_filtering_ok:
            print("✅ Query file has proper null filtering")
        else:
            print("❌ Query file missing some null filtering checks")

    except Exception as e:
        print(f"❌ Error reading query file: {e}")

    # Test 3: Test with different search terms
    print("\n3. Testing with different search terms...")
    search_terms = ['air', 'belt', 'motor']

    for term in search_terms:
        try:
            with open('/home/291928k/uwa/alcoa/mining_reliability_db/configs/queries/potential_root_causes.cypher', 'r') as f:
                query_template = f.read()
            test_query = query_template.replace('{filter_clause}', f"toLower(p.what_happened) CONTAINS toLower('{term}')")
            results = db_connection.execute_query(test_query)
            null_count = sum(1 for r in results if any(v is None for v in [r.get('incident_id'), r.get('facility'), r.get('problem_description'), r.get('proven_solution')]))
            print(f"  Term '{term}': {len(results)} results, {null_count} null records")
        except Exception as e:
            print(f"  Term '{term}': Error - {e}")

if __name__ == "__main__":
    test_complete_fix()

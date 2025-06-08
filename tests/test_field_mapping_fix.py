#!/usr/bin/env python3
"""
Test the fixed field mapping for stakeholder essentials
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.database.db import get_database

def test_field_mapping_fix():
    """Test that the updated query returns the correct field names"""
    print("="*80)
    print("TESTING FIELD MAPPING FIX")
    print("="*80)

    db_connection = get_database()

    # Test the updated query similar to potential_root_causes.cypher
    test_query = """
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
    OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
    WHERE toLower(p.what_happened) CONTAINS toLower('vibration')
      AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
      AND ar.action_request_number IS NOT NULL
      AND f.facility_id IS NOT NULL
      AND p.what_happened IS NOT NULL
      AND rc.root_cause IS NOT NULL
    WITH ar.action_request_number AS incident_id,
         f.facility_id AS facility,
         p.what_happened AS problem_description,
         rc.root_cause AS proven_solution,
         rc.root_cause_tail_extraction AS root_cause_details,
         ar.categories AS equipment_category,
         ar.initiation_date AS initiation_date
    RETURN incident_id,
           facility,
           problem_description,
           proven_solution,
           root_cause_details,
           equipment_category,
           count(*) as frequency,
           max(initiation_date) as latest_date
    ORDER BY frequency DESC, latest_date DESC
    LIMIT 10
    """

    print("Testing updated query with correct field mapping...")
    try:
        results = db_connection.execute_query(test_query)
        print(f"Found {len(results)} records")

        if results:
            print("\n✅ FIELD MAPPING TEST RESULTS:")
            print("="*60)

            # Check first record field names
            first_record = results[0]
            expected_fields = {
                'incident_id': 'Incident ID',
                'facility': 'Facility/Location',
                'problem_description': 'Problem Description',
                'proven_solution': 'Proven Solution',
                'frequency': 'Frequency Count',
                'latest_date': 'Latest Date'
            }

            print(f"Record fields present:")
            all_fields_correct = True
            for field, description in expected_fields.items():
                if field in first_record:
                    value = first_record[field]
                    if value is None:
                        print(f"  ❌ {field} ({description}): {value} (NULL VALUE)")
                        all_fields_correct = False
                    else:
                        print(f"  ✅ {field} ({description}): {value}")
                else:
                    print(f"  ❌ {field} ({description}): MISSING")
                    all_fields_correct = False

            if all_fields_correct:
                print(f"\n🎉 SUCCESS: All expected fields present with values!")
            else:
                print(f"\n❌ FAILURE: Some fields missing or null")

            print(f"\nAll records:")
            for i, record in enumerate(results):
                print(f"\nRecord {i+1}:")
                print(f"  Incident: {record.get('incident_id')}")
                print(f"  Facility: {record.get('facility')}")
                print(f"  Problem: {record.get('problem_description', 'N/A')[:80]}...")
                print(f"  Solution: {record.get('proven_solution', 'N/A')[:80]}...")
                print(f"  Frequency: {record.get('frequency')}")

        else:
            print("❌ No results found")

    except Exception as e:
        print(f"❌ Error executing query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_field_mapping_fix()

#!/usr/bin/env python3
"""
Test the updated query with null filtering directly
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.database.db import get_database

def test_updated_query():
    """Test the updated query with null filtering"""
    print("="*80)
    print("TESTING UPDATED QUERY WITH NULL FILTERING")
    print("="*80)

    db_connection = get_database()

    # Test the updated query with null filtering
    updated_query = """
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
    OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
    WHERE toLower(p.what_happened) CONTAINS toLower('contamination')
      AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
      AND ar.action_request_number IS NOT NULL
      AND f.facility_id IS NOT NULL
      AND p.what_happened IS NOT NULL
      AND rc.root_cause IS NOT NULL
    WITH ar.action_request_number AS incident_id,
         f.facility_id AS facility,
         p.what_happened AS similar_symptoms,
         rc.root_cause AS identified_root_cause,
         rc.root_cause_tail_extraction AS root_cause_details,
         ar.categories AS equipment_category,
         ar.initiation_date AS initiation_date
    RETURN incident_id,
           facility,
           similar_symptoms,
           identified_root_cause,
           root_cause_details,
           equipment_category,
           count(*) as frequency,
           max(initiation_date) as latest_date
    ORDER BY frequency DESC, latest_date DESC
    LIMIT 10
    """

    print("Running updated query with null filtering...")
    try:
        results = db_connection.execute_query(updated_query)
        print(f"Found {len(results)} records")

        if results:
            for i, record in enumerate(results):
                print(f"Record {i+1}:")
                for key, value in record.items():
                    print(f"  {key}: {value}")
                print()

                # Check for null values
                null_count = sum(1 for value in record.values() if value is None)
                if null_count > 0:
                    print(f"  ❌ Contains {null_count} null values")
                else:
                    print(f"  ✅ No null values")
                print()
        else:
            print("No results found")

    except Exception as e:
        print(f"❌ Error executing query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_updated_query()

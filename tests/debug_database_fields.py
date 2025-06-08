#!/usr/bin/env python3
"""
Debug what fields exist in the database
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.database.db import get_database

def debug_database_fields():
    """Debug what fields exist in the database"""
    print("="*80)
    print("DEBUGGING DATABASE FIELDS")
    print("="*80)

    db_connection = get_database()

    # First, let's see what data we have
    sample_query = """
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
    OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
    RETURN ar.action_request_number AS incident_id,
           f.facility_id AS facility,
           p.what_happened AS similar_symptoms,
           rc.root_cause AS identified_root_cause,
           rc.root_cause_tail_extraction AS root_cause_details,
           ar.categories AS equipment_category,
           ar.initiation_date AS initiation_date,
           v.is_action_plan_effective AS verification_status
    LIMIT 5
    """

    print("Running sample query to see raw data...")
    try:
        results = db_connection.execute_query(sample_query)
        print(f"Found {len(results)} records")

        if results:
            print("\nFirst record:")
            for key, value in results[0].items():
                print(f"  {key}: {value}")

            print("\nAll records summary:")
            for i, record in enumerate(results):
                print(f"Record {i+1}:")
                print(f"  incident_id: {record.get('incident_id')}")
                print(f"  facility: {record.get('facility')}")
                print(f"  similar_symptoms: {record.get('similar_symptoms')}")
                print(f"  identified_root_cause: {record.get('identified_root_cause')}")
                print(f"  verification_status: {record.get('verification_status')}")
                print()
        else:
            print("No results found")

        # Now test with filter
        print("\n" + "="*60)
        print("TESTING WITH FILTER")
        print("="*60)

        filter_query = """
        MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
        MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
        OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
        WHERE toLower(p.what_happened) CONTAINS toLower('contamination')
          AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
        RETURN ar.action_request_number AS incident_id,
               f.facility_id AS facility,
               p.what_happened AS similar_symptoms,
               rc.root_cause AS identified_root_cause,
               rc.root_cause_tail_extraction AS root_cause_details,
               ar.categories AS equipment_category,
               ar.initiation_date AS initiation_date
        LIMIT 5
        """

        print("Running query with 'contamination' filter...")
        filtered_results = db_connection.execute_query(filter_query)
        print(f"Found {len(filtered_results)} filtered records")

        if filtered_results:
            print("\nFiltered results:")
            for i, record in enumerate(filtered_results):
                print(f"Record {i+1}:")
                for key, value in record.items():
                    print(f"  {key}: {value}")
                print()

    except Exception as e:
        print(f"❌ Error executing query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_database_fields()

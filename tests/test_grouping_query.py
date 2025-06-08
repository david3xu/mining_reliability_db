#!/usr/bin/env python3
"""
Test the exact query with grouping
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.database.db import get_database

def test_grouping_query():
    """Test the exact query used by the system"""
    print("="*80)
    print("TESTING GROUPING QUERY")
    print("="*80)

    db_connection = get_database()

    # This is the exact query structure from potential_root_causes.cypher
    query_with_grouping = """
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
    OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
    WHERE toLower(p.what_happened) CONTAINS toLower('contamination')
      AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
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

    print("Running query with grouping...")
    try:
        results = db_connection.execute_query(query_with_grouping)
        print(f"Found {len(results)} records")

        if results:
            for i, record in enumerate(results):
                print(f"Record {i+1}:")
                for key, value in record.items():
                    print(f"  {key}: {value}")
                print()
        else:
            print("No results found")

        # Now test without the grouping/aggregation to see if that fixes it
        print("\n" + "="*60)
        print("TESTING WITHOUT GROUPING")
        print("="*60)

        query_without_grouping = """
        MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
        MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
        OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
        WHERE toLower(p.what_happened) CONTAINS toLower('air')
          AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
        RETURN ar.action_request_number AS incident_id,
               f.facility_id AS facility,
               p.what_happened AS similar_symptoms,
               rc.root_cause AS identified_root_cause,
               rc.root_cause_tail_extraction AS root_cause_details,
               ar.categories AS equipment_category,
               ar.initiation_date AS initiation_date
        ORDER BY ar.initiation_date DESC
        LIMIT 10
        """

        print("Running query without grouping (searching for 'air')...")
        results_no_group = db_connection.execute_query(query_without_grouping)
        print(f"Found {len(results_no_group)} records")

        if results_no_group:
            for i, record in enumerate(results_no_group):
                print(f"Record {i+1}:")
                for key, value in record.items():
                    print(f"  {key}: {value}")
                print()

    except Exception as e:
        print(f"❌ Error executing query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_grouping_query()

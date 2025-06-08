#!/usr/bin/env python3
"""
Debug the grouping issue that's allowing null records through
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.database.db import get_database

def debug_grouping_issue():
    """Debug why null records are still appearing with grouping"""
    print("="*80)
    print("DEBUGGING GROUPING ISSUE")
    print("="*80)

    db_connection = get_database()

    # Test without grouping first
    print("\n1. Testing WITHOUT grouping (should have no nulls)...")
    query_no_group = """
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
    OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
    WHERE toLower(p.what_happened) CONTAINS toLower('contamination')
      AND COALESCE(v.is_action_plan_effective, "No") = "Yes"
      AND ar.action_request_number IS NOT NULL
      AND f.facility_id IS NOT NULL
      AND p.what_happened IS NOT NULL
      AND rc.root_cause IS NOT NULL
    RETURN ar.action_request_number AS incident_id,
           f.facility_id AS facility,
           p.what_happened AS problem_description,
           rc.root_cause AS proven_solution
    ORDER BY ar.initiation_date DESC
    LIMIT 10
    """

    try:
        results_no_group = db_connection.execute_query(query_no_group)
        print(f"Results without grouping: {len(results_no_group)}")

        null_count = sum(1 for r in results_no_group if any(v is None for v in [r.get('incident_id'), r.get('facility'), r.get('problem_description'), r.get('proven_solution')]))
        print(f"Null records without grouping: {null_count}")

        for i, record in enumerate(results_no_group[:3]):
            print(f"  Record {i+1}: id={record.get('incident_id')}, facility={record.get('facility')[:20] if record.get('facility') else None}...")

    except Exception as e:
        print(f"❌ Error without grouping: {e}")

    # Test with grouping
    print("\n2. Testing WITH grouping (problematic)...")
    query_with_group = """
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

    try:
        results_with_group = db_connection.execute_query(query_with_group)
        print(f"Results with grouping: {len(results_with_group)}")

        null_count = sum(1 for r in results_with_group if any(v is None for v in [r.get('incident_id'), r.get('facility'), r.get('problem_description'), r.get('proven_solution')]))
        print(f"Null records with grouping: {null_count}")

        for i, record in enumerate(results_with_group[:3]):
            print(f"  Record {i+1}: id={record.get('incident_id')}, facility={record.get('facility')[:20] if record.get('facility') else None}...")

    except Exception as e:
        print(f"❌ Error with grouping: {e}")

    # Test with explicit grouping by non-null fields
    print("\n3. Testing WITH explicit grouping by non-null fields...")
    query_explicit_group = """
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
         p.what_happened AS problem_description,
         rc.root_cause AS proven_solution,
         rc.root_cause_tail_extraction AS root_cause_details,
         ar.categories AS equipment_category,
         ar.initiation_date AS initiation_date
    WHERE incident_id IS NOT NULL AND facility IS NOT NULL AND problem_description IS NOT NULL AND proven_solution IS NOT NULL
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

    try:
        results_explicit = db_connection.execute_query(query_explicit_group)
        print(f"Results with explicit grouping: {len(results_explicit)}")

        null_count = sum(1 for r in results_explicit if any(v is None for v in [r.get('incident_id'), r.get('facility'), r.get('problem_description'), r.get('proven_solution')]))
        print(f"Null records with explicit grouping: {null_count}")

        if null_count == 0:
            print("✅ Fixed! No null records with explicit filtering after WITH clause")

    except Exception as e:
        print(f"❌ Error with explicit grouping: {e}")

if __name__ == "__main__":
    debug_grouping_issue()

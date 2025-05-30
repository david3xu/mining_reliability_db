#!/usr/bin/env python3
"""
Test for verifying correct relationship creation in Mining Reliability DB
"""

import pytest
from mine_core.database.db import get_database
from mine_core.pipelines.loader import Neo4jLoader

def test_hierarchical_relationship_chain():
    """Test that hierarchical relationships are created with correct directionality"""
    # Sample test data with minimal hierarchy
    test_data = {
        "facility": {
            "facility_id": "test-facility",
            "facility_name": "Test Facility",
            "active": True
        },
        "entities": {
            "ActionRequest": [{
                "action_request_id": "ar-test",
                "facility_id": "test-facility",
                "action_request_number": "TEST-001",
                "title": "Test Request",
                "initiation_date": "2025-01-01"
            }],
            "Problem": [{
                "problem_id": "prob-test",
                "action_request_id": "ar-test",
                "what_happened": "Test problem description"
            }],
            "RootCause": [{
                "cause_id": "cause-test",
                "problem_id": "prob-test",
                "root_cause": "Test root cause"
            }],
            "ActionPlan": [{
                "plan_id": "plan-test",
                "root_cause_id": "cause-test",
                "action_plan": "Test action plan"
            }],
            "Verification": [{
                "verification_id": "ver-test",
                "action_plan_id": "plan-test",
                "is_action_plan_effective": True
            }]
        }
    }

    # Load test data
    loader = Neo4jLoader()
    result = loader.load_data(test_data)
    assert result is True

    db = get_database()

    # Test 1: Verify ActionRequest → Facility relationship
    query = """
    MATCH (ar:ActionRequest {action_request_id: 'ar-test'})
    MATCH (f:Facility {facility_id: 'test-facility'})
    RETURN EXISTS((ar)-[:BELONGS_TO]->(f)) as relationship_exists
    """
    result = db.execute_query(query)
    assert result[0]['relationship_exists'] is True

    # Test 2: Verify Problem → ActionRequest relationship
    query = """
    MATCH (p:Problem {problem_id: 'prob-test'})
    MATCH (ar:ActionRequest {action_request_id: 'ar-test'})
    RETURN EXISTS((p)-[:IDENTIFIED_IN]->(ar)) as relationship_exists
    """
    result = db.execute_query(query)
    assert result[0]['relationship_exists'] is True

    # Test 3: Verify RootCause → Problem relationship
    query = """
    MATCH (rc:RootCause {cause_id: 'cause-test'})
    MATCH (p:Problem {problem_id: 'prob-test'})
    RETURN EXISTS((rc)-[:ANALYZES]->(p)) as relationship_exists
    """
    result = db.execute_query(query)
    assert result[0]['relationship_exists'] is True

    # Test 4: Verify ActionPlan → RootCause relationship
    query = """
    MATCH (ap:ActionPlan {plan_id: 'plan-test'})
    MATCH (rc:RootCause {cause_id: 'cause-test'})
    RETURN EXISTS((ap)-[:RESOLVES]->(rc)) as relationship_exists
    """
    result = db.execute_query(query)
    assert result[0]['relationship_exists'] is True

    # Test 5: Verify Verification → ActionPlan relationship
    query = """
    MATCH (v:Verification {verification_id: 'ver-test'})
    MATCH (ap:ActionPlan {plan_id: 'plan-test'})
    RETURN EXISTS((v)-[:VALIDATES]->(ap)) as relationship_exists
    """
    result = db.execute_query(query)
    assert result[0]['relationship_exists'] is True

    # Test 6: Verify full chain traversal (corrected direction)
    query = """
    MATCH path = (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility),
                 (p:Problem)-[:IDENTIFIED_IN]->(ar),
                 (rc:RootCause)-[:ANALYZES]->(p),
                 (ap:ActionPlan)-[:RESOLVES]->(rc),
                 (v:Verification)-[:VALIDATES]->(ap)
    WHERE f.facility_id = 'test-facility'
    RETURN count(path) as path_count
    """
    result = db.execute_query(query)
    assert result[0]['path_count'] > 0

#!/usr/bin/env python3
"""
Neo4j Database Queries
Core queries for mining reliability data.
"""

import logging
from typing import Dict, List, Any, Optional

from mine_core.database.db import get_database

logger = logging.getLogger(__name__)

# Facility Queries

def get_facilities() -> List[Dict[str, Any]]:
    """Get all facilities"""
    query = """
    MATCH (f:Facility)
    RETURN f.facility_id AS id, f.facility_name AS name, f.active AS active
    ORDER BY f.facility_name
    """
    return get_database().execute_query(query)

def get_facility(facility_id: str) -> Optional[Dict[str, Any]]:
    """Get facility by ID"""
    query = """
    MATCH (f:Facility {facility_id: $facility_id})
    RETURN f.facility_id AS id, f.facility_name AS name, f.active AS active
    """
    results = get_database().execute_query(query, facility_id=facility_id)
    return results[0] if results else None

# ActionRequest Queries

def get_action_requests(facility_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Get action requests, optionally filtered by facility"""
    params = {"limit": limit}

    if facility_id:
        query = """
        MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility {facility_id: $facility_id})
        RETURN ar.action_request_id AS id,
               ar.action_request_number AS number,
               ar.title AS title,
               ar.initiation_date AS date,
               ar.stage AS stage,
               ar.categories AS categories,
               f.facility_id AS facility_id
        ORDER BY ar.initiation_date DESC
        LIMIT $limit
        """
        params["facility_id"] = facility_id
    else:
        query = """
        MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
        RETURN ar.action_request_id AS id,
               ar.action_request_number AS number,
               ar.title AS title,
               ar.initiation_date AS date,
               ar.stage AS stage,
               ar.categories AS categories,
               f.facility_id AS facility_id
        ORDER BY ar.initiation_date DESC
        LIMIT $limit
        """

    return get_database().execute_query(query, **params)

def get_action_request(action_request_id: str) -> Optional[Dict[str, Any]]:
    """Get action request by ID"""
    query = """
    MATCH (ar:ActionRequest {action_request_id: $action_request_id})
    OPTIONAL MATCH (ar)-[:BELONGS_TO]->(f:Facility)
    RETURN ar.action_request_id AS id,
           ar.action_request_number AS number,
           ar.title AS title,
           ar.initiation_date AS date,
           ar.stage AS stage,
           ar.categories AS categories,
           ar.action_types AS action_types,
           ar.requested_response_time AS response_time,
           ar.past_due_status AS past_due_status,
           ar.days_past_due AS days_past_due,
           ar.operating_centre AS operating_centre,
           f.facility_id AS facility_id,
           f.facility_name AS facility_name
    """
    results = get_database().execute_query(query, action_request_id=action_request_id)
    return results[0] if results else None

# Incident Chain Queries

def get_incident_chain(action_request_id: str) -> Dict[str, Any]:
    """Get complete incident chain for an action request with correct relationship traversal"""
    query = """
    MATCH (ar:ActionRequest {action_request_id: $action_request_id})
    OPTIONAL MATCH (ar)-[:BELONGS_TO]->(f:Facility)
    OPTIONAL MATCH (p:Problem)-[:IDENTIFIED_IN]->(ar)
    OPTIONAL MATCH (rc:RootCause)-[:ANALYZES]->(p)
    OPTIONAL MATCH (ap:ActionPlan)-[:RESOLVES]->(rc)
    OPTIONAL MATCH (v:Verification)-[:VALIDATES]->(ap)

    RETURN ar.action_request_id AS request_id,
           ar.action_request_number AS request_number,
           ar.title AS title,
           ar.initiation_date AS date,
           ar.stage AS stage,
           f.facility_id AS facility_id,

           p.problem_id AS problem_id,
           p.what_happened AS what_happened,
           p.requirement AS requirement,

           rc.cause_id AS cause_id,
           rc.root_cause AS root_cause,
           rc.objective_evidence AS objective_evidence,

           ap.plan_id AS plan_id,
           ap.action_plan AS action_plan,
           ap.recommended_action AS recommended_action,
           ap.immediate_containment AS immediate_containment,
           ap.due_date AS due_date,
           ap.complete AS complete,
           ap.completion_date AS completion_date,

           v.verification_id AS verification_id,
           v.is_action_plan_effective AS is_effective,
           v.action_plan_eval_comment AS eval_comment,
           v.action_plan_verification_date AS verification_date
    """
    results = get_database().execute_query(query, action_request_id=action_request_id)
    return results[0] if results else {}

# Supporting Entity Queries

def get_department(action_request_id: str) -> Optional[Dict[str, Any]]:
    """Get department info for an action request"""
    query = """
    MATCH (d:Department)-[:ASSIGNED_TO]->(ar:ActionRequest {action_request_id: $action_request_id})
    RETURN d.dept_id AS id,
           d.init_dept AS init_dept,
           d.rec_dept AS rec_dept
    """
    results = get_database().execute_query(query, action_request_id=action_request_id)
    return results[0] if results else None

def get_assets(problem_id: str) -> List[Dict[str, Any]]:
    """Get assets for a problem"""
    query = """
    MATCH (a:Asset)-[:INVOLVED_IN]->(p:Problem {problem_id: $problem_id})
    RETURN a.asset_id AS id,
           a.asset_numbers AS asset_numbers,
           a.asset_activity_numbers AS activity_numbers
    """
    return get_database().execute_query(query, problem_id=problem_id)

# Analysis Queries

def get_incident_counts_by_category() -> List[Dict[str, Any]]:
    """Get incident counts by category"""
    query = """
    MATCH (ar:ActionRequest)
    WHERE ar.categories IS NOT NULL
    RETURN ar.categories AS category, count(ar) AS count
    ORDER BY count DESC
    """
    return get_database().execute_query(query)

def get_root_cause_frequency() -> List[Dict[str, Any]]:
    """Get frequency of different root causes"""
    query = """
    MATCH (rc:RootCause)
    WHERE rc.root_cause IS NOT NULL
    RETURN rc.root_cause AS cause, count(rc) AS count
    ORDER BY count DESC
    LIMIT 10
    """
    return get_database().execute_query(query)

def get_effectiveness_stats() -> Dict[str, Any]:
    """Get statistics on action plan effectiveness"""
    query = """
    MATCH (v:Verification)
    WITH
      count(v) AS total,
      sum(CASE WHEN v.is_action_plan_effective = true THEN 1 ELSE 0 END) AS effective,
      sum(CASE WHEN v.is_action_plan_effective = false THEN 1 ELSE 0 END) AS ineffective,
      sum(CASE WHEN v.is_action_plan_effective IS NULL THEN 1 ELSE 0 END) AS unknown
    RETURN total, effective, ineffective, unknown,
           toFloat(effective) / total * 100 AS effective_percent
    """
    results = get_database().execute_query(query)
    return results[0] if results else {
        "total": 0, "effective": 0, "ineffective": 0,
        "unknown": 0, "effective_percent": 0
    }

#!/usr/bin/env python3
"""
Schema-driven database queries using model_schema.json
"""

import logging
from typing import Dict, List, Any, Optional
from mine_core.database.db import get_database
from configs.environment import get_schema

logger = logging.getLogger(__name__)

class SchemaQueries:
    """Schema-driven query builder"""

    def __init__(self):
        self.schema = get_schema()
        self.entities = {e["name"]: e for e in self.schema.get("entities", [])}

    def _get_primary_key(self, entity_name: str) -> Optional[str]:
        """Get primary key from schema"""
        entity = self.entities.get(entity_name, {})
        properties = entity.get("properties", {})

        for prop_name, prop_info in properties.items():
            if prop_info.get("primary_key", False):
                return prop_name
        return None

# Schema-driven query functions
def get_facilities() -> List[Dict[str, Any]]:
    """Get facilities using schema"""
    queries = SchemaQueries()
    facility_pk = queries._get_primary_key("Facility")

    query = f"""
    MATCH (f:Facility)
    RETURN f.{facility_pk} AS id, f.facility_name AS name, f.active AS active
    ORDER BY f.facility_name
    """
    return get_database().execute_query(query)

def get_facility(facility_id: str) -> Optional[Dict[str, Any]]:
    """Get facility by ID using schema"""
    queries = SchemaQueries()
    facility_pk = queries._get_primary_key("Facility")

    query = f"""
    MATCH (f:Facility {{{facility_pk}: $facility_id}})
    RETURN f.{facility_pk} AS id, f.facility_name AS name, f.active AS active
    """
    results = get_database().execute_query(query, facility_id=facility_id)
    return results[0] if results else None

def get_action_requests(facility_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Get action requests using schema"""
    queries = SchemaQueries()
    ar_pk = queries._get_primary_key("ActionRequest")
    facility_pk = queries._get_primary_key("Facility")

    params = {"limit": limit}

    if facility_id:
        query = f"""
        MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility {{{facility_pk}: $facility_id}})
        RETURN ar.{ar_pk} AS id,
               ar.action_request_number AS number,
               ar.title AS title,
               ar.initiation_date AS date,
               ar.stage AS stage,
               ar.categories AS categories,
               f.{facility_pk} AS facility_id
        ORDER BY ar.initiation_date DESC
        LIMIT $limit
        """
        params["facility_id"] = facility_id
    else:
        query = f"""
        MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
        RETURN ar.{ar_pk} AS id,
               ar.action_request_number AS number,
               ar.title AS title,
               ar.initiation_date AS date,
               ar.stage AS stage,
               ar.categories AS categories,
               f.{facility_pk} AS facility_id
        ORDER BY ar.initiation_date DESC
        LIMIT $limit
        """

    return get_database().execute_query(query, **params)

def get_action_request(action_request_id: str) -> Optional[Dict[str, Any]]:
    """Get action request by ID using schema"""
    queries = SchemaQueries()
    ar_pk = queries._get_primary_key("ActionRequest")
    facility_pk = queries._get_primary_key("Facility")

    query = f"""
    MATCH (ar:ActionRequest {{{ar_pk}: $action_request_id}})
    OPTIONAL MATCH (ar)-[:BELONGS_TO]->(f:Facility)
    RETURN ar.{ar_pk} AS id,
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
           f.{facility_pk} AS facility_id,
           f.facility_name AS facility_name
    """
    results = get_database().execute_query(query, action_request_id=action_request_id)
    return results[0] if results else None

def get_incident_chain(action_request_id: str) -> Dict[str, Any]:
    """Get complete incident chain using schema"""
    queries = SchemaQueries()
    ar_pk = queries._get_primary_key("ActionRequest")
    facility_pk = queries._get_primary_key("Facility")
    problem_pk = queries._get_primary_key("Problem")
    rc_pk = queries._get_primary_key("RootCause")
    ap_pk = queries._get_primary_key("ActionPlan")
    v_pk = queries._get_primary_key("Verification")

    query = f"""
    MATCH (ar:ActionRequest {{{ar_pk}: $action_request_id}})
    OPTIONAL MATCH (ar)-[:BELONGS_TO]->(f:Facility)
    OPTIONAL MATCH (p:Problem)-[:IDENTIFIED_IN]->(ar)
    OPTIONAL MATCH (rc:RootCause)-[:ANALYZES]->(p)
    OPTIONAL MATCH (ap:ActionPlan)-[:RESOLVES]->(rc)
    OPTIONAL MATCH (v:Verification)-[:VALIDATES]->(ap)

    RETURN ar.{ar_pk} AS request_id,
           ar.action_request_number AS request_number,
           ar.title AS title,
           ar.initiation_date AS date,
           ar.stage AS stage,
           f.{facility_pk} AS facility_id,

           p.{problem_pk} AS problem_id,
           p.what_happened AS what_happened,
           p.requirement AS requirement,

           rc.{rc_pk} AS cause_id,
           rc.root_cause AS root_cause,
           rc.objective_evidence AS objective_evidence,

           ap.{ap_pk} AS plan_id,
           ap.action_plan AS action_plan,
           ap.recommended_action AS recommended_action,
           ap.immediate_containment AS immediate_containment,
           ap.due_date AS due_date,
           ap.complete AS complete,
           ap.completion_date AS completion_date,

           v.{v_pk} AS verification_id,
           v.is_action_plan_effective AS is_effective,
           v.action_plan_eval_comment AS eval_comment,
           v.action_plan_verification_date AS verification_date
    """
    results = get_database().execute_query(query, action_request_id=action_request_id)
    return results[0] if results else {}

def get_department(action_request_id: str) -> Optional[Dict[str, Any]]:
    """Get department info using schema"""
    queries = SchemaQueries()
    dept_pk = queries._get_primary_key("Department")
    ar_pk = queries._get_primary_key("ActionRequest")

    query = f"""
    MATCH (d:Department)-[:ASSIGNED_TO]->(ar:ActionRequest {{{ar_pk}: $action_request_id}})
    RETURN d.{dept_pk} AS id,
           d.init_dept AS init_dept,
           d.rec_dept AS rec_dept
    """
    results = get_database().execute_query(query, action_request_id=action_request_id)
    return results[0] if results else None

def get_assets(problem_id: str) -> List[Dict[str, Any]]:
    """Get assets using schema"""
    queries = SchemaQueries()
    asset_pk = queries._get_primary_key("Asset")
    problem_pk = queries._get_primary_key("Problem")

    query = f"""
    MATCH (a:Asset)-[:INVOLVED_IN]->(p:Problem {{{problem_pk}: $problem_id}})
    RETURN a.{asset_pk} AS id,
           a.asset_numbers AS asset_numbers,
           a.asset_activity_numbers AS activity_numbers
    """
    return get_database().execute_query(query, problem_id=problem_id)

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
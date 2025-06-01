#!/usr/bin/env python3
"""
Simplified Operational Intelligence Queries for Mining Reliability Database
Streamlined analytics with enhanced causal intelligence capabilities.
"""

import logging
from typing import Dict, List, Any, Optional
from mine_core.database.db import get_database

logger = logging.getLogger(__name__)

# Core facility and incident queries

def get_facilities() -> List[Dict[str, Any]]:
    """Get all facilities with operational metrics"""
    query = """
    MATCH (f:Facility)
    WHERE NOT '_SchemaTemplate' IN labels(f)
    OPTIONAL MATCH (f)<-[:BELONGS_TO]-(ar:ActionRequest)
    WITH f, count(ar) AS incident_count
    RETURN f.facility_id AS id,
           f.facility_name AS name,
           f.active AS active,
           incident_count
    ORDER BY f.facility_name
    """
    return get_database().execute_query(query)

def get_facility(facility_id: str) -> Optional[Dict[str, Any]]:
    """Get facility details with operational summary"""
    query = """
    MATCH (f:Facility {facility_id: $facility_id})
    WHERE NOT '_SchemaTemplate' IN labels(f)
    OPTIONAL MATCH (f)<-[:BELONGS_TO]-(ar:ActionRequest)
    OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)
    WITH f, count(DISTINCT ar) AS total_incidents,
         count(DISTINCT rc) AS analyzed_causes
    RETURN f.facility_id AS id,
           f.facility_name AS name,
           f.active AS active,
           total_incidents,
           analyzed_causes
    """
    results = get_database().execute_query(query, facility_id=facility_id)
    return results[0] if results else None

def get_action_requests(facility_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Get action requests with enhanced operational context"""
    params = {"limit": limit}

    if facility_id:
        query = """
        MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility {facility_id: $facility_id})
        OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)
        RETURN ar.actionrequest_id AS id,
               ar.action_request_number AS number,
               ar.title AS title,
               ar.initiation_date AS date,
               ar.stage AS stage,
               ar.categories AS categories,
               labels(ar) AS dynamic_labels,
               f.facility_id AS facility_id,
               CASE WHEN rc IS NOT NULL THEN true ELSE false END AS has_root_cause_analysis
        ORDER BY ar.initiation_date DESC
        LIMIT $limit
        """
        params["facility_id"] = facility_id
    else:
        query = """
        MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
        WHERE NOT '_SchemaTemplate' IN labels(f)
        OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)
        RETURN ar.actionrequest_id AS id,
               ar.action_request_number AS number,
               ar.title AS title,
               ar.initiation_date AS date,
               ar.stage AS stage,
               ar.categories AS categories,
               labels(ar) AS dynamic_labels,
               f.facility_id AS facility_id,
               CASE WHEN rc IS NOT NULL THEN true ELSE false END AS has_root_cause_analysis
        ORDER BY ar.initiation_date DESC
        LIMIT $limit
        """

    return get_database().execute_query(query, **params)

# Enhanced causal intelligence queries

def get_root_cause_intelligence_summary(facility_id: str = None) -> Dict[str, Any]:
    """Comprehensive causal intelligence analysis for operational decision-making"""
    facility_filter = "WHERE f.facility_id = $facility_id" if facility_id else ""
    params = {"facility_id": facility_id} if facility_id else {}

    # Primary vs secondary cause analysis
    causal_analysis_query = f"""
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    WHERE NOT '_SchemaTemplate' IN labels(f) {' AND f.facility_id = $facility_id' if facility_filter else ''}
    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)
    WHERE rc.root_cause IS NOT NULL AND rc.root_cause <> 'DATA_NOT_AVAILABLE'
    WITH rc.root_cause AS primary_cause,
         rc.root_cause_tail AS secondary_cause,
         ar.categories AS category,
         count(*) AS frequency
    RETURN primary_cause, secondary_cause, category, frequency
    ORDER BY frequency DESC
    LIMIT 15
    """

    # Causal pattern effectiveness
    effectiveness_query = f"""
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    WHERE NOT '_SchemaTemplate' IN labels(f) {' AND f.facility_id = $facility_id' if facility_filter else ''}
    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
    WHERE rc.root_cause IS NOT NULL AND v.is_action_plan_effective IS NOT NULL
    WITH rc.root_cause AS cause_type,
         count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) AS effective_resolutions,
         count(*) AS total_resolutions
    WHERE total_resolutions >= 2
    RETURN cause_type, effective_resolutions, total_resolutions,
           toFloat(effective_resolutions) / total_resolutions * 100 AS effectiveness_percentage
    ORDER BY total_resolutions DESC, effectiveness_percentage DESC
    """

    causal_patterns = get_database().execute_query(causal_analysis_query, **params)
    effectiveness_data = get_database().execute_query(effectiveness_query, **params)

    return {
        "causal_patterns": causal_patterns,
        "resolution_effectiveness": effectiveness_data,
        "analysis_scope": facility_id or "all_facilities",
        "total_patterns_identified": len(causal_patterns)
    }

def get_operational_performance_dashboard(facility_id: str = None) -> Dict[str, Any]:
    """Comprehensive operational performance metrics for management oversight"""
    facility_filter = "WHERE f.facility_id = $facility_id" if facility_id else ""
    params = {"facility_id": facility_id} if facility_id else {}

    # Incident volume and resolution trends
    performance_query = f"""
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    WHERE NOT '_SchemaTemplate' IN labels(f) {' AND f.facility_id = $facility_id' if facility_filter else ''}
    OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
    OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
    WITH substring(ar.initiation_date, 0, 7) AS year_month,
         count(DISTINCT ar) AS total_incidents,
         count(DISTINCT ap) AS planned_responses,
         count(CASE WHEN ap.complete = true THEN 1 END) AS completed_actions,
         count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) AS effective_resolutions
    WHERE year_month IS NOT NULL
    RETURN year_month, total_incidents, planned_responses, completed_actions, effective_resolutions,
           CASE WHEN planned_responses > 0 THEN toFloat(completed_actions) / planned_responses * 100 ELSE 0 END AS completion_rate,
           CASE WHEN completed_actions > 0 THEN toFloat(effective_resolutions) / completed_actions * 100 ELSE 0 END AS effectiveness_rate
    ORDER BY year_month DESC
    LIMIT 12
    """

    # Category distribution with resolution success rates
    category_query = f"""
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    WHERE NOT '_SchemaTemplate' IN labels(f) {' AND f.facility_id = $facility_id' if facility_filter else ''}
          AND ar.categories IS NOT NULL AND ar.categories <> 'DATA_NOT_AVAILABLE'
    OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
    WITH ar.categories AS category,
         count(DISTINCT ar) AS incident_count,
         count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) AS successful_resolutions
    RETURN category, incident_count, successful_resolutions,
           CASE WHEN incident_count > 0 THEN toFloat(successful_resolutions) / incident_count * 100 ELSE 0 END AS success_rate
    ORDER BY incident_count DESC
    """

    # Workflow efficiency metrics
    workflow_query = f"""
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    {facility_filter}
    OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)
    OPTIONAL MATCH (p)<-[:ANALYZES]-(rc:RootCause)
    OPTIONAL MATCH (rc)<-[:RESOLVES]-(ap:ActionPlan)
    OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)
    WITH count(DISTINCT ar) AS total_incidents,
         count(DISTINCT p) AS problems_defined,
         count(DISTINCT rc) AS causes_analyzed,
         count(DISTINCT ap) AS plans_developed,
         count(DISTINCT v) AS plans_verified
    RETURN total_incidents, problems_defined, causes_analyzed, plans_developed, plans_verified,
           toFloat(problems_defined) / total_incidents * 100 AS problem_definition_rate,
           toFloat(causes_analyzed) / problems_defined * 100 AS cause_analysis_rate,
           toFloat(plans_developed) / causes_analyzed * 100 AS planning_rate,
           toFloat(plans_verified) / plans_developed * 100 AS verification_rate
    """

    return {
        "temporal_trends": get_database().execute_query(performance_query, **params),
        "category_performance": get_database().execute_query(category_query, **params),
        "workflow_efficiency": get_database().execute_query(workflow_query, **params)[0] if get_database().execute_query(workflow_query, **params) else {},
        "facility_scope": facility_id or "enterprise_wide"
    }

def get_predictive_intelligence_indicators() -> List[Dict[str, Any]]:
    """Identify patterns for predictive operational intelligence"""
    query = """
    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
    WHERE rc.root_cause IS NOT NULL AND rc.root_cause <> 'DATA_NOT_AVAILABLE'
      AND ar.categories IS NOT NULL AND ar.categories <> 'DATA_NOT_AVAILABLE'
      AND v.is_action_plan_effective IS NOT NULL

    WITH ar.categories AS incident_category,
         rc.root_cause AS primary_cause,
         rc.root_cause_tail AS secondary_cause,
         f.facility_id AS facility,
         count(*) AS pattern_frequency,
         count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) AS successful_outcomes

    WHERE pattern_frequency >= 3  // Statistical significance threshold

    RETURN incident_category, primary_cause, secondary_cause, facility,
           pattern_frequency, successful_outcomes,
           toFloat(successful_outcomes) / pattern_frequency AS success_probability,
           CASE
             WHEN successful_outcomes = 0 THEN 'high_risk'
             WHEN toFloat(successful_outcomes) / pattern_frequency < 0.5 THEN 'moderate_risk'
             ELSE 'low_risk'
           END AS risk_classification
    ORDER BY pattern_frequency DESC, success_probability ASC
    """
    return get_database().execute_query(query)

def get_missing_data_quality_intelligence() -> Dict[str, Any]:
    """Systematic missing data analysis for operational process improvement"""
    query = """
    MATCH (ar:ActionRequest)
    OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)
    OPTIONAL MATCH (p)<-[:ANALYZES]-(rc:RootCause)
    OPTIONAL MATCH (rc)<-[:RESOLVES]-(ap:ActionPlan)
    OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)

    WITH count(ar) AS total_incidents,
         count(p) AS incidents_with_problems,
         count(rc) AS incidents_with_causes,
         count(ap) AS incidents_with_plans,
         count(v) AS incidents_with_verification,
         count(CASE WHEN ar.title IS NULL OR ar.title = 'DATA_NOT_AVAILABLE' THEN 1 END) AS missing_titles,
         count(CASE WHEN ar.categories IS NULL OR ar.categories = 'DATA_NOT_AVAILABLE' THEN 1 END) AS missing_categories,
         count(CASE WHEN rc.root_cause IS NULL OR rc.root_cause = 'DATA_NOT_AVAILABLE' THEN 1 END) AS missing_root_causes

    RETURN total_incidents,
           toFloat(incidents_with_problems) / total_incidents * 100 AS problem_definition_completeness,
           toFloat(incidents_with_causes) / total_incidents * 100 AS causal_analysis_completeness,
           toFloat(incidents_with_plans) / total_incidents * 100 AS action_planning_completeness,
           toFloat(incidents_with_verification) / total_incidents * 100 AS verification_completeness,
           toFloat(missing_titles) / total_incidents * 100 AS title_missing_rate,
           toFloat(missing_categories) / total_incidents * 100 AS category_missing_rate,
           toFloat(missing_root_causes) / incidents_with_causes * 100 AS root_cause_missing_rate
    """

    results = get_database().execute_query(query)
    return results[0] if results else {}

def get_causal_correlation_matrix() -> List[Dict[str, Any]]:
    """Advanced causal correlation analysis for root cause intelligence"""
    query = """
    MATCH (rc1:RootCause)<-[:ANALYZES]-(p:Problem)-[:INVOLVED_IN]-(a:Asset)
    MATCH (p)-[:IDENTIFIED_IN]->(ar:ActionRequest)
    WHERE rc1.root_cause IS NOT NULL AND rc1.root_cause <> 'DATA_NOT_AVAILABLE'
      AND ar.categories IS NOT NULL AND ar.categories <> 'DATA_NOT_AVAILABLE'

    WITH ar.categories AS incident_category,
         rc1.root_cause AS primary_cause,
         rc1.root_cause_tail AS secondary_cause,
         a.asset_numbers AS asset_involved,
         count(*) AS correlation_strength

    WHERE correlation_strength >= 2

    RETURN incident_category, primary_cause, secondary_cause, asset_involved, correlation_strength
    ORDER BY correlation_strength DESC
    LIMIT 25
    """
    return get_database().execute_query(query)

def get_field_completion_statistics() -> Dict[str, Any]:
    """Get field completion statistics directly from Neo4j graph data"""
    query = """
    MATCH (ar:ActionRequest)
    WITH ar, keys(ar) as field_names, count(ar) as total_records
    UNWIND field_names as field_name
    WITH field_name, total_records,
         count(ar) as total_for_field,
         sum(case
             when ar[field_name] is not null
             and toString(ar[field_name]) <> ''
             and toString(ar[field_name]) <> 'DATA_NOT_AVAILABLE'
             and toString(ar[field_name]) <> 'NOT_SPECIFIED'
             and toString(ar[field_name]) <> 'null'
             and toString(ar[field_name]) <> 'none'
             and toString(ar[field_name]) <> 'n/a'
             then 1 else 0
         end) as completed_records
    WITH field_name, total_for_field, completed_records,
         round(toFloat(completed_records) / total_for_field * 100, 1) as completion_rate
    WHERE field_name IS NOT NULL
    RETURN field_name,
           total_for_field as total_records,
           completed_records,
           completion_rate
    ORDER BY completion_rate ASC, field_name ASC
    """

    results = get_database().execute_query(query)

    field_completion = {}
    total_fields = 0

    for record in results:
        field_completion[record["field_name"]] = record["completion_rate"]
        total_fields += 1

    return {
        "field_completion_rates": field_completion,
        "total_fields": total_fields,
        "source": "neo4j_direct_query"
    }

# Neo4j-driven analytics queries for completion rates system

def get_entity_completion_rates() -> Dict[str, Any]:
    """Get completion rates for all workflow entities using separate simple queries"""

    try:
        db = get_database()
        entity_rates = {}

        # ActionRequest completion rates
        ar_query = """
        MATCH (ar:ActionRequest)
        RETURN count(ar) AS total_count,
               count(CASE WHEN ar.title IS NOT NULL AND ar.title <> '' THEN 1 END) AS title_complete,
               count(CASE WHEN ar.initiation_date IS NOT NULL THEN 1 END) AS date_complete,
               count(CASE WHEN ar.stage IS NOT NULL AND ar.stage <> '' THEN 1 END) AS stage_complete
        """
        ar_results = db.execute_query(ar_query)
        if ar_results:
            ar_data = ar_results[0]
            total = ar_data['total_count']
            completed = ar_data['title_complete'] + ar_data['date_complete'] + ar_data['stage_complete']
            total_fields = total * 3
            entity_rates['ActionRequest'] = {
                'total_count': total,
                'completed_fields': completed,
                'total_fields': total_fields,
                'completion_rate': round(completed * 100.0 / total_fields, 1) if total_fields > 0 else 0.0
            }

        # Problem completion rates
        p_query = """
        MATCH (p:Problem)
        RETURN count(p) AS total_count,
               count(CASE WHEN p.what_happened IS NOT NULL AND p.what_happened <> '' THEN 1 END) AS what_complete,
               count(CASE WHEN p.requirement IS NOT NULL AND p.requirement <> '' THEN 1 END) AS req_complete
        """
        p_results = db.execute_query(p_query)
        if p_results:
            p_data = p_results[0]
            total = p_data['total_count']
            completed = p_data['what_complete'] + p_data['req_complete']
            total_fields = total * 2
            entity_rates['Problem'] = {
                'total_count': total,
                'completed_fields': completed,
                'total_fields': total_fields,
                'completion_rate': round(completed * 100.0 / total_fields, 1) if total_fields > 0 else 0.0
            }

        # RootCause completion rates
        rc_query = """
        MATCH (rc:RootCause)
        RETURN count(rc) AS total_count,
               count(CASE WHEN rc.root_cause IS NOT NULL AND rc.root_cause <> '' THEN 1 END) AS cause_complete,
               count(CASE WHEN rc.objective_evidence IS NOT NULL AND rc.objective_evidence <> '' THEN 1 END) AS evidence_complete
        """
        rc_results = db.execute_query(rc_query)
        if rc_results:
            rc_data = rc_results[0]
            total = rc_data['total_count']
            completed = rc_data['cause_complete'] + rc_data['evidence_complete']
            total_fields = total * 2
            entity_rates['RootCause'] = {
                'total_count': total,
                'completed_fields': completed,
                'total_fields': total_fields,
                'completion_rate': round(completed * 100.0 / total_fields, 1) if total_fields > 0 else 0.0
            }

        # ActionPlan completion rates
        ap_query = """
        MATCH (ap:ActionPlan)
        RETURN count(ap) AS total_count,
               count(CASE WHEN ap.action_plan IS NOT NULL AND ap.action_plan <> '' THEN 1 END) AS plan_complete,
               count(CASE WHEN ap.due_date IS NOT NULL THEN 1 END) AS date_complete
        """
        ap_results = db.execute_query(ap_query)
        if ap_results:
            ap_data = ap_results[0]
            total = ap_data['total_count']
            completed = ap_data['plan_complete'] + ap_data['date_complete']
            total_fields = total * 2
            entity_rates['ActionPlan'] = {
                'total_count': total,
                'completed_fields': completed,
                'total_fields': total_fields,
                'completion_rate': round(completed * 100.0 / total_fields, 1) if total_fields > 0 else 0.0
            }

        # Verification completion rates
        v_query = """
        MATCH (v:Verification)
        RETURN count(v) AS total_count,
               count(CASE WHEN v.is_action_plan_effective IS NOT NULL THEN 1 END) AS effective_complete,
               count(CASE WHEN v.action_plan_verification_date IS NOT NULL THEN 1 END) AS date_complete
        """
        v_results = db.execute_query(v_query)
        if v_results:
            v_data = v_results[0]
            total = v_data['total_count']
            completed = v_data['effective_complete'] + v_data['date_complete']
            total_fields = total * 2
            entity_rates['Verification'] = {
                'total_count': total,
                'completed_fields': completed,
                'total_fields': total_fields,
                'completion_rate': round(completed * 100.0 / total_fields, 1) if total_fields > 0 else 0.0
            }

        return entity_rates

    except Exception as e:
        logger.error(f"Error getting entity completion rates: {e}")
        return {}

def get_facility_action_statistics(facility_id: str = None) -> Dict[str, Any]:
    """Get facility action statistics using direct Neo4j aggregation"""

    if facility_id:
        # Single facility analysis
        query = """
        MATCH (f:Facility {facility_id: $facility_id})
        WHERE NOT '_SchemaTemplate' IN labels(f)
        OPTIONAL MATCH (f)<-[:BELONGS_TO]-(ar:ActionRequest)
        OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
        OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)

        WITH f, ar, p, rc, ap, v
        // Calculate workflow completion based on progression through stages
        WITH f,
             count(DISTINCT ar) AS total_action_requests,
             count(DISTINCT p) AS total_problems,
             count(DISTINCT rc) AS total_root_causes,
             count(DISTINCT ap) AS total_action_plans,
             count(DISTINCT v) AS total_verifications,
             // Completion rate: ActionRequests that reached ActionPlan stage
             count(DISTINCT CASE WHEN ap IS NOT NULL THEN ar END) AS completed_to_plan,
             // Effectiveness rate: ActionPlans that reached Verification stage
             count(DISTINCT CASE WHEN v IS NOT NULL THEN ap END) AS completed_to_verification

        RETURN {
            facility_id: COALESCE(f.facility_id, f.name, 'unknown'),
            facility_name: COALESCE(f.facility_name, f.name, 'Unknown Facility'),
            total_action_requests: total_action_requests,
            total_problems: total_problems,
            total_root_causes: total_root_causes,
            total_action_plans: total_action_plans,
            total_verifications: total_verifications,
            completed_action_plans: completed_to_plan,
            effective_verifications: completed_to_verification,
            completion_rate: CASE
                WHEN total_action_requests > 0
                THEN round(completed_to_plan * 100.0 / total_action_requests, 1)
                ELSE 0.0
            END,
            effectiveness_rate: CASE
                WHEN total_action_plans > 0
                THEN round(completed_to_verification * 100.0 / total_action_plans, 1)
                ELSE 0.0
            END
        } AS facility_stats
        """
        params = {"facility_id": facility_id}
    else:
        # All facilities analysis
        query = """
        MATCH (f:Facility)
        WHERE NOT '_SchemaTemplate' IN labels(f)
        OPTIONAL MATCH (f)<-[:BELONGS_TO]-(ar:ActionRequest)
        OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
        OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)

        WITH f,
             count(DISTINCT ar) AS facility_action_requests,
             count(DISTINCT p) AS facility_problems,
             count(DISTINCT rc) AS facility_root_causes,
             count(DISTINCT ap) AS facility_action_plans,
             count(DISTINCT v) AS facility_verifications,
             // Completion rate: ActionRequests that reached ActionPlan stage
             count(DISTINCT CASE WHEN ap IS NOT NULL THEN ar END) AS facility_completed_plans,
             // Effectiveness rate: ActionPlans that reached Verification stage
             count(DISTINCT CASE WHEN v IS NOT NULL THEN ap END) AS facility_effective_verifications

        RETURN {
            facilities: collect({
                facility_id: COALESCE(f.facility_id, f.name, 'unknown'),
                facility_name: COALESCE(f.facility_name, f.name, 'Unknown Facility'),
                total_action_requests: facility_action_requests,
                total_problems: facility_problems,
                total_root_causes: facility_root_causes,
                total_action_plans: facility_action_plans,
                total_verifications: facility_verifications,
                completed_action_plans: facility_completed_plans,
                effective_verifications: facility_effective_verifications,
                completion_rate: CASE
                    WHEN facility_action_requests > 0
                    THEN round(facility_completed_plans * 100.0 / facility_action_requests, 1)
                    ELSE 0.0
                END,
                effectiveness_rate: CASE
                    WHEN facility_action_plans > 0
                    THEN round(facility_effective_verifications * 100.0 / facility_action_plans, 1)
                    ELSE 0.0
                END
            }),
            aggregate: {
                total_facilities: count(f),
                total_action_requests: sum(facility_action_requests),
                total_problems: sum(facility_problems),
                total_root_causes: sum(facility_root_causes),
                total_action_plans: sum(facility_action_plans),
                total_verifications: sum(facility_verifications),
                total_completed_plans: sum(facility_completed_plans),
                total_effective_verifications: sum(facility_effective_verifications),
                average_completion_rate: CASE
                    WHEN sum(facility_action_requests) > 0
                    THEN round(sum(facility_completed_plans) * 100.0 / sum(facility_action_requests), 1)
                    ELSE 0.0
                END,
                average_effectiveness_rate: CASE
                    WHEN sum(facility_action_plans) > 0
                    THEN round(sum(facility_effective_verifications) * 100.0 / sum(facility_action_plans), 1)
                    ELSE 0.0
                END
            }
        } AS facility_statistics
        """
        params = {}

    try:
        results = get_database().execute_query(query, **params)
        if results and len(results) > 0:
            return results[0].get('facility_statistics', {}) if not facility_id else results[0].get('facility_stats', {})
        return {}
    except Exception as e:
        logger.error(f"Error getting facility action statistics: {e}")
        return {}

# Backward compatibility functions
def get_incident_chain(action_request_id: str) -> Dict[str, Any]:
    """Get complete incident workflow chain with causal intelligence"""
    query = """
    MATCH (ar:ActionRequest {actionrequest_id: $action_request_id})
    OPTIONAL MATCH (ar)-[:BELONGS_TO]->(f:Facility)
    OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)
    OPTIONAL MATCH (p)<-[:ANALYZES]-(rc:RootCause)
    OPTIONAL MATCH (rc)<-[:RESOLVES]-(ap:ActionPlan)
    OPTIONAL MATCH (ap)<-[:VALIDATES]-(v:Verification)

    RETURN ar.actionrequest_id AS request_id,
           ar.action_request_number AS request_number,
           ar.title AS title,
           ar.initiation_date AS date,
           ar.stage AS stage,
           f.facility_id AS facility_id,

           p.problem_id AS problem_id,
           p.what_happened AS what_happened,
           p.requirement AS requirement,

           rc.rootcause_id AS cause_id,
           rc.root_cause AS primary_cause,
           rc.root_cause_tail AS secondary_cause,
           rc.objective_evidence AS objective_evidence,

           ap.actionplan_id AS plan_id,
           ap.action_plan AS action_plan,
           ap.recommended_action AS recommended_action,
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

# Legacy function aliases for backward compatibility
get_department = get_operational_performance_dashboard
get_effectiveness_stats = get_root_cause_intelligence_summary
get_incident_counts_by_category = get_operational_performance_dashboard
get_root_cause_frequency = get_causal_correlation_matrix
get_assets = lambda problem_id: []  # Simplified - no longer needed

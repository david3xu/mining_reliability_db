#!/usr/bin/env python3
"""
Quality Intelligence Engine - Data Quality Assessment
Focused analysis of data completeness, consistency, and operational quality.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from configs.environment import (
    get_entity_connections,
    get_entity_names,
    get_entity_primary_key,
)
from mine_core.database.query_manager import get_query_manager
from mine_core.shared.common import handle_error
from mine_core.business.intelligence_models import IntelligenceResult

logger = logging.getLogger(__name__)


class QualityIntelligence:
    """Data quality assessment and operational intelligence"""

    def __init__(self):
        self.query_manager = get_query_manager()

    def analyze_data_quality(self) -> Dict[str, Any]:
        """Comprehensive data quality assessment"""
        try:
            # Get workflow completion rates
            workflow_result = self.query_manager.get_workflow_completion_rates()

            if not workflow_result.success or not workflow_result.data:
                return self._create_empty_result("data_quality")

            completion_data = workflow_result.data[0]

            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(completion_data)

            # Analyze entity completeness
            entity_completeness_result = self._analyze_entity_completeness()
            entity_completeness = entity_completeness_result.data

            quality_data = {
                "workflow_completeness": quality_metrics,
                "entity_completeness": entity_completeness,
                "overall_score": quality_metrics.get("overall_score", 0.0),
                "recommendations": self._generate_quality_recommendations(quality_metrics, entity_completeness),
            }

            return IntelligenceResult(
                analysis_type="data_quality",
                data=quality_data,
                metadata={
                    "entities_analyzed": len(entity_completeness),
                    "workflow_stages": 5,
                },
                quality_score=quality_data["overall_score"],
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "data quality analysis")
            return self._create_empty_result("data_quality")

    def analyze_facility_completeness(self, facility_id: str = None) -> Dict[str, Any]:
        """Schema-driven completeness analysis for facilities"""
        try:
            if facility_id:
                analysis = self._analyze_single_facility_completeness(facility_id)
            else:
                analysis = self._analyze_all_facilities_completeness()

            quality_score = 1.0 if analysis and not analysis.get("error") else 0.0

            return IntelligenceResult(
                analysis_type="facility_completeness",
                data=analysis,
                metadata={"facility_filter": facility_id or "all_facilities"},
                quality_score=quality_score,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, f"facility completeness analysis for {facility_id or 'all'}")
            return self._create_empty_result("facility_completeness")

    def get_missing_data_impact(self) -> Dict[str, Any]:
        """Schema-driven missing data impact analysis"""
        try:
            # Get entity names from schema
            entity_names = get_entity_names()
            entity_connections = get_entity_connections()

            ar_entity = entity_names.get("ActionRequest", "ActionRequest")
            problem_entity = entity_names.get("Problem", "Problem")
            rootcause_entity = entity_names.get("RootCause", "RootCause")
            actionplan_entity = entity_names.get("ActionPlan", "ActionPlan")
            verification_entity = entity_names.get("Verification", "Verification")

            # Build impact analysis query
            impact_query = f"""
            MATCH (ar:{ar_entity})
            OPTIONAL MATCH (ar)-[:IDENTIFIED_IN]->(p:{problem_entity})
            OPTIONAL MATCH (p)<-[:ANALYZES]-(rc:{rootcause_entity})
            OPTIONAL MATCH (rc)-[:RESOLVES]->(ap:{actionplan_entity})
            OPTIONAL MATCH (ap)-[:VALIDATES]->(v:{verification_entity})

            WITH ar,
                 CASE WHEN p IS NOT NULL AND rc IS NOT NULL AND ap IS NOT NULL AND v IS NOT NULL
                      THEN 'complete' ELSE 'incomplete' END as chain_status,
                 CASE WHEN p.what_happened IS NOT NULL AND rc.root_cause IS NOT NULL
                      AND ap.action_plan IS NOT NULL AND v.is_action_plan_effective IS NOT NULL
                      THEN 'usable' ELSE 'not_usable' END as usability_status

            RETURN chain_status, usability_status, count(*) as count
            """

            impact_results = self.query_manager.execute_query(impact_query)
            analysis = self._process_impact_results(impact_results.data)

            return IntelligenceResult(
                analysis_type="missing_data_impact",
                data=analysis,
                metadata={"total_incidents_analyzed": analysis.get("total_incidents", 0)},
                quality_score=analysis.get("usability_score", 0.0),
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "missing data impact analysis")
            return self._create_empty_result("missing_data_impact")

    def analyze_action_request_facility_statistics(self) -> Dict[str, Any]:
        """Analyze ActionRequest statistics by facility"""
        try:
            facility_stats_query = """
            MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
            WHERE NOT '_SchemaTemplate' IN labels(ar)
            WITH f.facility_id AS facility_id,
                 count(ar) AS total_records,
                 count(DISTINCT ar.action_request_number) AS unique_actions,
                 collect(ar.action_request_number) AS action_numbers
            WITH facility_id, total_records, unique_actions, action_numbers,
                 toFloat(total_records) / unique_actions AS records_per_action

            UNWIND action_numbers AS action_num
            WITH facility_id, total_records, unique_actions, records_per_action, action_num
            MATCH (ar:ActionRequest {action_request_number: action_num})
            WITH facility_id, total_records, unique_actions, records_per_action,
                 action_num, count(ar) AS records_for_action
            WITH facility_id, total_records, unique_actions, records_per_action,
                 max(records_for_action) AS max_records_per_action

            RETURN facility_id, total_records, unique_actions,
                   round(records_per_action, 1) AS records_per_action,
                   max_records_per_action
            ORDER BY facility_id
            """

            result = self.query_manager.execute_query(facility_stats_query)

            if not result or not result.data:
                return self._create_empty_result("action_request_statistics")

            facility_data = result.data
            summary_totals = self._calculate_facility_summary(facility_data)

            analysis_data = {
                "facility_statistics": facility_data,
                "summary_totals": summary_totals,
            }

            return IntelligenceResult(
                analysis_type="action_request_statistics",
                data=analysis_data,
                metadata={"facilities_analyzed": len(facility_data)},
                quality_score=1.0 if facility_data else 0.0,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "action request facility statistics analysis")
            return self._create_empty_result("action_request_statistics")

    # Quality Analysis Methods

    def _calculate_quality_metrics(self, completion_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall data quality metrics"""
        total_requests = completion_data.get("total_requests", 0)
        problems_defined = completion_data.get("problems_defined", 0)
        causes_analyzed = completion_data.get("causes_analyzed", 0)
        plans_developed = completion_data.get("plans_developed", 0)
        plans_verified = completion_data.get("plans_verified", 0)

        # Calculate completion rates
        rates = self._calculate_completion_rates(
            total_requests, problems_defined, causes_analyzed, plans_developed, plans_verified
        )

        overall_completion_rate = sum(rates) / len(rates)
        overall_status = overall_completion_rate > 0.7

        return {
            "overall_status": overall_status,
            "overall_score": round(overall_completion_rate * 100, 2),
            "details": {
                "total_requests": total_requests,
                "problems_defined": problems_defined,
                "causes_analyzed": causes_analyzed,
                "plans_developed": plans_developed,
                "plans_verified": plans_verified,
                "problem_completion_rate": round(rates[0] * 100, 2),
                "cause_completion_rate": round(rates[1] * 100, 2),
                "plan_completion_rate": round(rates[2] * 100, 2),
                "verification_completion_rate": round(rates[3] * 100, 2),
            },
            "completeness_score": round(overall_completion_rate * 100, 2),
            "consistency_score": 0.0,
            "freshness_score": 0.0,
        }

    def _calculate_completion_rates(self, total_requests, problems_defined, causes_analyzed, plans_developed, plans_verified):
        """Calculate completion rates for each workflow stage"""
        problem_completion = (problems_defined / total_requests) if total_requests > 0 else 0
        cause_completion = (causes_analyzed / problems_defined) if problems_defined > 0 else 0
        plan_completion = (plans_developed / causes_analyzed) if causes_analyzed > 0 else 0
        verification_completion = (plans_verified / plans_developed) if plans_developed > 0 else 0

        return [problem_completion, cause_completion, plan_completion, verification_completion]

    def _analyze_entity_completeness(self) -> Dict[str, Any]:
        """Analyze completeness of key entities"""
        entity_completeness_data = {}
        entity_types = ["ActionRequest", "Problem", "RootCause", "ActionPlan", "Verification"]

        for entity_type in entity_types:
            total_count = self.query_manager.get_entity_count(entity_type)
            meaningful_data_count = self.query_manager.get_entity_count(entity_type)

            completeness_percentage = (meaningful_data_count / total_count) * 100 if total_count > 0 else 0

            entity_completeness_data[entity_type] = {
                "total_count": total_count,
                "meaningful_data_count": meaningful_data_count,
                "completeness_percentage": round(completeness_percentage, 2),
                "is_complete": completeness_percentage > 80,
            }

        return IntelligenceResult(
            analysis_type="_analyze_entity_completeness",
            data=entity_completeness_data,
            metadata={
                "total_entities_analyzed": len(entity_types),
                "timestamp": datetime.now().isoformat()
            },
            quality_score=self._calculate_overall_completeness_score(entity_completeness_data),
            generated_at=datetime.now().isoformat()
        )

    def _process_impact_results(self, impact_results: List[Dict]) -> Dict[str, Any]:
        """Process impact analysis query results"""
        total_incidents = sum(item["count"] for item in impact_results)
        complete_chain_count = 0
        incomplete_chain_count = 0
        usable_data_count = 0
        not_usable_data_count = 0

        for item in impact_results:
            if item["chain_status"] == "complete":
                complete_chain_count += item["count"]
            else:
                incomplete_chain_count += item["count"]

            if item["usability_status"] == "usable":
                usable_data_count += item["count"]
            else:
                not_usable_data_count += item["count"]

        completeness_score = (complete_chain_count / total_incidents) if total_incidents > 0 else 0.0
        usability_score = (usable_data_count / total_incidents) if total_incidents > 0 else 0.0

        return IntelligenceResult(
            analysis_type="_process_impact_results",
            data={
                "total_incidents": total_incidents,
                "complete_chains": complete_chain_count,
                "incomplete_chains": incomplete_chain_count,
                "usable_data": usable_data_count,
                "not_usable_data": not_usable_data_count,
                "completeness_score": round(completeness_score, 2),
                "usability_score": round(usability_score, 2)
            },
            metadata={
                "timestamp": datetime.now().isoformat()
            },
            quality_score=round(usability_score, 2),
            generated_at=datetime.now().isoformat()
        )

    def _calculate_facility_summary(self, facility_data: List[Dict]) -> Dict[str, Any]:
        """Calculate summary totals for facility statistics"""
        total_records = sum(f.get("total_records", 0) for f in facility_data)
        total_unique_actions = sum(f.get("unique_actions", 0) for f in facility_data)

        return IntelligenceResult(
            analysis_type="_calculate_facility_summary",
            data={
                "total_records_across_facilities": total_records,
                "total_unique_actions_across_facilities": total_unique_actions,
                "average_records_per_action": round(total_records / total_unique_actions, 1) if total_unique_actions > 0 else 0.0,
                "facilities_count": len(facility_data)
            },
            metadata={
                "timestamp": datetime.now().isoformat()
            },
            quality_score=1.0 if total_records > 0 else 0.0,
            generated_at=datetime.now().isoformat()
        )

    def _analyze_single_facility_completeness(self, facility_id: str) -> Dict[str, Any]:
        """Analyze completeness for a single facility based on schema"""
        stats = self._get_facility_completeness_stats(facility_id)
        if not stats:
            return IntelligenceResult(
                analysis_type="_analyze_single_facility_completeness",
                data={
                    "facility_id": facility_id,
                    "error": "No data found for facility"
                },
                metadata={},
                quality_score=0.0,
                generated_at=datetime.now().isoformat()
            )

        total_expected_records = self._get_total_expected_records_for_facility(facility_id)
        completeness_metrics = self._calculate_completeness_metrics(stats, total_expected_records)

        return IntelligenceResult(
            analysis_type="_analyze_single_facility_completeness",
            data={
                "facility_id": facility_id,
                "overall_completeness": completeness_metrics["overall_percentage"],
                "details": completeness_metrics,
                "insights": self._generate_quality_insights(completeness_metrics)
            },
            metadata={
                "timestamp": datetime.now().isoformat()
            },
            quality_score=completeness_metrics["overall_percentage"] / 100.0,
            generated_at=datetime.now().isoformat()
        )

    def _get_facility_completeness_stats(self, facility_id: str) -> Dict[str, Any]:
        """Retrieve raw completeness statistics for a single facility"""
        query = f"""
        MATCH (f:Facility {{facility_id: $facility_id}})
        OPTIONAL MATCH (f)<-[:BELONGS_TO]-(ar:ActionRequest)
        OPTIONAL MATCH (ar)-[:IDENTIFIED_IN]->(p:Problem)
        OPTIONAL MATCH (p)<-[:ANALYZES]-(rc:RootCause)
        OPTIONAL MATCH (rc)-[:RESOLVES]->(ap:ActionPlan)
        OPTIONAL MATCH (ap)-[:VALIDATES]->(v:Verification)

        RETURN count(DISTINCT ar) AS action_requests,
               count(DISTINCT p) AS problems,
               count(DISTINCT rc) AS root_causes,
               count(DISTINCT ap) AS action_plans,
               count(DISTINCT v) AS verifications
        """
        params = {"facility_id": facility_id}
        result = self.query_manager.execute_query(query, params)
        return result.data[0] if result.success and result.data else {}

    def _get_total_expected_records_for_facility(self, facility_id: str) -> int:
        """Simulates fetching the expected number of records for a facility.
        In a real scenario, this would come from a configuration or a baseline.
        """
        # Placeholder: In a real system, this could be from a config file or a data model.
        return 100 # Example baseline

    def _calculate_completeness_metrics(self, stats: Dict[str, Any], total: int) -> Dict[str, Any]:
        """Calculate completeness percentages based on retrieved stats"""
        metrics = {}
        total_populated_fields = 0
        total_possible_fields = 0

        # Define the fields to check and their ideal counts
        fields_to_check = {
            "action_requests": stats.get("action_requests", 0),
            "problems": stats.get("problems", 0),
            "root_causes": stats.get("root_causes", 0),
            "action_plans": stats.get("action_plans", 0),
            "verifications": stats.get("verifications", 0),
        }

        for field, count in fields_to_check.items():
            percentage = (count / total) * 100 if total > 0 else 0
            metrics[f"{field}_percentage"] = round(percentage, 2)
            if count > 0: # Consider a field 'populated' if its count is greater than 0
                total_populated_fields += 1
            total_possible_fields += 1 # Each field represents a possible field

        overall_percentage = (total_populated_fields / total_possible_fields) * 100 if total_possible_fields > 0 else 0

        metrics["overall_percentage"] = round(overall_percentage, 2)
        metrics["is_fully_complete"] = overall_percentage >= 95 # Define 'fully complete' threshold

        return metrics

    def _analyze_all_facilities_completeness(self) -> Dict[str, Any]:
        """Analyze completeness across all facilities"""
        all_facility_ids_result = self.query_manager.get_all_facility_ids()
        if not all_facility_ids_result.success or not all_facility_ids_result.data:
            return IntelligenceResult(
                analysis_type="_analyze_all_facilities_completeness",
                data={
                    "error": "No facilities found"
                },
                metadata={},
                quality_score=0.0,
                generated_at=datetime.now().isoformat()
            )

        all_facilities_completeness = []
        for record in all_facility_ids_result.data:
            facility_id = record.get("facility_id")
            if facility_id:
                single_facility_analysis = self._analyze_single_facility_completeness(facility_id)
                all_facilities_completeness.append(single_facility_analysis.data) # Append the data part of the IntelligenceResult

        total_overall_completeness = sum(
            f.get("overall_completeness", 0) for f in all_facilities_completeness
        )
        average_overall_completeness = (
            total_overall_completeness / len(all_facilities_completeness)
            if all_facilities_completeness
            else 0.0
        )

        return IntelligenceResult(
            analysis_type="_analyze_all_facilities_completeness",
            data={
                "facilities_count": len(all_facilities_completeness),
                "average_overall_completeness": round(average_overall_completeness, 2),
                "facility_details": all_facilities_completeness,
                "insights": self._generate_cross_facility_insights(all_facilities_completeness)
            },
            metadata={
                "timestamp": datetime.now().isoformat()
            },
            quality_score=average_overall_completeness / 100.0,
            generated_at=datetime.now().isoformat()
        )

    def _generate_quality_recommendations(self, quality_metrics: Dict, entity_completeness: Dict) -> List[str]:
        """Generate recommendations based on quality analysis results"""
        recommendations = []

        if quality_metrics.get("overall_score", 0) < 70:
            recommendations.append("Overall data quality is low. Focus on improving data entry and workflow adherence.")

        for entity, data in entity_completeness.items():
            if not data.get("is_complete"):
                recommendations.append(f"Improve completeness for {entity} entity. Current: {data.get('completeness_percentage', 0)}%")

        return recommendations if recommendations else ["Data quality is generally good. Continue monitoring."]

    def _generate_quality_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate insights from a given quality analysis result"""
        insights = []
        if analysis.get("overall_completeness", 0) < 60:
            insights.append("Critical completeness gaps identified. Immediate data entry review is recommended.")
        elif analysis.get("overall_completeness", 0) < 85:
            insights.append("Moderate completeness issues. Review data input processes for improvements.")
        else:
            insights.append("Good data completeness. Maintain current data capture standards.")

        for field, percentage in analysis.items():
            if "_percentage" in field and percentage < 50:
                insights.append(f"Low completeness in {field.replace('_percentage', '')}. Focus on capturing this data.")

        return insights

    def _generate_cross_facility_insights(self, facilities: List[Dict]) -> Dict[str, Any]:
        """Generate cross-facility insights based on completeness data"""
        if not facilities:
            return {"overview": "No facility data to analyze.", "top_performers": [], "low_performers": []}

        sorted_facilities = sorted(facilities, key=lambda x: x.get("overall_completeness", 0), reverse=True)

        top_performers = [{
            "facility_id": f.get("facility_id"),
            "completeness": f.get("overall_completeness")
        } for f in sorted_facilities[:3]]

        low_performers = [{
            "facility_id": f.get("facility_id"),
            "completeness": f.get("overall_completeness")
        } for f in sorted_facilities[-3:]]

        return IntelligenceResult(
            analysis_type="_generate_cross_facility_insights",
            data={
                "overview": f"Analyzed {len(facilities)} facilities. Average completeness: {sum(f.get('overall_completeness', 0) for f in facilities) / len(facilities):.2f}%",
                "top_performers": top_performers,
                "low_performers": low_performers
            },
            metadata={
                "timestamp": datetime.now().isoformat()
            },
            quality_score=sum(f.get("overall_completeness", 0) for f in facilities) / len(facilities) / 100.0 if facilities else 0.0,
            generated_at=datetime.now().isoformat()
        )

    def _create_empty_result(self, analysis_type: str) -> IntelligenceResult:
        """Create empty result for any analysis type"""
        return IntelligenceResult(
            analysis_type=analysis_type,
            data={},
            metadata={"error": "Analysis failed"},
            quality_score=0.0,
            generated_at=datetime.now().isoformat()
        )

    def _calculate_overall_completeness_score(self, entity_completeness_data: Dict[str, Any]) -> float:
        """Calculate an overall completeness score from entity completeness data."""
        if not entity_completeness_data:
            return 0.0

        total_percentage = sum(data.get("completeness_percentage", 0) for data in entity_completeness_data.values())
        return round(total_percentage / len(entity_completeness_data), 2)

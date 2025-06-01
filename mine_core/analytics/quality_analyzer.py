#!/usr/bin/env python3
"""
Schema-Driven Data Quality Analyzer
All entity names, relationships, and fields sourced from model_schema.json
"""

import logging
from typing import Dict, List, Any, Tuple
from mine_core.database.db import get_database
from configs.environment import get_schema

logger = logging.getLogger(__name__)

class QualityAnalyzer:
    """Schema-driven data quality analysis for engineer root cause effectiveness"""

    def __init__(self):
        self.db = get_database()
        self.schema = get_schema()

        # Extract schema components
        self.entities = {e["name"]: e for e in self.schema.get("entities", [])}
        self.relationships = {r["type"]: r for r in self.schema.get("relationships", [])}

        # Cache entity and relationship mappings
        self.entity_names = {name: name for name in self.entities.keys()}
        self.relationship_types = {r["type"]: r for r in self.schema.get("relationships", [])}

    def _get_primary_key(self, entity_name: str) -> str:
        """Get primary key from schema"""
        entity = self.entities.get(entity_name, {})
        properties = entity.get("properties", {})

        for prop_name, prop_info in properties.items():
            if prop_info.get("primary_key", False):
                return prop_name
        return f"{entity_name.lower()}_id"  # fallback

    def _get_relationship_type(self, from_entity: str, to_entity: str) -> str:
        """Get relationship type from schema"""
        for rel in self.schema.get("relationships", []):
            if rel.get("from") == from_entity and rel.get("to") == to_entity:
                return rel["type"]
        return "RELATED_TO"  # fallback

    def analyze_facility_completeness(self, facility_id: str = None) -> Dict[str, Any]:
        """Schema-driven completeness analysis"""

        if facility_id:
            return self._analyze_single_facility(facility_id)
        else:
            return self._analyze_all_facilities()

    def _analyze_single_facility(self, facility_id: str) -> Dict[str, Any]:
        """Schema-driven single facility analysis"""

        # Get entity names from schema
        facility_entity = self.entity_names.get("Facility", "Facility")
        ar_entity = self.entity_names.get("ActionRequest", "ActionRequest")
        facility_pk = self._get_primary_key("Facility")
        belongs_to_rel = self._get_relationship_type("ActionRequest", "Facility")

        # Schema-driven facility overview query
        facility_query = f"""
        MATCH (f:{facility_entity} {{{facility_pk}: $facility_id}})<-[:{belongs_to_rel}]-(ar:{ar_entity})
        RETURN f.facility_name as name, count(ar) as total_incidents
        """

        facility_result = self.db.execute_query(facility_query, facility_id=facility_id)

        if not facility_result:
            return {"error": f"Facility {facility_id} not found"}

        facility_info = facility_result[0]

        # Schema-driven completeness analysis
        problem_entity = self.entity_names.get("Problem", "Problem")
        rootcause_entity = self.entity_names.get("RootCause", "RootCause")
        actionplan_entity = self.entity_names.get("ActionPlan", "ActionPlan")
        verification_entity = self.entity_names.get("Verification", "Verification")

        identified_rel = self._get_relationship_type("Problem", "ActionRequest")
        analyzes_rel = self._get_relationship_type("RootCause", "Problem")
        resolves_rel = self._get_relationship_type("ActionPlan", "RootCause")
        validates_rel = self._get_relationship_type("Verification", "ActionPlan")

        completeness_query = f"""
        MATCH (f:{facility_entity} {{{facility_pk}: $facility_id}})<-[:{belongs_to_rel}]-(ar:{ar_entity})
        OPTIONAL MATCH (ar)-[:{identified_rel}]->(p:{problem_entity})
        OPTIONAL MATCH (p)<-[:{analyzes_rel}]-(rc:{rootcause_entity})
        OPTIONAL MATCH (rc)-[:{resolves_rel}]->(ap:{actionplan_entity})
        OPTIONAL MATCH (ap)-[:{validates_rel}]->(v:{verification_entity})

        RETURN
            count(ar) as total_requests,
            count(ar.title) as has_title,
            count(ar.stage) as has_stage,
            count(ar.categories) as has_categories,
            count(p) as has_problem,
            count(p.what_happened) as has_problem_description,
            count(rc) as has_root_cause,
            count(rc.root_cause) as has_cause_description,
            count(ap) as has_action_plan,
            count(ap.action_plan) as has_plan_description,
            count(v) as has_verification,
            count(v.is_action_plan_effective) as has_effectiveness_data
        """

        completeness_result = self.db.execute_query(completeness_query, facility_id=facility_id)
        stats = completeness_result[0] if completeness_result else {}

        # Calculate completeness percentages
        total = stats.get('total_requests', 0)
        if total == 0:
            return {"error": f"No data found for facility {facility_id}"}

        completeness_analysis = {
            "facility_name": facility_info['name'],
            "total_incidents": total,
            "completeness_metrics": {
                "basic_info": {
                    "title": round((stats.get('has_title', 0) / total) * 100, 1),
                    "stage": round((stats.get('has_stage', 0) / total) * 100, 1),
                    "categories": round((stats.get('has_categories', 0) / total) * 100, 1)
                },
                "workflow_chain": {
                    "has_problem": round((stats.get('has_problem', 0) / total) * 100, 1),
                    "has_root_cause": round((stats.get('has_root_cause', 0) / total) * 100, 1),
                    "has_action_plan": round((stats.get('has_action_plan', 0) / total) * 100, 1),
                    "has_verification": round((stats.get('has_verification', 0) / total) * 100, 1)
                },
                "engineer_critical": {
                    "problem_description": round((stats.get('has_problem_description', 0) / total) * 100, 1),
                    "cause_description": round((stats.get('has_cause_description', 0) / total) * 100, 1),
                    "plan_description": round((stats.get('has_plan_description', 0) / total) * 100, 1),
                    "effectiveness_data": round((stats.get('has_effectiveness_data', 0) / total) * 100, 1)
                }
            }
        }

        completeness_analysis["quality_insights"] = self._generate_quality_insights(completeness_analysis)

        return completeness_analysis

    def _analyze_all_facilities(self) -> Dict[str, Any]:
        """Schema-driven multi-facility comparison"""

        facility_entity = self.entity_names.get("Facility", "Facility")
        facility_pk = self._get_primary_key("Facility")

        facilities_query = f"""
        MATCH (f:{facility_entity})
        WHERE NOT '_SchemaTemplate' IN labels(f)
        RETURN f.{facility_pk} as id, f.facility_name as name
        ORDER BY f.facility_name
        """
        facilities = self.db.execute_query(facilities_query)

        comparison = {
            "facilities": [],
            "cross_facility_insights": {}
        }

        for facility in facilities:
            facility_analysis = self._analyze_single_facility(facility['id'])
            if 'error' not in facility_analysis:
                comparison["facilities"].append(facility_analysis)

        comparison["cross_facility_insights"] = self._generate_cross_facility_insights(comparison["facilities"])

        return comparison

    def get_missing_data_impact(self) -> Dict[str, Any]:
        """Schema-driven missing data impact analysis"""

        # Get entity names from schema
        ar_entity = self.entity_names.get("ActionRequest", "ActionRequest")
        problem_entity = self.entity_names.get("Problem", "Problem")
        rootcause_entity = self.entity_names.get("RootCause", "RootCause")
        actionplan_entity = self.entity_names.get("ActionPlan", "ActionPlan")
        verification_entity = self.entity_names.get("Verification", "Verification")

        # Get relationship types from schema
        identified_rel = self._get_relationship_type("Problem", "ActionRequest")
        analyzes_rel = self._get_relationship_type("RootCause", "Problem")
        resolves_rel = self._get_relationship_type("ActionPlan", "RootCause")
        validates_rel = self._get_relationship_type("Verification", "ActionPlan")

        impact_query = f"""
        MATCH (ar:{ar_entity})
        OPTIONAL MATCH (ar)-[:{identified_rel}]->(p:{problem_entity})
        OPTIONAL MATCH (p)<-[:{analyzes_rel}]-(rc:{rootcause_entity})
        OPTIONAL MATCH (rc)-[:{resolves_rel}]->(ap:{actionplan_entity})
        OPTIONAL MATCH (ap)-[:{validates_rel}]->(v:{verification_entity})

        WITH ar,
             CASE WHEN p IS NOT NULL AND rc IS NOT NULL AND ap IS NOT NULL AND v IS NOT NULL
                  THEN 'complete' ELSE 'incomplete' END as chain_status,
             CASE WHEN p.what_happened IS NOT NULL AND rc.root_cause IS NOT NULL
                  AND ap.action_plan IS NOT NULL AND v.is_action_plan_effective IS NOT NULL
                  THEN 'usable' ELSE 'not_usable' END as usability_status

        RETURN
            chain_status,
            usability_status,
            count(*) as count
        """

        impact_results = self.db.execute_query(impact_query)

        analysis = {
            "chain_completeness": {},
            "usability_assessment": {},
            "engineer_impact": {}
        }

        total_incidents = sum(result['count'] for result in impact_results)

        for result in impact_results:
            chain_key = result['chain_status']
            usable_key = result['usability_status']
            count = result['count']
            percentage = round((count / total_incidents) * 100, 1)

            if chain_key not in analysis["chain_completeness"]:
                analysis["chain_completeness"][chain_key] = 0
            analysis["chain_completeness"][chain_key] += percentage

            if usable_key not in analysis["usability_assessment"]:
                analysis["usability_assessment"][usable_key] = 0
            analysis["usability_assessment"][usable_key] += percentage

        usable_percentage = analysis["usability_assessment"].get("usable", 0)
        analysis["engineer_impact"] = {
            "usable_for_analysis": usable_percentage,
            "data_quality_impact": round(100 - usable_percentage, 1),
            "recommendation": "Focus on completing workflow chains for engineer effectiveness"
        }

        return analysis

    def _generate_quality_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable insights"""
        insights = []
        metrics = analysis["completeness_metrics"]

        workflow = metrics["workflow_chain"]
        if workflow["has_root_cause"] < 70:
            insights.append(f"Critical: {100 - workflow['has_root_cause']:.1f}% of incidents lack root cause analysis")

        if workflow["has_verification"] < 50:
            insights.append(f"Warning: {100 - workflow['has_verification']:.1f}% of action plans lack effectiveness verification")

        engineer = metrics["engineer_critical"]
        if engineer["problem_description"] < 80:
            insights.append(f"Impact: {100 - engineer['problem_description']:.1f}% of problems lack clear descriptions")

        if engineer["effectiveness_data"] < 60:
            insights.append(f"Learning Gap: {100 - engineer['effectiveness_data']:.1f}% of solutions lack effectiveness data")

        return insights

    def _generate_cross_facility_insights(self, facilities: List[Dict]) -> Dict[str, Any]:
        """Generate cross-facility comparison insights"""
        if len(facilities) < 2:
            return {}

        insights = {
            "best_performers": {},
            "improvement_opportunities": [],
            "patterns": []
        }

        categories = ["workflow_chain", "engineer_critical"]
        for category in categories:
            best_facility = max(facilities,
                              key=lambda f: sum(f["completeness_metrics"][category].values()))
            worst_facility = min(facilities,
                                key=lambda f: sum(f["completeness_metrics"][category].values()))

            insights["best_performers"][category] = {
                "best": best_facility["facility_name"],
                "worst": worst_facility["facility_name"]
            }

        for facility in facilities:
            metrics = facility["completeness_metrics"]["engineer_critical"]
            if metrics["effectiveness_data"] < 50:
                insights["improvement_opportunities"].append(
                    f"{facility['facility_name']}: Improve solution effectiveness tracking"
                )

        return insights

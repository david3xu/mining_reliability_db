#!/usr/bin/env python3
"""
Workflow Analyzer - EDA for Incident Chain Validation (Schema-Driven)
Investigates workflow completeness patterns for engineer effectiveness
"""

import logging
from typing import Dict, List, Any, Tuple
from mine_core.database.db import get_database
from configs.environment import get_schema

logger = logging.getLogger(__name__)

class WorkflowAnalyzer:
    """Analyzes incident workflow completeness using EDA methodology with schema-driven queries"""

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

    def analyze_workflow_integrity(self, facility_id: str = None) -> Dict[str, Any]:
        """
        EDA Investigation: Analyze incident workflow chain completeness
        Focus: Engineer ability to trace complete incident resolution patterns
        """

        # Step 1: Pattern Discovery - Map workflow chain completeness
        chain_analysis = self._investigate_chain_patterns(facility_id)

        # Step 2: Gap Analysis - Identify critical missing links
        gap_analysis = self._investigate_workflow_gaps(facility_id)

        # Step 3: Impact Assessment - Measure engineer effectiveness impact
        impact_analysis = self._assess_engineer_impact(facility_id)

        return {
            "workflow_patterns": chain_analysis,
            "critical_gaps": gap_analysis,
            "engineer_impact": impact_analysis,
            "recommendations": self._generate_workflow_recommendations(chain_analysis, gap_analysis)
        }

    def _investigate_chain_patterns(self, facility_id: str = None) -> Dict[str, Any]:
        """EDA Step 1: Discover workflow chain completion patterns"""

        # Get entity names from schema
        facility_entity = self.entity_names.get("Facility", "Facility")
        ar_entity = self.entity_names.get("ActionRequest", "ActionRequest")
        problem_entity = self.entity_names.get("Problem", "Problem")
        rootcause_entity = self.entity_names.get("RootCause", "RootCause")
        actionplan_entity = self.entity_names.get("ActionPlan", "ActionPlan")
        verification_entity = self.entity_names.get("Verification", "Verification")

        # Get relationship types from schema
        belongs_to_rel = self._get_relationship_type("ActionRequest", "Facility")
        identified_rel = self._get_relationship_type("Problem", "ActionRequest")
        analyzes_rel = self._get_relationship_type("RootCause", "Problem")
        resolves_rel = self._get_relationship_type("ActionPlan", "RootCause")
        validates_rel = self._get_relationship_type("Verification", "ActionPlan")

        # Get primary key
        facility_pk = self._get_primary_key("Facility")

        # Build facility filter
        facility_filter = f"WHERE f.{facility_pk} = $facility_id" if facility_id else ""
        params = {"facility_id": facility_id} if facility_id else {}

        # Pattern Discovery Query: Complete workflow chains
        chain_query = f"""
        MATCH (f:{facility_entity})<-[:{belongs_to_rel}]-(ar:{ar_entity})
        {facility_filter}

        // Trace complete workflow chain
        OPTIONAL MATCH workflow_path = (ar)-[:{identified_rel}]->(p:{problem_entity})
                                      <-[:{analyzes_rel}]-(rc:{rootcause_entity})
                                      -[:{resolves_rel}]->(ap:{actionplan_entity})
                                      -[:{validates_rel}]->(v:{verification_entity})

        // Pattern classification
        WITH f, ar,
             CASE
                WHEN workflow_path IS NOT NULL THEN 'complete_chain'
                WHEN EXISTS((ar)-[:{identified_rel}]->(p:{problem_entity})<-[:{analyzes_rel}]-(rc:{rootcause_entity})-[:{resolves_rel}]->(ap:{actionplan_entity}))
                    THEN 'partial_chain'
                WHEN EXISTS((ar)-[:{identified_rel}]->(p:{problem_entity}))
                    THEN 'problem_only'
                ELSE 'request_only'
             END as pattern_type

        RETURN f.facility_name as facility,
               pattern_type,
               count(*) as incident_count
        ORDER BY facility, pattern_type
        """

        results = self.db.execute_query(chain_query, **params)

        # EDA Analysis: Pattern frequency distribution
        pattern_analysis = {}
        total_incidents = 0

        for result in results:
            facility = result.get('facility', 'Unknown')
            if facility not in pattern_analysis:
                pattern_analysis[facility] = {}

            pattern_type = result['pattern_type']
            count = result['incident_count']
            pattern_analysis[facility][pattern_type] = count
            total_incidents += count

        # Calculate pattern percentages
        pattern_analysis_with_percentages = {}
        for facility, patterns in pattern_analysis.items():
            facility_total = sum(patterns.values())
            pattern_analysis_with_percentages[facility] = patterns.copy()
            for pattern, count in patterns.items():
                pattern_analysis_with_percentages[facility][f"{pattern}_percentage"] = round((count / facility_total) * 100, 1)

        return {
            "patterns_by_facility": pattern_analysis_with_percentages,
            "total_incidents_analyzed": total_incidents,
            "pattern_insights": self._interpret_chain_patterns(pattern_analysis_with_percentages)
        }

    def _investigate_workflow_gaps(self, facility_id: str = None) -> Dict[str, Any]:
        """EDA Step 2: Identify critical workflow gaps"""

        # Get entity names from schema
        facility_entity = self.entity_names.get("Facility", "Facility")
        ar_entity = self.entity_names.get("ActionRequest", "ActionRequest")
        problem_entity = self.entity_names.get("Problem", "Problem")
        rootcause_entity = self.entity_names.get("RootCause", "RootCause")
        actionplan_entity = self.entity_names.get("ActionPlan", "ActionPlan")
        verification_entity = self.entity_names.get("Verification", "Verification")

        # Get relationship types from schema
        belongs_to_rel = self._get_relationship_type("ActionRequest", "Facility")
        identified_rel = self._get_relationship_type("Problem", "ActionRequest")
        analyzes_rel = self._get_relationship_type("RootCause", "Problem")
        resolves_rel = self._get_relationship_type("ActionPlan", "RootCause")
        validates_rel = self._get_relationship_type("Verification", "ActionPlan")

        # Get primary key
        facility_pk = self._get_primary_key("Facility")

        facility_filter = f"WHERE f.{facility_pk} = $facility_id" if facility_id else ""
        params = {"facility_id": facility_id} if facility_id else {}

        # Gap Investigation Query: Missing workflow components
        gap_query = f"""
        MATCH (f:{facility_entity})<-[:{belongs_to_rel}]-(ar:{ar_entity})
        {facility_filter}

        // Investigate missing workflow links
        OPTIONAL MATCH (ar)-[:{identified_rel}]->(p:{problem_entity})
        OPTIONAL MATCH (p)<-[:{analyzes_rel}]-(rc:{rootcause_entity})
        OPTIONAL MATCH (rc)-[:{resolves_rel}]->(ap:{actionplan_entity})
        OPTIONAL MATCH (ap)-[:{validates_rel}]->(v:{verification_entity})

        // Gap classification
        WITH f, ar,
             CASE WHEN p IS NULL THEN 'missing_problem'
                  WHEN rc IS NULL THEN 'missing_root_cause'
                  WHEN ap IS NULL THEN 'missing_action_plan'
                  WHEN v IS NULL THEN 'missing_verification'
                  ELSE 'complete'
             END as gap_type

        RETURN f.facility_name as facility,
               gap_type,
               count(*) as gap_count
        ORDER BY facility, gap_count DESC
        """

        gap_results = self.db.execute_query(gap_query, **params)

        # EDA Analysis: Gap impact assessment
        gap_analysis = {}
        critical_gaps = []

        for result in gap_results:
            facility = result.get('facility', 'Unknown')
            gap_type = result['gap_type']
            count = result['gap_count']

            if facility not in gap_analysis:
                gap_analysis[facility] = {}

            gap_analysis[facility][gap_type] = count

            # Identify critical gaps (>20% of incidents)
            if gap_type != 'complete' and count > 0:
                facility_total = sum(r['gap_count'] for r in gap_results if r['facility'] == facility)
                gap_percentage = (count / facility_total) * 100

                if gap_percentage > 20:
                    critical_gaps.append({
                        "facility": facility,
                        "gap_type": gap_type,
                        "affected_incidents": count,
                        "percentage": round(gap_percentage, 1)
                    })

        return {
            "gaps_by_facility": gap_analysis,
            "critical_gaps": critical_gaps,
            "gap_insights": self._interpret_workflow_gaps(critical_gaps)
        }

    def _assess_engineer_impact(self, facility_id: str = None) -> Dict[str, Any]:
        """EDA Step 3: Measure impact on engineer root cause analysis capability"""

        # Get entity names from schema
        facility_entity = self.entity_names.get("Facility", "Facility")
        ar_entity = self.entity_names.get("ActionRequest", "ActionRequest")
        problem_entity = self.entity_names.get("Problem", "Problem")
        rootcause_entity = self.entity_names.get("RootCause", "RootCause")
        actionplan_entity = self.entity_names.get("ActionPlan", "ActionPlan")
        verification_entity = self.entity_names.get("Verification", "Verification")

        # Get relationship types from schema
        belongs_to_rel = self._get_relationship_type("ActionRequest", "Facility")
        identified_rel = self._get_relationship_type("Problem", "ActionRequest")
        analyzes_rel = self._get_relationship_type("RootCause", "Problem")
        resolves_rel = self._get_relationship_type("ActionPlan", "RootCause")
        validates_rel = self._get_relationship_type("Verification", "ActionPlan")

        # Get primary key
        facility_pk = self._get_primary_key("Facility")

        facility_filter = f"WHERE f.{facility_pk} = $facility_id" if facility_id else ""
        params = {"facility_id": facility_id} if facility_id else {}

        # Engineer Impact Query: Usable vs unusable incidents for analysis
        impact_query = f"""
        MATCH (f:{facility_entity})<-[:{belongs_to_rel}]-(ar:{ar_entity})
        {facility_filter}

        OPTIONAL MATCH (ar)-[:{identified_rel}]->(p:{problem_entity})
        OPTIONAL MATCH (p)<-[:{analyzes_rel}]-(rc:{rootcause_entity})
        OPTIONAL MATCH (rc)-[:{resolves_rel}]->(ap:{actionplan_entity})
        OPTIONAL MATCH (ap)-[:{validates_rel}]->(v:{verification_entity})

        // Engineer usability assessment
        WITH f, ar,
             CASE
                WHEN p.what_happened IS NOT NULL AND rc.root_cause IS NOT NULL
                     AND ap.action_plan IS NOT NULL AND v.is_action_plan_effective IS NOT NULL
                    THEN 'engineer_usable'
                WHEN p.what_happened IS NOT NULL AND rc.root_cause IS NOT NULL
                    THEN 'partially_usable'
                ELSE 'not_usable'
             END as usability_status

        RETURN f.facility_name as facility,
               usability_status,
               count(*) as incident_count
        ORDER BY facility, usability_status
        """

        impact_results = self.db.execute_query(impact_query, **params)

        # EDA Analysis: Engineer effectiveness assessment
        engineer_impact = {}

        for result in impact_results:
            facility = result.get('facility', 'Unknown')
            usability = result['usability_status']
            count = result['incident_count']

            if facility not in engineer_impact:
                engineer_impact[facility] = {"total": 0}

            engineer_impact[facility][usability] = count
            engineer_impact[facility]["total"] += count

        # Calculate usability percentages
        for facility, data in engineer_impact.items():
            total = data["total"]
            if total > 0:
                usable = data.get("engineer_usable", 0)
                partially_usable = data.get("partially_usable", 0)

                data["usability_score"] = round((usable / total) * 100, 1)
                data["learning_potential"] = round(((usable + partially_usable) / total) * 100, 1)
                data["data_quality_impact"] = round(100 - data["usability_score"], 1)

        return {
            "engineer_effectiveness": engineer_impact,
            "impact_insights": self._interpret_engineer_impact(engineer_impact)
        }

    def _interpret_chain_patterns(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate insights from workflow pattern analysis"""
        insights = []

        for facility, data in patterns.items():
            complete_pct = data.get("complete_chain_percentage", 0)
            partial_pct = data.get("partial_chain_percentage", 0)
            problem_only_pct = data.get("problem_only_percentage", 0)

            if complete_pct < 30:
                insights.append(f"{facility}: Only {complete_pct}% complete workflows - major learning opportunity loss")

            if problem_only_pct > 40:
                insights.append(f"{facility}: {problem_only_pct}% incidents stop at problem stage - workflow breakdown")

        return insights

    def _interpret_workflow_gaps(self, critical_gaps: List[Dict]) -> List[str]:
        """Generate insights from gap analysis"""
        insights = []

        gap_priorities = {
            "missing_verification": "Critical: Cannot assess solution effectiveness",
            "missing_root_cause": "High: Cannot learn from failure patterns",
            "missing_action_plan": "Medium: Cannot understand solution approaches",
            "missing_problem": "Low: Basic data entry issue"
        }

        for gap in critical_gaps:
            gap_type = gap["gap_type"]
            facility = gap["facility"]
            percentage = gap["percentage"]

            priority = gap_priorities.get(gap_type, "Unknown impact")
            insights.append(f"{facility}: {percentage}% {gap_type.replace('_', ' ')} - {priority}")

        return insights

    def _interpret_engineer_impact(self, impact_data: Dict[str, Any]) -> List[str]:
        """Generate insights from engineer impact analysis"""
        insights = []

        for facility, data in impact_data.items():
            if "usability_score" in data:
                score = data["usability_score"]
                impact = data["data_quality_impact"]

                if score < 40:
                    insights.append(f"{facility}: Only {score}% of incidents usable for engineer analysis")

                if impact > 60:
                    insights.append(f"{facility}: {impact}% data quality impact severely limits learning")

        return insights

    def _generate_workflow_recommendations(self, chain_analysis: Dict, gap_analysis: Dict) -> List[str]:
        """Generate actionable recommendations based on workflow analysis"""
        recommendations = []

        # Priority 1: Address critical gaps
        critical_gaps = gap_analysis.get("critical_gaps", [])
        for gap in critical_gaps[:3]:  # Top 3 critical gaps
            facility = gap["facility"]
            gap_type = gap["gap_type"].replace("_", " ")
            recommendations.append(f"Priority: Improve {gap_type} completion at {facility}")

        # Priority 2: Focus on workflow completion
        patterns = chain_analysis.get("patterns_by_facility", {})
        for facility, data in patterns.items():
            complete_pct = data.get("complete_chain_percentage", 0)
            if complete_pct < 25:
                recommendations.append(f"Focus: Increase complete workflow chains at {facility} (currently {complete_pct}%)")

        return recommendations

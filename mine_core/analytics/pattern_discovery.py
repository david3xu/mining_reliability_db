#!/usr/bin/env python3
"""
Pattern Discovery - EDA for Cross-Facility Insights (Schema-Driven)
Systematic investigation of incident patterns for engineer knowledge sharing
"""

import logging
from typing import Dict, List, Any, Tuple
from mine_core.database.db import get_database
from configs.environment import get_schema

logger = logging.getLogger(__name__)

class PatternDiscovery:
    """
    EDA Framework for discovering actionable patterns across facility data (Schema-Driven)
    Focus: Cross-facility learning opportunities for engineer effectiveness
    """

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

    def investigate_cross_facility_patterns(self) -> Dict[str, Any]:
        """
        Primary EDA Investigation: Discover patterns across all facilities
        Methodology: Comparative analysis → Pattern identification → Learning opportunities
        """

        # Step 1: Facility Performance Profiling
        performance_patterns = self._profile_facility_performance()

        # Step 2: Asset-Based Pattern Analysis
        asset_patterns = self._investigate_asset_patterns()

        # Step 3: Solution Effectiveness Comparison
        solution_patterns = self._analyze_solution_effectiveness()

        # Step 4: Knowledge Transfer Opportunities
        transfer_opportunities = self._identify_knowledge_transfer_opportunities()

        return {
            "facility_performance_analysis": performance_patterns,
            "asset_pattern_insights": asset_patterns,
            "solution_effectiveness_patterns": solution_patterns,
            "knowledge_transfer_opportunities": transfer_opportunities,
            "strategic_recommendations": self._generate_strategic_recommendations(
                performance_patterns, asset_patterns, solution_patterns
            )
        }

    def _profile_facility_performance(self) -> Dict[str, Any]:
        """EDA Step 1: Systematic facility performance profiling"""

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

        # Performance Metrics Query: Multi-dimensional facility comparison
        performance_query = f"""
        MATCH (f:{facility_entity})<-[:{belongs_to_rel}]-(ar:{ar_entity})
        OPTIONAL MATCH (ar)-[:{identified_rel}]->(p:{problem_entity})<-[:{analyzes_rel}]-(rc:{rootcause_entity})
                           -[:{resolves_rel}]->(ap:{actionplan_entity})-[:{validates_rel}]->(v:{verification_entity})

        // Performance dimension analysis
        WITH f,
             count(ar) as total_incidents,
             count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) as effective_solutions,
             count(v) as verified_solutions,
             avg(ar.days_past_due) as avg_response_time,
             count(CASE WHEN ar.stage = 'Completed' THEN 1 END) as completed_incidents

        // Performance scoring
        WITH f, total_incidents, effective_solutions, verified_solutions, avg_response_time, completed_incidents,
             CASE WHEN verified_solutions > 0
                  THEN round((effective_solutions * 100.0 / verified_solutions), 1)
                  ELSE 0 END as effectiveness_rate,
             round((completed_incidents * 100.0 / total_incidents), 1) as completion_rate

        RETURN f.facility_name as facility,
               total_incidents,
               effectiveness_rate,
               completion_rate,
               round(avg_response_time, 1) as avg_days_past_due,
               effective_solutions,
               verified_solutions
        ORDER BY effectiveness_rate DESC, completion_rate DESC
        """

        performance_results = self.db.execute_query(performance_query)

        # EDA Analysis: Performance distribution and ranking
        performance_analysis = {
            "facility_rankings": performance_results,
            "performance_insights": [],
            "benchmarking_opportunities": []
        }

        if len(performance_results) >= 2:
            # Identify best and worst performers
            best_performer = performance_results[0]
            worst_performer = performance_results[-1]

            performance_analysis["performance_insights"] = [
                f"Best Performer: {best_performer['facility']} - {best_performer['effectiveness_rate']}% solution effectiveness",
                f"Improvement Target: {worst_performer['facility']} - {worst_performer['effectiveness_rate']}% solution effectiveness",
                f"Performance Gap: {best_performer['effectiveness_rate'] - worst_performer['effectiveness_rate']:.1f}% effectiveness difference"
            ]

            # Identify benchmarking opportunities
            avg_effectiveness = sum(r['effectiveness_rate'] for r in performance_results) / len(performance_results)
            for facility_data in performance_results:
                if facility_data['effectiveness_rate'] < avg_effectiveness:
                    gap = avg_effectiveness - facility_data['effectiveness_rate']
                    performance_analysis["benchmarking_opportunities"].append({
                        "facility": facility_data['facility'],
                        "improvement_potential": round(gap, 1),
                        "current_effectiveness": facility_data['effectiveness_rate']
                    })

        return performance_analysis

    def _investigate_asset_patterns(self) -> Dict[str, Any]:
        """EDA Step 2: Asset-based pattern investigation across facilities"""

        # Get entity names from schema
        facility_entity = self.entity_names.get("Facility", "Facility")
        ar_entity = self.entity_names.get("ActionRequest", "ActionRequest")
        problem_entity = self.entity_names.get("Problem", "Problem")
        asset_entity = self.entity_names.get("Asset", "Asset")
        rootcause_entity = self.entity_names.get("RootCause", "RootCause")
        actionplan_entity = self.entity_names.get("ActionPlan", "ActionPlan")
        verification_entity = self.entity_names.get("Verification", "Verification")

        # Get relationship types from schema
        belongs_to_rel = self._get_relationship_type("ActionRequest", "Facility")
        identified_rel = self._get_relationship_type("Problem", "ActionRequest")
        involved_rel = self._get_relationship_type("Asset", "Problem")
        analyzes_rel = self._get_relationship_type("RootCause", "Problem")
        resolves_rel = self._get_relationship_type("ActionPlan", "RootCause")
        validates_rel = self._get_relationship_type("Verification", "ActionPlan")

        # Asset Pattern Query: Cross-facility asset behavior analysis
        asset_query = f"""
        MATCH (f:{facility_entity})<-[:{belongs_to_rel}]-(ar:{ar_entity})-[:{identified_rel}]->(p:{problem_entity})
              <-[:{involved_rel}]-(a:{asset_entity})
        OPTIONAL MATCH (p)<-[:{analyzes_rel}]-(rc:{rootcause_entity})-[:{resolves_rel}]->(ap:{actionplan_entity})
                       -[:{validates_rel}]->(v:{verification_entity})

        // Asset pattern analysis
        WITH a.asset_numbers as asset_type,
             f.facility_name as facility,
             count(p) as incident_count,
             collect(DISTINCT rc.root_cause) as common_causes,
             count(CASE WHEN v.is_action_plan_effective = true THEN 1 END) as successful_fixes,
             count(v) as attempted_fixes

        // Pattern aggregation
        WITH asset_type,
             collect({{
                facility: facility,
                incidents: incident_count,
                causes: common_causes,
                success_rate: CASE WHEN attempted_fixes > 0
                                   THEN round((successful_fixes * 100.0 / attempted_fixes), 1)
                                   ELSE 0 END
             }}) as facility_patterns,
             sum(incident_count) as total_asset_incidents

        WHERE total_asset_incidents >= 3  // Focus on assets with meaningful data
        RETURN asset_type, facility_patterns, total_asset_incidents
        ORDER BY total_asset_incidents DESC
        LIMIT 10
        """

        asset_results = self.db.execute_query(asset_query)

        # EDA Analysis: Asset behavior pattern recognition
        asset_insights = {
            "high_risk_assets": [],
            "cross_facility_patterns": [],
            "knowledge_sharing_opportunities": []
        }

        for asset_data in asset_results:
            asset_type = asset_data['asset_type']
            patterns = asset_data['facility_patterns']
            total_incidents = asset_data['total_asset_incidents']

            # Identify high-risk assets (multiple facilities, high incident count)
            if len(patterns) >= 2 and total_incidents >= 5:
                asset_insights["high_risk_assets"].append({
                    "asset_type": asset_type,
                    "total_incidents": total_incidents,
                    "affected_facilities": len(patterns),
                    "facility_details": patterns
                })

            # Identify cross-facility patterns
            if len(patterns) >= 2:
                success_rates = [p['success_rate'] for p in patterns if p['success_rate'] > 0]
                if success_rates:
                    max_success = max(success_rates)
                    min_success = min(success_rates)

                    if max_success - min_success > 30:  # Significant difference
                        best_facility = next(p['facility'] for p in patterns if p['success_rate'] == max_success)
                        worst_facility = next(p['facility'] for p in patterns if p['success_rate'] == min_success)

                        asset_insights["knowledge_sharing_opportunities"].append({
                            "asset_type": asset_type,
                            "learn_from": best_facility,
                            "apply_to": worst_facility,
                            "success_gap": round(max_success - min_success, 1)
                        })

        return asset_insights

    def _analyze_solution_effectiveness(self) -> Dict[str, Any]:
        """EDA Step 3: Solution effectiveness pattern analysis"""

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

        # Solution Effectiveness Query: Cross-facility solution success patterns
        solution_query = f"""
        MATCH (f:{facility_entity})<-[:{belongs_to_rel}]-(ar:{ar_entity})-[:{identified_rel}]->(p:{problem_entity})
              <-[:{analyzes_rel}]-(rc:{rootcause_entity})-[:{resolves_rel}]->(ap:{actionplan_entity})
              -[:{validates_rel}]->(v:{verification_entity})

        // Solution pattern analysis
        WITH f.facility_name as facility,
             rc.root_cause as cause_category,
             ap.action_plan as solution_approach,
             v.is_action_plan_effective as effectiveness,
             count(*) as solution_frequency

        WHERE cause_category IS NOT NULL AND solution_approach IS NOT NULL
              AND effectiveness IS NOT NULL

        // Effectiveness aggregation by cause-solution pattern
        WITH cause_category,
             collect({{
                facility: facility,
                solution: solution_approach,
                effective: effectiveness,
                frequency: solution_frequency
             }}) as solution_patterns

        RETURN cause_category, solution_patterns
        ORDER BY size(solution_patterns) DESC
        LIMIT 15
        """

        solution_results = self.db.execute_query(solution_query)

        # EDA Analysis: Solution effectiveness pattern discovery
        solution_insights = {
            "proven_solutions": [],
            "failed_approaches": [],
            "best_practice_opportunities": []
        }

        for result in solution_results:
            cause = result['cause_category']
            patterns = result['solution_patterns']

            # Analyze solution effectiveness patterns
            effective_solutions = [p for p in patterns if p['effective']]
            failed_solutions = [p for p in patterns if not p['effective']]

            # Identify proven solutions (high success rate, multiple facilities)
            if len(effective_solutions) >= 2:
                solution_insights["proven_solutions"].append({
                    "root_cause": cause,
                    "successful_approaches": len(effective_solutions),
                    "proven_solutions": [p['solution'][:100] + "..." for p in effective_solutions[:3]]
                })

            # Identify consistently failed approaches
            if len(failed_solutions) >= 2:
                solution_insights["failed_approaches"].append({
                    "root_cause": cause,
                    "failed_attempts": len(failed_solutions),
                    "avoid_solutions": [p['solution'][:100] + "..." for p in failed_solutions[:2]]
                })

        return solution_insights

    def _identify_knowledge_transfer_opportunities(self) -> Dict[str, Any]:
        """EDA Step 4: Systematic identification of knowledge transfer opportunities"""

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

        # Knowledge Transfer Query: Facility expertise and gap analysis
        transfer_query = f"""
        MATCH (f:{facility_entity})<-[:{belongs_to_rel}]-(ar:{ar_entity})-[:{identified_rel}]->(p:{problem_entity})
              <-[:{analyzes_rel}]-(rc:{rootcause_entity})-[:{resolves_rel}]->(ap:{actionplan_entity})
              -[:{validates_rel}]->(v:{verification_entity})

        // Expertise mapping by facility and cause type
        WITH f.facility_name as facility,
             rc.root_cause as cause_type,
             count(*) as experience_count,
             sum(CASE WHEN v.is_action_plan_effective = true THEN 1 ELSE 0 END) as success_count

        WHERE cause_type IS NOT NULL AND experience_count >= 2

        WITH cause_type,
             collect({{
                facility: facility,
                experience: experience_count,
                successes: success_count,
                expertise_score: round((success_count * 100.0 / experience_count), 1)
             }}) as facility_expertise

        WHERE size(facility_expertise) >= 2  // Multiple facilities must have experience
        RETURN cause_type, facility_expertise
        ORDER BY size(facility_expertise) DESC
        """

        transfer_results = self.db.execute_query(transfer_query)

        # EDA Analysis: Knowledge transfer opportunity mapping
        transfer_opportunities = {
            "high_value_transfers": [],
            "expertise_centers": {},
            "learning_gaps": []
        }

        for result in transfer_results:
            cause_type = result['cause_type']
            expertise_data = result['facility_expertise']

            # Identify expertise centers and learning gaps
            expertise_data.sort(key=lambda x: x['expertise_score'], reverse=True)

            if len(expertise_data) >= 2:
                expert_facility = expertise_data[0]
                learning_facility = expertise_data[-1]

                expertise_gap = expert_facility['expertise_score'] - learning_facility['expertise_score']

                # High-value transfer opportunity (>30% expertise gap)
                if expertise_gap > 30:
                    transfer_opportunities["high_value_transfers"].append({
                        "knowledge_area": cause_type,
                        "expert_facility": expert_facility['facility'],
                        "expert_success_rate": expert_facility['expertise_score'],
                        "learning_facility": learning_facility['facility'],
                        "learning_success_rate": learning_facility['expertise_score'],
                        "improvement_potential": round(expertise_gap, 1)
                    })

                # Map expertise centers
                expert_name = expert_facility['facility']
                if expert_name not in transfer_opportunities["expertise_centers"]:
                    transfer_opportunities["expertise_centers"][expert_name] = []

                if expert_facility['expertise_score'] > 70:  # High expertise threshold
                    transfer_opportunities["expertise_centers"][expert_name].append({
                        "expertise_area": cause_type,
                        "success_rate": expert_facility['expertise_score']
                    })

        return transfer_opportunities

    def _generate_strategic_recommendations(self, performance: Dict, assets: Dict, solutions: Dict) -> List[str]:
        """Generate strategic recommendations based on pattern analysis"""
        recommendations = []

        # Performance-based recommendations
        if performance.get("benchmarking_opportunities"):
            top_opportunity = performance["benchmarking_opportunities"][0]
            recommendations.append(
                f"Priority: {top_opportunity['facility']} has {top_opportunity['improvement_potential']:.1f}% "
                f"improvement potential - implement best practices from top performer"
            )

        # Asset-based recommendations
        high_risk_assets = assets.get("high_risk_assets", [])
        if high_risk_assets:
            critical_asset = high_risk_assets[0]
            recommendations.append(
                f"Critical: {critical_asset['asset_type']} affects {critical_asset['affected_facilities']} facilities "
                f"with {critical_asset['total_incidents']} incidents - develop standardized response protocol"
            )

        # Knowledge transfer recommendations
        sharing_opportunities = assets.get("knowledge_sharing_opportunities", [])
        if sharing_opportunities:
            top_transfer = sharing_opportunities[0]
            recommendations.append(
                f"Knowledge Transfer: {top_transfer['learn_from']} → {top_transfer['apply_to']} "
                f"for {top_transfer['asset_type']} ({top_transfer['success_gap']:.1f}% success rate improvement potential)"
            )

        # Solution effectiveness recommendations
        proven_solutions = solutions.get("proven_solutions", [])
        if proven_solutions:
            recommendations.append(
                f"Best Practice: Standardize proven solutions for {len(proven_solutions)} root cause categories "
                f"across all facilities"
            )

        return recommendations[:5]  # Top 5 strategic recommendations

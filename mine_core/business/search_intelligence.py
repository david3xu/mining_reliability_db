#!/usr/bin/env python3
"""
Search Intelligence Engine - Stakeholder Emergency Decision Support
Transforms incident search into immediate actionable intelligence.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from configs.environment import get_graph_search_config, get_mappings
from mine_core.database.query_manager import get_query_manager
from mine_core.shared.common import handle_error
from mine_core.business.intelligence_models import IntelligenceResult

logger = logging.getLogger(__name__)


class SearchIntelligence:
    """Emergency decision intelligence for maintenance engineers"""

    def __init__(self):
        self.query_manager = get_query_manager()
        self.mappings = get_mappings()
        self.graph_search_config = get_graph_search_config()

        # Search dimension mapping for comprehensive queries
        self._search_dimensions = {
            "direct_matches": ["search_queries", "direct_field_matches", "incident_query"],
            "equipment_patterns": ["search_queries", "equipment_patterns", "incident_query"],
            "causal_chains": ["search_queries", "causal_chains", "chain_query"],
            "cross_facility_patterns": ["search_queries", "cross_facility_patterns", "cross_facility_query"],
            "temporal_patterns": ["search_queries", "temporal_patterns", "temporal_query"],
            "recurring_sequences": ["search_queries", "recurring_sequences", "recurring_query"],
            "solution_effectiveness": ["search_queries", "solution_effectiveness", "effective_solutions_query"],
            "equipment_failure_clusters": ["search_queries", "equipment_failure_clusters", "cluster_analysis_query"],
        }

    def analyze_incident_intelligence(self, search_terms: str) -> Dict[str, Any]:
        """Core stakeholder intelligence extraction for emergency response"""
        try:
            logger.info(f"Search Intelligence: Analyzing incident intelligence for '{search_terms}'")

            # Execute comprehensive search first
            search_result = self.execute_comprehensive_search(search_terms)
            similar_incidents = self._consolidate_search_results(search_result.data)

            # Extract stakeholder decision intelligence
            action_intelligence = self._extract_immediate_actions(similar_incidents)
            criticality_score = self._calculate_criticality_score(similar_incidents)
            proven_solutions = self._filter_proven_solutions(similar_incidents)
            time_estimates = self._calculate_resolution_times(similar_incidents)

            return IntelligenceResult(
                analysis_type="incident_intelligence",
                data={
                    "immediate_actions": action_intelligence,
                    "criticality_assessment": criticality_score,
                    "proven_solutions": proven_solutions,
                    "time_estimates": time_estimates,
                    "similar_incidents": similar_incidents[:10]  # Top 10 for reference
                },
                metadata={"search_terms": search_terms},
                quality_score=self._validate_intelligence_confidence(similar_incidents),
                generated_at=datetime.now().isoformat()
            )

        except Exception as e:
            handle_error(logger, e, f"incident intelligence analysis for '{search_terms}'")
            return self._create_empty_intelligence_result()

    def execute_comprehensive_search(self, search_terms: str) -> Dict[str, Any]:
        """Multi-dimensional search across graph structure"""
        try:
            logger.info(f"Search Intelligence: Executing comprehensive search for '{search_terms}'")

            search_results = {}
            successful_searches = 0

            for dimension, query_path in self._search_dimensions.items():
                try:
                    results = self._execute_search_query(query_path, search_terms)
                    search_results[dimension] = results if results else []
                    if results:
                        successful_searches += 1
                except Exception as e:
                    handle_error(logger, e, f"search dimension {dimension}")
                    search_results[dimension] = []

            return IntelligenceResult(
                analysis_type="comprehensive_search",
                data=search_results,
                metadata={"search_terms": search_terms},
                quality_score=successful_searches / len(self._search_dimensions),
                generated_at=datetime.now().isoformat()
            )

        except Exception as e:
            handle_error(logger, e, f"comprehensive search for '{search_terms}'")
            return self._create_empty_search_result()

    def analyze_causal_intelligence(self, facility_id: str = None) -> Dict[str, Any]:
        """Analyze causal patterns and intelligence"""
        try:
            causal_result = self.query_manager.get_causal_intelligence_data(facility_id)

            if not causal_result.success:
                return self._create_empty_result("causal_intelligence")

            patterns_analysis = self._analyze_causal_patterns(causal_result.data)

            intelligence_data = {
                "causal_patterns": causal_result.data,
                "pattern_analysis": patterns_analysis,
                "facility_scope": facility_id or "all_facilities",
                "total_patterns": len(causal_result.data),
            }

            quality_score = self._calculate_causal_quality(causal_result.data)

            return {
                "analysis_type": "causal_intelligence",
                "data": intelligence_data,
                "metadata": {
                    "facility_filter": facility_id,
                    "patterns_found": len(causal_result.data),
                },
                "quality_score": quality_score,
                "generated_at": datetime.now().isoformat(),
            }

        except Exception as e:
            handle_error(logger, e, "causal intelligence analysis")
            return self._create_empty_result("causal_intelligence")

    # Stakeholder Intelligence Processing Methods

    def _consolidate_search_results(self, search_data: Dict) -> List[Dict]:
        """Consolidate 8 search dimensions into unified incident list"""
        incidents = []
        for dimension_results in search_data.values():
            if isinstance(dimension_results, list):
                incidents.extend(dimension_results)
        return incidents

    def _extract_immediate_actions(self, incidents: List[Dict]) -> List[str]:
        """Extract immediate containment actions from historical data"""
        actions = []
        for incident in incidents:
            # Check multiple field variations for immediate actions
            action = (incident.get("immediate_containment") or
                     incident.get("immediate_contain_action") or
                     incident.get("immd_contain_action"))

            if action and len(action.strip()) > 10:  # Filter meaningful content
                actions.append(action.strip())

        # Return top 5 unique actions
        unique_actions = list(set(actions))
        return unique_actions[:5]

    def _calculate_criticality_score(self, incidents: List[Dict]) -> Dict[str, Any]:
        """Calculate criticality based on historical impact patterns"""
        days_past_due = [inc.get("days_past_due", 0) for inc in incidents if inc.get("days_past_due")]
        loss_amounts = [inc.get("amount_of_loss", 0) for inc in incidents if inc.get("amount_of_loss")]

        avg_urgency = sum(days_past_due) / len(days_past_due) if days_past_due else 0
        avg_loss = sum(loss_amounts) / len(loss_amounts) if loss_amounts else 0

        # Criticality assessment logic
        if avg_urgency > 10 or avg_loss > 5000:
            level, color = "HIGH", "red"
        elif avg_urgency > 5 or avg_loss > 1000:
            level, color = "MEDIUM", "yellow"
        else:
            level, color = "LOW", "green"

        return {
            "level": level,
            "color": color,
            "avg_urgency_days": round(avg_urgency, 1),
            "avg_loss_amount": round(avg_loss, 0),
            "sample_size": len(incidents)
        }

    def _filter_proven_solutions(self, incidents: List[Dict]) -> List[Dict]:
        """Filter only verified effective solutions"""
        proven = []
        for incident in incidents:
            # Check for solution effectiveness indicators
            effective = (incident.get("is_action_plan_effective") == "Yes" or
                        incident.get("effective") == "Yes" or
                        incident.get("is_resp_satisfactory") == "Yes")

            if effective and incident.get("action_plan"):
                proven.append({
                    "action_plan": incident.get("action_plan", ""),
                    "effectiveness": incident.get("is_action_plan_effective", "Unknown"),
                    "verification": incident.get("is_resp_satisfactory", "Unknown"),
                    "facility": incident.get("facility", "Unknown")
                })

        return proven[:3]  # Top 3 proven solutions

    def _calculate_resolution_times(self, incidents: List[Dict]) -> Dict[str, Any]:
        """Calculate average resolution times from similar incidents"""
        resolution_times = []

        for incident in incidents:
            start = incident.get("initiation_date")
            end = incident.get("completion_date")

            if start and end:
                try:
                    # Handle various date formats
                    start_clean = start.replace('T00:00:00', '') if 'T' in start else start
                    end_clean = end.replace('T00:00:00', '') if 'T' in end else end

                    start_date = datetime.fromisoformat(start_clean)
                    end_date = datetime.fromisoformat(end_clean)

                    time_diff = (end_date - start_date).days
                    if time_diff > 0 and time_diff < 365:  # Reasonable range
                        resolution_times.append(time_diff)
                except Exception:
                    continue

        if resolution_times:
            avg_time = sum(resolution_times) / len(resolution_times)
            return {
                "average_days": round(avg_time, 1),
                "range": f"{min(resolution_times)}-{max(resolution_times)} days",
                "sample_size": len(resolution_times)
            }

        return {"average_days": 0, "range": "No data", "sample_size": 0}

    def _validate_intelligence_confidence(self, incidents: List[Dict]) -> float:
        """Calculate confidence score for intelligence quality"""
        if not incidents:
            return 0.0

        # Score based on data completeness of critical fields
        complete_fields = 0
        total_fields = 0

        critical_fields = ["what_happened", "root_cause", "action_plan", "title"]

        for incident in incidents:
            for field in critical_fields:
                total_fields += 1
                if incident.get(field) and len(str(incident.get(field)).strip()) > 5:
                    complete_fields += 1

        return complete_fields / total_fields if total_fields > 0 else 0.0

    # Helper Methods

    def _execute_search_query(self, query_path: List[str], terms: str) -> List[Dict]:
        """Execute specific search query from graph search config"""
        try:
            query = self.graph_search_config
            for key in query_path:
                query = query.get(key, {})

            if isinstance(query, str):
                result = self.query_manager.execute_query(query, {"search_term": terms})
                return result.data if result.success else []

            return []

        except Exception as e:
            handle_error(logger, e, f"search query execution for path {query_path}")
            return []

    def _analyze_causal_patterns(self, patterns: List[Dict]) -> Dict[str, Any]:
        """Analyze causal intelligence patterns"""
        if not patterns:
            return {}

        frequencies = [p.get("frequency", 0) for p in patterns]

        return {
            "pattern_count": len(patterns),
            "frequency_range": {"min": min(frequencies), "max": max(frequencies)},
            "high_frequency_patterns": len([f for f in frequencies if f > 5]),
            "pattern_diversity": len(set([p.get("primary_cause") for p in patterns])),
        }

    def _calculate_causal_quality(self, patterns: List[Dict]) -> float:
        """Calculate causal intelligence quality score"""
        if not patterns:
            return 0.0

        pattern_score = min(1.0, len(patterns) / 10)
        diversity_score = len(set([p.get("primary_cause") for p in patterns])) / len(patterns)

        return (pattern_score + diversity_score) / 2

    def _create_empty_intelligence_result(self) -> Dict[str, Any]:
        """Create empty intelligence result for error cases"""
        return {
            "analysis_type": "incident_intelligence",
            "data": {
                "immediate_actions": [],
                "criticality_assessment": {"level": "UNKNOWN", "color": "gray"},
                "proven_solutions": [],
                "time_estimates": {"average_days": 0, "range": "No data", "sample_size": 0},
                "similar_incidents": []
            },
            "metadata": {"error": "Analysis failed"},
            "quality_score": 0.0,
            "generated_at": datetime.now().isoformat()
        }

    def _create_empty_search_result(self) -> Dict[str, Any]:
        """Create empty search result for error cases"""
        return {
            "analysis_type": "comprehensive_search",
            "data": {dimension: [] for dimension in self._search_dimensions.keys()},
            "metadata": {"error": "Search failed"},
            "quality_score": 0.0,
            "generated_at": datetime.now().isoformat()
        }

    def _create_empty_result(self, analysis_type: str) -> Dict[str, Any]:
        """Create empty result for any analysis type"""
        return {
            "analysis_type": analysis_type,
            "data": {},
            "metadata": {"error": "Analysis failed"},
            "quality_score": 0.0,
            "generated_at": datetime.now().isoformat()
        }


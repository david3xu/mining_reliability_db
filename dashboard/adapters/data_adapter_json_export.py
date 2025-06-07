#!/usr/bin/env python3
"""
Data Adapter JSON Export Extension
Add JSON file output for stakeholder essential query results.
"""

import logging
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

from dashboard.adapters.data_adapter import get_data_adapter
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


class JSONExportAdapter:
    """Extended data adapter with JSON export capability"""

    def __init__(self):
        self.data_adapter = get_data_adapter()
        self.export_directory = "data/stakeholder_results"
        self._ensure_export_directory()

    def execute_essential_stakeholder_query(
        self,
        query_type: str,
        incident_keywords: List[str]
    ) -> List[Dict[str, Any]]:
        """Execute standard stakeholder query (delegate to existing adapter)"""
        return self.data_adapter.execute_essential_stakeholder_query(query_type, incident_keywords)

    def execute_essential_stakeholder_query_with_export(
        self,
        query_type: str,
        incident_keywords: List[str]
    ) -> Tuple[List[Dict[str, Any]], str]:
        """Execute query and export results to JSON file"""

        try:
            # Execute standard query
            results = self.execute_essential_stakeholder_query(query_type, incident_keywords)

            # Generate export file
            export_filename = self._generate_export_filename(query_type, incident_keywords)
            export_path = self._export_results_to_json(results, query_type, incident_keywords, export_filename)

            logger.info(f"Stakeholder query results exported to: {export_path}")
            return results, export_path

        except Exception as e:
            handle_error(logger, e, f"JSON export for {query_type}")
            return [], ""

    def execute_comprehensive_stakeholder_export(
        self,
        incident_keywords: List[str]
    ) -> Tuple[Dict[str, List[Dict[str, Any]]], str]:
        """Execute all 4 essential queries and export comprehensive results to JSON file"""

        try:
            all_results = {}
            query_types = [
                "can_this_be_fixed",
                "who_do_i_call",
                "how_long_will_this_take",
                "what_works_and_why"
            ]

            # Execute all 4 essential queries
            for query_type in query_types:
                results = self.execute_essential_stakeholder_query(query_type, incident_keywords)
                all_results[query_type] = results
                logger.info(f"Executed {query_type}: {len(results)} results")

            # Generate comprehensive export file
            export_filename = self._generate_comprehensive_export_filename(incident_keywords)
            export_path = self._export_comprehensive_results_to_json(all_results, incident_keywords, export_filename)

            logger.info(f"Comprehensive stakeholder analysis exported to: {export_path}")
            return all_results, export_path

        except Exception as e:
            handle_error(logger, e, "Comprehensive JSON export")
            return {}, ""

    def _generate_export_filename(self, query_type: str, keywords: List[str]) -> str:
        """Generate structured filename for export"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        keyword_str = "_".join([k.replace(" ", "_") for k in keywords[:3]])  # Limit to 3 keywords for filename
        clean_keyword_str = "".join(c for c in keyword_str if c.isalnum() or c == "_")[:30]  # Clean and limit length
        return f"stakeholder_{query_type}_{timestamp}_{clean_keyword_str}.json"

    def _generate_comprehensive_export_filename(self, keywords: List[str]) -> str:
        """Generate filename for comprehensive export"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        keyword_str = "_".join([k.replace(" ", "_") for k in keywords[:3]])  # Limit to 3 keywords for filename
        clean_keyword_str = "".join(c for c in keyword_str if c.isalnum() or c == "_")[:30]  # Clean and limit length
        return f"stakeholder_comprehensive_{timestamp}_{clean_keyword_str}.json"

    def _export_results_to_json(
        self,
        results: List[Dict],
        query_type: str,
        keywords: List[str],
        filename: str
    ) -> str:
        """Export results to structured JSON file"""

        export_data = {
            "metadata": {
                "query_type": query_type,
                "search_keywords": keywords,
                "timestamp": datetime.now().isoformat(),
                "result_count": len(results),
                "query_description": self._get_query_description(query_type)
            },
            "search_parameters": {
                "keywords": keywords,
                "filter_logic": "flexible_equipment_focused",
                "max_results": 10
            },
            "results": results,
            "summary": {
                "total_found": len(results),
                "confidence_distribution": self._analyze_confidence_distribution(results),
                "key_insights": self._extract_key_insights(results, query_type)
            }
        }

        export_path = os.path.join(self.export_directory, filename)

        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return export_path

    def _export_comprehensive_results_to_json(
        self,
        all_results: Dict[str, List[Dict]],
        keywords: List[str],
        filename: str
    ) -> str:
        """Export comprehensive results to structured JSON file"""

        # Calculate total results across all questions
        total_results = sum(len(results) for results in all_results.values())

        export_data = {
            "metadata": {
                "analysis_type": "comprehensive_stakeholder_investigation",
                "search_keywords": keywords,
                "timestamp": datetime.now().isoformat(),
                "total_result_count": total_results,
                "questions_analyzed": 4,
                "description": "Complete stakeholder intelligence analysis covering all 4 essential questions"
            },
            "search_parameters": {
                "keywords": keywords,
                "filter_logic": "flexible_equipment_focused",
                "max_results_per_question": 10,
                "questions_included": [
                    "can_this_be_fixed",
                    "who_do_i_call",
                    "how_long_will_this_take",
                    "what_works_and_why"
                ]
            },
            "analysis_results": {
                "can_this_be_fixed": {
                    "question": "Can this be fixed? Historical solution precedents",
                    "description": "Analysis of past successful repairs and solution methods",
                    "result_count": len(all_results.get("can_this_be_fixed", [])),
                    "results": all_results.get("can_this_be_fixed", [])
                },
                "who_do_i_call": {
                    "question": "Who do I call? Department expertise mapping",
                    "description": "Identification of expert departments and responsible teams",
                    "result_count": len(all_results.get("who_do_i_call", [])),
                    "results": all_results.get("who_do_i_call", [])
                },
                "how_long_will_this_take": {
                    "question": "How long will this take? Timeline analysis",
                    "description": "Historical repair duration patterns and time estimates",
                    "result_count": len(all_results.get("how_long_will_this_take", [])),
                    "results": all_results.get("how_long_will_this_take", [])
                },
                "what_works_and_why": {
                    "question": "What works and why? Proven effective actions",
                    "description": "Evidence-based effective actions with success rationale",
                    "result_count": len(all_results.get("what_works_and_why", [])),
                    "results": all_results.get("what_works_and_why", [])
                }
            },
            "summary": {
                "total_found": total_results,
                "results_by_question": {
                    question: len(results) for question, results in all_results.items()
                },
                "overall_confidence_distribution": self._analyze_comprehensive_confidence_distribution(all_results),
                "key_insights": self._extract_comprehensive_insights(all_results, keywords),
                "cross_question_analysis": self._perform_cross_question_analysis(all_results)
            }
        }

        export_path = os.path.join(self.export_directory, filename)

        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return export_path

    def _get_query_description(self, query_type: str) -> str:
        """Get human-readable query description"""
        descriptions = {
            "can_this_be_fixed": "Historical solution precedents analysis",
            "who_do_i_call": "Department expertise and responsibility mapping",
            "how_long_will_this_take": "Timeline analysis for similar repairs",
            "what_works_and_why": "Proven effective actions with rationale"
        }
        return descriptions.get(query_type, "Unknown query type")

    def _analyze_confidence_distribution(self, results: List[Dict]) -> Dict[str, int]:
        """Analyze confidence level distribution in results"""
        confidence_counts = {"High": 0, "Medium": 0, "Low": 0, "Unknown": 0}

        for result in results:
            confidence = result.get("confidence_level", "Unknown")
            if confidence in confidence_counts:
                confidence_counts[confidence] += 1
            else:
                confidence_counts["Unknown"] += 1

        return confidence_counts

    def _analyze_comprehensive_confidence_distribution(self, all_results: Dict[str, List[Dict]]) -> Dict[str, Dict[str, int]]:
        """Analyze confidence distribution across all questions"""
        confidence_by_question = {}

        for question, results in all_results.items():
            confidence_counts = {"High": 0, "Medium": 0, "Low": 0, "Unknown": 0}

            for result in results:
                confidence = result.get("confidence_level", "Unknown")
                if confidence in confidence_counts:
                    confidence_counts[confidence] += 1
                else:
                    confidence_counts["Unknown"] += 1

            confidence_by_question[question] = confidence_counts

        # Calculate overall distribution
        overall_confidence = {"High": 0, "Medium": 0, "Low": 0, "Unknown": 0}
        for question_confidence in confidence_by_question.values():
            for level, count in question_confidence.items():
                overall_confidence[level] += count

        return {
            "by_question": confidence_by_question,
            "overall": overall_confidence
        }

    def _extract_key_insights(self, results: List[Dict], query_type: str) -> List[str]:
        """Extract key insights from results"""
        insights = []

        if not results:
            insights.append("No relevant data found for search keywords")
            return insights

        if query_type == "what_works_and_why":
            # Analyze effective actions
            high_freq_actions = [r for r in results if r.get("usage_frequency", 0) >= 3]
            if high_freq_actions:
                insights.append(f"{len(high_freq_actions)} actions have been used multiple times")

            strong_evidence = [r for r in results if r.get("evidence_quality") == "Strong"]
            if strong_evidence:
                insights.append(f"{len(strong_evidence)} actions have strong supporting evidence")

        elif query_type == "who_do_i_call":
            # Analyze department expertise
            if results:
                success_rates = [r.get("success_rate", 0) for r in results if isinstance(r.get("success_rate"), (int, float))]
                if success_rates:
                    avg_success_rate = sum(success_rates) / len(success_rates)
                    insights.append(f"Average department success rate: {avg_success_rate:.1f}%")

        elif query_type == "how_long_will_this_take":
            # Analyze timeline patterns
            if results:
                durations = [r.get("average_days", 0) for r in results if isinstance(r.get("average_days"), (int, float))]
                if durations:
                    avg_duration = sum(durations) / len(durations)
                    insights.append(f"Average repair duration: {avg_duration:.1f} days")

        insights.append(f"Found {len(results)} relevant records")
        return insights

    def _extract_comprehensive_insights(self, all_results: Dict[str, List[Dict]], keywords: List[str]) -> List[str]:
        """Extract comprehensive insights across all questions"""
        insights = []

        # Overall analysis
        total_results = sum(len(results) for results in all_results.values())
        insights.append(f"Found {total_results} total relevant records across all 4 essential questions")

        # Per-question insights
        for question, results in all_results.items():
            if results:
                if question == "what_works_and_why":
                    high_freq_actions = [r for r in results if r.get("usage_frequency", 0) >= 3]
                    if high_freq_actions:
                        insights.append(f"Effective Actions: {len(high_freq_actions)} proven solutions with multiple uses")

                elif question == "who_do_i_call":
                    success_rates = [r.get("success_rate", 0) for r in results if isinstance(r.get("success_rate"), (int, float))]
                    if success_rates:
                        avg_success_rate = sum(success_rates) / len(success_rates)
                        insights.append(f"Expert Departments: Average success rate {avg_success_rate:.1f}%")

                elif question == "how_long_will_this_take":
                    durations = [r.get("average_days", 0) for r in results if isinstance(r.get("average_days"), (int, float))]
                    if durations:
                        avg_duration = sum(durations) / len(durations)
                        insights.append(f"Timeline Analysis: Average repair duration {avg_duration:.1f} days")

                elif question == "can_this_be_fixed":
                    insights.append(f"Solution Precedents: {len(results)} historical repair cases found")

        # Keywords analysis
        if keywords:
            insights.append(f"Search focused on: {', '.join(keywords[:3])}")

        return insights

    def _perform_cross_question_analysis(self, all_results: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Perform analysis across all questions to find patterns"""
        cross_analysis = {}

        # Find common incident IDs across questions
        incident_ids_by_question = {}
        for question, results in all_results.items():
            incident_ids = set(r.get("incident_id", "") for r in results if r.get("incident_id"))
            incident_ids_by_question[question] = incident_ids

        # Find incidents appearing in multiple questions
        all_incident_ids = set()
        for ids in incident_ids_by_question.values():
            all_incident_ids.update(ids)

        cross_referenced_incidents = []
        for incident_id in all_incident_ids:
            questions_found = [q for q, ids in incident_ids_by_question.items() if incident_id in ids]
            if len(questions_found) > 1:
                cross_referenced_incidents.append({
                    "incident_id": incident_id,
                    "appears_in_questions": questions_found,
                    "question_count": len(questions_found)
                })

        cross_analysis["cross_referenced_incidents"] = cross_referenced_incidents
        cross_analysis["total_cross_references"] = len(cross_referenced_incidents)

        # Confidence correlation
        high_confidence_by_question = {}
        for question, results in all_results.items():
            high_confidence_count = sum(1 for r in results if r.get("confidence_level") == "High")
            high_confidence_by_question[question] = {
                "high_confidence_count": high_confidence_count,
                "total_count": len(results),
                "percentage": (high_confidence_count / len(results) * 100) if results else 0
            }

        cross_analysis["confidence_analysis"] = high_confidence_by_question

        return cross_analysis

    def _ensure_export_directory(self):
        """Ensure export directory exists"""
        try:
            os.makedirs(self.export_directory, exist_ok=True)
            logger.info(f"Export directory ready: {self.export_directory}")
        except Exception as e:
            logger.warning(f"Could not create export directory: {e}")
            self.export_directory = "."  # Fallback to current directory


# Singleton pattern
_json_export_adapter = None

def get_json_export_adapter() -> JSONExportAdapter:
    """Get JSON export-enabled data adapter"""
    global _json_export_adapter
    if _json_export_adapter is None:
        _json_export_adapter = JSONExportAdapter()
    return _json_export_adapter

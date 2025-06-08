#!/usr/bin/env python3
"""
Data Adapter - Core Data Pipeline Integration (Enhanced)
Unified data access layer for comprehensive graph data extraction.
Architecture compliant: uses config_adapter instead of direct config imports.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from dashboard.adapters.config_adapter import get_config_adapter
from dashboard.adapters.interfaces import (
    ComponentMetadata,
    FacilityData,
    FieldData,
    PortfolioData,
    TimelineData,
    ValidationResult,
)
from dashboard.adapters.workflow_adapter import get_workflow_adapter
from mine_core.business.intelligence_engine import IntelligenceEngine, get_intelligence_engine
from mine_core.database.query_manager import get_query_manager
from mine_core.shared.common import handle_error

__all__ = [
    "PurifiedDataAdapter",
    "get_data_adapter",
    "reset_adapter",
]

logger = logging.getLogger(__name__)


class PurifiedDataAdapter:
    """Pure data access adapter - calls core business logic only (Enhanced for Graph Search)"""

    def __init__(self):
        """Initialize with core service connections"""
        self.intelligence_engine = get_intelligence_engine()
        self._cache = {}
        self._cache_ttl = 300

    def get_portfolio_metrics(self) -> PortfolioData:
        """Pure data access for portfolio metrics"""
        try:
            logger.info("Adapter: Fetching portfolio metrics from core")

            # Call core business logic
            analysis_result = self.intelligence_engine.analyze_portfolio_metrics()

            if not analysis_result.data:
                return self._create_empty_portfolio_data()

            # Pure data transformation - no business logic
            portfolio_data = analysis_result.data

            return PortfolioData(
                total_records=portfolio_data.get("total_records", 0),
                data_fields=portfolio_data.get("data_fields", 0),
                facilities=portfolio_data.get("facilities", 0),
                years_coverage=portfolio_data.get("years_coverage", 0),
                year_detail=analysis_result.data.get("year_detail", "Unknown"),
                metadata=ComponentMetadata(
                    source="core.intelligence_engine",
                    generated_at=analysis_result.generated_at,
                    data_quality=analysis_result.quality_score,
                ),
            )

        except Exception as e:
            handle_error(logger, e, "portfolio metrics data access")
            return self._create_empty_portfolio_data()

    def get_facility_breakdown(self) -> FacilityData:
        """Pure data access for facility distribution"""
        try:
            logger.info("Adapter: Fetching facility breakdown from core")

            # Call core business logic
            analysis_result = self.intelligence_engine.analyze_facility_distribution()

            if not analysis_result.data:
                return self._create_empty_facility_data()

            # Pure data transformation
            facility_data = analysis_result.data

            return FacilityData(
                labels=facility_data.get("labels", []),
                values=facility_data.get("values", []),
                percentages=facility_data.get("percentages", []),
                total_records=facility_data.get("total_records", 0),
                metadata=ComponentMetadata(
                    source="core.intelligence_engine",
                    generated_at=analysis_result.generated_at,
                    data_quality=analysis_result.quality_score,
                ),
            )

        except Exception as e:
            handle_error(logger, e, "facility breakdown data access")
            return self._create_empty_facility_data()

    def get_field_distribution(self) -> FieldData:
        """Pure data access for field type distribution"""
        try:
            logger.info("Adapter: Fetching field distribution from core")

            # Call core business logic
            analysis_result = self.intelligence_engine.analyze_field_type_distribution()

            if not analysis_result.data:
                return self._create_empty_field_data()

            # Pure data transformation
            field_data = analysis_result.data

            return FieldData(
                labels=field_data.get("labels", []),
                values=field_data.get("values", []),
                percentages=field_data.get("percentages", []),
                total_fields=field_data.get("total_fields", 0),
                category_counts=field_data.get("category_counts", {}),
                detailed_field_names=field_data.get("detailed_field_names", {}),
                metadata=ComponentMetadata(
                    source="core.intelligence_engine",
                    generated_at=analysis_result.generated_at,
                    data_quality=analysis_result.quality_score,
                ),
            )

        except Exception as e:
            handle_error(logger, e, "field distribution data access")
            return self._create_empty_field_data()

    def get_historical_timeline(self) -> TimelineData:
        """Pure data access for temporal timeline"""
        try:
            logger.info("Adapter: Fetching historical timeline from core")

            # Call core business logic
            analysis_result = self.intelligence_engine.analyze_temporal_timeline()

            if not analysis_result.data:
                return self._create_empty_timeline_data()

            # Pure data transformation
            timeline_data = analysis_result.data

            return TimelineData(
                columns=timeline_data.get("columns", []),
                rows=timeline_data.get("rows", []),
                year_range=timeline_data.get("year_range", []),
                total_records=timeline_data.get("total_records", 0),
                facilities_count=timeline_data.get("facilities_count", 0),
                metadata=ComponentMetadata(
                    source="core.intelligence_engine",
                    generated_at=analysis_result.generated_at,
                    data_quality=analysis_result.quality_score,
                ),
            )

        except Exception as e:
            handle_error(logger, e, "historical timeline data access")
            return self._create_empty_timeline_data()

    def get_data_quality_validation(self) -> ValidationResult:
        """Pure data access for data quality validation results"""
        try:
            logger.info("Adapter: Fetching data quality validation from core")

            # Call core business logic for data quality analysis
            analysis_result = self.intelligence_engine.analyze_data_quality()

            # Extract component status from entity_completeness for ValidationResult
            component_status = {
                entity: data.get("is_complete", False)
                for entity, data in analysis_result.data.get("entity_completeness", {}).items()
            }

            return ValidationResult(
                overall_status=analysis_result.data.get("workflow_completeness", {}).get(
                    "overall_status", False
                ),
                component_status=component_status,
                score=analysis_result.quality_score,
                error_details=analysis_result.data.get("details", None),
            )

        except Exception as e:
            handle_error(logger, e, "data quality validation access")
            return ValidationResult(
                overall_status=False, component_status={}, score=0.0, error_details=str(e)
            )

    def get_all_field_completion_rates(self) -> Dict[str, float]:
        """Get completion rate for every field across all entities"""
        try:
            workflow_adapter = get_workflow_adapter()
            completion_analysis = workflow_adapter.get_comprehensive_completion_analysis()

            all_field_rates = {}

            # Extract field completion from all entities
            all_entities = {
                **completion_analysis.get("workflow_completions", {}),
                **completion_analysis.get("supporting_completions", {}),
            }

            for entity_name, entity_data in all_entities.items():
                field_details = entity_data.get("field_details", [])
                for field_info in field_details:
                    field_name = field_info.get("field_name", "")
                    completion_rate = field_info.get("completion_rate", 0.0)
                    all_field_rates[field_name] = completion_rate

            return all_field_rates

        except Exception as e:
            handle_error(logger, e, "all field completion rates")
            return {}

    def get_41_raw_field_completion_rates(self) -> Dict[str, float]:
        """Get completion rates for all 41 raw field names"""
        try:
            workflow_adapter = get_workflow_adapter()
            # Get raw field completion from workflow processor
            raw_field_rates = (
                workflow_adapter.workflow_processor.calculate_raw_field_completion_rates()
            )

            logger.info(
                f"Raw field completion data from workflow processor: {len(raw_field_rates)} fields"
            )
            return raw_field_rates
        except Exception as e:
            handle_error(logger, e, "41 raw field completion rates")
            return {}

    def search_problems_and_causes(self, search_text: str) -> List[Dict[str, Any]]:
        """Schema-driven search through core layer"""
        try:
            logger.info(f"Adapter: Schema-driven search for '{search_text}'")

            query_manager = get_query_manager()

            # Use schema-driven method
            search_result = query_manager.search_using_schema_configuration(search_text)

            if not search_result.success or not search_result.data:
                return []

            # Process and return data in a clean format
            return search_result.data

        except Exception as e:
            handle_error(logger, e, f"schema-driven search for '{search_text}'")
            return []

    def get_solution_sequence_case_study(self) -> Dict[str, Any]:
        """Get solution sequence case study data"""
        try:
            config_adapter = get_config_adapter()
            case_study_config = config_adapter.get_case_study_config()
            study_params = case_study_config["case_study_definitions"][
                "solution_sequence_analysis"
            ]["input_parameters"]
            action_request_number = study_params["action_request_number"]["default"]
            facility_name = study_params["facility_name"]["default"]
            logger.info(
                f"Adapter: Fetching case study data for {action_request_number} in facility {facility_name}"
            )

            query_manager = get_query_manager()

            case_study_result = query_manager.get_case_study_solution_sequence(
                action_request_number, facility_name
            )

            if not case_study_result.success or not case_study_result.data:
                return {"error": "Case study data not found"}

            # Group the records by sequence_id (actionrequest_id) to create multiple solution sequences
            sequences = {}
            for record in case_study_result.data:
                sequence_id = record["sequence_id"]
                if sequence_id not in sequences:
                    sequences[sequence_id] = {
                        "action_request": record["action_number"],
                        "action_title": record["action_title"],
                        "facility": record["facility"],
                        "problem": record["problem_description"],
                        "root_cause": record["root_cause"],
                        "root_cause_tail_extraction": record["root_cause_tail_extraction"],
                        "action_sequence": [],
                    }

                # Add action plan if it exists
                if record["action_plan_id"]:
                    sequences[sequence_id]["action_sequence"].append(
                        {
                            "action_plan_id": record["action_plan_id"],
                            "action_description": record["action_description"],
                            "due_date": record["due_date"],
                            "complete": record["complete"],
                            "completion_date": record["completion_date"],
                            "verification_status": record["verification_status"],
                        }
                    )

            # Convert to list and add total counts
            solution_sequences = []
            for seq_id, seq_data in sequences.items():
                seq_data["sequence_id"] = seq_id
                seq_data["total_actions"] = len(seq_data["action_sequence"])
                solution_sequences.append(seq_data)

            return {
                "solution_sequences": solution_sequences,
                "total_sequences": len(solution_sequences),
                "action_request_number": action_request_number,
            }

        except Exception as e:
            handle_error(logger, e, f"solution sequence case study for {action_request_number}")
            return {"error": str(e)}

    def get_action_request_facility_summary(self) -> Dict[str, Any]:
        """Pure data access for ActionRequest facility statistics summary"""
        try:
            logger.info("Adapter: Fetching ActionRequest facility summary from core")

            # Call core business logic
            analysis_result = self.intelligence_engine.analyze_action_request_facility_statistics()

            if not analysis_result.data:
                return {
                    "facility_statistics": [],
                    "summary_totals": {
                        "total_records": 0,
                        "total_unique_actions": 0,
                        "average_records_per_action": 0.0,
                    },
                    "metadata": {
                        "source": "empty",
                        "generated_at": self._get_timestamp(),
                        "data_quality": 0.0,
                    },
                }

            # Pure data transformation
            return {
                "facility_statistics": analysis_result.data.get("facility_statistics", []),
                "summary_totals": analysis_result.data.get("summary_totals", {}),
                "metadata": {
                    "source": "core.intelligence_engine",
                    "generated_at": analysis_result.generated_at,
                    "data_quality": analysis_result.quality_score,
                    "facilities_analyzed": analysis_result.metadata.get("facilities_analyzed", 0),
                },
            }

        except Exception as e:
            handle_error(logger, e, "ActionRequest facility summary data access")
            return {
                "facility_statistics": [],
                "summary_totals": {
                    "total_records": 0,
                    "total_unique_actions": 0,
                    "average_records_per_action": 0.0,
                },
                "metadata": {
                    "source": "error",
                    "generated_at": self._get_timestamp(),
                    "data_quality": 0.0,
                },
            }

    def debug_search_data_structure(self) -> Dict[str, Any]:
        """Debug method to understand search data structure"""
        try:
            logger.info("Adapter: Debugging search data structure")

            query_manager = get_query_manager()

            discovery_result = query_manager.discover_search_data_structure()

            if not discovery_result.success:
                return {"error": "Discovery failed", "details": discovery_result.metadata}

            # Organize discovery results by type
            findings = {}
            for result in discovery_result.data:
                discovery_type = result.get("discovery_type")
                findings[discovery_type] = result.get("findings")

            logger.info(f"Database structure discovery: {findings}")
            return findings

        except Exception as e:
            handle_error(logger, e, "search structure debugging")
            return {"error": str(e)}

    def get_core_workflow_labels(self) -> List[str]:
        """Get core workflow entity labels only"""
        try:
            query_manager = get_query_manager()

            result = query_manager.get_core_workflow_labels()
            return [row["label"] for row in result.data] if result.success else []

        except Exception as e:
            handle_error(logger, e, "core workflow labels access")
            return []

    def execute_comprehensive_graph_search(self, search_term: str) -> Dict[str, List[Dict[str, Any]]]:
        """Enhanced comprehensive graph search - return raw dimension-based data for comprehensive search layout"""
        try:
            # Call enhanced core intelligence
            intelligence_result = self.intelligence_engine.execute_comprehensive_incident_search(search_term)

            # Return raw dimension-based data directly for comprehensive search layout
            search_data = intelligence_result.data if intelligence_result.data else {}

            # Ensure all expected dimensions exist, even if empty
            dimension_keys = [
                "direct_matches", "equipment_patterns", "causal_chains",
                "cross_facility_patterns", "temporal_patterns", "recurring_sequences",
                "solution_effectiveness", "equipment_clusters"
            ]

            for key in dimension_keys:
                if key not in search_data:
                    search_data[key] = []

            # Add search coverage metadata
            search_data["search_coverage"] = len([k for k in dimension_keys if search_data.get(k)])

            return search_data

        except Exception as e:
            handle_error(logger, e, f"comprehensive graph search for '{search_term}'")
            # Return empty dimension structure
            return {
                "direct_matches": [],
                "equipment_patterns": [],
                "causal_chains": [],
                "cross_facility_patterns": [],
                "temporal_patterns": [],
                "recurring_sequences": [],
                "solution_effectiveness": [],
                "equipment_clusters": [],
                "search_coverage": 0
            }

    def get_consolidated_search_results(self, search_term: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get search results in consolidated incidents/solutions/facilities format"""
        try:
            # Call enhanced core intelligence
            intelligence_result = self.intelligence_engine.execute_comprehensive_incident_search(search_term)

            # Transform comprehensive results to consolidated format
            incidents = self._consolidate_incident_results(intelligence_result.data)
            solutions = self._consolidate_solution_results(intelligence_result.data)
            facilities = self._consolidate_facility_results(intelligence_result.data)

            return {
                "incidents": incidents,
                "solutions": solutions,
                "facilities": facilities
            }
        except Exception as e:
            handle_error(logger, e, f"consolidated search for '{search_term}'")
            return {"incidents": [], "solutions": [], "facilities": []}

    def _consolidate_incident_results(self, comprehensive_data: Dict) -> List[Dict]:
        """Consolidate search dimensions into incidents format"""
        incidents = []

        # Merge results from all search dimensions
        for dimension in ["direct_matches", "equipment_patterns", "causal_chains", "cross_facility_patterns", "temporal_patterns", "recurring_sequences", "solution_effectiveness", "equipment_failure_clusters"]:
            dimension_results = comprehensive_data.get(dimension, [])
            for result in dimension_results:
                incidents.append({
                    "incident_id": result.get("action_request_number", "N/A"),
                    "facility": result.get("facility_name", "N/A"),
                    "problem_description": result.get("what_happened", "N/A"),
                    "root_cause": result.get("root_cause", "N/A"),
                    "solution": result.get("action_plan", "N/A"),
                    "effective": result.get("is_action_plan_effective", "Unknown")
                })

        return incidents[:50]  # Existing limit

    def _consolidate_solution_results(self, comprehensive_data: Dict) -> List[Dict]:
        """Consolidate search dimensions into solutions format"""
        solutions = []
        dimension_results = comprehensive_data.get("solution_effectiveness", [])
        for result in dimension_results:
            if result.get("is_action_plan_effective") == "Yes":
                solutions.append({
                    "solution_id": result.get("action_request_number", "N/A"),
                    "action_plan": result.get("action_plan", "N/A"),
                    "root_cause": result.get("root_cause", "N/A"),
                    "effectiveness": result.get("is_action_plan_effective", "Unknown"),
                    "comment": result.get("action_plan_eval_comment", "N/A")
                })
        return solutions[:50]

    def _consolidate_facility_results(self, comprehensive_data: Dict) -> List[Dict]:
        """Consolidate search dimensions into facilities format"""
        facilities = []
        dimension_results = comprehensive_data.get("cross_facility_patterns", [])
        for result in dimension_results:
            facilities.append({
                "facility_1": result.get("facility_1", "N/A"),
                "facility_2": result.get("facility_2", "N/A"),
                "title": result.get("title", "N/A"),
                "categories": result.get("categories", "N/A")
            })
        return facilities[:50]

    def _execute_basic_graph_search(self, search_term: str) -> Dict[str, List[Dict[str, Any]]]:
        """Fallback basic graph search method (original implementation)"""
        try:
            logger.info(f"Adapter: Executing fallback basic graph search for '{search_term}'")

            query_manager = get_query_manager()
            results = {"incidents": [], "solutions": [], "facilities": []}

            # Comprehensive incident search
            incident_query = """
            MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
            MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)
            WHERE toLower(p.what_happened) CONTAINS toLower($search_term)
            OPTIONAL MATCH (p)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
            RETURN ar.action_request_number AS incident_id,
                   f.facility_id AS facility,
                   p.what_happened AS problem_description,
                   rc.root_cause AS root_cause,
                   ap.action_plan AS solution,
                   v.is_action_plan_effective AS effective
            ORDER BY ar.initiation_date DESC
            LIMIT 50
            """

            incident_result = query_manager.execute_query(
                incident_query, params={"search_term": search_term}
            )
            if incident_result.success:
                results["incidents"] = incident_result.data

            # Solution effectiveness search
            solution_query = """
            MATCH (ap:ActionPlan)<-[:VALIDATES]-(v:Verification)
            WHERE toLower(ap.action_plan) CONTAINS toLower($search_term)
            MATCH (ap)-[:RESOLVES]->(rc:RootCause)-[:ANALYZES]->(p:Problem)-[:IDENTIFIED_IN]->(ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
            RETURN ap.action_plan AS solution,
                   v.is_action_plan_effective AS effective,
                   rc.root_cause AS root_cause,
                   f.facility_id AS facility
            ORDER BY v.is_action_plan_effective DESC
            LIMIT 30
            """

            solution_result = query_manager.execute_query(
                solution_query, params={"search_term": search_term}
            )
            if solution_result.success:
                results["solutions"] = solution_result.data

            # Facility network search
            facility_query = """
            MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
            WHERE toLower(ar.categories) CONTAINS toLower($search_term)
               OR toLower(ar.title) CONTAINS toLower($search_term)
            MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)
            WITH f.facility_id AS facility_id,
                 count(*) AS incident_count,
                 collect(DISTINCT ar.categories) AS equipment_types
            RETURN facility_id, incident_count, equipment_types
            ORDER BY incident_count DESC
            LIMIT 10
            """

            facility_result = query_manager.execute_query(
                facility_query, params={"search_term": search_term}
            )
            if facility_result.success:
                results["facilities"] = facility_result.data

            return results

        except Exception as e:
            handle_error(logger, e, f"basic graph search for '{search_term}'")
            return {"incidents": [], "solutions": [], "facilities": []}

    # Symptom-based filtering and diagnostic methods for incident root cause investigation

    def classify_incident_symptoms(self, incident_description: str) -> Dict[str, Any]:
        """Classify incident symptoms using symptom classification config"""
        try:
            config_adapter = get_config_adapter()
            symptom_config = config_adapter.get_symptom_classification_config()

            # Extract keyword categories
            keyword_categories = symptom_config.get("keyword_categories", {})
            equipment_terms = keyword_categories.get("equipment_terms", {}).get("terms", [])
            symptom_terms = keyword_categories.get("symptom_terms", {}).get("terms", [])
            component_terms = keyword_categories.get("component_terms", {}).get("terms", [])
            severity_indicators = keyword_categories.get("severity_indicators", {}).get("terms", [])

            description_lower = incident_description.lower()

            classification = {
                "equipment_matches": [],
                "symptom_matches": [],
                "component_matches": [],
                "severity_matches": [],
                "classification_score": 0
            }

            # Find keyword matches
            for term in equipment_terms:
                if term.lower() in description_lower:
                    classification["equipment_matches"].append(term)
                    classification["classification_score"] += 3

            for term in symptom_terms:
                if term.lower() in description_lower:
                    classification["symptom_matches"].append(term)
                    classification["classification_score"] += 2

            for term in component_terms:
                if term.lower() in description_lower:
                    classification["component_matches"].append(term)
                    classification["classification_score"] += 1

            for term in severity_indicators:
                if term.lower() in description_lower:
                    classification["severity_matches"].append(term)
                    classification["classification_score"] += 2

            return classification

        except Exception as e:
            handle_error(logger, e, f"symptom classification for '{incident_description}'")
            return {
                "equipment_matches": [],
                "symptom_matches": [],
                "component_matches": [],
                "severity_matches": [],
                "classification_score": 0
            }

    def build_symptom_based_filter(self, incident_keywords: List[str]) -> str:
        """Build symptom-based filter clause using classification logic"""
        try:
            config_adapter = get_config_adapter()
            symptom_config = config_adapter.get_symptom_classification_config()

            # Get filter logic configuration
            filter_logic = symptom_config.get("filter_logic", {})
            primary_pattern = filter_logic.get("primary_pattern", "(equipment OR component) AND symptom")
            conjunction_op = filter_logic.get("conjunction_operator", "AND")
            disjunction_op = filter_logic.get("disjunction_operator", "OR")

            # Extract keyword categories for classification
            keyword_categories = symptom_config.get("keyword_categories", {})
            equipment_terms = set(term.lower() for term in keyword_categories.get("equipment_terms", {}).get("terms", []))
            symptom_terms = set(term.lower() for term in keyword_categories.get("symptom_terms", {}).get("terms", []))
            component_terms = set(term.lower() for term in keyword_categories.get("component_terms", {}).get("terms", []))

            # Classify the input keywords
            equipment_filters = []
            symptom_filters = []
            component_filters = []

            for keyword in incident_keywords:
                keyword_lower = keyword.lower()

                if keyword_lower in equipment_terms:
                    equipment_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")
                    equipment_filters.append(f"toLower(ar.categories) CONTAINS toLower('{keyword}')")
                elif keyword_lower in symptom_terms:
                    symptom_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")
                elif keyword_lower in component_terms:
                    component_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")
                    component_filters.append(f"toLower(ar.categories) CONTAINS toLower('{keyword}')")
                else:
                    # Fallback: treat as general search term
                    symptom_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")

            # Build filter according to primary pattern
            conditions = []

            if "equipment" in primary_pattern.lower() and equipment_filters:
                conditions.append(f"({' OR '.join(equipment_filters)})")

            if "component" in primary_pattern.lower() and component_filters:
                conditions.append(f"({' OR '.join(component_filters)})")

            if "symptom" in primary_pattern.lower() and symptom_filters:
                conditions.append(f"({' OR '.join(symptom_filters)})")

            # Combine conditions based on pattern
            if "AND" in primary_pattern and len(conditions) > 1:
                return f" {conjunction_op} ".join(conditions)
            elif conditions:
                return f" {disjunction_op} ".join(conditions)
            else:
                # Fallback to general keyword search
                all_filters = []
                for keyword in incident_keywords:
                    all_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")
                return f" {disjunction_op} ".join(all_filters) if all_filters else "1=1"

        except Exception as e:
            handle_error(logger, e, f"symptom-based filter building")
            # Fallback to existing flexible keyword filter
            return self.build_flexible_keyword_filter(incident_keywords)

    def execute_diagnostic_query(self, query_type: str, incident_keywords: List[str]) -> List[Dict[str, Any]]:
        """Execute diagnostic queries for root cause investigation"""
        try:
            query_manager = get_query_manager()
            config_adapter = get_config_adapter()

            # Get stakeholder queries config for diagnostic query mappings
            stakeholder_config = config_adapter.get_stakeholder_queries_config()
            essential_queries = stakeholder_config.get("essential_queries", {})

            # Check if this is a diagnostic query type
            diagnostic_query_types = [
                "what_could_be_causing_this",
                "what_investigation_steps_worked",
                "who_has_diagnostic_experience",
                "what_should_i_check_first"
            ]

            if query_type not in diagnostic_query_types:
                logger.warning(f"Query type '{query_type}' is not a diagnostic query")
                return []

            # Get query configuration
            query_config = essential_queries.get(query_type)
            if not query_config:
                logger.error(f"No configuration found for query type: {query_type}")
                return []

            query_file_path = query_config.get("query_file")
            if not query_file_path:
                logger.error(f"No query file specified for query type: {query_type}")
                return []

            # Build symptom-based filter clause
            filter_clause = self.build_symptom_based_filter(incident_keywords)

            # Execute the diagnostic query
            result = query_manager.execute_stakeholder_essential_query(query_file_path, filter_clause)

            if result.success and result.data:
                # Filter out None objects and ensure all records are dictionaries
                filtered_data = []
                for record in result.data:
                    if record is not None and isinstance(record, dict):
                        filtered_data.append(record)
                    elif record is not None:
                        logger.warning(f"Non-dict record encountered in diagnostic query: {type(record)} - {record}")

                logger.info(f"Diagnostic query {query_type}: {len(filtered_data)} valid records")
                return filtered_data
            else:
                logger.warning(f"Diagnostic query {query_type}: No data or query failed")
                return []

        except Exception as e:
            logger.error(f"Error executing diagnostic query {query_type}: {e}")
            handle_error(logger, e, f"diagnostic query: {query_type}")
            return []

    def get_potential_root_causes(self, incident_keywords: List[str]) -> List[Dict[str, Any]]:
        """Get potential root causes based on similar symptom patterns"""
        return self.execute_diagnostic_query("what_could_be_causing_this", incident_keywords)

    def get_investigation_approaches(self, incident_keywords: List[str]) -> List[Dict[str, Any]]:
        """Get investigation approaches that worked for similar symptoms"""
        return self.execute_diagnostic_query("what_investigation_steps_worked", incident_keywords)

    def get_diagnostic_experts(self, incident_keywords: List[str]) -> List[Dict[str, Any]]:
        """Get departments with diagnostic experience for similar symptoms"""
        return self.execute_diagnostic_query("who_has_diagnostic_experience", incident_keywords)

    def get_prioritized_investigation_steps(self, incident_keywords: List[str]) -> List[Dict[str, Any]]:
        """Get prioritized investigation steps based on success patterns"""
        return self.execute_diagnostic_query("what_should_i_check_first", incident_keywords)

    def execute_comprehensive_incident_investigation(self, incident_description: str, incident_keywords: List[str]) -> Dict[str, Any]:
        """Execute comprehensive incident investigation using all diagnostic queries"""
        try:
            logger.info(f"Starting comprehensive incident investigation for: {incident_keywords}")

            # First, classify the incident symptoms
            symptom_classification = self.classify_incident_symptoms(incident_description)

            # Execute all diagnostic queries
            investigation_results = {
                "symptom_classification": symptom_classification,
                "potential_root_causes": self.get_potential_root_causes(incident_keywords),
                "investigation_approaches": self.get_investigation_approaches(incident_keywords),
                "diagnostic_experts": self.get_diagnostic_experts(incident_keywords),
                "prioritized_steps": self.get_prioritized_investigation_steps(incident_keywords),
                "investigation_summary": {
                    "keywords_analyzed": incident_keywords,
                    "classification_score": symptom_classification.get("classification_score", 0),
                    "total_root_causes_found": 0,
                    "total_approaches_found": 0,
                    "total_experts_found": 0,
                    "total_steps_found": 0
                }
            }

            # Update summary counts
            investigation_results["investigation_summary"]["total_root_causes_found"] = len(investigation_results["potential_root_causes"])
            investigation_results["investigation_summary"]["total_approaches_found"] = len(investigation_results["investigation_approaches"])
            investigation_results["investigation_summary"]["total_experts_found"] = len(investigation_results["diagnostic_experts"])
            investigation_results["investigation_summary"]["total_steps_found"] = len(investigation_results["prioritized_steps"])

            logger.info(f"Investigation completed: {investigation_results['investigation_summary']}")
            return investigation_results

        except Exception as e:
            handle_error(logger, e, f"comprehensive incident investigation")
            return {
                "symptom_classification": {"equipment_matches": [], "symptom_matches": [], "component_matches": [], "severity_matches": [], "classification_score": 0},
                "potential_root_causes": [],
                "investigation_approaches": [],
                "diagnostic_experts": [],
                "prioritized_steps": [],
                "investigation_summary": {"error": str(e)}
            }

    # End of symptom-based filtering and diagnostic methods

    def execute_essential_stakeholder_query(self, query_type: str, incident_keywords: List[str]) -> List[Dict[str, Any]]:
        """Execute with fixed query manager and NoneType filtering"""
        try:
            query_manager = get_query_manager()
            config_adapter = get_config_adapter()
            essential_queries_config = config_adapter.get_stakeholder_queries_config().get("essential_queries", {})

            # Build filter clause using flexible logic
            filter_clause = self.build_flexible_keyword_filter(incident_keywords)

            query_config = essential_queries_config.get(query_type)
            query_file_path = query_config.get("query_file")

            # Use new method with syntax fixes
            result = query_manager.execute_stakeholder_essential_query(query_file_path, filter_clause)

            if result.success and result.data:
                # Filter out None objects and ensure all records are dictionaries
                filtered_data = []
                for record in result.data:
                    if record is not None and isinstance(record, dict):
                        filtered_data.append(record)
                    elif record is not None:
                        logger.warning(f"Non-dict record encountered: {type(record)} - {record}")

                logger.info(f"Query {query_type}: {len(filtered_data)} valid records after filtering")
                return filtered_data
            else:
                logger.warning(f"Query {query_type}: No data or query failed")
                return []

        except Exception as e:
            logger.error(f"Error in essential stakeholder query: {query_type}: {e}")
            handle_error(logger, e, f"essential stakeholder query: {query_type}")
            return []

    def build_flexible_keyword_filter(self, keywords: List[str]) -> str:
        """Build flexible keyword filter with equipment-focused logic and fallback for all keywords"""

        # Equipment terms (high priority)
        equipment_terms = ['excavator', 'motor', 'pump', 'conveyor', 'crusher']

        # Failure modes (medium priority)
        failure_terms = ['failed', 'leak', 'noise', 'vibration', 'wear']

        # Component terms (lower priority)
        component_terms = ['swing', 'rear', 'front', 'hydraulic']

        equipment_filters = []
        failure_filters = []
        component_filters = []
        general_filters = []  # For keywords not in predefined lists

        for keyword in keywords:
            keyword_lower = keyword.lower()

            if keyword_lower in equipment_terms:
                equipment_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")
            elif keyword_lower in failure_terms:
                failure_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")
            elif keyword_lower in component_terms:
                component_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")
            else:
                # CRITICAL FIX: Include ALL keywords, not just predefined ones
                general_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")

        # Build flexible logic: Equipment AND (Failure OR Component OR General)
        conditions = []

        if equipment_filters:
            conditions.append(f"({' OR '.join(equipment_filters)})")

        # Combine all other filters
        other_filters = failure_filters + component_filters + general_filters
        if other_filters:
            conditions.append(f"({' OR '.join(other_filters)})")

        # If we have specific equipment and other terms, combine with AND
        # Otherwise, use OR to be more inclusive
        if len(conditions) > 1:
            return ' AND '.join(conditions)
        elif conditions:
            return conditions[0]
        else:
            # Final fallback: search all keywords with OR
            all_filters = [f"toLower(p.what_happened) CONTAINS toLower('{keyword}')" for keyword in keywords]
            return ' OR '.join(all_filters) if all_filters else "1=1"

    def _get_timestamp(self) -> str:
        """Generate current timestamp for metadata"""
        return datetime.now().isoformat()

    def _create_empty_portfolio_data(self) -> PortfolioData:
        """Create empty PortfolioData instance for error cases"""
        return PortfolioData(
            total_records=0,
            data_fields=0,
            facilities=0,
            years_coverage=0,
            year_detail="N/A",
            metadata=ComponentMetadata(
                source="empty", generated_at=self._get_timestamp(), data_quality=0.0
            ),
        )

    def _create_empty_facility_data(self) -> FacilityData:
        """Create empty FacilityData instance for error cases"""
        return FacilityData(
            labels=[],
            values=[],
            percentages=[],
            total_records=0,
            metadata=ComponentMetadata(
                source="empty", generated_at=self._get_timestamp(), data_quality=0.0
            ),
        )

    def _create_empty_field_data(self) -> FieldData:
        """Create empty FieldData instance for error cases"""
        return FieldData(
            labels=[],
            values=[],
            percentages=[],
            total_fields=0,
            metadata=ComponentMetadata(
                source="empty", generated_at=self._get_timestamp(), data_quality=0.0
            ),
        )

    def _create_empty_timeline_data(self) -> TimelineData:
        """Create empty TimelineData instance for error cases"""
        return TimelineData(
            columns=[],
            rows=[],
            year_range=[],
            total_records=0,
            facilities_count=0,
            metadata=ComponentMetadata(
                source="empty", generated_at=self._get_timestamp(), data_quality=0.0
            ),
        )

    def execute_complete_stakeholder_journey(self, user_input: str) -> Dict[str, Any]:
        """Execute complete stakeholder journey with single input returning five outputs"""
        try:
            logger.info(f"Adapter: Executing complete stakeholder journey for input: {user_input}")

            # Extract keywords from user input
            keywords = self._extract_keywords_from_input(user_input)

            # Build filter clause for queries
            filter_clause = self._build_filter_clause(keywords)

            # Execute all five journey queries
            journey_results = {}

            # 1. Why did this happen?
            why_results = self._execute_journey_query("why_did_this_happen", filter_clause)
            journey_results["why_did_this_happen"] = {
                "title": "Why did this happen?",
                "results": why_results,
                "count": len(why_results) if why_results else 0
            }

            # 2. How do I figure out what's wrong?
            investigation_results = self._execute_journey_query("how_do_i_figure_out_whats_wrong", filter_clause)
            journey_results["how_do_i_figure_out_whats_wrong"] = {
                "title": "How do I figure out what's wrong?",
                "results": investigation_results,
                "count": len(investigation_results) if investigation_results else 0
            }

            # 3. Who can help me?
            experts_results = self._execute_journey_query("who_can_help_me", filter_clause)
            journey_results["who_can_help_me"] = {
                "title": "Who can help me?",
                "results": experts_results,
                "count": len(experts_results) if experts_results else 0
            }

            # 4. What should I check first?
            checklist_results = self._execute_journey_query("what_should_i_check_first", filter_clause)
            journey_results["what_should_i_check_first"] = {
                "title": "What should I check first?",
                "results": checklist_results,
                "count": len(checklist_results) if checklist_results else 0
            }

            # 5. How do I fix it?
            solutions_results = self._execute_journey_query("how_do_i_fix_it", filter_clause)
            journey_results["how_do_i_fix_it"] = {
                "title": "How do I fix it?",
                "results": solutions_results,
                "count": len(solutions_results) if solutions_results else 0
            }

            # Add summary metadata
            total_results = sum(section["count"] for section in journey_results.values())
            journey_results["metadata"] = {
                "user_input": user_input,
                "keywords_used": keywords,
                "total_results": total_results,
                "generated_at": self._get_timestamp(),
                "success": True
            }

            logger.info(f"Stakeholder journey completed with {total_results} total results")
            return journey_results

        except Exception as e:
            handle_error(logger, e, "complete stakeholder journey execution")
            return {
                "metadata": {
                    "user_input": user_input,
                    "error": str(e),
                    "generated_at": self._get_timestamp(),
                    "success": False
                }
            }

    def _extract_keywords_from_input(self, user_input: str) -> List[str]:
        """Extract relevant keywords from user input using symptom classification config"""
        try:
            config_adapter = get_config_adapter()
            symptom_config = config_adapter.get_symptom_classification_config()

            keywords = []
            input_lower = user_input.lower()

            # Extract equipment terms
            for equipment in symptom_config.get("equipment_terms", []):
                if equipment.lower() in input_lower:
                    keywords.append(equipment)

            # Extract symptom terms
            for symptom in symptom_config.get("symptom_terms", []):
                if symptom.lower() in input_lower:
                    keywords.append(symptom)

            # Extract component terms
            for component in symptom_config.get("component_terms", []):
                if component.lower() in input_lower:
                    keywords.append(component)

            # Extract operational context
            for context in symptom_config.get("operational_context", []):
                if context.lower() in input_lower:
                    keywords.append(context)

            # If no specific terms found, use the entire input as keywords
            if not keywords:
                keywords = [word.strip() for word in user_input.split() if len(word.strip()) > 2]

            return list(set(keywords))  # Remove duplicates

        except Exception as e:
            logger.warning(f"Error extracting keywords: {e}")
            return [word.strip() for word in user_input.split() if len(word.strip()) > 2]

    def _build_filter_clause(self, keywords: List[str]) -> str:
        """Build Neo4j filter clause from keywords"""
        if not keywords:
            return "true"  # No filtering if no keywords

        # Build CONTAINS clauses for different fields
        conditions = []

        for keyword in keywords:
            keyword_conditions = [
                f"toLower(p.what_happened) CONTAINS toLower('{keyword}')",
                f"toLower(rc.root_cause) CONTAINS toLower('{keyword}')",
                f"toLower(f.facility_id) CONTAINS toLower('{keyword}')",
                f"toLower(ar.operating_centre) CONTAINS toLower('{keyword}')"
            ]
            conditions.append(f"({' OR '.join(keyword_conditions)})")

        return " AND ".join(conditions)

    def _execute_journey_query(self, query_name: str, filter_clause: str) -> List[Dict[str, Any]]:
        """Execute a single journey query with filter clause substitution"""
        try:
            query_manager = get_query_manager()

            # Load configuration to get query file path
            config_path = "/home/291928k/uwa/alcoa/mining_reliability_db/configs/stakeholder_essential_queries.json"
            with open(config_path, 'r') as f:
                config = json.load(f)

            # Get query file path from configuration
            if query_name in config.get("complete_stakeholder_journey", {}):
                query_file_path = config["complete_stakeholder_journey"][query_name]["query_file"]
            elif query_name in config.get("essential_queries", {}):
                query_file_path = config["essential_queries"][query_name]["query_file"]
            else:
                logger.error(f"Query {query_name} not found in configuration")
                return []

            # Execute the query with correct parameters
            result = query_manager.execute_stakeholder_essential_query(
                query_file_path,
                filter_clause
            )

            if result and result.success and result.data:
                return result.data
            else:
                logger.warning(f"Query {query_name} returned no results or failed")
                return []

        except Exception as e:
            logger.error(f"Error executing journey query {query_name}: {e}")
            return []

    def execute_stakeholder_essential_query(self, query_type: str, user_input: str = "") -> Dict[str, Any]:
        """Execute individual stakeholder essential query with optional user input filtering"""
        try:
            logger.info(f"Adapter: Executing stakeholder essential query: {query_type}")

            if user_input:
                keywords = self._extract_keywords_from_input(user_input)
                filter_clause = self._build_filter_clause(keywords)
            else:
                filter_clause = "true"  # No filtering

            results = self._execute_journey_query(query_type, filter_clause)

            return {
                "query_type": query_type,
                "user_input": user_input,
                "results": results,
                "count": len(results) if results else 0,
                "generated_at": self._get_timestamp(),
                "success": True
            }

        except Exception as e:
            handle_error(logger, e, f"stakeholder essential query {query_type}")
            return {
                "query_type": query_type,
                "user_input": user_input,
                "error": str(e),
                "generated_at": self._get_timestamp(),
                "success": False
            }


# Singleton pattern implementation
_data_adapter_instance = None

def get_data_adapter():
    """Get the singleton instance of PurifiedDataAdapter."""
    global _data_adapter_instance
    if _data_adapter_instance is None:
        _data_adapter_instance = PurifiedDataAdapter()
    return _data_adapter_instance

def reset_adapter():
    """Reset the singleton instance (mainly for testing)."""
    global _data_adapter_instance
    _data_adapter_instance = None

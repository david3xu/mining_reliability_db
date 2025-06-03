#!/usr/bin/env python3
"""
Core Business Intelligence Engine - Pure Business Logic
Centralized intelligence operations with schema-driven analysis capabilities.
"""

import logging
import re  # Re-added for markdown link parsing
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from configs.environment import (
    get_entity_connections,
    get_entity_names,
    get_entity_primary_key,
    get_field_category_display_mapping,
    get_mappings,
    get_schema,
)
from mine_core.database.query_manager import QueryResult, get_query_manager
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


@dataclass
class IntelligenceResult:
    """Standardized intelligence analysis result"""

    analysis_type: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    quality_score: float
    generated_at: str


class IntelligenceEngine:
    """Core business intelligence and analysis engine"""

    def __init__(self):
        self.query_manager = get_query_manager()
        self.schema = get_schema()
        self.mappings = get_mappings()

    def analyze_portfolio_metrics(self) -> IntelligenceResult:
        """Analyze portfolio-level metrics and coverage"""
        try:
            # Get facility data
            facility_result = self.query_manager.get_facility_metrics()
            facilities = facility_result.data

            # Get action request counts
            ar_count_result = self.query_manager.get_entity_count("ActionRequest")
            total_records = ar_count_result

            # Analyze field coverage from schema
            field_analysis = self._analyze_field_coverage()

            # Calculate temporal coverage
            temporal_result = self.query_manager.get_temporal_analysis_data()
            year_coverage = len(temporal_result.data) if temporal_result.success else 0

            # Generate year detail
            year_detail = self._calculate_year_span(temporal_result.data)

            portfolio_data = {
                "total_records": total_records,
                "data_fields": field_analysis["total_fields"],
                "facilities": len(facilities),
                "years_coverage": year_coverage,
                "year_detail": year_detail,
                "facilities_data": facilities,
            }

            quality_score = self._calculate_portfolio_quality(portfolio_data)

            return IntelligenceResult(
                analysis_type="portfolio_metrics",
                data=portfolio_data,
                metadata={"source": "core_intelligence", "facilities_analyzed": len(facilities)},
                quality_score=quality_score,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "portfolio metrics analysis")
            return self._create_empty_result("portfolio_metrics")

    def analyze_facility_distribution(self) -> IntelligenceResult:
        """Analyze facility-wise record distribution"""
        try:
            facility_result = self.query_manager.get_facility_metrics()
            facilities = facility_result.data

            if not facilities:
                return self._create_empty_result("facility_distribution")

            # Extract distribution data
            labels = [f.get("facility_id", "Unknown") for f in facilities]
            values = [f.get("incident_count", 0) for f in facilities]
            total_records = sum(values)

            # Calculate percentages
            percentages = self._calculate_percentages(values, total_records)

            distribution_data = {
                "labels": labels,
                "values": values,
                "percentages": percentages,
                "total_records": total_records,
                "distribution_analysis": self._analyze_distribution_balance(values),
            }

            quality_score = 1.0 if total_records > 0 else 0.0

            return IntelligenceResult(
                analysis_type="facility_distribution",
                data=distribution_data,
                metadata={"facilities_count": len(facilities), "total_records": total_records},
                quality_score=quality_score,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "facility distribution analysis")
            return self._create_empty_result("facility_distribution")

    def analyze_field_type_distribution(self) -> IntelligenceResult:
        """Analyze field type distribution from schema configuration"""
        try:
            # Step 1: Count data types and map to categories based on field_mappings.json
            categorized_counts = {}
            schema_entities_map = {
                entity.get("name"): entity.get("properties", {})
                for entity in self.schema.get("entities", [])
            }

            # Define mapping from raw types to category keys
            raw_type_to_category_key_map = {
                "string": "descriptive_fields",
                "text": "descriptive_fields",
                "date": "temporal_fields",
                "integer": "quantitative_fields",
                "boolean": "boolean_fields",
            }

            entity_mappings_from_config = self.mappings.get("entity_mappings", {})
            for entity_name, field_map in entity_mappings_from_config.items():
                if entity_name == "Facility":
                    continue  # Exclude Facility entity fields as per the rule

                entity_properties_in_schema = schema_entities_map.get(entity_name, {})

                for internal_field_name, raw_data_field_name in field_map.items():
                    if internal_field_name == "root_cause_tail_extraction":
                        continue  # Exclude 'root_cause_tail_extraction' as it is a derived field

                    prop_details = entity_properties_in_schema.get(internal_field_name)

                    if prop_details:
                        raw_type = prop_details.get("type")
                        if raw_type:
                            category_key = raw_type_to_category_key_map.get(raw_type)
                            if category_key:
                                categorized_counts[category_key] = (
                                    categorized_counts.get(category_key, 0) + 1
                                )
                            else:
                                logger.warning(
                                    f"Unknown data type '{raw_type}' for internal field '{internal_field_name}' mapped to '{raw_data_field_name}'."
                                )
                        else:
                            logger.warning(
                                f"Type not found for internal field '{internal_field_name}' mapped to '{raw_data_field_name}'."
                            )
                    else:
                        logger.warning(
                            f"Internal field '{internal_field_name}' from field_mappings not found in model_schema for entity '{entity_name}'."
                        )

            # Step 2: Prepare labels and values for the chart using display names
            labels = []
            values = []
            total_fields = 0
            detailed_field_names = {}

            # Get display mapping from config
            category_display_mapping = get_field_category_display_mapping()

            for category_key, count in categorized_counts.items():
                display_name = category_display_mapping.get(
                    category_key, category_key.replace("_", " ").title()
                )
                labels.append(display_name)
                values.append(count)
                total_fields += count
                # Collect detailed field names for the current category
                detailed_field_names[category_key] = []

            # Populate detailed_field_names by iterating through field_mappings.json again
            for entity_name, field_map in entity_mappings_from_config.items():
                if entity_name == "Facility":
                    continue  # Exclude Facility entity fields

                entity_properties_in_schema = schema_entities_map.get(entity_name, {})

                for internal_field_name, raw_data_field_name in field_map.items():
                    if internal_field_name == "root_cause_tail_extraction":
                        continue  # Exclude 'root_cause_tail_extraction' as it is a derived field

                    prop_details = entity_properties_in_schema.get(internal_field_name)

                    if prop_details:
                        raw_type = prop_details.get("type")
                        if raw_type:
                            category_key = raw_type_to_category_key_map.get(raw_type)
                            if category_key and category_key in detailed_field_names:
                                detailed_field_names[category_key].append(
                                    raw_data_field_name
                                )  # Add raw data field name

            percentages = self._calculate_percentages(values, total_fields)

            distribution_data = {
                "labels": labels,
                "values": values,
                "percentages": percentages,
                "total_fields": total_fields,
                "category_counts": categorized_counts,  # Include category counts
                "detailed_field_names": detailed_field_names,  # Include detailed field names
                "category_analysis": self._analyze_field_balance(
                    self.mappings.get("field_categories", {})
                ),
            }

            quality_score = 1.0 if total_fields > 0 else 0.0

            return IntelligenceResult(
                analysis_type="field_distribution",
                data=distribution_data,
                metadata={
                    "source": "schema_configuration",
                    "categories": len(category_display_mapping),
                },
                quality_score=quality_score,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "field distribution analysis")
            return self._create_empty_result("field_distribution")

    def analyze_temporal_timeline(self) -> IntelligenceResult:
        """Analyze historical timeline patterns"""
        try:
            # Get facility data for timeline structure
            facility_result = self.query_manager.get_facility_metrics()
            facilities = facility_result.data

            # Get temporal data
            temporal_result = self.query_manager.get_temporal_analysis_data()

            if not facilities or not temporal_result.success:
                return self._create_empty_result("temporal_timeline")

            # Build timeline structure
            timeline_data = self._build_timeline_matrix(facilities, temporal_result.data)

            return IntelligenceResult(
                analysis_type="temporal_timeline",
                data=timeline_data,
                metadata={
                    "facilities": len(facilities),
                    "years": len(timeline_data.get("year_range", [])),
                },
                quality_score=1.0 if timeline_data["total_records"] > 0 else 0.0,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "temporal timeline analysis")
            return self._create_empty_result("temporal_timeline")

    def analyze_causal_intelligence(self, facility_id: str = None) -> IntelligenceResult:
        """Analyze causal patterns and intelligence"""
        try:
            causal_result = self.query_manager.get_causal_intelligence_data(facility_id)

            if not causal_result.success:
                return self._create_empty_result("causal_intelligence")

            # Analyze causal patterns
            patterns_analysis = self._analyze_causal_patterns(causal_result.data)

            intelligence_data = {
                "causal_patterns": causal_result.data,
                "pattern_analysis": patterns_analysis,
                "facility_scope": facility_id or "all_facilities",
                "total_patterns": len(causal_result.data),
            }

            quality_score = self._calculate_causal_quality(causal_result.data)

            return IntelligenceResult(
                analysis_type="causal_intelligence",
                data=intelligence_data,
                metadata={
                    "facility_filter": facility_id,
                    "patterns_found": len(causal_result.data),
                },
                quality_score=quality_score,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "causal intelligence analysis")
            return self._create_empty_result("causal_intelligence")

    def analyze_data_quality(self) -> IntelligenceResult:
        """Comprehensive data quality assessment"""
        quality_data: Dict[str, Any] = {}
        try:
            # Get workflow completion rates
            workflow_result = self.query_manager.get_workflow_completion_rates()

            if not workflow_result.success or not workflow_result.data:
                return self._create_empty_result("data_quality")

            completion_data = workflow_result.data[0]

            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(completion_data)

            # Analyze entity completeness based on actual data
            entity_completeness = self._analyze_entity_completeness()

            quality_data = {
                "workflow_completeness": quality_metrics,
                "entity_completeness": entity_completeness,
                "overall_score": quality_metrics.get("overall_score", 0.0),
                "recommendations": self._generate_quality_recommendations(quality_data),
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

    def analyze_facility_completeness(self, facility_id: str = None) -> IntelligenceResult:
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
                metadata={
                    "facility_filter": facility_id or "all_facilities",
                },
                quality_score=quality_score,
                generated_at=datetime.now().isoformat(),
            )
        except Exception as e:
            handle_error(logger, e, f"facility completeness analysis for {facility_id or 'all'}")
            return self._create_empty_result("facility_completeness")

    def get_missing_data_impact(self) -> IntelligenceResult:
        """Schema-driven missing data impact analysis"""
        try:
            # Get entity names from schema
            ar_entity = get_entity_names().get("ActionRequest", "ActionRequest")
            problem_entity = get_entity_names().get("Problem", "Problem")
            rootcause_entity = get_entity_names().get("RootCause", "RootCause")
            actionplan_entity = get_entity_names().get("ActionPlan", "ActionPlan")
            verification_entity = get_entity_names().get("Verification", "Verification")

            # Get relationship types from schema
            # These would ideally be from a get_relationships utility or config
            identified_rel = "IDENTIFIED_PROBLEM"
            analyzes_rel = "ANALYZES_PROBLEM"
            resolves_rel = "RESOLVES_ROOT_CAUSE"
            validates_rel = "VALIDATES_ACTION_PLAN"

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

            impact_results = self.query_manager.execute_query(impact_query)

            analysis = {"chain_completeness": {}, "usability_assessment": {}, "engineer_impact": {}}

            total_incidents = sum(result["count"] for result in impact_results)

            for result in impact_results:
                chain_key = result["chain_status"]
                usable_key = result["usability_status"]
                count = result["count"]
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
                "recommendation": "Focus on completing workflow chains for engineer effectiveness",
            }

            quality_score = 1.0 if usable_percentage > 0 else 0.0
            return IntelligenceResult(
                analysis_type="missing_data_impact",
                data=analysis,
                metadata={
                    "total_incidents_analyzed": total_incidents,
                },
                quality_score=quality_score,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "missing data impact analysis")
            return self._create_empty_result("missing_data_impact")

    def analyze_action_request_facility_statistics(self) -> IntelligenceResult:
        """Analyze ActionRequest statistics by facility"""
        try:
            # Get ActionRequest data per facility
            facility_stats_query = """
            MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
            WHERE NOT '_SchemaTemplate' IN labels(ar)
            WITH f.facility_id AS facility_id,
                 count(ar) AS total_records,
                 count(DISTINCT ar.action_request_number) AS unique_actions,
                 collect(ar.action_request_number) AS action_numbers
            WITH facility_id, total_records, unique_actions, action_numbers,
                 toFloat(total_records) / unique_actions AS records_per_action

            // Calculate max records per action number
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

            # Extract the actual data from QueryResult
            facility_data = result.data

            # Calculate totals
            total_records = sum(row["total_records"] for row in facility_data)
            total_unique_actions = sum(row["unique_actions"] for row in facility_data)
            average_records_per_action = (
                total_records / total_unique_actions if total_unique_actions > 0 else 0
            )

            analysis_data = {
                "facility_statistics": facility_data,
                "summary_totals": {
                    "total_records": total_records,
                    "total_unique_actions": total_unique_actions,
                    "average_records_per_action": round(average_records_per_action, 1),
                },
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

    # Private analysis methods

    def _analyze_field_coverage(self) -> Dict[str, Any]:
        """Analyze field coverage from schema, excluding Facility entity and underscore-prefixed fields."""
        entity_mappings = self.mappings.get("entity_mappings", {})
        unique_fields = set()

        for entity_name, field_map in entity_mappings.items():
            if entity_name == "Facility":
                continue  # Exclude Facility entity

            # Filter out fields that start with an underscore
            filtered_fields = [field for field in field_map.values() if not field.startswith("_")]
            unique_fields.update(filtered_fields)

        return {
            "total_fields": len(unique_fields),
            "entities_mapped": len(entity_mappings) - (1 if "Facility" in entity_mappings else 0),
            "field_list": sorted(list(unique_fields)),
        }

    def _calculate_year_span(self, temporal_data: List[Dict[str, Any]]) -> str:
        """Calculate year span from temporal data"""
        if not temporal_data:
            return "Unknown"

        years = [int(item["year"]) for item in temporal_data if item.get("year")]
        if not years:
            return "Unknown"

        return f"{min(years)}-{max(years)}"

    def _calculate_percentages(self, values: List[int], total: int) -> List[float]:
        """Calculate percentage distribution"""
        if total == 0:
            return [0.0] * len(values)
        return [round((value / total) * 100, 1) for value in values]

    def _analyze_distribution_balance(self, values: List[int]) -> Dict[str, Any]:
        """Analyze distribution balance and concentration"""
        if not values:
            return {}

        total = sum(values)
        max_value = max(values)

        return {
            "concentration_ratio": round((max_value / total) * 100, 1) if total > 0 else 0,
            "balance_score": 1.0 - (max_value / total) if total > 0 else 0,
            "distribution_type": "concentrated" if max_value / total > 0.5 else "balanced",
        }

    def _analyze_field_balance(self, field_categories: Dict[str, List]) -> Dict[str, Any]:
        """Analyze field type balance"""
        category_counts = {cat: len(fields) for cat, fields in field_categories.items()}
        total_fields = sum(category_counts.values())

        return {
            "category_distribution": category_counts,
            "dominant_category": max(category_counts, key=category_counts.get)
            if category_counts
            else None,
            "balance_score": len([c for c in category_counts.values() if c > 0])
            / len(category_counts),
        }

    def _build_timeline_matrix(
        self, facilities: List[Dict], temporal_data: List[Dict]
    ) -> Dict[str, Any]:
        """Build timeline matrix from facility and temporal data"""
        # Extract years
        years = sorted(list(set([int(item["year"]) for item in temporal_data if item.get("year")])))

        # Build matrix structure (simplified for core logic)
        facility_names = [f.get("facility_id", "Unknown") for f in facilities]

        # Helper to parse markdown link from facility_id
        def _parse_markdown_link(text: str) -> Tuple[Optional[str], Optional[str]]:
            match = re.match(r"\[(.*?)\]\((.*?)\)", text)
            if match:
                display_text, url = match.groups()
                # Extract facility_id from /facility/{facility_id}
                if url.startswith("/facility/"):
                    raw_id = url.replace("/facility/", "")
                    return display_text, raw_id
            return None, None

        # Create rows structure
        rows = []
        total_records = 0

        for facility_id in facility_names:
            display_facility_name = ""
            facility_id_raw = ""

            # Check if facility_id is already a markdown link
            parsed_text, parsed_id = _parse_markdown_link(facility_id)
            if parsed_text and parsed_id:
                display_facility_name = parsed_text
                facility_id_raw = parsed_id
            else:
                # Original logic for non-markdown facility_ids
                display_facility_name = facility_id.replace("_", " ").title()
                facility_id_raw = facility_id

            row = {
                "facility": display_facility_name,
                "facility_id_raw": facility_id_raw,
                "total": 0,
            }
            for year in years:
                # Match actual incident counts from temporal_data
                # temporal_data structure: [{'facility_id': '...', 'year': 'YYYY', 'incident_count': N}]
                # Find the incident count for the current facility and year
                incident_count = next(
                    (
                        item.get("incident_count", 0)
                        for item in temporal_data
                        if item.get("facility_id") == facility_id and item.get("year") == str(year)
                    ),
                    0,
                )
                row[str(year)] = incident_count
                row["total"] += incident_count

            rows.append(row)
            total_records += row["total"]

        # Add totals row
        # For the total row, facility_id_raw is not applicable for linking.
        totals_row = {"facility": "Total", "facility_id_raw": "Total", "total": total_records}
        for year in years:
            totals_row[str(year)] = sum(
                row.get(str(year), 0) for row in rows[:-1]
            )  # Sum all facility rows excluding the 'Total' row
        rows.append(totals_row)

        return {
            "columns": ["facility"] + [str(year) for year in years] + ["total"],
            "rows": rows,
            "year_range": years,
            "total_records": total_records,
            "facilities_count": len(facility_names),
        }

    def _analyze_causal_patterns(self, patterns: List[Dict]) -> Dict[str, Any]:
        """Analyze causal intelligence patterns"""
        if not patterns:
            return {}

        # Analyze pattern frequency distribution
        frequencies = [p.get("frequency", 0) for p in patterns]

        return {
            "pattern_count": len(patterns),
            "frequency_range": {"min": min(frequencies), "max": max(frequencies)},
            "high_frequency_patterns": len([f for f in frequencies if f > 5]),
            "pattern_diversity": len(set([p.get("primary_cause") for p in patterns])),
        }

    def _calculate_portfolio_quality(self, portfolio_data: Dict) -> float:
        """Calculate portfolio data quality score"""
        factors = [
            1.0 if portfolio_data["total_records"] > 0 else 0.0,
            1.0 if portfolio_data["facilities"] > 0 else 0.0,
            1.0 if portfolio_data["data_fields"] > 0 else 0.0,
            1.0 if portfolio_data["years_coverage"] > 0 else 0.0,
        ]
        return sum(factors) / len(factors)

    def _calculate_causal_quality(self, patterns: List[Dict]) -> float:
        """Calculate causal intelligence quality score"""
        if not patterns:
            return 0.0

        # Quality based on pattern count and diversity
        pattern_score = min(1.0, len(patterns) / 10)
        diversity_score = len(set([p.get("primary_cause") for p in patterns])) / len(patterns)

        return (pattern_score + diversity_score) / 2

    def _analyze_facility_performance_metrics(
        self, causal_patterns: List[Dict], facility_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze and calculate facility performance metrics"""
        category_distribution = {}
        for pattern in causal_patterns:
            category = pattern.get("category", "Unknown")
            category_distribution[category] = category_distribution.get(category, 0) + pattern.get(
                "frequency", 0
            )

        total_records = sum(category_distribution.values())
        category_percentages = {}
        for category, count in category_distribution.items():
            percentage = round((count / total_records * 100), 1) if total_records > 0 else 0
            category_percentages[category] = percentage

        facility_info = facility_metrics.data[0] if facility_metrics.data else {}

        return {
            "total_records": total_records,
            "incident_count": facility_info.get("incident_count", 0),
            "facility_name": facility_info.get("facility_name", "Unknown"),
            "active": facility_info.get("active", True),
            "category_distribution": category_distribution,
            "category_percentages": category_percentages,
            "categories_count": len(category_distribution),
            "causal_patterns": causal_patterns,
        }

    def _calculate_facility_comparison_metrics(
        self, target_facility_data: Dict[str, Any], all_facilities_metrics: List[Dict]
    ) -> Dict[str, Any]:
        """Calculate comparison metrics for a facility against others"""
        target_records = target_facility_data.get("total_records", 0)

        other_facilities = [
            f
            for f in all_facilities_metrics
            if f.get("facility_id") != target_facility_data.get("facility_id")
        ]

        other_records = [f.get("incident_count", 0) for f in other_facilities]
        avg_other_records = sum(other_records) / len(other_records) if other_records else 0

        performance_rank = sum(1 for r in other_records if r < target_records) + 1
        total_facilities = len(other_records) + 1

        return {
            "target_records": target_records,
            "average_other_records": avg_other_records,
            "performance_rank": performance_rank,
            "total_facilities": total_facilities,
            "percentile": round((performance_rank / total_facilities) * 100, 1),
            "vs_average": round(((target_records - avg_other_records) / avg_other_records * 100), 1)
            if avg_other_records > 0
            else 0,
        }

    def _create_empty_result(self, analysis_type: str) -> IntelligenceResult:
        """Create empty result for error cases"""
        empty_data: Dict[str, Any] = {}
        if analysis_type == "data_quality":
            empty_data = {
                "workflow_completeness": {
                    "overall_status": False,
                    "overall_score": 0.0,
                    "details": {},
                    "completeness_score": 0.0,
                    "consistency_score": 0.0,
                    "freshness_score": 0.0,
                },
                "entity_completeness": {},
                "overall_score": 0.0,
                "recommendations": [],
            }
        return IntelligenceResult(
            analysis_type=analysis_type,
            data=empty_data,
            metadata={"error": "Analysis failed"},
            quality_score=0.0,
            generated_at=datetime.now().isoformat(),
        )

    def _calculate_quality_metrics(self, completion_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall data quality metrics based on Neo4j data"""
        total_requests = completion_data.get("total_requests", 0)
        problems_defined = completion_data.get("problems_defined", 0)
        causes_analyzed = completion_data.get("causes_analyzed", 0)
        plans_developed = completion_data.get("plans_developed", 0)
        plans_verified = completion_data.get("plans_verified", 0)

        # Calculate completion rates for each stage
        problem_completion = (problems_defined / total_requests) if total_requests > 0 else 0
        cause_completion = (causes_analyzed / problems_defined) if problems_defined > 0 else 0
        plan_completion = (plans_developed / causes_analyzed) if causes_analyzed > 0 else 0
        verification_completion = (plans_verified / plans_developed) if plans_developed > 0 else 0

        # Overall completion rate (simplified average for now)
        completion_rates = [
            problem_completion,
            cause_completion,
            plan_completion,
            verification_completion,
        ]
        overall_completion_rate = sum(completion_rates) / len(completion_rates)

        # Determine overall status based on a threshold
        overall_status = overall_completion_rate > 0.7  # Example threshold

        return {
            "overall_status": overall_status,
            "overall_score": round(overall_completion_rate * 100, 2),
            "details": {
                "total_requests": total_requests,
                "problems_defined": problems_defined,
                "causes_analyzed": causes_analyzed,
                "plans_developed": plans_developed,
                "plans_verified": plans_verified,
                "problem_completion_rate": round(problem_completion * 100, 2),
                "cause_completion_rate": round(cause_completion * 100, 2),
                "plan_completion_rate": round(plan_completion * 100, 2),
                "verification_completion_rate": round(verification_completion * 100, 2),
            },
            "completeness_score": round(overall_completion_rate * 100, 2),
            "consistency_score": 0.0,  # TODO: Implement actual consistency score query
            "freshness_score": 0.0,  # TODO: Implement actual freshness score query
        }

    def _analyze_entity_completeness(self) -> Dict[str, Any]:
        """Analyze completeness of key entities from Neo4j"""
        entity_completeness_data = {}
        entity_types = [
            "ActionRequest",
            "Problem",
            "RootCause",
            "ActionPlan",
            "Verification",
        ]

        for entity_type in entity_types:
            total_count = self.query_manager.get_entity_count(entity_type)

            meaningful_data_count = self.query_manager.get_entity_count(entity_type)

            completeness_percentage = (
                (meaningful_data_count / total_count) * 100 if total_count > 0 else 0
            )

            entity_completeness_data[entity_type] = {
                "total_count": total_count,
                "meaningful_data_count": meaningful_data_count,
                "completeness_percentage": round(completeness_percentage, 2),
                "is_complete": completeness_percentage > 80,  # Example threshold
            }

        return entity_completeness_data

    def _generate_quality_recommendations(self, quality_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on data quality metrics"""
        recommendations = []
        # Check overall status from workflow completeness
        if not quality_data.get("workflow_completeness", {}).get("overall_status", False):
            recommendations.append("Investigate workflow stage completion rates for bottlenecks.")

        # Iterate over entity completeness details
        for entity, data in quality_data.get("entity_completeness", {}).items():
            if "completeness_percentage" in data and data["completeness_percentage"] < 90:
                recommendations.append(
                    f"Improve data completeness for {entity} entity (currently {data['completeness_percentage']}%)."
                )
        return recommendations

    def _analyze_single_facility_completeness(self, facility_id: str) -> Dict[str, Any]:
        """Schema-driven single facility completeness analysis"""
        facility_entity = get_entity_names().get("Facility", "Facility")
        ar_entity = get_entity_names().get("ActionRequest", "ActionRequest")
        facility_pk = get_entity_primary_key("Facility")
        entity_connections = get_entity_connections()
        belongs_to_rel = entity_connections.get("ActionRequest_BELONGS_TO_Facility", "BELONGS_TO")

        facility_query = f"""
        MATCH (f:{facility_entity} {{{facility_pk}: $facility_id}})<-[:{belongs_to_rel}]-(ar:{ar_entity})
        RETURN f.facility_name as name, count(ar) as total_incidents
        """

        facility_result = self.query_manager.execute_query(facility_query, facility_id=facility_id)

        if not facility_result:
            return {"error": f"Facility {facility_id} not found"}

        facility_info = facility_result[0]

        problem_entity = get_entity_names().get("Problem", "Problem")
        rootcause_entity = get_entity_names().get("RootCause", "RootCause")
        actionplan_entity = get_entity_names().get("ActionPlan", "ActionPlan")
        verification_entity = get_entity_names().get("Verification", "Verification")

        identified_rel = entity_connections.get(
            "Problem_IDENTIFIED_FROM_ActionRequest", "IDENTIFIED_PROBLEM"
        )
        analyzes_rel = entity_connections.get("RootCause_ANALYZES_Problem", "ANALYZES_PROBLEM")
        resolves_rel = entity_connections.get(
            "ActionPlan_RESOLVES_RootCause", "RESOLVES_ROOT_CAUSE"
        )
        validates_rel = entity_connections.get(
            "Verification_VALIDATES_ActionPlan", "VALIDATES_ACTION_PLAN"
        )

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

        completeness_result = self.query_manager.execute_query(
            completeness_query, facility_id=facility_id
        )
        stats = completeness_result[0] if completeness_result else {}

        total = stats.get("total_requests", 0)
        if total == 0:
            return {"error": f"No data found for facility {facility_id}"}

        completeness_analysis = {
            "facility_name": facility_info["name"],
            "total_incidents": total,
            "completeness_metrics": {
                "basic_info": {
                    "title": round((stats.get("has_title", 0) / total) * 100, 1),
                    "stage": round((stats.get("has_stage", 0) / total) * 100, 1),
                    "categories": round((stats.get("has_categories", 0) / total) * 100, 1),
                },
                "workflow_chain": {
                    "has_problem": round((stats.get("has_problem", 0) / total) * 100, 1),
                    "has_root_cause": round((stats.get("has_root_cause", 0) / total) * 100, 1),
                    "has_action_plan": round((stats.get("has_action_plan", 0) / total) * 100, 1),
                    "has_verification": round((stats.get("has_verification", 0) / total) * 100, 1),
                },
                "engineer_critical": {
                    "problem_description": round(
                        (stats.get("has_problem_description", 0) / total) * 100, 1
                    ),
                    "cause_description": round(
                        (stats.get("has_cause_description", 0) / total) * 100, 1
                    ),
                    "plan_description": round(
                        (stats.get("has_plan_description", 0) / total) * 100, 1
                    ),
                    "effectiveness_data": round(
                        (stats.get("has_effectiveness_data", 0) / total) * 100, 1
                    ),
                },
            },
        }

        completeness_analysis["quality_insights"] = self._generate_quality_insights(
            completeness_analysis
        )

        return completeness_analysis

    def _analyze_all_facilities_completeness(self) -> Dict[str, Any]:
        """Schema-driven multi-facility comparison analysis"""

        facility_entity = get_entity_names().get("Facility", "Facility")
        facility_pk = get_entity_primary_key("Facility")

        facilities_query = f"""
        MATCH (f:{facility_entity})
        WHERE NOT '_SchemaTemplate' IN labels(f)
        RETURN f.{facility_pk} as id, f.facility_name as name
        ORDER BY f.facility_name
        """
        facilities = self.query_manager.execute_query(facilities_query)

        comparison = {"facilities": [], "cross_facility_insights": {}}

        for facility in facilities:
            facility_analysis = self._analyze_single_facility_completeness(facility["id"])
            if "error" not in facility_analysis:
                comparison["facilities"].append(facility_analysis)

        comparison["cross_facility_insights"] = self._generate_cross_facility_insights(
            comparison["facilities"]
        )

        return comparison

    def _generate_quality_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable insights based on completeness analysis"""
        insights = []
        metrics = analysis["completeness_metrics"]

        workflow = metrics["workflow_chain"]
        if workflow["has_root_cause"] < 70:
            insights.append(
                f"Critical: {100 - workflow['has_root_cause']:.1f}% of incidents lack root cause analysis"
            )

        if workflow["has_verification"] < 50:
            insights.append(
                f"Warning: {100 - workflow['has_verification']:.1f}% of action plans lack effectiveness verification"
            )

        engineer = metrics["engineer_critical"]
        if engineer["problem_description"] < 80:
            insights.append(
                f"Impact: {100 - engineer['problem_description']:.1f}% of problems lack clear descriptions"
            )

        if engineer["effectiveness_data"] < 60:
            insights.append(
                f"Learning Gap: {100 - engineer['effectiveness_data']:.1f}% of solutions lack effectiveness data"
            )

        return insights

    def _generate_cross_facility_insights(self, facilities: List[Dict]) -> Dict[str, Any]:
        """Generate cross-facility comparison insights"""
        if len(facilities) < 2:
            return {}

        insights = {"best_performers": {}, "improvement_opportunities": [], "patterns": []}

        categories = ["workflow_chain", "engineer_critical"]
        for category in categories:
            best_facility = max(
                facilities, key=lambda f: sum(f["completeness_metrics"][category].values())
            )
            worst_facility = min(
                facilities, key=lambda f: sum(f["completeness_metrics"][category].values())
            )

            insights["best_performers"][category] = {
                "best": best_facility["facility_name"],
                "worst": worst_facility["facility_name"],
            }

        for facility in facilities:
            metrics = facility["completeness_metrics"]["engineer_critical"]
            if metrics["effectiveness_data"] < 50:
                insights["improvement_opportunities"].append(
                    f"{facility['facility_name']}: Improve solution effectiveness tracking"
                )

        return insights


# Singleton pattern
_intelligence_engine = None


def get_intelligence_engine() -> IntelligenceEngine:
    """Get singleton intelligence engine instance"""
    global _intelligence_engine
    if _intelligence_engine is None:
        _intelligence_engine = IntelligenceEngine()
    return _intelligence_engine

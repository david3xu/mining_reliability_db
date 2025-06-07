#!/usr/bin/env python3
"""
Portfolio Intelligence Engine - Portfolio and Distribution Analysis
Focused analysis of portfolio metrics, facility distribution, and temporal patterns.
"""

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Tuple, Optional

from configs.environment import (
    get_entity_names,
    get_field_category_display_mapping,
    get_mappings,
    get_schema,
)
from mine_core.database.query_manager import get_query_manager
from mine_core.shared.common import handle_error
from mine_core.business.intelligence_models import IntelligenceResult

logger = logging.getLogger(__name__)


class PortfolioIntelligence:
    """Portfolio-level analysis and distribution intelligence"""

    def __init__(self):
        self.query_manager = get_query_manager()
        self.schema = get_schema()
        self.mappings = get_mappings()

    def analyze_metrics(self) -> IntelligenceResult:
        """Analyze portfolio-level metrics and coverage"""
        try:
            # Get facility data
            facility_result = self.query_manager.get_facility_metrics()
            facilities = facility_result.data

            # Get total records from temporal analysis
            temporal_analysis_result = self.analyze_temporal_timeline()
            total_records = temporal_analysis_result.data.get("total_records", 0)

            # Analyze field coverage
            field_analysis = self._analyze_field_coverage()

            # Extract temporal coverage
            years_coverage = len(temporal_analysis_result.metadata.get("years", []))
            year_detail = temporal_analysis_result.data.get("year_detail", "Unknown")

            portfolio_data = {
                "total_records": total_records,
                "data_fields": field_analysis["total_fields"],
                "facilities": len(facilities),
                "years_coverage": years_coverage,
                "year_detail": year_detail,
                "facilities_data": facilities,
            }

            quality_score = self._calculate_portfolio_quality(portfolio_data)

            return IntelligenceResult(
                analysis_type="portfolio_metrics",
                data=portfolio_data,
                metadata={"source": "portfolio_intelligence", "facilities_analyzed": len(facilities)},
                quality_score=quality_score,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "portfolio metrics analysis")
            return self._create_empty_intelligence_result("portfolio_metrics")

    def analyze_facility_distribution(self) -> IntelligenceResult:
        """Analyze facility-wise record distribution"""
        try:
            facility_result = self.query_manager.get_facility_metrics()
            facilities = facility_result.data

            if not facilities:
                return self._create_empty_intelligence_result("facility_distribution")

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
            return self._create_empty_intelligence_result("facility_distribution")

    def analyze_field_type_distribution(self) -> IntelligenceResult:
        """Analyze field type distribution from schema configuration"""
        try:
            categorized_counts = {}
            schema_entities_map = {
                entity.get("name"): entity.get("properties", {})
                for entity in self.schema.get("entities", [])
            }

            # Type mapping
            raw_type_to_category_key_map = {
                "string": "descriptive_fields",
                "text": "descriptive_fields",
                "date": "temporal_fields",
                "integer": "quantitative_fields",
                "boolean": "boolean_fields",
            }

            # Process entity mappings
            entity_mappings_from_config = self.mappings.get("entity_mappings", {})
            detailed_field_names = {category: [] for category in raw_type_to_category_key_map.values()}

            for entity_name, field_map in entity_mappings_from_config.items():
                if entity_name == "Facility":
                    continue  # Exclude Facility entity

                entity_properties = schema_entities_map.get(entity_name, {})

                for internal_field_name, raw_data_field_name in field_map.items():
                    if internal_field_name == "root_cause_tail_extraction":
                        continue  # Exclude derived field

                    prop_details = entity_properties.get(internal_field_name)
                    if prop_details:
                        raw_type = prop_details.get("type")
                        category_key = raw_type_to_category_key_map.get(raw_type)

                        if category_key:
                            categorized_counts[category_key] = categorized_counts.get(category_key, 0) + 1
                            detailed_field_names[category_key].append(raw_data_field_name)

            # Prepare chart data
            labels, values, total_fields = self._prepare_chart_data(categorized_counts)
            percentages = self._calculate_percentages(values, total_fields)

            distribution_data = {
                "labels": labels,
                "values": values,
                "percentages": percentages,
                "total_fields": total_fields,
                "category_counts": categorized_counts,
                "detailed_field_names": detailed_field_names,
                "category_analysis": self._analyze_field_balance(self.mappings.get("field_categories", {})),
            }

            quality_score = 1.0 if total_fields > 0 else 0.0

            return IntelligenceResult(
                analysis_type="field_distribution",
                data=distribution_data,
                metadata={"source": "schema_configuration", "categories": len(categorized_counts)},
                quality_score=quality_score,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "field distribution analysis")
            return self._create_empty_intelligence_result("field_distribution")

    def analyze_temporal_timeline(self) -> IntelligenceResult:
        """Analyze historical timeline patterns"""
        try:
            # Get facility data
            facility_result = self.query_manager.get_facility_metrics()
            facilities = facility_result.data

            # Get temporal data
            temporal_result = self.query_manager.get_temporal_analysis_data()

            if not facilities or not temporal_result.success:
                return self._create_empty_intelligence_result("temporal_timeline")

            # Build timeline structure
            timeline_data = self._build_timeline_matrix(facilities, temporal_result.data)

            # Calculate year span
            year_span_str = self._calculate_year_span(temporal_result.data)
            timeline_data["year_detail"] = year_span_str

            return IntelligenceResult(
                analysis_type="temporal_timeline",
                data=timeline_data,
                metadata={"years": timeline_data.get("year_range", []), "total_records": timeline_data.get("total_records", 0)},
                quality_score=1.0 if timeline_data.get("total_records", 0) > 0 else 0.0,
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "temporal timeline analysis")
            return self._create_empty_intelligence_result("temporal_timeline")

    # Helper Methods

    def _analyze_field_coverage(self) -> Dict[str, Any]:
        """Analyze field coverage and completeness based on schema"""
        try:
            entity_properties_map = {
                entity["name"]: entity["properties"]
                for entity in self.schema["entities"]
                if "properties" in entity
            }

            field_completeness = []
            total_required_fields = 0
            covered_fields = 0

            for entity_name, entity_fields in self.mappings["entity_mappings"].items():
                if entity_name == "Facility":
                    continue

                for internal_field_name, external_field_name in entity_fields.items():
                    if internal_field_name == "root_cause_tail_extraction":
                        continue  # Skip derived field

                    if external_field_name and entity_properties_map.get(entity_name, {}).get(internal_field_name, {}).get("required", False):
                        total_required_fields += 1
                        # For actual coverage, we'd need to query the database and count non-null values.
                        # For this simulation, we'll assume a certain level of coverage.
                        # In a real system, this would involve a database query.
                        covered_fields += 1  # Placeholder

                    field_completeness.append({
                        "entity": entity_name,
                        "internal_field": internal_field_name,
                        "external_field": external_field_name,
                        "is_required": entity_properties_map.get(entity_name, {}).get(internal_field_name, {}).get("required", False)
                    })

            return {
                "total_fields": len(field_completeness),
                "required_fields": total_required_fields,
                "covered_required_fields": covered_fields,
                "field_details": field_completeness,
                "coverage_percentage": covered_fields / total_required_fields if total_required_fields > 0 else 0.0,
            }

        except Exception as e:
            handle_error(logger, e, "field coverage analysis")
            return {
                "total_fields": 0,
                "required_fields": 0,
                "covered_required_fields": 0,
                "field_details": [],
                "coverage_percentage": 0.0,
            }

    def _calculate_year_span(self, temporal_data: List[Dict[str, Any]]) -> str:
        """Calculate year span from temporal data"""
        if not temporal_data:
            return "Unknown"

        years = []
        for item in temporal_data:
            year_str = item.get("year")
            if year_str:
                try:
                    year = int(year_str)
                    if 1900 <= year <= 2100:
                        years.append(year)
                except (ValueError, TypeError):
                    continue

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
            "dominant_category": max(category_counts, key=category_counts.get) if category_counts else None,
            "balance_score": len([c for c in category_counts.values() if c > 0]) / len(category_counts),
        }

    def _prepare_chart_data(self, categorized_counts: Dict[str, int]) -> Tuple[List[str], List[int], int]:
        """Prepare chart data with display names"""
        labels = []
        values = []
        total_fields = 0

        category_display_mapping = get_field_category_display_mapping()

        for category_key, count in categorized_counts.items():
            display_name = category_display_mapping.get(
                category_key, category_key.replace("_", " ").title()
            )
            labels.append(display_name)
            values.append(count)
            total_fields += count

        return labels, values, total_fields

    def _build_timeline_matrix(self, facilities: List[Dict], temporal_data: List[Dict]) -> Dict[str, Any]:
        """Build timeline matrix from facility and temporal data"""
        logger.info(f"Building timeline matrix with {len(temporal_data)} temporal records")

        # Extract and validate years
        valid_years = []
        for item in temporal_data:
            year_str = item.get("year")
            if year_str:
                try:
                    year = int(year_str)
                    if 1900 <= year <= 2100:
                        valid_years.append(year)
                except (ValueError, TypeError):
                    continue

        years = sorted(list(set(valid_years)))
        logger.info(f"Valid years extracted: {years}")

        if not years:
            return {
                "columns": ["facility", "total"],
                "rows": [],
                "year_range": [],
                "total_records": 0,
                "facilities_count": 0,
            }

        # Build matrix structure
        facility_names = [f.get("facility_id", "Unknown") for f in facilities]
        rows = []
        total_records = 0

        for facility_id in facility_names:
            display_name, raw_id = self._parse_facility_display(facility_id)

            row = {"facility": display_name, "facility_id_raw": raw_id, "total": 0}

            for year in years:
                incident_count = self._get_incident_count_for_year(temporal_data, facility_id, year)
                row[str(year)] = incident_count
                row["total"] += incident_count

            rows.append(row)
            total_records += row["total"]

        # Add totals row
        totals_row = {"facility": "Total", "facility_id_raw": "Total", "total": total_records}
        for year in years:
            totals_row[str(year)] = sum(row.get(str(year), 0) for row in rows)
        rows.append(totals_row)

        return {
            "columns": ["facility"] + [str(year) for year in years] + ["total"],
            "rows": rows,
            "year_range": years,
            "total_records": total_records,
            "facilities_count": len(facility_names),
        }

    def _parse_facility_display(self, facility_id: str) -> Tuple[str, str]:
        """Parse facility display name and raw ID"""
        match = re.match(r"\[(.*?)\]\((.*?)\)", facility_id)
        if match:
            display_text, url = match.groups()
            if url.startswith("/facility/"):
                raw_id = url.replace("/facility/", "")
                return display_text, raw_id

        # Default handling
        display_name = facility_id.replace("_", " ").title()
        return display_name, facility_id

    def _get_incident_count_for_year(self, temporal_data: List[Dict], facility_id: str, year: int) -> int:
        """Get incident count for specific facility and year"""
        for item in temporal_data:
            if (item.get("facility_id") == facility_id and
                item.get("year") == str(year)):
                return item.get("incident_count", 0)
        return 0

    def _calculate_portfolio_quality(self, portfolio_data: Dict) -> float:
        """Calculate portfolio data quality score"""
        factors = [
            1.0 if portfolio_data["total_records"] > 0 else 0.0,
            1.0 if portfolio_data["facilities"] > 0 else 0.0,
            1.0 if portfolio_data["data_fields"] > 0 else 0.0,
            1.0 if portfolio_data["years_coverage"] > 0 else 0.0,
        ]
        return sum(factors) / len(factors)

    def _create_empty_result(self, analysis_type: str) -> Dict[str, Any]:
        """Create empty result for error cases"""
        return {
            "analysis_type": analysis_type,
            "data": {},
            "metadata": {"error": "Analysis failed"},
            "quality_score": 0.0,
            "generated_at": datetime.now().isoformat(),
        }

    def _create_empty_intelligence_result(self, analysis_type: str) -> IntelligenceResult:
        """Create empty IntelligenceResult for error cases"""
        return IntelligenceResult(
            analysis_type=analysis_type,
            data={},
            metadata={"error": "Analysis failed"},
            quality_score=0.0,
            generated_at=datetime.now().isoformat(),
        )

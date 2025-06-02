#!/usr/bin/env python3
"""
Core Business Intelligence Engine - Pure Business Logic
Centralized intelligence operations with schema-driven analysis capabilities.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from configs.environment import get_entity_names, get_mappings, get_schema
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
            field_categories = self.mappings.get("field_categories", {})

            if not field_categories:
                return self._create_empty_result("field_distribution")

            # Category mapping for display
            category_mapping = {
                "descriptive_fields": "Text/String (Unstructured)",
                "temporal_fields": "Date (Temporal)",
                "categorical_fields": "Categorical (Discrete)",
                "boolean_fields": "Boolean (Binary)",
                "identification_fields": "List (Multi-value)",
                "quantitative_fields": "Numeric (Quantitative)",
            }

            labels = []
            values = []
            total_fields = 0

            for category, display_name in category_mapping.items():
                field_count = len(field_categories.get(category, []))
                labels.append(display_name)
                values.append(field_count)
                total_fields += field_count

            percentages = self._calculate_percentages(values, total_fields)

            distribution_data = {
                "labels": labels,
                "values": values,
                "percentages": percentages,
                "total_fields": total_fields,
                "category_analysis": self._analyze_field_balance(field_categories),
            }

            quality_score = 1.0 if total_fields > 0 else 0.0

            return IntelligenceResult(
                analysis_type="field_distribution",
                data=distribution_data,
                metadata={"source": "schema_configuration", "categories": len(category_mapping)},
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
        try:
            # Get workflow completion rates
            workflow_result = self.query_manager.get_workflow_completion_rates()

            if not workflow_result.success or not workflow_result.data:
                return self._create_empty_result("data_quality")

            completion_data = workflow_result.data[0]

            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(completion_data)

            # Analyze entity completeness
            entity_analysis = self._analyze_entity_completeness()

            quality_data = {
                "workflow_completeness": quality_metrics,
                "entity_analysis": entity_analysis,
                "overall_score": quality_metrics.get("overall_quality", 0.0),
                "recommendations": self._generate_quality_recommendations(quality_metrics),
            }

            return IntelligenceResult(
                analysis_type="data_quality",
                data=quality_data,
                metadata={"entities_analyzed": len(entity_analysis), "workflow_stages": 5},
                quality_score=quality_data["overall_score"],
                generated_at=datetime.now().isoformat(),
            )

        except Exception as e:
            handle_error(logger, e, "data quality analysis")
            return self._create_empty_result("data_quality")

    # Private analysis methods

    def _analyze_field_coverage(self) -> Dict[str, Any]:
        """Analyze field coverage from schema"""
        entity_mappings = self.mappings.get("entity_mappings", {})
        unique_fields = set()

        for field_mapping in entity_mappings.values():
            unique_fields.update(field_mapping.values())

        return {
            "total_fields": len(unique_fields),
            "entities_mapped": len(entity_mappings),
            "field_list": list(unique_fields),
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

        # Create rows structure
        rows = []
        total_records = 0

        for facility in facility_names:
            row = {"facility": facility, "total": 0}
            for year in years:
                # Simplified assignment - in real implementation would match facility to year data
                count = sum(1 for f in facilities if f.get("facility_id") == facility)
                row[str(year)] = count
                row["total"] += count

            rows.append(row)
            total_records += row["total"]

        # Add totals row
        totals_row = {"facility": "Total", "total": total_records}
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

    def _create_empty_result(self, analysis_type: str) -> IntelligenceResult:
        """Create empty result for error cases"""
        return IntelligenceResult(
            analysis_type=analysis_type,
            data={},
            metadata={"error": "Analysis failed"},
            quality_score=0.0,
            generated_at=datetime.now().isoformat(),
        )


# Singleton pattern
_intelligence_engine = None


def get_intelligence_engine() -> IntelligenceEngine:
    """Get singleton intelligence engine instance"""
    global _intelligence_engine
    if _intelligence_engine is None:
        _intelligence_engine = IntelligenceEngine()
    return _intelligence_engine

#!/usr/bin/env python3
"""
Purified Data Adapter - Pure Data Access Layer
Clean adapter calling core business logic with zero embedded intelligence.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Pure core layer imports - no business logic in adapter
from mine_core.business.intelligence_engine import get_intelligence_engine
from dashboard.adapters.interfaces import (
    PortfolioData, FacilityData, FieldData, TimelineData,
    ComponentMetadata, ValidationResult
)
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

class PurifiedDataAdapter:
    """Pure data access adapter - calls core business logic only"""

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
                year_detail=portfolio_data.get("year_detail", "Unknown"),
                metadata=ComponentMetadata(
                    source="core.intelligence_engine",
                    generated_at=analysis_result.generated_at,
                    data_quality=analysis_result.quality_score
                )
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
                    data_quality=analysis_result.quality_score
                )
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
                metadata=ComponentMetadata(
                    source="core.intelligence_engine",
                    generated_at=analysis_result.generated_at,
                    data_quality=analysis_result.quality_score
                )
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
                    data_quality=analysis_result.quality_score
                )
            )

        except Exception as e:
            handle_error(logger, e, "historical timeline data access")
            return self._create_empty_timeline_data()

    def get_facility_performance_analysis(self, facility_id: str) -> Dict[str, Any]:
        """Pure data access for facility-specific analysis"""
        try:
            logger.info(f"Adapter: Fetching facility analysis from core for {facility_id}")

            # Call core business logic with facility filter
            analysis_result = self.intelligence_engine.analyze_causal_intelligence(facility_id)

            if not analysis_result.data:
                return {}

            # Pure data pass-through - no adapter business logic
            return {
                "facility_id": facility_id,
                "causal_patterns": analysis_result.data.get("causal_patterns", []),
                "pattern_analysis": analysis_result.data.get("pattern_analysis", {}),
                "total_records": analysis_result.data.get("total_patterns", 0),
                "metadata": ComponentMetadata(
                    source="core.intelligence_engine",
                    generated_at=analysis_result.generated_at,
                    data_quality=analysis_result.quality_score
                ).__dict__
            }

        except Exception as e:
            handle_error(logger, e, f"facility performance data access for {facility_id}")
            return {}

    def get_facility_comparison_metrics(self, facility_id: str) -> Dict[str, Any]:
        """Pure data access for facility comparison"""
        try:
            logger.info(f"Adapter: Fetching facility comparison from core for {facility_id}")

            # Get facility analysis
            facility_analysis = self.get_facility_performance_analysis(facility_id)

            # Get portfolio metrics for comparison baseline
            portfolio_result = self.intelligence_engine.analyze_portfolio_metrics()

            if not portfolio_result.data:
                return {}

            # Pure calculation - no business intelligence
            target_records = facility_analysis.get("total_records", 0)
            total_facilities = portfolio_result.data.get("facilities", 1)
            avg_records = portfolio_result.data.get("total_records", 0) / total_facilities

            return {
                "facility_id": facility_id,
                "target_records": target_records,
                "average_other_records": avg_records,
                "vs_average": ((target_records - avg_records) / avg_records * 100) if avg_records > 0 else 0,
                "performance_rank": 1,  # Simplified - core logic would calculate
                "total_facilities": total_facilities
            }

        except Exception as e:
            handle_error(logger, e, f"facility comparison data access for {facility_id}")
            return {}

    def validate_data_availability(self) -> ValidationResult:
        """Pure validation check using core services"""
        try:
            validation_status = {}

            # Test each core service
            portfolio_result = self.intelligence_engine.analyze_portfolio_metrics()
            validation_status["portfolio_metrics"] = portfolio_result.quality_score > 0

            facility_result = self.intelligence_engine.analyze_facility_distribution()
            validation_status["facility_breakdown"] = facility_result.quality_score > 0

            field_result = self.intelligence_engine.analyze_field_type_distribution()
            validation_status["field_distribution"] = field_result.quality_score > 0

            timeline_result = self.intelligence_engine.analyze_temporal_timeline()
            validation_status["historical_timeline"] = timeline_result.quality_score > 0

            # Calculate overall status
            all_valid = all(validation_status.values())
            quality_score = sum(validation_status.values()) / len(validation_status)

            return ValidationResult(
                is_valid=all_valid,
                component_status=validation_status,
                error_details=None if all_valid else "Some core services failed",
                data_quality_score=quality_score
            )

        except Exception as e:
            handle_error(logger, e, "data validation")
            return ValidationResult(
                is_valid=False,
                component_status={},
                error_details=str(e),
                data_quality_score=0.0
            )

    # Pure data transformation helpers - no business logic

    def _get_timestamp(self) -> str:
        """Pure timestamp generation"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _create_empty_portfolio_data(self) -> PortfolioData:
        """Pure empty data creation"""
        return PortfolioData(
            total_records=0, data_fields=0, facilities=0, years_coverage=0,
            year_detail="No data", metadata=ComponentMetadata(
                source="adapter_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    def _create_empty_facility_data(self) -> FacilityData:
        """Pure empty data creation"""
        return FacilityData(
            labels=[], values=[], percentages=[], total_records=0,
            metadata=ComponentMetadata(
                source="adapter_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    def _create_empty_field_data(self) -> FieldData:
        """Pure empty data creation"""
        return FieldData(
            labels=[], values=[], percentages=[], total_fields=0,
            metadata=ComponentMetadata(
                source="adapter_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    def _create_empty_timeline_data(self) -> TimelineData:
        """Pure empty data creation"""
        return TimelineData(
            columns=[], rows=[], year_range=[], total_records=0, facilities_count=0,
            metadata=ComponentMetadata(
                source="adapter_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

# Singleton pattern
_purified_adapter = None

def get_data_adapter() -> PurifiedDataAdapter:
    """Get singleton purified adapter instance"""
    global _purified_adapter
    if _purified_adapter is None:
        _purified_adapter = PurifiedDataAdapter()
    return _purified_adapter

def reset_adapter():
    """Reset adapter instance"""
    global _purified_adapter
    if _purified_adapter:
        logger.info("Resetting purified data adapter")
        _purified_adapter = None
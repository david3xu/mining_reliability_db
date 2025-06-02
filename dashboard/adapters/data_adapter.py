#!/usr/bin/env python3
"""
Data Adapter - Core Data Pipeline Integration
Unified data access layer with standardized interface.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from dashboard.adapters.interfaces import (
    ComponentMetadata,
    FacilityData,
    FieldData,
    PortfolioData,
    TimelineData,
    ValidationResult,
)
from mine_core.business.intelligence_engine import IntelligenceEngine, get_intelligence_engine
from mine_core.shared.common import handle_error

__all__ = [
    "PurifiedDataAdapter",
    "get_data_adapter",
    "reset_adapter",
]

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


# Singleton pattern
_data_adapter: Optional[PurifiedDataAdapter] = None


def get_data_adapter() -> PurifiedDataAdapter:
    """Get singleton data adapter instance"""
    global _data_adapter
    if _data_adapter is None:
        _data_adapter = PurifiedDataAdapter()
    return _data_adapter


def reset_adapter():
    """Reset data adapter for testing or re-initialization"""
    global _data_adapter
    _data_adapter = None

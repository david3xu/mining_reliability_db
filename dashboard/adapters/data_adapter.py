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
from dashboard.adapters.workflow_adapter import get_workflow_adapter
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

            from mine_core.database.query_manager import get_query_manager
            query_manager = get_query_manager()

            # Use schema-driven method
            search_result = query_manager.search_using_schema_configuration(search_text)

            if not search_result.success:
                logger.warning(f"Schema search failed: {search_result.metadata}")
                return []

            logger.info(f"Schema search found {search_result.count} results")
            return search_result.data

        except Exception as e:
            handle_error(logger, e, f"schema-driven search adapter for '{search_text}'")
            return []

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

            from mine_core.database.query_manager import get_query_manager

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
            from mine_core.database.query_manager import get_query_manager

            query_manager = get_query_manager()

            result = query_manager.get_core_workflow_labels()
            return [row["label"] for row in result.data] if result.success else []

        except Exception as e:
            handle_error(logger, e, "core workflow labels access")
            return []

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

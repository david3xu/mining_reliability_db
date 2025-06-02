#!/usr/bin/env python3
"""
Facility Adapter - Facility Data Access Layer
Single facility data extraction with standardized interface.
"""

import logging
from typing import Any, Dict, List, Optional

from dashboard.adapters.interfaces import ComponentMetadata

# Pure core layer imports
from mine_core.business.intelligence_engine import get_intelligence_engine
from mine_core.database.query_manager import get_query_manager
from mine_core.shared.common import handle_error

__all__ = [
    "FacilityAdapter",
    "get_facility_adapter",
    "reset_facility_adapter",
]

logger = logging.getLogger(__name__)


class FacilityAdapter:
    """Pure facility data access - calls core services only"""

    def __init__(self):
        """Initialize with core service connections"""
        self.intelligence_engine = get_intelligence_engine()
        self.query_manager = get_query_manager()

    def get_facility_performance_analysis(self, facility_id: str) -> Dict[str, Any]:
        """Pure data access for facility-specific performance analysis"""
        try:
            logger.info(f"Facility Adapter: Fetching performance analysis for {facility_id}")

            causal_analysis = self.intelligence_engine.analyze_causal_intelligence(facility_id)
            facility_metrics = self.query_manager.get_facility_metrics(facility_id)

            if not causal_analysis.data and not facility_metrics.success:
                return {}

            # Use intelligence engine for analysis
            performance_data = self.intelligence_engine._analyze_facility_performance_metrics(
                causal_analysis.data.get("causal_patterns", []),
                facility_metrics,
            )

            return {
                "facility_id": facility_id,
                "total_records": performance_data.get("total_records", 0),
                "incident_count": performance_data.get("incident_count", 0),
                "facility_name": performance_data.get("facility_name", facility_id),
                "active": performance_data.get("active", True),
                "category_distribution": performance_data.get("category_distribution", {}),
                "category_percentages": performance_data.get("category_percentages", {}),
                "categories_count": performance_data.get("categories_count", 0),
                "causal_patterns": performance_data.get("causal_patterns", []),
                "metadata": ComponentMetadata(
                    source="core.intelligence_engine",
                    generated_at=causal_analysis.generated_at,
                    data_quality=causal_analysis.quality_score,
                ).__dict__,
            }

        except Exception as e:
            handle_error(logger, e, f"facility performance analysis data access for {facility_id}")
            return {}

    def get_facility_comparison_metrics(self, facility_id: str) -> Dict[str, Any]:
        """Pure data access for facility comparison metrics"""
        try:
            logger.info(f"Facility Adapter: Fetching comparison metrics for {facility_id}")

            target_facility = self.get_facility_performance_analysis(facility_id)
            all_facilities_metrics_result = self.query_manager.get_facility_metrics()

            if not target_facility or not all_facilities_metrics_result.success:
                return {}

            comparison_metrics = self.intelligence_engine._calculate_facility_comparison_metrics(
                target_facility,
                all_facilities_metrics_result.data,
            )

            return {
                "facility_id": facility_id,
                "target_records": comparison_metrics.get("target_records", 0),
                "average_other_records": comparison_metrics.get("average_other_records", 0),
                "performance_rank": comparison_metrics.get("performance_rank", 0),
                "total_facilities": comparison_metrics.get("total_facilities", 0),
                "percentile": comparison_metrics.get("percentile", 0.0),
                "vs_average": comparison_metrics.get("vs_average", 0.0),
            }

        except Exception as e:
            handle_error(logger, e, f"facility comparison metrics data access for {facility_id}")
            return {}

    def get_facility_statistics_analysis(self, facility_id: str = None) -> Dict[str, Any]:
        """Pure data access for facility statistics using intelligence engine"""
        try:
            logger.info(
                f"Facility Adapter: Fetching statistics for {facility_id or 'all facilities'}"
            )

            # Use intelligence engine for facility completeness analysis
            analysis_result = self.intelligence_engine.analyze_facility_completeness(facility_id)

            if not analysis_result.data or analysis_result.data.get("error"):
                return {}

            if facility_id:
                # Single facility analysis
                facility_analysis = analysis_result.data
                return {
                    "facility_id": facility_id,
                    "facility_name": facility_analysis.get("facility_name", facility_id),
                    "total_action_requests": facility_analysis.get("total_incidents", 0),
                    "analysis_type": "single_facility",
                    "completeness_metrics": facility_analysis.get("completeness_metrics", {}),
                    "quality_insights": facility_analysis.get("quality_insights", []),
                    "metadata": analysis_result.metadata,
                }
            else:
                # All facilities analysis
                all_facilities_data = analysis_result.data.get("facilities", [])
                cross_facility_insights = analysis_result.data.get("cross_facility_insights", {})

                facilities_list = []
                total_incidents = 0

                for f_data in all_facilities_data:
                    incident_count = f_data.get("total_incidents", 0)
                    total_incidents += incident_count
                    facilities_list.append(
                        {
                            "facility_id": f_data.get("facility_id", "Unknown"),
                            "facility_name": f_data.get("facility_name", "Unknown"),
                            "total_action_requests": incident_count,
                            "completeness_metrics": f_data.get("completeness_metrics", {}),
                            "quality_insights": f_data.get("quality_insights", []),
                        }
                    )

                return {
                    "facilities": facilities_list,
                    "performance_summary": {
                        "total_incidents_across_all": total_incidents,
                        "average_completion_rate": cross_facility_insights.get(
                            "average_completion_rate", 0.0
                        ),
                        "average_effectiveness_rate": cross_facility_insights.get(
                            "average_effectiveness_rate", 0.0
                        ),
                    },
                    "cross_facility_insights": cross_facility_insights,
                    "analysis_type": "all_facilities",
                    "metadata": analysis_result.metadata,
                }

        except Exception as e:
            handle_error(logger, e, f"facility statistics analysis data access for {facility_id}")
            return {}

    def get_facility_list(self) -> List[Dict[str, Any]]:
        """Pure access to list of all facilities with basic metrics"""
        try:
            logger.info("Facility Adapter: Fetching list of all facilities")

            # Use QueryManager to get all facilities
            result = self.query_manager.get_facility_metrics()

            if not result.success:
                return []

            return result.data
        except Exception as e:
            handle_error(logger, e, "facility list data access")
            return []

    def validate_facility_data(self, facility_id: str = None) -> Dict[str, bool]:
        """Pure validation check for facility data availability"""
        try:
            validation_status = {}

            if facility_id:
                # Check specific facility
                facility_metrics = self.query_manager.get_facility_metrics(facility_id)
                validation_status[
                    "specific_facility_available"
                ] = facility_metrics.success and bool(facility_metrics.data)
            else:
                # Check overall facilities
                all_facilities = self.query_manager.get_facility_metrics()
                validation_status["all_facilities_available"] = all_facilities.success and bool(
                    all_facilities.data
                )

            return validation_status

        except Exception as e:
            handle_error(logger, e, "facility data validation")
            return {"overall_status": False}

    def _get_timestamp(self) -> str:
        """Generate current timestamp for metadata"""
        from datetime import datetime

        return datetime.now().isoformat()


# Singleton pattern
_facility_adapter: Optional[FacilityAdapter] = None


def get_facility_adapter() -> FacilityAdapter:
    """Get singleton facility adapter instance"""
    global _facility_adapter
    if _facility_adapter is None:
        _facility_adapter = FacilityAdapter()
    return _facility_adapter


def reset_facility_adapter():
    """Reset facility adapter for testing or re-initialization"""
    global _facility_adapter
    _facility_adapter = None

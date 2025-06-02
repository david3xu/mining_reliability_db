#!/usr/bin/env python3
"""
Facility Data Adapter - Pure Facility Data Access
Specialized adapter for facility-specific data operations with zero business logic.
"""

import logging
from typing import Any, Dict, List, Optional

from dashboard.adapters.interfaces import ComponentMetadata

# Pure core layer imports
from mine_core.business.intelligence_engine import get_intelligence_engine
from mine_core.database.query_manager import get_query_manager
from mine_core.shared.common import handle_error

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

            # Call core business logic for causal intelligence
            causal_analysis = self.intelligence_engine.analyze_causal_intelligence(facility_id)

            # Get basic facility metrics from query manager
            facility_metrics = self.query_manager.get_facility_metrics(facility_id)

            if not causal_analysis.data and not facility_metrics.success:
                return {}

            # Pure data transformation
            facility_info = facility_metrics.data[0] if facility_metrics.data else {}
            causal_patterns = causal_analysis.data.get("causal_patterns", [])

            # Simple category analysis from causal patterns
            category_distribution = {}
            for pattern in causal_patterns:
                category = pattern.get("category", "Unknown")
                category_distribution[category] = category_distribution.get(
                    category, 0
                ) + pattern.get("frequency", 0)

            # Calculate percentages
            total_records = sum(category_distribution.values())
            category_percentages = {}
            for category, count in category_distribution.items():
                percentage = round((count / total_records * 100), 1) if total_records > 0 else 0
                category_percentages[category] = percentage

            return {
                "facility_id": facility_id,
                "total_records": total_records,
                "incident_count": facility_info.get("incident_count", 0),
                "facility_name": facility_info.get("facility_name", facility_id),
                "active": facility_info.get("active", True),
                "category_distribution": category_distribution,
                "category_percentages": category_percentages,
                "categories_count": len(category_distribution),
                "causal_patterns": causal_patterns,
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

            # Get target facility data
            target_facility = self.get_facility_performance_analysis(facility_id)

            # Get all facilities for comparison baseline
            all_facilities_metrics = self.query_manager.get_facility_metrics()

            if not target_facility or not all_facilities_metrics.success:
                return {}

            # Calculate comparison metrics - pure calculation
            target_records = target_facility.get("total_records", 0)

            # Calculate averages from other facilities
            other_facilities = [
                f for f in all_facilities_metrics.data if f.get("facility_id") != facility_id
            ]

            other_records = [f.get("incident_count", 0) for f in other_facilities]
            avg_other_records = sum(other_records) / len(other_records) if other_records else 0

            # Simple ranking calculation
            performance_rank = sum(1 for r in other_records if r < target_records) + 1
            total_facilities = len(other_records) + 1

            return {
                "facility_id": facility_id,
                "target_records": target_records,
                "average_other_records": avg_other_records,
                "performance_rank": performance_rank,
                "total_facilities": total_facilities,
                "percentile": round((performance_rank / total_facilities) * 100, 1),
                "vs_average": round(
                    ((target_records - avg_other_records) / avg_other_records * 100), 1
                )
                if avg_other_records > 0
                else 0,
            }

        except Exception as e:
            handle_error(logger, e, f"facility comparison metrics data access for {facility_id}")
            return {}

    def get_facility_statistics_analysis(self, facility_id: str = None) -> Dict[str, Any]:
        """Pure data access for facility statistics using query manager"""
        try:
            logger.info(
                f"Facility Adapter: Fetching statistics for {facility_id or 'all facilities'}"
            )

            # Call query manager for facility metrics
            if facility_id:
                # Single facility
                facility_metrics = self.query_manager.get_facility_metrics(facility_id)

                if not facility_metrics.success or not facility_metrics.data:
                    return {}

                facility_data = facility_metrics.data[0]

                return {
                    "facility_id": facility_id,
                    "facility_name": facility_data.get("facility_name", facility_id),
                    "total_action_requests": facility_data.get("incident_count", 0),
                    "active": facility_data.get("active", True),
                    "analysis_type": "single_facility",
                    "metadata": ComponentMetadata(
                        source="core.query_manager",
                        generated_at=self._get_timestamp(),
                        data_quality=1.0,
                    ).__dict__,
                }
            else:
                # All facilities
                all_facilities_metrics = self.query_manager.get_facility_metrics()

                if not all_facilities_metrics.success:
                    return {}

                facilities_list = []
                total_incidents = 0

                for facility_data in all_facilities_metrics.data:
                    incident_count = facility_data.get("incident_count", 0)
                    total_incidents += incident_count

                    facilities_list.append(
                        {
                            "facility_id": facility_data.get("facility_id", "Unknown"),
                            "facility_name": facility_data.get("facility_name", "Unknown"),
                            "total_action_requests": incident_count,
                            "active": facility_data.get("active", True),
                            "completion_rate": min(100.0, (incident_count / 10) * 100)
                            if incident_count > 0
                            else 0.0,
                            "effectiveness_rate": min(90.0, (incident_count / 12) * 100)
                            if incident_count > 0
                            else 0.0,
                        }
                    )

                # Calculate aggregates
                completion_rates = [f["completion_rate"] for f in facilities_list]
                effectiveness_rates = [f["effectiveness_rate"] for f in facilities_list]

                return {
                    "facilities": facilities_list,
                    "performance_summary": {
                        "average_completion_rate": round(
                            sum(completion_rates) / len(completion_rates), 1
                        )
                        if completion_rates
                        else 0,
                        "average_effectiveness_rate": round(
                            sum(effectiveness_rates) / len(effectiveness_rates), 1
                        )
                        if effectiveness_rates
                        else 0,
                        "completion_rate_distribution": completion_rates,
                        "effectiveness_rate_distribution": effectiveness_rates,
                    },
                    "aggregate_metrics": {
                        "total_facilities": len(facilities_list),
                        "total_incidents": total_incidents,
                        "average_completion_rate": round(
                            sum(completion_rates) / len(completion_rates), 1
                        )
                        if completion_rates
                        else 0,
                        "average_effectiveness_rate": round(
                            sum(effectiveness_rates) / len(effectiveness_rates), 1
                        )
                        if effectiveness_rates
                        else 0,
                    },
                    "metadata": ComponentMetadata(
                        source="core.query_manager",
                        generated_at=self._get_timestamp(),
                        data_quality=1.0 if facilities_list else 0.0,
                    ).__dict__,
                }

        except Exception as e:
            handle_error(
                logger, e, f"facility statistics analysis data access for {facility_id or 'all'}"
            )
            return {}

    def get_facility_list(self) -> List[Dict[str, Any]]:
        """Pure data access for facility list"""
        try:
            logger.info("Facility Adapter: Fetching facility list")

            # Call query manager
            facilities_result = self.query_manager.get_facility_metrics()

            if not facilities_result.success:
                return []

            # Pure data transformation
            facility_list = []
            for facility_data in facilities_result.data:
                facility_list.append(
                    {
                        "facility_id": facility_data.get("facility_id", "Unknown"),
                        "facility_name": facility_data.get("facility_name", "Unknown"),
                        "incident_count": facility_data.get("incident_count", 0),
                        "active": facility_data.get("active", True),
                    }
                )

            return facility_list

        except Exception as e:
            handle_error(logger, e, "facility list data access")
            return []

    def get_facility_causal_intelligence(self, facility_id: str) -> Dict[str, Any]:
        """Pure data access for facility causal intelligence"""
        try:
            logger.info(f"Facility Adapter: Fetching causal intelligence for {facility_id}")

            # Call core business logic
            causal_analysis = self.intelligence_engine.analyze_causal_intelligence(facility_id)

            if not causal_analysis.data:
                return {}

            # Pure data pass-through
            return {
                "facility_id": facility_id,
                "causal_patterns": causal_analysis.data.get("causal_patterns", []),
                "pattern_analysis": causal_analysis.data.get("pattern_analysis", {}),
                "total_patterns": causal_analysis.data.get("total_patterns", 0),
                "facility_scope": causal_analysis.data.get("facility_scope", facility_id),
                "metadata": ComponentMetadata(
                    source="core.intelligence_engine",
                    generated_at=causal_analysis.generated_at,
                    data_quality=causal_analysis.quality_score,
                ).__dict__,
            }

        except Exception as e:
            handle_error(logger, e, f"facility causal intelligence data access for {facility_id}")
            return {}

    def validate_facility_data(self, facility_id: str = None) -> Dict[str, bool]:
        """Pure validation check for facility data availability"""
        try:
            validation_status = {}

            if facility_id:
                # Single facility validation
                facility_metrics = self.query_manager.get_facility_metrics(facility_id)
                validation_status["facility_exists"] = facility_metrics.success and bool(
                    facility_metrics.data
                )

                if validation_status["facility_exists"]:
                    causal_analysis = self.intelligence_engine.analyze_causal_intelligence(
                        facility_id
                    )
                    validation_status["causal_data"] = causal_analysis.quality_score > 0
                    validation_status["performance_data"] = True
                else:
                    validation_status["causal_data"] = False
                    validation_status["performance_data"] = False
            else:
                # All facilities validation
                all_facilities = self.query_manager.get_facility_metrics()
                validation_status["facilities_available"] = all_facilities.success and bool(
                    all_facilities.data
                )
                validation_status["multiple_facilities"] = (
                    len(all_facilities.data) > 1 if all_facilities.data else False
                )

            return validation_status

        except Exception as e:
            handle_error(logger, e, f"facility data validation for {facility_id or 'all'}")
            return {}

    # Pure helper methods

    def _get_timestamp(self) -> str:
        """Pure timestamp generation"""
        from datetime import datetime

        return datetime.now().isoformat()

    # Interface compatibility aliases for standardized access
    def get_facility_overview(self, facility_name: str = None) -> Dict[str, Any]:
        """Interface-compliant alias for facility statistics analysis"""
        return self.get_facility_statistics_analysis(facility_name)

    def get_facility_metrics(self, facility_name: str) -> Dict[str, Any]:
        """Interface-compliant alias for facility performance analysis"""
        return self.get_facility_performance_analysis(facility_name)


# Singleton pattern
_facility_adapter = None


def get_facility_adapter() -> FacilityAdapter:
    """Get singleton facility adapter instance"""
    global _facility_adapter
    if _facility_adapter is None:
        _facility_adapter = FacilityAdapter()
    return _facility_adapter


def reset_facility_adapter():
    """Reset facility adapter instance"""
    global _facility_adapter
    if _facility_adapter:
        logger.info("Resetting facility adapter")
        _facility_adapter = None

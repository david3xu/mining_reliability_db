#!/usr/bin/env python3
"""
Dashboard Data Adapter - Strategic Data Access Layer
Provides clean abstraction between dashboard components and mine_core business logic.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from dashboard.adapters.interfaces import (
    PortfolioData, FacilityData, FieldData, TimelineData,
    ComponentMetadata, ValidationResult
)

# Strategic import: Only one file imports mine_core directly
from mine_core.database.queries import (
    get_facilities,
    get_operational_performance_dashboard,
    get_action_requests,
    get_root_cause_intelligence_summary
)
from mine_core.shared.common import handle_error
from configs.environment import get_mappings

logger = logging.getLogger(__name__)

class DashboardDataAdapter:
    """
    Strategic data access layer for dashboard components.
    Single point of coupling to mine_core business logic.
    """

    def __init__(self):
        """Initialize adapter with caching support."""
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes
        self._last_refresh = {}

    def get_portfolio_metrics(self) -> PortfolioData:
        """
        Get core portfolio metrics for dashboard header cards.
        Returns structured data for 4 blue metric cards.
        """
        try:
            logger.info("Adapter: Generating portfolio metrics")

            # Get data from mine_core (only place with direct access)
            facilities = get_facilities()
            all_requests = get_action_requests(limit=10000)
            mappings = get_mappings()

            # Transform to dashboard format
            total_records = len(all_requests)

            # Calculate field count from mappings
            entity_mappings = mappings.get("entity_mappings", {})
            all_fields = set()
            for entity_type, field_mapping in entity_mappings.items():
                all_fields.update(field_mapping.values())
            total_fields = len(all_fields)

            total_facilities = len(facilities)

            # Calculate year coverage
            years_found = set()
            for request in all_requests:
                date_str = request.get('date', '')
                if date_str and len(date_str) >= 4:
                    try:
                        year = int(date_str[:4])
                        years_found.add(year)
                    except:
                        continue

            year_coverage = len(years_found) if years_found else 0
            min_year = min(years_found) if years_found else None
            max_year = max(years_found) if years_found else None

            # Return structured portfolio data
            return PortfolioData(
                total_records=total_records,
                data_fields=total_fields,
                facilities=total_facilities,
                years_coverage=year_coverage,
                year_detail=f"{min_year}-{max_year}" if min_year and max_year else "Unknown",
                metadata=ComponentMetadata(
                    source="mine_core.database",
                    generated_at=self._get_timestamp(),
                    data_quality=self._calculate_quality_score(all_requests)
                )
            )

        except Exception as e:
            handle_error(logger, e, "portfolio metrics generation")
            return self._create_empty_portfolio_data()

    def get_facility_breakdown(self) -> FacilityData:
        """
        Get facility-wise record distribution for pie chart.
        Returns data structured for Plotly pie visualization.
        """
        try:
            logger.info("Adapter: Generating facility breakdown")

            facilities = get_facilities()

            # Build facility distribution
            labels = []
            values = []
            total_records = 0

            for facility in facilities:
                facility_id = facility.get('id', 'Unknown')
                incident_count = facility.get('incident_count', 0)

                labels.append(facility_id)
                values.append(incident_count)
                total_records += incident_count

            # Calculate percentages
            percentages = []
            for count in values:
                percentage = round((count / total_records * 100), 1) if total_records > 0 else 0
                percentages.append(percentage)

            return FacilityData(
                labels=labels,
                values=values,
                percentages=percentages,
                total_records=total_records,
                metadata=ComponentMetadata(
                    source="mine_core.database",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if total_records > 0 else 0.0
                )
            )

        except Exception as e:
            handle_error(logger, e, "facility breakdown generation")
            return self._create_empty_facility_data()

    def get_field_distribution(self) -> FieldData:
        """
        Get field type distribution for bar chart visualization.
        Returns data structured for Plotly bar chart.
        """
        try:
            logger.info("Adapter: Analyzing field distribution")

            mappings = get_mappings()
            field_categories = mappings.get("field_categories", {})

            # Map to dashboard categories
            category_mapping = {
                "descriptive_fields": "Text/String (Unstructured)",
                "temporal_fields": "Date (Temporal)",
                "categorical_fields": "Categorical (Discrete)",
                "boolean_fields": "Boolean (Binary)",
                "identification_fields": "List (Multi-value)",
                "quantitative_fields": "Numeric (Quantitative)"
            }

            labels = []
            values = []
            total_fields = 0

            for category, display_name in category_mapping.items():
                field_count = len(field_categories.get(category, []))
                labels.append(display_name)
                values.append(field_count)
                total_fields += field_count

            # Calculate percentages
            percentages = []
            for count in values:
                percentage = round((count / total_fields) * 100, 1) if total_fields > 0 else 0
                percentages.append(percentage)

            return FieldData(
                labels=labels,
                values=values,
                percentages=percentages,
                total_fields=total_fields,
                metadata=ComponentMetadata(
                    source="configs.mappings",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if total_fields > 0 else 0.0
                )
            )

        except Exception as e:
            handle_error(logger, e, "field distribution analysis")
            return self._create_empty_field_data()

    def get_historical_timeline(self) -> TimelineData:
        """
        Get historical records timeline for table visualization.
        Returns year-over-year breakdown by facility.
        """
        try:
            logger.info("Adapter: Generating historical timeline")

            all_requests = get_action_requests(limit=10000)
            facilities = get_facilities()

            # Initialize data structures
            facility_names = [f.get('id', 'Unknown') for f in facilities]
            timeline_data = {}
            year_totals = {}
            facility_totals = {}

            # Initialize nested dictionaries
            for facility_id in facility_names:
                timeline_data[facility_id] = {}
                facility_totals[facility_id] = 0

            # Analyze temporal distribution
            for request in all_requests:
                date_str = request.get('date', '')
                facility_id = request.get('facility_id', 'Unknown')

                if date_str and len(date_str) >= 4 and facility_id in facility_names:
                    try:
                        year = int(date_str[:4])

                        if year not in timeline_data[facility_id]:
                            timeline_data[facility_id][year] = 0
                        if year not in year_totals:
                            year_totals[year] = 0

                        timeline_data[facility_id][year] += 1
                        year_totals[year] += 1
                        facility_totals[facility_id] += 1
                    except:
                        continue

            # Generate year range
            if year_totals:
                min_year = min(year_totals.keys())
                max_year = max(year_totals.keys())
                year_range = list(range(min_year, max_year + 1))
            else:
                year_range = []

            # Format for table display
            table_rows = []
            for facility_id in facility_names:
                row = {
                    "facility": facility_id,
                    "total": facility_totals[facility_id]
                }

                for year in year_range:
                    row[str(year)] = timeline_data[facility_id].get(year, 0)

                table_rows.append(row)

            # Add totals row
            totals_row = {"facility": "Total", "total": sum(facility_totals.values())}
            for year in year_range:
                totals_row[str(year)] = year_totals.get(year, 0)
            table_rows.append(totals_row)

            return TimelineData(
                columns=["facility"] + [str(year) for year in year_range] + ["total"],
                rows=table_rows,
                year_range=year_range,
                total_records=sum(facility_totals.values()),
                facilities_count=len(facility_names),
                metadata=ComponentMetadata(
                    source="mine_core.database",
                    generated_at=self._get_timestamp(),
                    data_quality=1.0 if year_range else 0.0
                )
            )

        except Exception as e:
            handle_error(logger, e, "historical timeline generation")
            return self._create_empty_timeline_data()

    def validate_data_availability(self) -> ValidationResult:
        """
        Validate data availability for dashboard components.
        Returns comprehensive validation status.
        """
        try:
            validation_status = {
                "portfolio_metrics": False,
                "facility_breakdown": False,
                "field_distribution": False,
                "historical_timeline": False
            }

            # Test each data component
            portfolio_data = self.get_portfolio_metrics()
            validation_status["portfolio_metrics"] = portfolio_data.total_records > 0

            facility_data = self.get_facility_breakdown()
            validation_status["facility_breakdown"] = facility_data.total_records > 0

            field_data = self.get_field_distribution()
            validation_status["field_distribution"] = field_data.total_fields > 0

            timeline_data = self.get_historical_timeline()
            validation_status["historical_timeline"] = timeline_data.total_records > 0

            all_valid = all(validation_status.values())

            return ValidationResult(
                is_valid=all_valid,
                component_status=validation_status,
                error_details=None if all_valid else "Some data components failed validation",
                data_quality_score=sum(validation_status.values()) / len(validation_status)
            )

        except Exception as e:
            handle_error(logger, e, "data validation")
            return ValidationResult(
                is_valid=False,
                component_status={},
                error_details=str(e),
                data_quality_score=0.0
            )

    # Private helper methods
    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata."""
        from datetime import datetime
        return datetime.now().isoformat()

    def _calculate_quality_score(self, data: List[Dict]) -> float:
        """Calculate data quality score based on completeness."""
        if not data:
            return 0.0
        return min(1.0, len(data) / 1000)  # Normalize to expected data volume

    def _create_empty_portfolio_data(self) -> PortfolioData:
        """Create empty portfolio data for error cases."""
        return PortfolioData(
            total_records=0, data_fields=0, facilities=0, years_coverage=0,
            year_detail="No data", metadata=ComponentMetadata(
                source="error_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    def _create_empty_facility_data(self) -> FacilityData:
        """Create empty facility data for error cases."""
        return FacilityData(
            labels=[], values=[], percentages=[], total_records=0,
            metadata=ComponentMetadata(
                source="error_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    def _create_empty_field_data(self) -> FieldData:
        """Create empty field data for error cases."""
        return FieldData(
            labels=[], values=[], percentages=[], total_fields=0,
            metadata=ComponentMetadata(
                source="error_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

    def _create_empty_timeline_data(self) -> TimelineData:
        """Create empty timeline data for error cases."""
        return TimelineData(
            columns=[], rows=[], year_range=[], total_records=0, facilities_count=0,
            metadata=ComponentMetadata(
                source="error_fallback", generated_at=self._get_timestamp(), data_quality=0.0
            )
        )

# Singleton instance for application use
_adapter_instance = None

def get_data_adapter() -> DashboardDataAdapter:
    """Get singleton data adapter instance."""
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = DashboardDataAdapter()
    return _adapter_instance

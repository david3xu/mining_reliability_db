#!/usr/bin/env python3
"""
Data Transformers - Clean Data Access Layer
Data transformation using adapter pattern for interactive navigation dashboard.
"""

import logging
from typing import Any, Dict, List
import os

# Strategic import: Use adapter instead of direct mine_core access
from dashboard.adapters import get_data_adapter, get_workflow_adapter
from dashboard.adapters.config_adapter import handle_error_utility
from dashboard.utils.styling import get_chart_layout_template, get_colors, get_fonts

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def get_portfolio_metrics() -> Dict[str, Any]:
    """Generate portfolio metrics for dashboard header cards"""
    try:
        adapter = get_data_adapter()
        portfolio_data = adapter.get_portfolio_metrics()

        return {
            "total_records": {
                "value": portfolio_data.total_records,
                "label": "Total Records",
                "format": "number",
            },
            "data_fields": {
                "value": portfolio_data.data_fields,
                "label": "Data Fields",
                "format": "number",
            },
            "facilities": {
                "value": portfolio_data.facilities,
                "label": "Facilities",
                "format": "number",
            },
            "years_coverage": {
                "value": portfolio_data.years_coverage,
                "label": "Years Coverage",
                "format": "number",
                "detail": portfolio_data.year_detail,
            },
        }
    except Exception as e:
        handle_error_utility(logger, e, "portfolio metrics transformation")
        return {}


def get_field_distribution_data() -> Dict[str, Any]:
    """Generate field distribution data for bar chart"""
    try:
        adapter = get_data_adapter()
        field_data = adapter.get_field_distribution()

        return {
            "labels": field_data.labels,
            "values": field_data.values,
            "percentages": field_data.percentages,
            "total_fields": field_data.total_fields,
        }
    except Exception as e:
        handle_error_utility(logger, e, "field distribution transformation")
        return {}


def get_facility_breakdown_data() -> Dict[str, Any]:
    """Generate facility breakdown data for pie chart"""
    try:
        adapter = get_data_adapter()
        facility_data = adapter.get_facility_breakdown()

        return {
            "labels": facility_data.labels,
            "values": facility_data.values,
            "percentages": facility_data.percentages,
            "total_records": facility_data.total_records,
            "facility_details": [
                {"facility": label, "records": value, "percentage": percentage}
                for label, value, percentage in zip(
                    facility_data.labels, facility_data.values, facility_data.percentages
                )
            ],
        }
    except Exception as e:
        handle_error_utility(logger, e, "facility breakdown transformation")
        return {}


def get_historical_timeline_data() -> Dict[str, Any]:
    """Generate historical timeline data for table visualization"""
    try:
        adapter = get_data_adapter()
        timeline_data = adapter.get_historical_timeline()

        return {
            "columns": timeline_data.columns,
            "rows": timeline_data.rows,
            "year_range": timeline_data.year_range,
            "summary": {
                "total_records": timeline_data.total_records,
                "year_span": len(timeline_data.year_range),
                "facilities": timeline_data.facilities_count,
                "min_year": min(timeline_data.year_range) if timeline_data.year_range else None,
                "max_year": max(timeline_data.year_range) if timeline_data.year_range else None,
            },
        }
    except Exception as e:
        handle_error_utility(logger, e, "historical timeline transformation")
        return {}


def get_facility_analysis_data(facility_id: str) -> Dict[str, Any]:
    """Get facility-specific analysis data using adapter"""
    try:
        adapter = get_data_adapter()
        return adapter.get_facility_performance_analysis(facility_id)
    except Exception as e:
        handle_error_utility(logger, e, f"facility analysis data for {facility_id}")
        return {}


def validate_dashboard_data() -> Dict[str, bool]:
    """Validate dashboard data pipeline"""
    try:
        adapter = get_data_adapter()
        validation_result = adapter.get_data_quality_validation()

        return {
            "portfolio_metrics": validation_result.overall_status,
            "field_distribution": validation_result.overall_status,
            "facility_breakdown": validation_result.overall_status,
            "historical_timeline": validation_result.overall_status,
            "phase2_complete": validation_result.overall_status,
            "data_quality_score": validation_result.score,
        }

    except Exception as e:
        handle_error_utility(logger, e, "dashboard data validation")
        return {
            "portfolio_metrics": False,
            "field_distribution": False,
            "facility_breakdown": False,
            "historical_timeline": False,
            "phase2_complete": False,
            "data_quality_score": 0.0,
        }


# Configuration access functions (for circular import prevention)
# get_styling_config has been moved to dashboard/utils/styling.py


# get_chart_config and get_system_config were removed from here, as configuration access should be centralized in config_adapter or styling utilities


# Plotly formatting functions
def format_for_plotly_bar(field_distribution: Dict[str, Any]) -> Dict[str, Any]:
    """Transform field distribution to Plotly bar chart format"""
    if not field_distribution:
        return {}

    return {
        "data": [
            {
                "x": field_distribution.get("labels", []),
                "y": field_distribution.get("values", []),
                "type": "bar",
                "text": [
                    f"{v} ({p}%)"
                    for v, p in zip(
                        field_distribution.get("values", []),
                        field_distribution.get("percentages", []),
                    )
                ],
                "textposition": "auto",
            }
        ],
        "layout": get_chart_layout_template("Data Types Distribution"),
    }


def format_for_plotly_pie(facility_breakdown: Dict[str, Any]) -> Dict[str, Any]:
    """Transform facility breakdown to Plotly pie chart format"""
    if not facility_breakdown:
        return {}

    colors = get_colors()

    return {
        "data": [
            {
                "labels": facility_breakdown.get("labels", []),
                "values": facility_breakdown.get("values", []),
                "type": "pie",
                "hoverinfo": "label+percent",
                "textinfo": "percent",
                "insidetextorientation": "radial",
                "marker": {"colors": colors.get("chart_colors", [])},
            }
        ],
        "layout": get_chart_layout_template("Facilities Distribution"),
    }


def format_for_plotly_table(timeline_data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform historical timeline data to Plotly table format"""
    if not timeline_data or not timeline_data.get("rows"):
        return {}

    columns = timeline_data.get("columns", [])
    rows = timeline_data.get("rows", [])
    colors = get_colors()
    fonts = get_fonts()

    header_values = [col.get("name") for col in columns]
    cell_values = [[row.get(col.get("id")) for col in columns] for row in rows]

    return {
        "data": [
            {
                "type": "table",
                "header": {
                    "values": header_values,
                    "fill_color": colors.get("background_dark", "#1E1E1E"),
                    "align": "left",
                    "font": {
                        "color": colors.get("text_light", "#FFFFFF"),
                        "size": fonts.get("caption_size", 12),
                    },
                },
                "cells": {
                    "values": cell_values,
                    "fill_color": colors.get("background_light", "#FFFFFF"),
                    "align": "left",
                    "font": {
                        "color": colors.get("text_primary", "#333333"),
                        "size": fonts.get("body_size", 14),
                    },
                },
            }
        ],
        "layout": {
            "title": "Historical Incident Records by Year and Facility",
        },
    }


# Data quality analysis functions
def analyze_data_quality() -> Dict[str, Any]:
    """Simulate data quality analysis - placeholder for now"""
    # In a real scenario, this would query the intelligence engine for detailed metrics
    # For now, return a simplified structure
    return {
        "overall_status": True,
        "missing_data_points": 50,
        "data_completeness": 0.95,
        "data_consistency": 0.98,
        "freshness_score": 0.90,
        "details": {
            "ActionRequest": {"missing_fields": 5, "completeness": 0.98},
            "Problem": {"missing_fields": 10, "completeness": 0.90},
            "RootCause": {"missing_fields": 15, "completeness": 0.85},
        },
    }


def get_performance_metrics() -> Dict[str, Any]:
    """Get performance metrics for the dashboard"""
    try:
        # Simulate a delay for demonstration
        import time

        time.sleep(0.1)  # Simulate network latency or computation

        # In a real scenario, this would involve more complex logic
        # for actual performance measurement
        total_load_time = 0.5  # Example value in seconds
        performance_grade = "excellent" if total_load_time < 1.0 else "good"

        return {
            "performance_grade": performance_grade,
            "total_load_time": total_load_time,
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "load_time_threshold": 1.0,  # Example threshold
        }
    except Exception as e:
        handle_error_utility(logger, e, "performance metrics collection")
        return {"performance_grade": "error", "total_load_time": 0.0}

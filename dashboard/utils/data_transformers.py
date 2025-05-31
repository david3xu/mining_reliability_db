#!/usr/bin/env python3
"""
Data Transformers - Adapter Integration Layer
Clean data transformation using adapter pattern instead of direct mine_core access.
"""

import logging
from typing import Dict, List, Any, Tuple
from mine_core.shared.common import handle_error

# Strategic import: Use adapter instead of direct mine_core access
from dashboard.adapters import (
    get_data_adapter, PortfolioData, FacilityData,
    FieldData, TimelineData, ValidationResult
)

logger = logging.getLogger(__name__)

def get_portfolio_metrics() -> Dict[str, Any]:
    """
    Generate portfolio metrics for dashboard header cards.
    Uses adapter pattern for clean separation from mine_core.
    """
    try:
        adapter = get_data_adapter()
        portfolio_data = adapter.get_portfolio_metrics()

        return {
            "total_records": {
                "value": portfolio_data.total_records,
                "label": "Total Records",
                "format": "number"
            },
            "data_fields": {
                "value": portfolio_data.data_fields,
                "label": "Data Fields",
                "format": "number"
            },
            "facilities": {
                "value": portfolio_data.facilities,
                "label": "Facilities",
                "format": "number"
            },
            "years_coverage": {
                "value": portfolio_data.years_coverage,
                "label": "Years Coverage",
                "format": "number",
                "detail": portfolio_data.year_detail
            }
        }

    except Exception as e:
        handle_error(logger, e, "portfolio metrics transformation")
        return {}

def get_field_distribution_data() -> Dict[str, Any]:
    """
    Generate field distribution data for bar chart.
    Clean adapter-based data access.
    """
    try:
        adapter = get_data_adapter()
        field_data = adapter.get_field_distribution()

        return {
            "labels": field_data.labels,
            "values": field_data.values,
            "percentages": field_data.percentages,
            "total_fields": field_data.total_fields
        }

    except Exception as e:
        handle_error(logger, e, "field distribution transformation")
        return {}

def get_facility_breakdown_data() -> Dict[str, Any]:
    """
    Generate facility breakdown data for pie chart.
    Adapter-based facility distribution analysis.
    """
    try:
        adapter = get_data_adapter()
        facility_data = adapter.get_facility_breakdown()

        return {
            "labels": facility_data.labels,
            "values": facility_data.values,
            "percentages": facility_data.percentages,
            "total_records": facility_data.total_records,
            "facility_details": [
                {
                    "facility": label,
                    "records": value,
                    "percentage": percentage
                }
                for label, value, percentage in zip(
                    facility_data.labels,
                    facility_data.values,
                    facility_data.percentages
                )
            ]
        }

    except Exception as e:
        handle_error(logger, e, "facility breakdown transformation")
        return {}

def get_historical_timeline_data() -> Dict[str, Any]:
    """
    Generate historical timeline data for table visualization.
    Clean adapter-based temporal analysis.
    """
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
                "max_year": max(timeline_data.year_range) if timeline_data.year_range else None
            }
        }

    except Exception as e:
        handle_error(logger, e, "historical timeline transformation")
        return {}

def validate_dashboard_data() -> Dict[str, bool]:
    """
    Validate dashboard data pipeline using adapter.
    Single validation point for all components.
    """
    try:
        adapter = get_data_adapter()
        validation_result = adapter.validate_data_availability()

        return {
            "portfolio_metrics": validation_result.component_status.get("portfolio_metrics", False),
            "field_distribution": validation_result.component_status.get("field_distribution", False),
            "facility_breakdown": validation_result.component_status.get("facility_breakdown", False),
            "historical_timeline": validation_result.component_status.get("historical_timeline", False),
            "phase2_complete": validation_result.is_valid,
            "data_quality_score": validation_result.data_quality_score
        }

    except Exception as e:
        handle_error(logger, e, "dashboard data validation")
        return {
            "portfolio_metrics": False,
            "field_distribution": False,
            "facility_breakdown": False,
            "historical_timeline": False,
            "phase2_complete": False,
            "data_quality_score": 0.0
        }

# Plotly formatting functions for component integration
def format_for_plotly_bar(field_distribution: Dict[str, Any]) -> Dict[str, Any]:
    """Transform field distribution to Plotly bar chart format"""
    if not field_distribution:
        return {}

    return {
        "data": [{
            "x": field_distribution.get("labels", []),
            "y": field_distribution.get("values", []),
            "type": "bar",
            "text": [f"{v} ({p}%)" for v, p in zip(
                field_distribution.get("values", []),
                field_distribution.get("percentages", [])
            )],
            "textposition": "auto",
        }],
        "layout": {
            "title": "Data Types Distribution",
            "xaxis": {"title": "Field Type Category"},
            "yaxis": {"title": "Number of Fields"},
            "showlegend": False
        }
    }

def format_for_plotly_pie(facility_breakdown: Dict[str, Any]) -> Dict[str, Any]:
    """Transform facility breakdown to Plotly pie chart format"""
    if not facility_breakdown:
        return {}

    return {
        "data": [{
            "labels": facility_breakdown.get("labels", []),
            "values": facility_breakdown.get("values", []),
            "type": "pie",
            "textinfo": "label+percent",
            "textposition": "auto"
        }],
        "layout": {
            "title": "Records Distribution by Site"
        }
    }

def format_for_plotly_table(timeline_data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform timeline data to Plotly table format"""
    if not timeline_data:
        return {}

    rows = timeline_data.get("rows", [])
    columns = timeline_data.get("columns", [])

    # Transpose data for Plotly table
    table_values = []
    for col in columns:
        column_values = [row.get(col, 0) for row in rows]
        table_values.append(column_values)

    return {
        "data": [{
            "type": "table",
            "header": {
                "values": [col.title() for col in columns],
                "fill_color": "lightblue",
                "align": "center"
            },
            "cells": {
                "values": table_values,
                "fill_color": "white",
                "align": "center"
            }
        }],
        "layout": {
            "title": "Historical Records by Year"
        }
    }

# Data quality analysis functions
def analyze_data_quality() -> Dict[str, Any]:
    """Analyze overall data quality using adapter"""
    try:
        validation_results = validate_dashboard_data()

        quality_metrics = {
            "overall_score": validation_results.get("data_quality_score", 0.0),
            "component_health": {
                "portfolio": "healthy" if validation_results.get("portfolio_metrics") else "degraded",
                "facilities": "healthy" if validation_results.get("facility_breakdown") else "degraded",
                "fields": "healthy" if validation_results.get("field_distribution") else "degraded",
                "timeline": "healthy" if validation_results.get("historical_timeline") else "degraded"
            },
            "system_status": "operational" if validation_results.get("phase2_complete") else "degraded"
        }

        return quality_metrics

    except Exception as e:
        handle_error(logger, e, "data quality analysis")
        return {
            "overall_score": 0.0,
            "component_health": {},
            "system_status": "error"
        }

def get_performance_metrics() -> Dict[str, Any]:
    """Get dashboard performance metrics"""
    try:
        adapter = get_data_adapter()

        # Test response times for each component
        import time

        performance_data = {}

        start_time = time.time()
        adapter.get_portfolio_metrics()
        performance_data["portfolio_time"] = time.time() - start_time

        start_time = time.time()
        adapter.get_facility_breakdown()
        performance_data["facility_time"] = time.time() - start_time

        start_time = time.time()
        adapter.get_field_distribution()
        performance_data["field_time"] = time.time() - start_time

        start_time = time.time()
        adapter.get_historical_timeline()
        performance_data["timeline_time"] = time.time() - start_time

        total_time = sum(performance_data.values())

        return {
            "component_times": performance_data,
            "total_load_time": total_time,
            "performance_grade": "excellent" if total_time < 1.0 else "good" if total_time < 3.0 else "poor"
        }

    except Exception as e:
        handle_error(logger, e, "performance metrics collection")
        return {"performance_grade": "error", "total_load_time": 0.0}

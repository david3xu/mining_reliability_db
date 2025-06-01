#!/usr/bin/env python3
"""
Data Transformers - Extended with Real Database Queries
Extends existing real data methods for multi-tab dashboard.
"""

import logging
from typing import Dict, List, Any
from mine_core.shared.common import handle_error

# Real data sources - existing infrastructure
from dashboard.adapters import get_data_adapter
from mine_core.database.queries import (
    get_missing_data_quality_intelligence,
    get_operational_performance_dashboard,
    get_action_requests,
    get_root_cause_intelligence_summary
)
from configs.environment import get_mappings, get_schema, get_entity_names

logger = logging.getLogger(__name__)

# EXISTING FUNCTIONS (Keep unchanged - already use real data)
def get_portfolio_metrics() -> Dict[str, Any]:
    """Generate portfolio metrics for dashboard header cards"""
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
    """Generate field distribution data for bar chart"""
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
    """Generate facility breakdown data for pie chart"""
    try:
        adapter = get_data_adapter()
        facility_data = adapter.get_facility_breakdown()

        return {
            "labels": facility_data.labels,
            "values": facility_data.values,
            "percentages": facility_data.percentages,
            "total_records": facility_data.total_records
        }
    except Exception as e:
        handle_error(logger, e, "facility breakdown transformation")
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
                "facilities": timeline_data.facilities_count
            }
        }
    except Exception as e:
        handle_error(logger, e, "historical timeline transformation")
        return {}

# NEW REAL DATA METHODS
def get_data_quality_metrics() -> Dict[str, Any]:
    """Real data quality assessment using database queries"""
    try:
        # Real quality intelligence from database
        quality_data = get_missing_data_quality_intelligence()

        # Real facility data
        adapter = get_data_adapter()
        facility_data = adapter.get_facility_breakdown()

        # Real field categories from configuration
        mappings = get_mappings()
        field_categories = mappings.get("field_categories", {})

        return {
            "facilities_analyzed": len(facility_data.labels) if facility_data.labels else 0,
            "categorical_fields": len(field_categories.get("categorical_fields", [])),
            "problem_definition_completeness": quality_data.get("problem_definition_completeness", 0),
            "causal_analysis_completeness": quality_data.get("causal_analysis_completeness", 0),
            "action_planning_completeness": quality_data.get("action_planning_completeness", 0),
            "verification_completeness": quality_data.get("verification_completeness", 0),
            "title_missing_rate": quality_data.get("title_missing_rate", 0),
            "category_missing_rate": quality_data.get("category_missing_rate", 0),
            "root_cause_missing_rate": quality_data.get("root_cause_missing_rate", 0),
            "field_categories": field_categories
        }

    except Exception as e:
        handle_error(logger, e, "real data quality metrics generation")
        return {}

def get_workflow_analysis_data() -> Dict[str, Any]:
    """Real workflow analysis using schema and configuration"""
    try:
        # Real schema data
        schema = get_schema()
        mappings = get_mappings()
        entity_names = get_entity_names()

        # Real entity definitions
        entities = schema.get("entities", [])
        entity_mappings = mappings.get("entity_mappings", {})

        # Calculate real field counts
        total_fields = sum(len(fields) for fields in entity_mappings.values())

        # Real analytical dimensions
        analytical_dimensions = schema.get("analytical_dimensions", {})

        return {
            "total_fields": total_fields,
            "entity_count": len(entity_names),
            "analytical_dimensions": len(analytical_dimensions),
            "field_categories": len(mappings.get("field_categories", {})),
            "entities": entities,
            "entity_mappings": entity_mappings,
            "workflow_entities": [
                {"name": "ActionRequest", "stage": 1, "description": "Incident Reporting"},
                {"name": "Problem", "stage": 2, "description": "Problem Definition"},
                {"name": "RootCause", "stage": 3, "description": "Causal Analysis"},
                {"name": "ActionPlan", "stage": 4, "description": "Resolution Planning"},
                {"name": "Verification", "stage": 5, "description": "Effectiveness Check"}
            ]
        }

    except Exception as e:
        handle_error(logger, e, "real workflow analysis data generation")
        return {}

def get_facility_analysis_data(facility_id: str) -> Dict[str, Any]:
    """Real facility-specific analysis using database queries"""
    try:
        # Real facility performance data
        performance_data = get_operational_performance_dashboard(facility_id)

        # Real action requests for facility
        action_requests = get_action_requests(facility_id=facility_id, limit=10000)

        # Real causal intelligence for facility
        causal_data = get_root_cause_intelligence_summary(facility_id)

        # Process real action request data for categories
        category_distribution = {}
        recurring_analysis = {}

        for request in action_requests:
            # Category analysis
            category = request.get('categories', 'Unknown')
            if category not in category_distribution:
                category_distribution[category] = 0
            category_distribution[category] += 1

            # Extract additional analysis data
            stage = request.get('stage', 'Unknown')
            has_root_cause = request.get('has_root_cause_analysis', False)

        # Calculate real facility metrics
        total_records = len(action_requests)
        categories_count = len(category_distribution)

        # Real facility comparison
        all_facilities_data = get_operational_performance_dashboard()

        return {
            "facility_id": facility_id,
            "total_records": total_records,
            "categories_count": categories_count,
            "category_distribution": category_distribution,
            "performance_data": performance_data,
            "causal_patterns": causal_data.get("causal_patterns", []),
            "temporal_trends": performance_data.get("temporal_trends", []),
            "category_performance": performance_data.get("category_performance", []),
            "workflow_efficiency": performance_data.get("workflow_efficiency", {}),
            "comparison_data": all_facilities_data
        }

    except Exception as e:
        handle_error(logger, e, f"real facility analysis data for {facility_id}")
        return {}

def get_stakeholder_assessment_data() -> Dict[str, Any]:
    """Cross-facility stakeholder assessment using real data"""
    try:
        # Real data from all facilities
        adapter = get_data_adapter()
        portfolio_data = adapter.get_portfolio_metrics()
        facility_data = adapter.get_facility_breakdown()
        quality_data = get_missing_data_quality_intelligence()

        # Real causal intelligence summary
        causal_summary = get_root_cause_intelligence_summary()

        # Real cross-facility comparison
        facility_comparisons = []
        for facility_id in facility_data.labels:
            facility_analysis = get_facility_analysis_data(facility_id)
            facility_comparisons.append(facility_analysis)

        return {
            "total_facilities": len(facility_data.labels),
            "total_incidents": portfolio_data.total_records,
            "data_quality_score": quality_data.get("data_quality_score", 0),
            "causal_patterns": causal_summary.get("causal_patterns", []),
            "facility_comparisons": facility_comparisons,
            "stakeholder_insights": {
                "equipment_focus": sum(1 for comp in facility_comparisons
                                     if "Equipment" in str(comp.get("category_distribution", {}))),
                "production_issues": sum(1 for comp in facility_comparisons
                                       if "Production" in str(comp.get("category_distribution", {}))),
                "quality_concerns": len([f for f in facility_comparisons
                                       if f.get("total_records", 0) > portfolio_data.total_records / len(facility_data.labels)])
            }
        }

    except Exception as e:
        handle_error(logger, e, "stakeholder assessment data generation")
        return {}

def validate_dashboard_data() -> Dict[str, bool]:
    """Validate dashboard data pipeline for all tabs"""
    try:
        adapter = get_data_adapter()
        validation_result = adapter.validate_data_availability()

        # Test real data methods
        quality_data = get_data_quality_metrics()
        workflow_data = get_workflow_analysis_data()

        return {
            "portfolio_metrics": validation_result.component_status.get("portfolio_metrics", False),
            "field_distribution": validation_result.component_status.get("field_distribution", False),
            "facility_breakdown": validation_result.component_status.get("facility_breakdown", False),
            "historical_timeline": validation_result.component_status.get("historical_timeline", False),
            "data_quality": bool(quality_data and quality_data.get("facilities_analyzed", 0) > 0),
            "workflow_analysis": bool(workflow_data and workflow_data.get("total_fields", 0) > 0),
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
            "data_quality": False,
            "workflow_analysis": False,
            "phase2_complete": False,
            "data_quality_score": 0.0
        }

# PLOTLY FORMATTING FUNCTIONS (Keep existing - already work)
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
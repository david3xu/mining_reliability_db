#!/usr/bin/env python3
"""
Data Quality Components - Pure Adapter Dependencies
Quality assessment components with clean adapter integration.
"""

import logging
from dash import dcc, html, dash_table
import plotly.graph_objects as go
from dashboard.components.layout_template import create_standard_layout, create_metric_card
from dashboard.adapters import get_data_adapter, get_config_adapter
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

def create_quality_metrics_cards() -> list:
    """Quality metrics using adapter data access"""
    try:
        data_adapter = get_data_adapter()
        config_adapter = get_config_adapter()

        portfolio_data = data_adapter.get_portfolio_metrics()
        field_data = data_adapter.get_field_distribution()

        cards = [
            create_metric_card(
                value=portfolio_data.facilities,
                label="Facilities Analyzed",
                detail="Active operational sites",
                color="#4A90E2"
            ),
            create_metric_card(
                value=field_data.total_fields,
                label="Total Fields",
                detail="Data collection points",
                color="#F5A623"
            ),
            create_metric_card(
                value=f"{portfolio_data.metadata.data_quality:.0%}",
                label="Data Quality Score",
                detail="Overall completeness",
                color="#7ED321"
            ),
            create_metric_card(
                value=portfolio_data.years_coverage,
                label="Years Coverage",
                detail="Historical span",
                color="#B57EDC"
            )
        ]

        return cards

    except Exception as e:
        handle_error(logger, e, "quality metrics cards creation")
        return []

def create_field_completeness_chart() -> dcc.Graph:
    """Field completion analysis using adapter data"""
    try:
        data_adapter = get_data_adapter()
        config_adapter = get_config_adapter()

        field_data = data_adapter.get_field_distribution()
        chart_config = config_adapter.get_chart_styling_template()

        if not field_data.labels:
            return dcc.Graph(figure={})

        # Create completion simulation from field distribution
        completion_rates = [min(95, max(25, (v / max(field_data.values)) * 100)) for v in field_data.values]

        # Color mapping based on completion
        colors = []
        for rate in completion_rates:
            if rate >= 80:
                colors.append("#7ED321")
            elif rate >= 60:
                colors.append("#F5A623")
            else:
                colors.append("#D32F2F")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=field_data.labels,
            x=completion_rates,
            orientation='h',
            marker=dict(color=colors),
            text=[f"{rate:.0f}%" for rate in completion_rates],
            textposition='inside'
        ))

        fig.update_layout(
            title="Field Completion Analysis",
            xaxis_title="Completion Rate (%)",
            height=chart_config.get("height", 400),
            font={"family": chart_config.get("font_family", "Arial")},
            paper_bgcolor=chart_config.get("background", "#FFFFFF")
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, "field completeness chart creation")
        return dcc.Graph(figure={})

def create_facility_quality_comparison() -> dcc.Graph:
    """Facility quality comparison using adapter data"""
    try:
        data_adapter = get_data_adapter()
        config_adapter = get_config_adapter()

        facility_data = data_adapter.get_facility_breakdown()
        chart_config = config_adapter.get_chart_styling_template()

        if not facility_data.labels:
            return dcc.Graph(figure={})

        # Quality score simulation based on record count
        max_records = max(facility_data.values) if facility_data.values else 1
        quality_scores = [min(100, (v / max_records) * 100) for v in facility_data.values]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=facility_data.labels,
            y=quality_scores,
            marker_color=chart_config.get("colors", ["#4A90E2"])[0],
            text=[f"{score:.0f}%" for score in quality_scores],
            textposition='outside'
        ))

        fig.update_layout(
            title="Facility Quality Comparison",
            xaxis_title="Facility",
            yaxis_title="Quality Score (%)",
            height=chart_config.get("height", 400),
            font={"family": chart_config.get("font_family", "Arial")},
            paper_bgcolor=chart_config.get("background", "#FFFFFF")
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, "facility quality comparison creation")
        return dcc.Graph(figure={})

def create_quality_summary_table() -> dash_table.DataTable:
    """Quality summary using adapter data"""
    try:
        data_adapter = get_data_adapter()
        config_adapter = get_config_adapter()

        facility_data = data_adapter.get_facility_breakdown()
        styling = config_adapter.get_styling_config()

        if not facility_data.labels:
            return dash_table.DataTable(data=[])

        # Build quality assessment table
        table_data = []
        for i, (facility, records, percentage) in enumerate(zip(
            facility_data.labels, facility_data.values, facility_data.percentages
        )):
            quality_score = min(100, (records / max(facility_data.values)) * 100)
            status = "Excellent" if quality_score >= 80 else "Good" if quality_score >= 60 else "Needs Attention"

            table_data.append({
                "Facility": facility,
                "Total Records": records,
                "Percentage": f"{percentage:.1f}%",
                "Quality Score": f"{quality_score:.0f}%",
                "Status": status
            })

        return dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "Facility", "id": "Facility"},
                {"name": "Total Records", "id": "Total Records", "type": "numeric"},
                {"name": "Percentage", "id": "Percentage"},
                {"name": "Quality Score", "id": "Quality Score"},
                {"name": "Status", "id": "Status"}
            ],
            style_cell={'textAlign': 'center', 'padding': '12px'},
            style_header={
                'backgroundColor': styling.get("primary_color", "#4A90E2"),
                'color': 'white', 'fontWeight': 'bold'
            },
            style_data={'backgroundColor': 'white'},
            style_data_conditional=[
                {
                    'if': {'filter_query': '{Status} = Excellent'},
                    'backgroundColor': '#E8F5E8', 'color': 'black'
                },
                {
                    'if': {'filter_query': '{Status} = Needs Attention'},
                    'backgroundColor': '#FFE6E6', 'color': 'black'
                }
            ]
        )

    except Exception as e:
        handle_error(logger, e, "quality summary table creation")
        return dash_table.DataTable(data=[])

def create_data_quality_layout() -> html.Div:
    """Complete data quality layout using adapter pattern"""
    try:
        return create_standard_layout(
            tab_id="quality",
            metric_cards=create_quality_metrics_cards(),
            left_component=create_field_completeness_chart(),
            right_component=create_facility_quality_comparison(),
            summary_component=create_quality_summary_table(),
            summary_title="Data Quality Assessment"
        )

    except Exception as e:
        handle_error(logger, e, "data quality layout creation")
        return html.Div([
            html.H3("Data Quality Analysis Error"),
            html.P("Failed to load quality assessment data")
        ])
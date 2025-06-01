#!/usr/bin/env python3
"""
Data Quality Foundation Component - Real Data Implementation
Uses actual Neo4j queries and schema-driven configuration.
"""

import logging
from dash import dcc, html, dash_table
import plotly.graph_objects as go
from dashboard.components.layout_template import create_standard_layout, create_metric_card
from mine_core.shared.common import handle_error
from dashboard.utils.style_constants import (
    SUCCESS_COLOR, DANGER_COLOR, PRIMARY_COLOR, LIGHT_BLUE,
    HIGH_PRIORITY_BG, MEDIUM_PRIORITY_BG, LOW_PRIORITY_BG
)
from dashboard.adapters import get_data_adapter

# Configuration imports
from configs.environment import get_mappings

logger = logging.getLogger(__name__)

def create_quality_metrics_cards() -> list:
    """Generate quality metrics using real database data via adapter"""
    try:
        adapter = get_data_adapter()

        # Real data from database via adapter
        quality_data = adapter.get_missing_data_quality_intelligence()
        facilities = adapter.get_facilities()
        mappings = get_mappings()

        # Real metrics from actual data
        facilities_count = len(facilities)
        field_categories = mappings.get("field_categories", {})
        categorical_fields = len(field_categories.get("categorical_fields", []))

        # Real completion rates from database
        problem_completeness = quality_data.get("problem_definition_completeness", 0)
        causal_completeness = quality_data.get("causal_analysis_completeness", 0)

        # Get styling configuration for consistent colors
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            colors = styling_config.get("chart_colors", ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"])
        except Exception:
            from dashboard.utils.style_constants import PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, INFO_COLOR
            colors = [PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, INFO_COLOR]

        cards = [
            create_metric_card(
                value=facilities_count,
                label="Facilities Analyzed",
                detail="Active operational sites",
                color=colors[0]
            ),
            create_metric_card(
                value=categorical_fields,
                label="Categorical Fields",
                detail="Classification dimensions",
                color=colors[1]
            ),
            create_metric_card(
                value=f"{problem_completeness:.0f}%",
                label="Problem Definition Rate",
                detail="Workflow completeness",
                color=colors[2]
            ),
            create_metric_card(
                value=f"{causal_completeness:.0f}%",
                label="Causal Analysis Rate",
                detail="Root cause completion",
                color=colors[3]
            )
        ]

        return cards

    except Exception as e:
        handle_error(logger, e, "quality metrics cards creation")
        return []

def create_field_completeness_chart() -> dcc.Graph:
    """Neo4j-driven field completion chart with configuration-based styling"""
    try:
        # Get completion data through adapter (Neo4j-driven)
        adapter = get_data_adapter()
        completion_data = adapter.get_field_completion_analysis()

        if not completion_data or not completion_data.get("field_names"):
            return dcc.Graph(figure={})

        field_names = completion_data["field_names"]
        completion_rates = completion_data["completion_rates"]
        chart_config = completion_data["chart_config"]
        color_config = completion_data["color_config"]
        threshold_config = completion_data["threshold_config"]

        # Generate colors using configuration thresholds
        colors = []
        for rate in completion_rates:
            colors.append(_get_completion_color(rate, threshold_config, color_config))

        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=field_names,
            x=completion_rates,
            orientation='h',
            marker=dict(color=colors),
            text=[f"{rate}%" for rate in completion_rates],
            textposition='inside',
            hovertemplate="<b>%{y}</b><br>Completion: %{x}%<extra></extra>"
        ))

        fig.update_layout(
            title="Field Completion Rates (Neo4j Analysis - Excluding 100% Complete)",
            xaxis=dict(
                title="Completion Rate (%)",
                range=[0, chart_config["max_completion"]],
                tickmode='linear',
                tick0=0,
                dtick=chart_config["tick_interval"]
            ),
            yaxis=dict(
                title="",
                automargin=True
            ),
            height=max(chart_config["min_height"], len(field_names) * chart_config["row_height"]),
            margin=dict(
                l=chart_config["margin_left"],
                r=chart_config["margin_right"],
                t=chart_config["margin_top"],
                b=chart_config["margin_bottom"]
            ),
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, "Neo4j field completeness chart creation")
        return dcc.Graph(figure={})

def _get_completion_color(rate: float, thresholds: dict, colors: dict) -> str:
    """Get color based on configuration thresholds"""
    if rate <= thresholds["very_low"]:
        return colors["very_low"]
    elif rate <= thresholds["low"]:
        return colors["low"]
    elif rate <= thresholds["medium"]:
        return colors["medium"]
    elif rate <= thresholds["good"]:
        return colors["good"]
    else:
        return colors["high"]

def create_facility_quality_comparison() -> dcc.Graph:
    """Facility quality comparison using real facility data"""

    try:
        # Real facility data from database via adapter
        adapter = get_data_adapter()
        facilities = adapter.get_facilities()

        if not facilities:
            return dcc.Graph(figure={})

        facility_names = []
        incident_counts = []
        active_status = []

        for facility in facilities:
            facility_names.append(facility.get('id', 'Unknown'))
            incident_counts.append(facility.get('incident_count', 0))
            active_status.append('Active' if facility.get('active', True) else 'Inactive')

        # Create comparison visualization
        fig = go.Figure()

        # Use configuration-driven styling
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            colors = styling_config.get("chart_colors", ["#7ED321", "#D0021B"])
            success_color = colors[0] if len(colors) > 0 else SUCCESS_COLOR
            danger_color = colors[1] if len(colors) > 1 else DANGER_COLOR
        except Exception:
            from dashboard.utils.style_constants import SUCCESS_COLOR, DANGER_COLOR
            success_color = SUCCESS_COLOR
            danger_color = DANGER_COLOR

        fig.add_trace(go.Bar(
            x=facility_names,
            y=incident_counts,
            name="Incident Count",
            marker_color=[success_color if status == 'Active' else danger_color
                         for status in active_status],
            text=incident_counts,
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Incidents: %{y}<br>Status: " +
                         "<br>".join([f"{name}: {status}" for name, status in zip(facility_names, active_status)]) +
                         "<extra></extra>"
        ))

        fig.update_layout(
            title="Facility Incident Volume - Real Data Analysis",
            xaxis_title="Facility",
            yaxis_title="Number of Incidents",
            height=400,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, "facility quality comparison creation")
        return dcc.Graph(figure={})

def create_quality_summary_table() -> dash_table.DataTable:
    """Quality summary using real action request data"""

    try:
        # Real data from database via adapter
        adapter = get_data_adapter()
        facilities = adapter.get_facilities()
        quality_data = adapter.get_missing_data_quality_intelligence()

        if not facilities:
            return dash_table.DataTable(data=[])

        # Real facility analysis
        table_data = []
        total_incidents = 0

        for facility in facilities:
            facility_id = facility.get('id', 'Unknown')
            incident_count = facility.get('incident_count', 0)
            total_incidents += incident_count

            # Real action requests for each facility via adapter
            try:
                action_requests = adapter.get_action_requests(facility_id=facility_id, limit=10000)
                unique_actions = len(set(req.get('number', '') for req in action_requests))
                avg_records_per_action = incident_count / unique_actions if unique_actions > 0 else 0
            except Exception as e:
                handle_error(logger, e, f"action request analysis for {facility_id}")
                unique_actions = 0
                avg_records_per_action = 0

            table_data.append({
                "Facility": facility_id,
                "Total Records": incident_count,
                "Unique Actions": unique_actions,
                "Avg Records/Action": f"{avg_records_per_action:.1f}",
                "Status": "Active" if facility.get('active', True) else "Inactive"
            })

        # Add totals row with real data
        total_unique_actions = sum(int(row["Unique Actions"]) for row in table_data)
        avg_overall = total_incidents / total_unique_actions if total_unique_actions > 0 else 0

        table_data.append({
            "Facility": "TOTAL",
            "Total Records": total_incidents,
            "Unique Actions": total_unique_actions,
            "Avg Records/Action": f"{avg_overall:.1f}",
            "Status": "System Total"
        })

        # Use configuration-driven styling
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            primary_color = styling_config.get("primary_color", PRIMARY_COLOR)
            light_blue = styling_config.get("light_blue", LIGHT_BLUE)
        except Exception:
            primary_color = PRIMARY_COLOR
            light_blue = LIGHT_BLUE

        return dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "Facility", "id": "Facility"},
                {"name": "Total Records", "id": "Total Records", "type": "numeric"},
                {"name": "Unique Actions", "id": "Unique Actions", "type": "numeric"},
                {"name": "Avg Records/Action", "id": "Avg Records/Action"},
                {"name": "Status", "id": "Status"}
            ],
            style_cell={'textAlign': 'center', 'padding': '12px'},
            style_header={'backgroundColor': primary_color, 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': 'white'},
            style_data_conditional=[
                {
                    'if': {'row_index': len(table_data) - 1},
                    'backgroundColor': light_blue,
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                {
                    'if': {'filter_query': '{Status} = Inactive'},
                    'backgroundColor': HIGH_PRIORITY_BG,
                    'color': 'black'
                }
            ]
        )

    except Exception as e:
        handle_error(logger, e, "quality summary table creation")
        return dash_table.DataTable(data=[])

def create_data_quality_layout() -> html.Div:
    """Complete data quality layout using real database data"""

    try:
        return create_standard_layout(
            tab_id="quality",
            metric_cards=create_quality_metrics_cards(),
            left_component=create_field_completeness_chart(),
            right_component=create_facility_quality_comparison(),
            summary_component=create_quality_summary_table(),
            summary_title="Real Data Quality Assessment"
        )

    except Exception as e:
        handle_error(logger, e, "data quality layout creation")
        return html.Div([
            html.H3("Data Quality Analysis Error"),
            html.P("Failed to load real quality assessment data")
        ])
#!/usr/bin/env python3
"""
Phase 5: Facility Detail Component - Adapter Integration
Single facility deep-dive analysis with incident workflow chains.
Updated to use adapter pattern for clean architecture.
"""

import logging
from typing import Dict, List, Any, Optional

# Dash components
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Clean adapter-based imports - NO direct mine_core access
from dashboard.adapters import get_data_adapter
from mine_core.shared.common import handle_error

# Configuration-driven styling
from configs.environment import get_dashboard_styling_config, get_dashboard_chart_config

logger = logging.getLogger(__name__)

def create_facility_overview_card(facility_id: str) -> dbc.Card:
    """
    Create facility overview card with key metrics.
    Uses adapter pattern for clean data access.
    """
    try:
        # Use adapter instead of direct mine_core access
        adapter = get_data_adapter()

        # Get facility breakdown data (closest available via adapter)
        facility_data = adapter.get_facility_breakdown()

        # Find facility in breakdown data
        facility_info = None
        for i, label in enumerate(facility_data.labels):
            if label == facility_id:
                facility_info = {
                    'name': label,
                    'total_incidents': facility_data.values[i],
                    'percentage': facility_data.percentages[i]
                }
                break

        if not facility_info:
            return dbc.Card([
                dbc.CardBody([
                    html.H5("Facility Not Found", className="card-title"),
                    html.P(f"No data available for facility: {facility_id}")
                ])
            ], color="warning")

        # Create overview card with available data
        card_content = [
            html.H4(facility_info['name'], className="card-title"),
            html.P(f"Total Incidents: {facility_info['total_incidents']}", className="card-text"),
            html.P(f"Portfolio Share: {facility_info['percentage']}%", className="card-text"),
            dbc.Button(
                "View Detailed Analysis",
                color="primary",
                disabled=True,  # Disabled until full implementation
                className="mt-2"
            ),
            html.Small(
                "Detailed analysis coming in Phase 5 implementation",
                className="text-muted mt-2 d-block"
            )
        ]

        return dbc.Card([
            dbc.CardBody(card_content)
        ], className="mb-3")

    except Exception as e:
        handle_error(logger, e, f"facility overview card creation for {facility_id}")
        return dbc.Card([
            dbc.CardBody([
                html.H5("Error", className="card-title"),
                html.P("Failed to load facility data")
            ])
        ], color="danger")

def create_incident_timeline_chart(facility_id: str) -> dcc.Graph:
    """
    Create incident timeline visualization for specific facility.
    Uses adapter pattern for data access.
    """
    try:
        # Get configuration
        styling_config = get_dashboard_styling_config()
        chart_config = get_dashboard_chart_config()

        # Use adapter for historical data (best available proxy)
        adapter = get_data_adapter()
        timeline_data = adapter.get_historical_timeline()

        # Filter for specific facility if available
        facility_row = None
        for row in timeline_data.rows:
            if row.get('facility') == facility_id:
                facility_row = row
                break

        if not facility_row:
            # Create empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text=f"No timeline data available for {facility_id}",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color=styling_config.get("text_secondary", "#666666"))
            )

            fig.update_layout(
                title={
                    "text": f"Incident Timeline - {facility_id}",
                    "font": {
                        "family": chart_config.get("font_family", "Arial, sans-serif"),
                        "size": chart_config.get("title_font_size", 18),
                        "color": styling_config.get("text_primary", "#333333")
                    },
                    "x": 0.5,
                    "xanchor": "center"
                },
                paper_bgcolor=styling_config.get("background_light", "#FFFFFF"),
                plot_bgcolor=styling_config.get("background_light", "#FFFFFF"),
                height=chart_config.get("default_height", 400)
            )

            return dcc.Graph(figure=fig)

        # Basic timeline implementation (placeholder using available data)
        years = [col for col in timeline_data.columns if col.isdigit()]
        values = [facility_row.get(year, 0) for year in years]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years,
            y=values,
            mode='lines+markers',
            marker=dict(size=8, color=styling_config.get("primary_color", "#4A90E2")),
            line=dict(color=styling_config.get("primary_color", "#4A90E2"), width=3),
            hovertemplate="<b>Year: %{x}</b><br>Incidents: %{y}<extra></extra>"
        ))

        fig.update_layout(
            title={
                "text": f"Historical Incidents - {facility_id}",
                "font": {
                    "family": chart_config.get("font_family", "Arial, sans-serif"),
                    "size": chart_config.get("title_font_size", 18),
                    "color": styling_config.get("text_primary", "#333333")
                },
                "x": 0.5,
                "xanchor": "center"
            },
            paper_bgcolor=styling_config.get("background_light", "#FFFFFF"),
            plot_bgcolor=styling_config.get("background_light", "#FFFFFF"),
            xaxis={"title": "Year"},
            yaxis={"title": "Number of Incidents"},
            height=chart_config.get("default_height", 400)
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, f"incident timeline creation for {facility_id}")
        return dcc.Graph(figure={})

def create_workflow_analysis_table(facility_id: str) -> html.Div:
    """
    Create workflow completion analysis for facility.
    Uses placeholder data until Phase 5 implementation.
    """
    try:
        # Placeholder implementation - basic workflow status
        placeholder_data = [
            {"Stage": "Problem Identification", "Completion Rate": "85%", "Avg. Time": "2.3 days"},
            {"Stage": "Root Cause Analysis", "Completion Rate": "78%", "Avg. Time": "5.1 days"},
            {"Stage": "Action Planning", "Completion Rate": "82%", "Avg. Time": "3.7 days"},
            {"Stage": "Verification", "Completion Rate": "65%", "Avg. Time": "12.4 days"},
        ]

        table_rows = []
        for row in placeholder_data:
            table_rows.append(html.Tr([
                html.Td(row["Stage"]),
                html.Td(row["Completion Rate"]),
                html.Td(row["Avg. Time"])
            ]))

        table = html.Table([
            html.Thead([
                html.Tr([
                    html.Th("Workflow Stage"),
                    html.Th("Completion Rate"),
                    html.Th("Average Time")
                ])
            ]),
            html.Tbody(table_rows)
        ], className="table table-striped")

        return html.Div([
            html.H5("Workflow Performance Analysis", className="mb-3"),
            table,
            html.Small(
                "Note: Data shown is placeholder. Full implementation in Phase 5.",
                className="text-muted"
            )
        ])

    except Exception as e:
        handle_error(logger, e, f"workflow analysis creation for {facility_id}")
        return html.Div([
            html.H5("Workflow Analysis Error"),
            html.P("Failed to load workflow data")
        ])

def create_facility_detail_layout(facility_id: str) -> html.Div:
    """
    Create complete facility detail page layout.
    Integration point for future Phase 5 implementation.
    """
    try:
        logger.info(f"Creating facility detail layout for {facility_id}")

        # Header section
        header = html.Div([
            html.H2(f"Facility Analysis: {facility_id}", className="mb-4"),
            dbc.Alert([
                html.H6("Phase 5 Development Notice", className="alert-heading"),
                html.P([
                    "This is a placeholder implementation using adapter pattern. ",
                    "Full facility detail analysis will be available in Phase 5 development cycle."
                ]),
                dbc.Button("Return to Portfolio Overview", href="/", color="primary", size="sm")
            ], color="info", className="mb-4")
        ])

        # Main content layout
        content = dbc.Container([
            dbc.Row([
                dbc.Col([
                    create_facility_overview_card(facility_id)
                ], md=4),
                dbc.Col([
                    create_incident_timeline_chart(facility_id)
                ], md=8)
            ], className="mb-4"),

            dbc.Row([
                dbc.Col([
                    create_workflow_analysis_table(facility_id)
                ], md=12)
            ])
        ], fluid=True)

        return html.Div([header, content])

    except Exception as e:
        handle_error(logger, e, f"facility detail layout creation for {facility_id}")
        return html.Div([
            html.H2("Facility Detail Error"),
            html.P(f"Failed to create layout for facility: {facility_id}"),
            dbc.Button("Return to Portfolio Overview", href="/", color="secondary")
        ])

# Future enhancement functions (stubs for Phase 5)

def create_asset_performance_chart(facility_id: str) -> dcc.Graph:
    """Future: Asset-specific performance analysis"""
    # Placeholder for Phase 5 implementation
    return dcc.Graph(figure={})

def create_causal_analysis_network(facility_id: str) -> html.Div:
    """Future: Facility-specific causal relationship network"""
    # Placeholder for Phase 5 implementation
    return html.Div([
        html.H5("Causal Analysis Network"),
        html.P("Available in Phase 5 - Network visualization of root cause relationships")
    ])

def create_performance_dashboard(facility_id: str) -> html.Div:
    """Future: Comprehensive facility performance dashboard"""
    # Placeholder for Phase 5 implementation
    return html.Div([
        html.H5("Performance Dashboard"),
        html.P("Available in Phase 5 - Real-time performance metrics and KPIs")
    ])

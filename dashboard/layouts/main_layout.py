#!/usr/bin/env python3
"""
Main Layout Infrastructure - Pure Adapter Dependencies
Professional layout authority with adapter-driven configuration.
"""

import logging
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

from dashboard.adapters import get_config_adapter, get_facility_adapter
from dashboard.routing.navigation_builder import get_navigation_builder
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

def create_main_layout(content: html.Div = None) -> html.Div:
    """Main application layout with navigation delegation"""
    try:
        config_adapter = get_config_adapter()
        navigation_builder = get_navigation_builder()
        styling = config_adapter.get_styling_config()

        return html.Div([
            html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            navigation_builder.build_main_navigation(),
            dbc.Container([
                dcc.Loading(
                    id="main-loading",
                    children=[html.Div(id="main-content", children=[content or html.Div()])],
                    color=styling.get("primary_color", "#4A90E2")
                )
            ], fluid=True, className="px-3"),
            create_footer(),
            html.Div([
                dcc.Store(id="dashboard-state", data={}),
                dcc.Location(id="url-location", refresh=False)
            ], style={"display": "none"})
        ], style={
            "fontFamily": "Arial, sans-serif",
            "backgroundColor": styling.get("background_light", "#FFFFFF"),
            "minHeight": "100vh"
        })

    except Exception as e:
        handle_error(logger, e, "main layout creation")
        return html.Div([html.H1("Layout Error"), html.P(str(e))])

def create_navigation_bar() -> dbc.NavbarSimple:
    """Navigation bar using navigation builder"""
    try:
        navigation_builder = get_navigation_builder()
        return navigation_builder.build_main_navigation()
    except Exception as e:
        handle_error(logger, e, "navigation bar creation")
        return dbc.NavbarSimple(brand="Mining Reliability Database", color="#1E1E1E", dark=True)

def create_footer() -> html.Footer:
    """Professional footer with system information"""
    try:
        config_adapter = get_config_adapter()
        styling = config_adapter.get_styling_config()

        return html.Footer([
            html.Hr(style={"margin": "40px 0 20px 0", "borderColor": "#E5E5E5"}),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H6("Mining Reliability Database v2.0", style={"fontWeight": "bold"}),
                        html.P([
                            "Professional Analytics Platform | ",
                            html.Small(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                        ], style={"margin": "0", "fontSize": "12px"})
                    ], md=6),
                    dbc.Col([
                        html.P([
                            html.Strong("Architecture: "), "Core → Adapter → Component | ",
                            html.Strong("Performance: "), "Sub-second response"
                        ], style={"textAlign": "right", "margin": "0", "fontSize": "12px"})
                    ], md=6)
                ])
            ], fluid=True)
        ], style={
            "backgroundColor": "#F8F9FA", "padding": "20px 0",
            "marginTop": "40px", "borderTop": "1px solid #E5E5E5"
        })

    except Exception as e:
        handle_error(logger, e, "footer creation")
        return html.Footer([html.P("Mining Reliability Database", style={"textAlign": "center"})])

def create_error_boundary(error_message: str = None) -> html.Div:
    """Error boundary for graceful failure handling"""
    return dbc.Container([
        dbc.Alert([
            html.H4("System Error", className="alert-heading"),
            html.P(error_message or "Application encountered an unexpected error"),
            html.Hr(),
            dbc.ButtonGroup([
                dbc.Button("Return to Portfolio", href="/", color="primary"),
                dbc.Button("Refresh Page", id="refresh-btn", color="secondary")
            ])
        ], color="danger")
    ])

def get_layout_config() -> dict:
    """Layout configuration from adapters"""
    try:
        config_adapter = get_config_adapter()
        return {
            "styling": config_adapter.get_styling_config(),
            "chart": config_adapter.get_chart_config(),
            "server": config_adapter.get_server_config()
        }
    except Exception as e:
        handle_error(logger, e, "layout configuration access")
        return {"styling": {}, "chart": {}, "server": {}}
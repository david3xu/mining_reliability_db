#!/usr/bin/env python3
"""
Portfolio Overview Component - Interactive Implementation
Clean component implementation with enhanced user interaction.
"""

import logging
from typing import Dict, List, Any

# Dash components
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# Interactive components
from dashboard.components.interactive_elements import (
    create_interactive_metric_card,
    create_interactive_pie_chart,
    create_interactive_bar_chart,
    create_interactive_timeline_table,
    create_interaction_feedback_toast,
    create_loading_overlay
)

# Data pipeline
from dashboard.utils.data_transformers import (
    get_portfolio_metrics,
    get_field_distribution_data,
    get_facility_breakdown_data,
    get_historical_timeline_data,
    validate_dashboard_data,
    get_styling_config,
    get_chart_config
)

# Configuration
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

def create_metrics_cards() -> List[dbc.Card]:
    """Create interactive metric cards with click functionality"""
    try:
        logger.info("Creating interactive metrics cards...")

        # Get data via adapter
        metrics_data = get_portfolio_metrics()

        if not metrics_data:
            logger.warning("No metrics data available")
            return []

        cards = []
        card_configs = [
            ("total_records", "total-records-card"),
            ("data_fields", "data-fields-card"),
            ("facilities", "facilities-card"),
            ("years_coverage", "years-card")
        ]

        for metric_key, card_id in card_configs:
            metric_info = metrics_data.get(metric_key, {})
            card = create_interactive_metric_card(metric_info, card_id)
            cards.append(card)

        logger.info(f"Created {len(cards)} interactive metric cards")
        return cards

    except Exception as e:
        handle_error(logger, e, "interactive metrics cards creation")
        return []

def create_field_distribution_chart() -> dcc.Graph:
    """Create interactive field distribution bar chart"""
    try:
        logger.info("Creating enhanced field distribution chart...")

        # Get data via adapter
        field_data = get_field_distribution_data()

        if not field_data:
            logger.warning("No field distribution data available")
            return dcc.Graph(figure={})

        # Create interactive bar chart
        chart = create_interactive_bar_chart(field_data)

        logger.info("Field distribution chart created successfully")
        return chart

    except Exception as e:
        handle_error(logger, e, "field distribution chart creation")
        return dcc.Graph(figure={})

def create_facility_pie_chart() -> dcc.Graph:
    """Create interactive facility pie chart"""
    try:
        logger.info("Creating enhanced facility pie chart...")

        # Get data via adapter
        facility_data = get_facility_breakdown_data()

        if not facility_data:
            logger.warning("No facility breakdown data available")
            return dcc.Graph(figure={})

        # Create interactive pie chart
        chart = create_interactive_pie_chart(facility_data)

        logger.info("Facility pie chart created successfully")
        return chart

    except Exception as e:
        handle_error(logger, e, "facility pie chart creation")
        return dcc.Graph(figure={})

def create_historical_table() -> dash_table.DataTable:
    """Create interactive historical timeline table"""
    try:
        logger.info("Creating enhanced historical timeline table...")

        # Get data via adapter
        timeline_data = get_historical_timeline_data()

        if not timeline_data:
            logger.warning("No timeline data available")
            return dash_table.DataTable(data=[])

        # Create interactive table
        table = create_interactive_timeline_table(timeline_data)

        logger.info("Historical table created successfully")
        return table

    except Exception as e:
        handle_error(logger, e, "enhanced historical table creation")
        return dash_table.DataTable(data=[])

def create_interaction_stores() -> List[dcc.Store]:
    """Create data stores for interaction management"""
    return [
        dcc.Store(id="chart-interaction-store", data={}),
        dcc.Store(id="table-interaction-store", data={}),
        dcc.Store(id="card-interaction-store", data={})
    ]

def create_enhanced_dashboard_layout() -> html.Div:
    """Create complete interactive dashboard layout"""
    try:
        logger.info("Creating enhanced dashboard layout...")

        # Get configuration
        styling_config = get_styling_config()
        chart_config = get_chart_config()

        # Validate data before rendering
        validation_results = validate_dashboard_data()

        if not validation_results.get("phase2_complete", False):
            logger.warning("Data validation failed - showing error state")
            return html.Div([
                dbc.Alert([
                    html.H4("Data Validation Error", className="alert-heading"),
                    html.P("Dashboard data pipeline validation failed. Interactive features may be limited."),
                    html.Hr(),
                    html.P("Run system diagnostics to resolve issues.", className="mb-0")
                ], color="warning", dismissable=True)
            ], style={"padding": "50px"})

        # Create interactive components
        metric_cards = create_metrics_cards()
        field_chart = create_field_distribution_chart()
        facility_chart = create_facility_pie_chart()
        timeline_table = create_historical_table()

        # Main layout with enhanced interactivity
        layout = html.Div([
            # Interaction stores (hidden)
            html.Div(
                create_interaction_stores(),
                style={"display": "none"}
            ),

            # Loading overlay
            create_loading_overlay(),

            # Toast notifications
            create_interaction_feedback_toast(),

            # Header section
            html.Div([
                html.H1(
                    "Portfolio Overview - What data do we have?",
                    style={
                        "fontSize": chart_config.get("title_font_size", 24),
                        "fontWeight": "bold",
                        "marginBottom": "10px",
                        "color": styling_config.get("text_light", "#FFFFFF")
                    }
                ),
                html.H4(
                    "Comprehensive Analysis Across Operational Facilities",
                    style={
                        "fontSize": chart_config.get("subtitle_font_size", 18),
                        "fontWeight": "normal",
                        "margin": "0",
                        "color": styling_config.get("text_light", "#FFFFFF"),
                        "opacity": "0.9"
                    }
                )
            ], style={
                "textAlign": "center",
                "marginBottom": "30px",
                "padding": "20px",
                "backgroundColor": styling_config.get("background_dark", "#1E1E1E"),
                "color": styling_config.get("text_light", "#FFFFFF"),
                "borderRadius": "10px"
            }),

            # Interactive metrics cards
            html.Div([
                html.H3(
                    "Key Portfolio Metrics",
                    style={
                        "textAlign": "center",
                        "marginBottom": "20px",
                        "color": styling_config.get("text_primary", "#333333"),
                        "fontSize": chart_config.get("subtitle_font_size", 18)
                    }
                ),
                html.Div(
                    metric_cards,
                    style={
                        "display": "flex",
                        "justifyContent": "space-around",
                        "flexWrap": "wrap",
                        "marginBottom": "30px",
                        "gap": "15px"
                    }
                )
            ], style={"marginBottom": "40px"}),

            # Interactive charts section
            html.Div([
                # Left: Interactive field distribution
                html.Div([
                    field_chart
                ], style={"width": "48%", "display": "inline-block"}),

                # Right: Interactive facility pie chart
                html.Div([
                    facility_chart
                ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%"})
            ], style={"marginBottom": "40px"}),

            # Interactive timeline table
            html.Div([
                html.H3(
                    "Historical Records by Year",
                    style={
                        "marginBottom": "20px",
                        "color": styling_config.get("text_primary", "#333333"),
                        "fontSize": chart_config.get("subtitle_font_size", 18)
                    }
                ),
                timeline_table
            ], style={
                "marginTop": "30px",
                "backgroundColor": styling_config.get("background_light", "#FFFFFF"),
                "borderRadius": "8px",
                "padding": "20px",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
            })

        ], style={
            "backgroundColor": styling_config.get("background_light", "#FFFFFF"),
            "padding": "20px",
            "fontFamily": chart_config.get("font_family", "Arial, sans-serif")
        })

        logger.info("Enhanced dashboard layout created successfully")
        return layout

    except Exception as e:
        handle_error(logger, e, "enhanced dashboard layout creation")
        return html.Div([
            dbc.Alert([
                html.H2("Dashboard Error", className="alert-heading"),
                html.P(f"Failed to initialize interactive dashboard: {str(e)}"),
                html.P("Please contact system administrator.", className="mb-0")
            ], color="danger")
        ], style={"padding": "50px"})

def create_complete_dashboard() -> html.Div:
    """Create complete interactive dashboard with error handling"""
    try:
        logger.info("Initializing complete interactive dashboard...")

        # Validate data availability before rendering
        validation_results = validate_dashboard_data()

        if not validation_results.get("phase2_complete", False):
            logger.warning("Phase 2 data validation failed - showing limited dashboard")
            return html.Div([
                dbc.Alert([
                    html.H4("System Status", className="alert-heading"),
                    html.P("Dashboard running in limited mode due to data validation issues."),
                    html.Ul([
                        html.Li(f"{component}: {'✅ OK' if status else '❌ Limited'}")
                        for component, status in validation_results.items()
                        if component != "phase2_complete"
                    ])
                ], color="warning", dismissable=True),
                create_enhanced_dashboard_layout()  # Still show dashboard
            ])

        # Create full interactive dashboard
        dashboard = create_enhanced_dashboard_layout()

        # Wrap in error boundary with metadata
        complete_dashboard = html.Div([
            # Meta information
            html.Div([
                html.Meta(name="viewport", content="width=device-width, initial-scale=1"),
                html.Title("Mining Reliability - Interactive Portfolio Overview")
            ], style={"display": "none"}),

            # Main dashboard content
            dashboard,

            # Footer with interaction status
            html.Footer([
                html.Hr(style={"margin": "40px 0 20px 0"}),
                html.P([
                    "Mining Reliability Database v1.0.0 | ",
                    "Interactive Dashboard | ",
                    html.Span(id="timestamp")
                ], style={
                    "textAlign": "center",
                    "fontSize": "12px",
                    "color": "#666666",
                    "margin": "20px 0"
                })
            ])
        ])

        logger.info("Complete interactive dashboard created successfully")
        return complete_dashboard

    except Exception as e:
        handle_error(logger, e, "complete interactive dashboard creation")

        # Fallback error display
        return html.Div([
            dbc.Alert([
                html.H2("Critical Dashboard Error", className="alert-heading"),
                html.P(f"Failed to initialize interactive dashboard: {str(e)}"),
                html.P("Please contact system administrator.", className="mb-0")
            ], color="danger")
        ], style={"padding": "50px"})

# Legacy compatibility function
def create_portfolio_layout() -> html.Div:
    """Legacy compatibility function"""
    return create_complete_dashboard()

#!/usr/bin/env python3
"""
Atomized Portfolio Overview - Pure Adapter Dependencies
Micro-component composition with zero direct configuration access.
"""

import logging
from typing import Any, Dict

import dash_bootstrap_components as dbc
from dash import dcc, html

# Pure adapter dependencies - no direct core/config access
from dashboard.adapters import get_config_adapter, get_data_adapter, handle_error_utility
from dashboard.components.micro.chart_base import create_bar_chart, create_pie_chart
from dashboard.components.micro.metric_card import create_metric_card
from dashboard.components.micro.table_base import create_data_table
from dashboard.utils.styling import get_colors, get_dashboard_styles

logger = logging.getLogger(__name__)

__all__ = [
    "create_metrics_section",
    "create_facility_chart",
    "create_field_chart",
    "create_timeline_table",
    "create_complete_dashboard",
    "create_historical_records_page",
    "create_facilities_distribution_page",
    "create_data_types_distribution_page",
]


def create_metrics_section() -> html.Div:
    """Pure metrics display - 12 lines"""
    try:
        adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        portfolio_data = adapter.get_portfolio_metrics()

        metrics = [
            create_metric_card(
                portfolio_data.total_records, "Total Records", True, "/historical-records"
            ),
            create_metric_card(
                portfolio_data.data_fields, "Data Fields", True, "/data-types-distribution"
            ),
            create_metric_card(
                portfolio_data.facilities, "Facilities", True, "/facilities-distribution"
            ),
            create_metric_card(portfolio_data.years_coverage, "Years Coverage"),
        ]

        return html.Div(
            [
                html.H3("Portfolio Metrics", className="text-center mb-4"),
                html.Div(metrics, className="d-flex justify-content-center gap-3"),
            ],
            className="p-4",
            style={
                "backgroundColor": get_colors().get("background_dark"),
                "color": get_colors().get("text_light"),
                "borderRadius": "8px",
            },
        )
    except Exception as e:
        handle_error_utility(logger, e, "metrics section creation")
        return html.Div("Metrics unavailable")


def create_facility_chart() -> dcc.Graph:
    """Pure facility chart - 8 lines"""
    try:
        adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        facility_data = adapter.get_facility_breakdown()
        return create_pie_chart(facility_data.labels, facility_data.values, "Facility Distribution")
    except Exception as e:
        handle_error_utility(logger, e, "facility chart creation")
        return dcc.Graph(figure={})


def create_field_chart() -> dcc.Graph:
    """Pure field chart - 8 lines"""
    try:
        adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        field_data = adapter.get_field_distribution()
        colors = get_colors()
        category_mapping = config_adapter.get_field_category_display_mapping()

        bar_colors = [
            colors.get("chart_colors", [])[i % len(colors.get("chart_colors", []))]
            for i, label in enumerate(field_data.labels)
        ]

        return create_bar_chart(
            field_data.labels, field_data.values, "Data Types Distribution", bar_colors
        )
    except Exception as e:
        handle_error_utility(logger, e, "field chart creation")
        return dcc.Graph(figure={})


def create_timeline_table() -> any:
    """Pure timeline table - 10 lines"""
    try:
        adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        timeline_data = adapter.get_historical_timeline()
        return create_data_table(
            timeline_data.rows, timeline_data.columns, "timeline-table", link_column="facility"
        )
    except Exception as e:
        handle_error_utility(logger, e, "timeline table creation")
        logger.exception("Error creating timeline table")
        return html.Div("Timeline unavailable")


def create_complete_dashboard() -> html.Div:
    """Main dashboard composition - 18 lines"""
    try:
        adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        validation = adapter.get_data_quality_validation()

        if not validation.overall_status:
            return dbc.Alert("Data validation failed", color="warning")

        return html.Div(
            [
                create_metrics_section(),
                html.Div(
                    [
                        html.P(
                            "Click metric cards to explore detailed analysis",
                            className="text-center text-muted mt-4 fst-italic",
                        )
                    ]
                ),
            ],
            className="container-fluid p-4",
            style=get_dashboard_styles().get("main_container"),
        )
    except Exception as e:
        handle_error_utility(logger, e, "complete dashboard creation")
        return dbc.Alert("Dashboard creation failed", color="danger")


def create_historical_records_page() -> html.Div:
    """Historical records analysis page - 15 lines"""
    try:
        config_adapter = get_config_adapter()
        return html.Div(
            [
                dbc.Container(
                    [
                        dbc.Button(
                            "← Back to Portfolio",
                            href="/",
                            color="secondary",
                            size="sm",
                            className="mb-3",
                        ),
                        html.H2("Historical Records Analysis", className="text-primary mb-4"),
                        create_timeline_table(),
                    ],
                    fluid=True,
                )
            ],
            className="p-4",
            style=get_dashboard_styles().get("main_container"),
        )
    except Exception as e:
        handle_error_utility(logger, e, "historical records page creation")
        return dbc.Alert("Historical records unavailable", color="danger")


def create_facilities_distribution_page() -> html.Div:
    """Facilities distribution page - 15 lines"""
    try:
        config_adapter = get_config_adapter()
        return html.Div(
            [
                dbc.Container(
                    [
                        dbc.Button(
                            "← Back to Portfolio",
                            href="/",
                            color="secondary",
                            size="sm",
                            className="mb-3",
                        ),
                        html.H2("Facilities Distribution", className="text-primary mb-4"),
                        create_facility_chart(),
                    ],
                    fluid=True,
                )
            ],
            className="p-4",
            style=get_dashboard_styles().get("main_container"),
        )
    except Exception as e:
        handle_error_utility(logger, e, "facilities distribution page creation")
        return dbc.Alert("Facilities distribution unavailable", color="danger")


def create_data_types_distribution_page() -> html.Div:
    """Data types distribution page - 15 lines"""
    try:
        adapter = get_data_adapter()
        config_adapter = get_config_adapter()
        field_data = adapter.get_field_distribution()
        return html.Div(
            [
                dbc.Container(
                    [
                        dbc.Button(
                            "← Back to Portfolio",
                            href="/",
                            color="secondary",
                            size="sm",
                            className="mb-3",
                        ),
                        html.H2("Data Types Distribution", className="text-primary mb-4"),
                        create_field_chart(),
                        html.H3(
                            "Detailed Field Counts by Category", className="text-primary mt-5 mb-3"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5(
                                                    category_display_name, className="card-title"
                                                ),
                                                html.P(
                                                    f"Count: {count}", className="card-text mb-2"
                                                ),
                                                html.Ul(
                                                    [
                                                        html.Li(field)
                                                        for field in field_data.detailed_field_names.get(
                                                            category_key, []
                                                        )
                                                    ],
                                                    className="list-unstyled small",
                                                ),
                                            ]
                                        )
                                    ),
                                    md=4,  # Adjust column width as needed
                                )
                                for category_key, count in field_data.category_counts.items()
                                for category_display_name in [
                                    config_adapter.get_field_category_display_mapping().get(
                                        category_key, category_key.replace("_", " ").title()
                                    )
                                ]
                            ],
                            className="mt-3",
                        ),
                    ],
                    fluid=True,
                )
            ],
            className="p-4",
            style=get_dashboard_styles().get("main_container"),
        )
    except Exception as e:
        handle_error_utility(logger, e, "data types distribution page creation")
        return dbc.Alert("Data types distribution unavailable", color="danger")

#!/usr/bin/env python3
"""
Micro-Component: Facility Card - Facility Summary Display
18-line atomic component for facility overview.
"""

import dash_bootstrap_components as dbc
from dash import html

from dashboard.adapters import get_config_adapter


def create_facility_summary_card(facility_data: dict) -> dbc.Card:
    """Pure facility card component - 14 lines of logic"""
    config = get_config_adapter().get_styling_config()

    facility_id = facility_data.get("facility_id", "Unknown")
    total_records = facility_data.get("total_records", 0)
    active_status = facility_data.get("active", True)

    status_color = config.get("chart_colors", ["#7ED321"])[0] if active_status else "#D32F2F"

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(facility_id, className="card-title"),
                    html.H3(
                        f"{total_records:,}",
                        style={"color": config.get("primary_color", "#4A90E2")},
                    ),
                    html.P("Total Records", className="text-muted"),
                    html.Span(
                        "Active" if active_status else "Inactive",
                        style={
                            "padding": "4px 8px",
                            "borderRadius": "4px",
                            "backgroundColor": status_color,
                            "color": "#FFFFFF",
                            "fontSize": "12px",
                        },
                    ),
                ]
            )
        ],
        style={"minHeight": "160px", "textAlign": "center"},
    )

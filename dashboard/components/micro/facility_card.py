#!/usr/bin/env python3
"""
Micro-Component: Facility Card - Facility Summary Display
18-line atomic component for facility overview.
"""

from typing import List

import dash_bootstrap_components as dbc
from dash import html

from dashboard.adapters import get_config_adapter
from mine_core.shared.common import get_logger, handle_error

logger = get_logger(__name__)


def create_facility_summary_card(facility_data: dict) -> dbc.Card:
    """Pure facility card component - 14 lines of logic"""
    config = get_config_adapter().get_styling_config()

    facility_id = facility_data.get("facility_id", "Unknown")
    total_records = facility_data.get("total_records", 0)
    active_status = facility_data.get("active", True)

    status_colors = (
        config.get("micro_component_styles", {})
        .get("facility_card", {})
        .get("status_indicators", {})
    )
    status_color = status_colors.get("active") if active_status else status_colors.get("inactive")

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(
                        facility_id,
                        className="card-title",
                        style={"color": config.get("text_primary")},
                    ),
                    html.H3(
                        f"{total_records:,}",
                        style={"color": config.get("primary_color")},
                    ),
                    html.P(
                        "Total Records",
                        className="text-muted",
                        style={"color": config.get("text_muted")},
                    ),
                    html.Span(
                        "Active" if active_status else "Inactive",
                        style={
                            "padding": "4px 8px",
                            "borderRadius": "4px",
                            "backgroundColor": status_color,
                            "color": config.get("text_light"),
                            "fontSize": "12px",
                        },
                    ),
                ]
            )
        ],
        style={
            "minHeight": config.get("micro_component_styles", {})
            .get("facility_card", {})
            .get("card_dimensions", {})
            .get("min_height", "160px"),
            "textAlign": config.get("micro_component_styles", {})
            .get("facility_card", {})
            .get("layout", {})
            .get("text_align", "center"),
            "backgroundColor": config.get("background_light"),
            "boxShadow": config.get("shadow_light"),
            "borderRadius": config.get("micro_component_styles", {})
            .get("facility_card", {})
            .get("card_dimensions", {})
            .get("border_radius", "8px"),
            "padding": config.get("micro_component_styles", {})
            .get("facility_card", {})
            .get("card_dimensions", {})
            .get("padding", "15px"),
            "border": f"1px solid {config.get('border_color')}",
        },
    )


def create_small_supporting_card(entity_data: dict) -> dbc.Card:
    """Compact supporting entity card with field details"""
    config = get_config_adapter().get_styling_config()
    entity_name = entity_data.get("name", "Unknown")
    description = entity_data.get("description", "")

    # Get actual field names from adapter
    fields = entity_data.get("field_names", [])  # Now comes from adapter
    field_count = len(fields)

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6(
                        entity_name,
                        className="card-title",
                        style={"fontSize": "12px", "fontWeight": "bold", "margin": "0 0 5px 0"},
                    ),
                    html.P(
                        f"{field_count} Fields",
                        style={"fontSize": "10px", "margin": "0 0 5px 0", "color": "#666"},
                    ),
                    html.Div(
                        [
                            html.P(
                                field, style={"fontSize": "9px", "margin": "1px 0", "color": "#555"}
                            )
                            for field in fields
                        ]
                    ),
                    html.Small(description, className="text-muted", style={"fontSize": "9px"}),
                ]
            )
        ],
        style={
            "minHeight": "100px",  # Reduced height
            "textAlign": "left",
            "backgroundColor": "#F8F9FA",
            "border": "1px solid #E5E5E5",
            "borderRadius": "6px",
            "padding": "8px",
        },
    )

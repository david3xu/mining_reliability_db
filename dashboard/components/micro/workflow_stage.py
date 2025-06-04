#!/usr/bin/env python3
"""
Micro-Component: Workflow Stage - Single Process Stage Display
22-line atomic component for workflow stage visualization.
"""

from typing import List

from dash import html

from dashboard.adapters import get_config_adapter
from mine_core.shared.common import get_logger

logger = get_logger(__name__)


def create_workflow_stage_card(stage_data: dict) -> html.Div:
    """Pure workflow stage component - 18 lines of logic"""
    config = get_config_adapter().get_workflow_display_config()

    # Extract core stage data
    stage_number = stage_data.get("stage_number", 1)
    title = stage_data.get("title", "Unknown")
    completion_rate = stage_data.get("completion_rate", 0.0)
    field_count = stage_data.get("field_count", 0)
    color = stage_data.get("color", "#4A90E2")

    # Build card content
    header = html.Div(
        [
            html.H6(f"STAGE {stage_number}", style={"fontSize": "14px", "margin": "0"}),
            html.H4(title, style={"fontSize": "18px", "margin": "5px 0 0 0"}),
        ],
        style={
            "backgroundColor": config.get("header_styling", {}).get(
                "background_color", "rgba(0,0,0,0.3)"
            ),
            "padding": config.get("header_styling", {}).get("padding", "10px"),
            "borderRadius": "8px 8px 0 0",
            "color": config.get("header_styling", {}).get("text_color", "#FFFFFF"),
        },
    )

    content = html.Div(
        [
            html.P(
                f"{field_count} Fields",
                style={
                    "fontSize": "14px",
                    "fontWeight": "bold",
                    "color": config.get("content_styling", {}).get("text_color", "#FFFFFF"),
                },
            ),
            html.Span(
                f"{completion_rate}% Complete",
                style={
                    "padding": "5px 10px",
                    "borderRadius": "10px",
                    "backgroundColor": config.get("header_styling", {}).get(
                        "background_color", "rgba(255,255,255,0.2)"
                    ),
                    "color": config.get("content_styling", {}).get("text_color", "#FFFFFF"),
                },
            ),
        ],
        style={"padding": config.get("content_styling", {}).get("padding", "15px")},
    )

    return html.Div(
        [header, content],
        style={
            "backgroundColor": color,
            "color": config.get("card_dimensions", {}).get("text_color", "#FFFFFF"),
            "borderRadius": config.get("card_dimensions", {}).get("border_radius", "8px"),
            "minHeight": config.get("card_dimensions", {}).get("min_height", "280px"),
            "margin": config.get("card_dimensions", {}).get("margin", "10px"),
            "boxShadow": config.get("card_dimensions", {}).get(
                "box_shadow", "0 4px 6px rgba(0,0,0,0.1)"
            ),
        },
    )


def create_large_workflow_stage_card(stage_data: dict) -> html.Div:
    """Pure component - receives processed data from adapter"""
    stage_number = stage_data.get("stage_number", 1)
    title = stage_data.get("title", "Unknown")
    completion_rate = stage_data.get("completion_rate", 0.0)
    color = stage_data.get("color", "#4A90E2")

    # Use only data provided by adapter
    field_names = stage_data.get("field_names", [])  # From adapter
    field_count = stage_data.get("field_count", 0)  # From adapter

    # Display logic for field names
    if len(field_names) <= 6:
        displayed_fields = field_names
        more_text = None
    else:
        displayed_fields = field_names[:6]
        more_text = f"... +{len(field_names)-6} more"

    header = html.Div(
        [
            html.H5(
                f"STAGE {stage_number}",
                style={"fontSize": "16px", "margin": "0", "fontWeight": "bold"},
            ),
            html.H3(title, style={"fontSize": "18px", "margin": "8px 0 0 0"}),
        ],
        style={
            "backgroundColor": "rgba(0,0,0,0.3)",
            "padding": "12px",
            "borderRadius": "8px 8px 0 0",
        },
    )

    field_list = [
        html.P(field, style={"fontSize": "11px", "margin": "2px 0", "opacity": "0.9"})
        for field in displayed_fields
    ]
    if more_text:
        field_list.append(
            html.P(more_text, style={"fontSize": "10px", "fontStyle": "italic", "margin": "2px 0"})
        )

    content = html.Div(
        [
            html.P(
                f"{field_count} Fields:",
                style={"fontSize": "14px", "fontWeight": "bold", "margin": "10px 0 8px 0"},
            ),
            html.Div(field_list),
            html.Div(
                [
                    html.Span(
                        f"{completion_rate:.1f}% Complete",
                        style={
                            "padding": "6px 12px",
                            "borderRadius": "12px",
                            "backgroundColor": "rgba(255,255,255,0.2)",
                            "fontSize": "12px",
                        },
                    )
                ],
                style={"marginTop": "15px"},
            ),
        ],
        style={"padding": "15px", "textAlign": "left"},
    )

    return html.Div(
        [header, content],
        style={
            "backgroundColor": color,
            "color": "#FFFFFF",
            "borderRadius": "8px",
            "minHeight": "400px",
            "width": "220px",
            "margin": "10px",
            "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
        },
    )

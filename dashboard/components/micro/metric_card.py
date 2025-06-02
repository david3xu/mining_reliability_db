#!/usr/bin/env python3
"""
Micro-Component: Metric Card - Single Purpose Display
15-line atomic component for metric visualization.
"""

from dash import html
from dashboard.adapters import get_config_adapter

def create_metric_card(value: any, label: str, clickable: bool = False, href: str = None) -> html.Div:
    """Pure metric card component - 12 lines of logic"""
    config = get_config_adapter().get_metric_card_styling()

    display_value = f"{value:,}" if isinstance(value, int) and value > 999 else str(value)

    card_style = {
        "backgroundColor": config.get("primary_color", "#4A90E2"),
        "color": config.get("text_light", "#FFFFFF"),
        "padding": "20px", "borderRadius": "8px", "textAlign": "center",
        "height": f"{config.get('card_height', 120)}px",
        "width": f"{config.get('card_width', 220)}px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "cursor": "pointer" if clickable else "default"
    }

    content = [
        html.H2(display_value, style={"fontSize": "32px", "fontWeight": "bold", "margin": "0"}),
        html.P(label, style={"fontSize": "14px", "margin": "5px 0 0 0", "opacity": "0.9"})
    ]

    return html.A(content, href=href, style=card_style) if clickable else html.Div(content, style=card_style)
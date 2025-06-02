#!/usr/bin/env python3
"""
Micro-Component: Metric Card - Single Purpose Display
15-line atomic component for metric visualization.
"""

from dash import html

from dashboard.utils.styling import get_metric_card_style


def create_metric_card(
    value: any, label: str, clickable: bool = False, href: str = None
) -> html.Div:
    """Pure metric card component - 12 lines of logic"""
    card_style = get_metric_card_style()

    display_value = str(value)

    content = [
        html.H2(
            display_value,
            style={
                "fontSize": "32px",
                "fontWeight": "bold",
                "margin": "0",
                "textDecoration": "none",
            },
        ),
        html.P(
            label,
            style={
                "fontSize": "14px",
                "margin": "5px 0 0 0",
                "opacity": "0.9",
                "textDecoration": "none",
            },
        ),
    ]

    # If clickable, ensure the anchor tag itself does not have a text-decoration
    clickable_card_style = {**card_style, **{"textDecoration": "none"}}

    return (
        html.A(content, href=href, style=clickable_card_style)
        if clickable
        else html.Div(content, style=card_style)
    )

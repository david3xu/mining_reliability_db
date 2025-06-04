#!/usr/bin/env python3
"""
Micro-Component: Chart Base - Reusable Chart Foundation
18-line atomic component for standardized chart creation.
"""

import plotly.graph_objects as go
from dash import dcc

from dashboard.adapters import get_config_adapter


def create_pie_chart(labels: list, values: list, title: str) -> dcc.Graph:
    """Pure pie chart component - 8 lines of logic"""
    config = get_config_adapter().get_dashboard_chart_styling_template()
    colors = get_colors()

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo="label+percent")])
    fig.update_layout(
        title=title,
        height=config.get("height", 400),
        font={
            "family": config.get("font_family", "Arial"),
            "size": 14,
            "color": colors.get("text_primary"),
        },
        paper_bgcolor=colors.get("background_dark"),
        plot_bgcolor=colors.get("background_dark"),
    )
    return dcc.Graph(figure=fig)


def create_bar_chart(x_data: list, y_data: list, title: str, bar_colors: list = None) -> dcc.Graph:
    """Pure bar chart component - 8 lines of logic"""
    config = get_config_adapter().get_dashboard_chart_styling_template()
    colors = get_colors()

    fig = go.Figure(
        data=[
            go.Bar(
                x=x_data, y=y_data, marker_color=bar_colors or config.get("colors", ["#64B5F6"])[0]
            )
        ]
    )
    fig.update_layout(
        title=title,
        height=config.get("height", 400),
        font={
            "family": config.get("font_family", "Arial"),
            "size": 14,
            "color": colors.get("text_primary"),
        },
        paper_bgcolor=colors.get("background_dark"),
        plot_bgcolor=colors.get("background_dark"),
    )
    return dcc.Graph(figure=fig)

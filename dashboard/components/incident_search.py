#!/usr/bin/env python3
"""
Incident Search Component - Layout Only
Search interface layout without callbacks (callbacks handled by interaction_handlers).
"""

import logging

import dash_bootstrap_components as dbc
from dash import html

from dashboard.components.layout_template import create_standard_layout
from dashboard.utils.styling import get_colors

logger = logging.getLogger(__name__)

__all__ = ["create_incident_search_layout"]


def create_incident_search_layout() -> html.Div:
    """Main search interface with results display"""
    try:
        colors = get_colors()

        search_interface = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.Input(
                                            id="search-input",
                                            placeholder="Search problems (e.g., 'pump failure', 'vibration', 'equipment')",
                                            type="text",
                                            style={"fontSize": "16px"},
                                        ),
                                        dbc.Button(
                                            "Search",
                                            id="search-button",
                                            color="primary",
                                            n_clicks=0,
                                        ),
                                    ],
                                    className="mb-3",
                                )
                            ],
                            md=8,
                        ),
                        dbc.Col(
                            [
                                dbc.Button(
                                    "Clear Results",
                                    id="clear-button",
                                    color="secondary",
                                    n_clicks=0,
                                    className="ms-2",
                                )
                            ],
                            md=2,
                        ),
                    ]
                ),
                html.Div(id="search-status", className="mb-3"),
                html.Div(id="search-results"),
            ]
        )

        return create_standard_layout(
            title="Incident Pattern Search",
            content_cards=[
                html.Div(
                    [
                        dbc.Button(
                            "← Back to Portfolio",
                            href="/",
                            color="secondary",
                            size="sm",
                            className="mb-3",
                        ),
                        search_interface,
                    ]
                )
            ],
        )

    except Exception as e:
        logger.error(f"Error creating incident search layout: {e}")
        return html.Div("Search interface unavailable")

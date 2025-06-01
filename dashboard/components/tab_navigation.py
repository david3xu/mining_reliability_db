#!/usr/bin/env python3
"""
Tab Navigation Component
Professional tab switcher for multi-view dashboard.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Optional

def create_tab_navigation(active_tab: str = "portfolio") -> dbc.Tabs:
    """Create professional tab navigation interface"""

    tabs = dbc.Tabs([
        dbc.Tab(
            label="Portfolio Overview",
            tab_id="portfolio",
            active_tab_class_name="fw-bold text-primary"
        ),
        dbc.Tab(
            label="Data Quality Foundation",
            tab_id="quality",
            active_tab_class_name="fw-bold text-primary"
        ),
        dbc.Tab(
            label="Workflow Understanding",
            tab_id="workflow",
            active_tab_class_name="fw-bold text-primary"
        )
    ],
    id="main-tabs",
    active_tab=active_tab,
    className="mb-4"
    )

    return tabs

def get_tab_content_id(tab_id: str) -> str:
    """Generate content container ID for tab"""
    return f"{tab_id}-content"

def create_tab_container() -> html.Div:
    """Create container for tab content with proper styling"""

    return html.Div([
        create_tab_navigation(),
        html.Div(id="tab-content", className="mt-3")
    ], className="tab-container")

def get_tab_metadata(tab_id: str) -> dict:
    """Get metadata for specific tab"""

    metadata = {
        "portfolio": {
            "title": "Portfolio Overview - What data do we have?",
            "subtitle": "Comprehensive Analysis Across Operational Facilities",
            "focus": "Data inventory and facility distribution"
        },
        "quality": {
            "title": "Data Quality Foundation - Where are the problems?",
            "subtitle": "Field Completeness, Action Request & Categorical Value Diversity",
            "focus": "Reliability assessment and problem identification"
        },
        "workflow": {
            "title": "Workflow Understanding - How is it organized?",
            "subtitle": "41 Fields Mapped Across 5 Core Process Stages",
            "focus": "Process mapping and stage analysis"
        }
    }

    return metadata.get(tab_id, {})

def create_tab_header(tab_id: str) -> html.Div:
    """Create standardized header for any tab"""

    metadata = get_tab_metadata(tab_id)

    return html.Div([
        html.H1(
            metadata.get("title", "Analysis Dashboard"),
            className="text-primary mb-2",
            style={"fontSize": "28px", "fontWeight": "bold"}
        ),
        html.H4(
            metadata.get("subtitle", "Data Analysis"),
            className="text-muted mb-4",
            style={"fontSize": "18px", "fontWeight": "normal"}
        )
    ],
    className="text-center p-4 bg-dark text-white rounded mb-4"
    )
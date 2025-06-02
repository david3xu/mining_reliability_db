#!/usr/bin/env python3
"""
Tab Navigation Component - Clean Navigation System
Direct tab interface with adapter-driven configuration.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard.adapters import get_config_adapter

def create_tab_navigation(active_tab: str = "portfolio") -> dbc.Tabs:
    """Professional tab navigation interface"""
    return dbc.Tabs([
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

def create_tab_container() -> html.Div:
    """Tab content container with navigation"""
    return html.Div([
        create_tab_navigation(),
        html.Div(id="tab-content", className="mt-3")
    ], className="tab-container")

def create_breadcrumb_navigation(pathname: str) -> dbc.Breadcrumb:
    """Breadcrumb navigation for current path"""
    breadcrumb_items = [dbc.BreadcrumbItem("Portfolio", href="/", external_link=True)]

    if pathname and pathname != "/":
        if pathname.startswith("/facility/"):
            facility_id = pathname.replace("/facility/", "")
            breadcrumb_items.append(dbc.BreadcrumbItem(f"Facility: {facility_id}", active=True))
        elif pathname == "/data-quality":
            breadcrumb_items.append(dbc.BreadcrumbItem("Data Quality", active=True))
        elif pathname == "/workflow":
            breadcrumb_items.append(dbc.BreadcrumbItem("Workflow", active=True))
        else:
            page_name = pathname.replace("/", "").replace("-", " ").title()
            breadcrumb_items.append(dbc.BreadcrumbItem(page_name, active=True))

    return dbc.Breadcrumb(items=breadcrumb_items)

def get_tab_content_id(tab_id: str) -> str:
    """Generate content container ID"""
    return f"{tab_id}-content"

def get_tab_metadata(tab_id: str) -> dict:
    """Tab configuration metadata"""
    metadata = {
        "portfolio": {
            "title": "Portfolio Overview - Data Inventory Analysis",
            "subtitle": "Comprehensive Assessment Across Operational Facilities",
            "focus": "Data coverage and facility distribution patterns"
        },
        "quality": {
            "title": "Data Quality Foundation - Problem Identification",
            "subtitle": "Field Completeness Assessment and Value Analysis",
            "focus": "Reliability evaluation and gap identification"
        },
        "workflow": {
            "title": "Workflow Understanding - Process Organization",
            "subtitle": "Field Mapping Across Core Process Stages",
            "focus": "Process structure and stage analysis"
        }
    }
    return metadata.get(tab_id, {"title": "Analysis Dashboard", "subtitle": "Data Analysis", "focus": "System analysis"})

def create_tab_header(tab_id: str) -> html.Div:
    """Standard tab header with metadata"""
    config_adapter = get_config_adapter()
    styling = config_adapter.get_styling_config()
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
    className="text-center p-4 text-white rounded mb-4",
    style={"backgroundColor": styling.get("background_dark", "#1E1E1E")}
    )

def create_page_header(title: str, subtitle: str = None, back_link: str = None) -> html.Div:
    """Standard page header with optional navigation"""
    config_adapter = get_config_adapter()
    styling = config_adapter.get_styling_config()

    header_content = []

    if back_link:
        header_content.append(
            dbc.Button("← Back", href=back_link, color="secondary", size="sm", className="mb-3")
        )

    header_content.extend([
        html.H2(title, className="text-primary mb-2"),
        html.P(subtitle, className="text-muted mb-0") if subtitle else html.Div()
    ])

    return html.Div(header_content, className="mb-4")
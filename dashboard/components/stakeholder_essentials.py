#!/usr/bin/env python3
"""
Essential Stakeholder Questions Component
Focused interface for the 3 most critical business questions in incident investigation.
"""

import logging
from typing import Any, Dict, List

import dash_bootstrap_components as dbc
from dash import dcc, html

from dashboard.adapters.data_adapter import get_data_adapter
from dashboard.components.layout_template import create_standard_layout

from dashboard.utils.styling import get_colors
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


def create_essential_questions_interface():
    """Simple interface for 3 essential questions"""

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Essential Investigation Questions"),
                    dbc.InputGroup(
                        [
                            dbc.Input(
                                id="incident-keywords", placeholder="excavator motor contamination"
                            ),
                            dbc.Button("Search", id="search-btn", color="primary"),
                        ]
                    ),
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Can this be fixed?", tab_id="tab-1"),
                            dbc.Tab(label="Who do I call?", tab_id="tab-2"),
                            dbc.Tab(label="How long will this take?", tab_id="tab-3"),
                        ],
                        id="question-tabs",
                    ),
                    html.Div(id="results-display"),
                ]
            )
        ]
    )


def create_solutions_table(results: List[Dict[str, Any]]) -> html.Div:
    """Create table for proven solutions"""
    if not results:
        return dbc.Alert("No proven solutions found for these keywords", color="warning")

    table_rows = []
    for result in results[:10]:
        table_rows.append(
            html.Tr(
                [
                    html.Td(result.get("incident_id", "N/A")),
                    html.Td(result.get("success_location", "N/A")),
                    html.Td(
                        html.Div(result.get("problem_description", "N/A")),
                        style={"whiteSpace": "normal", "wordBreak": "break-word"},
                    ),
                    html.Td(
                        html.Div(result.get("proven_solution", "N/A")),
                        style={"whiteSpace": "normal", "wordBreak": "break-word"},
                    ),
                    html.Td(
                        html.Span("✅ Verified", className="badge bg-success")
                        if result.get("outcome_validation")
                        else html.Span("Pending", className="badge bg-warning")
                    ),
                ]
            )
        )

    return html.Div(
        [
            html.H5(f"Proven Solutions ({len(results)} found)", className="text-success mb-3"),
            dbc.Table(
                [
                    html.Thead(
                        [
                            html.Tr(
                                [
                                    html.Th("Incident ID"),
                                    html.Th("Location"),
                                    html.Th("Problem"),
                                    html.Th("Proven Solution"),
                                    html.Th("Status"),
                                ]
                            )
                        ]
                    ),
                    html.Tbody(table_rows),
                ],
                striped=True,
                hover=True,
                responsive=True,
                size="sm",
            ),
        ]
    )


def create_expertise_table(results: List[Dict[str, Any]]) -> html.Div:
    """Create table for department expertise"""
    if not results:
        return dbc.Alert("No department expertise data found", color="warning")

    table_rows = []
    for result in results[:10]:
        success_rate = result.get("success_rate", 0)
        badge_color = (
            "success" if success_rate >= 80 else "warning" if success_rate >= 60 else "secondary"
        )

        table_rows.append(
            html.Tr(
                [
                    html.Td(result.get("initiating_department", "N/A")),
                    html.Td(result.get("receiving_department", "N/A")),
                    html.Td(result.get("facility", "N/A")),
                    html.Td(result.get("location", "N/A")),
                    html.Td(
                        f"{result.get('successful_resolutions', 0)}/{result.get('contamination_cases', 0)}"
                    ),
                    html.Td(html.Span(f"{success_rate}%", className=f"badge bg-{badge_color}")),
                ]
            )
        )

    return html.Div(
        [
            html.H5(f"Expert Departments ({len(results)} found)", className="text-info mb-3"),
            dbc.Table(
                [
                    html.Thead(
                        [
                            html.Tr(
                                [
                                    html.Th("Initiating Dept"),
                                    html.Th("Receiving Dept"),
                                    html.Th("Facility"),
                                    html.Th("Location"),
                                    html.Th("Success Record"),
                                    html.Th("Success Rate"),
                                ]
                            )
                        ]
                    ),
                    html.Tbody(table_rows),
                ],
                striped=True,
                hover=True,
                responsive=True,
                size="sm",
            ),
        ]
    )


def create_timeline_table(results: List[Dict[str, Any]]) -> html.Div:
    """Create table for timeline analysis"""
    if not results:
        return dbc.Alert("No timeline data found for these repairs", color="warning")

    table_rows = []
    for result in results[:10]:
        avg_days = result.get("average_days", 0)
        badge_color = "success" if avg_days <= 3 else "warning" if avg_days <= 7 else "danger"

        table_rows.append(
            html.Tr(
                [
                    html.Td(
                        html.Div(result.get("repair_type", "N/A")),
                        style={"whiteSpace": "normal", "wordBreak": "break-word"},
                    ),
                    html.Td(html.Span(f"{avg_days:.1f} days", className=f"badge bg-{badge_color}")),
                    html.Td(f"{result.get('fastest_completion', 0)} days"),
                    html.Td(f"{result.get('longest_completion', 0)} days"),
                    html.Td(result.get("repair_instances", 0)),
                    html.Td(f"{result.get('average_planned_days', 0):.1f} days"),
                ]
            )
        )

    return html.Div(
        [
            html.H5(
                f"Timeline Analysis ({len(results)} repair types)", className="text-warning mb-3"
            ),
            dbc.Table(
                [
                    html.Thead(
                        [
                            html.Tr(
                                [
                                    html.Th("Repair Type"),
                                    html.Th("Avg Duration"),
                                    html.Th("Fastest"),
                                    html.Th("Longest"),
                                    html.Th("Instances"),
                                    html.Th("Planned Avg"),
                                ]
                            )
                        ]
                    ),
                    html.Tbody(table_rows),
                ],
                striped=True,
                hover=True,
                responsive=True,
                size="sm",
            ),
        ]
    )


def create_stakeholder_essentials_layout(category_id=None):
    """Create the main stakeholder essentials layout"""
    return create_essential_questions_interface()

def create_essential_questions_layout():
    """Alias for backwards compatibility"""
    return create_stakeholder_essentials_layout()


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
    """Simple interface for essential questions with JSON export"""

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
                            dbc.Button("Search", id="search-btn", color="primary", className="me-2"),
                            dbc.Button("Export JSON", id="export-json-btn", color="secondary", outline=True, className="me-2"),
                            dbc.Button("Export All", id="export-all-btn", color="success", outline=True)
                        ]
                    ),
                    dbc.Tabs(
                        [
                            dbc.Tab(label="What could be causing this?", tab_id="tab-1"),
                            dbc.Tab(label="Who has diagnostic experience?", tab_id="tab-2"),
                            dbc.Tab(label="What should I check first?", tab_id="tab-3"),
                            dbc.Tab(label="What investigation steps worked?", tab_id="tab-4"),
                        ],
                        id="question-tabs",
                    ),
                    html.Div(id="export-status", className="mt-2"),
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


def create_effective_actions_table(results: List[Dict[str, Any]]) -> html.Div:
    """Create table for effective actions with rationale"""

    if not results:
        return dbc.Alert("No proven effective actions found for these keywords", color="warning")

    table_rows = []
    for result in results[:10]:
        # Create confidence badge
        confidence_level = result.get("confidence_level", "Low")
        confidence_colors = {"High": "success", "Medium": "warning", "Low": "secondary"}
        confidence_badge = dbc.Badge(
            confidence_level,
            color=confidence_colors.get(confidence_level, "secondary")
        )

        # Create evidence quality badge
        evidence_quality = result.get("evidence_quality", "Limited")
        evidence_colors = {"Strong": "success", "Moderate": "info", "Limited": "secondary"}
        evidence_badge = dbc.Badge(
            evidence_quality,
            color=evidence_colors.get(evidence_quality, "secondary")
        )

        table_rows.append(
            html.Tr([
                html.Td(result.get("incident_id", "N/A")),
                html.Td(result.get("facility", "N/A")),
                html.Td(
                    html.Div(result.get("effective_action", "")[:60] + "..."
                            if len(result.get("effective_action", "")) > 60
                            else result.get("effective_action", "")),
                    style={"whiteSpace": "normal", "wordBreak": "break-word"},
                ),
                html.Td(
                    html.Div(result.get("why_effective", "No explanation provided")[:50] + "..."
                            if len(result.get("why_effective", "")) > 50
                            else result.get("why_effective", "No explanation provided")),
                    style={"whiteSpace": "normal", "wordBreak": "break-word"},
                ),
                html.Td(str(result.get("usage_frequency", 0))),
                html.Td([confidence_badge, html.Br(), evidence_badge]),
            ])
        )

    return html.Div([
        html.H5(f"Proven Effective Actions ({len(results)} found)", className="text-success mb-3"),
        dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Action Request"),
                    html.Th("Facility"),
                    html.Th("Effective Action"),
                    html.Th("Why It Works"),
                    html.Th("Usage Count"),
                    html.Th("Confidence")
                ])
            ]),
            html.Tbody(table_rows),
        ], striped=True, hover=True, responsive=True, size="sm"),
    ])


# Export-enhanced table functions for JSON export feature

def create_effective_actions_table_with_export_info(results: List[Dict[str, Any]], export_path: str = None) -> html.Div:
    """Enhanced table with export information"""

    if not results:
        return dbc.Alert("No proven effective actions found for these keywords", color="warning")

    # Export notification
    export_info = []
    if export_path:
        export_info = [
            dbc.Alert([
                html.I(className="fas fa-download me-2"),
                f"Results exported to: {export_path.split('/')[-1]}"
            ], color="success", className="mb-3")
        ]

    # Create table rows
    table_rows = []
    for result in results[:10]:
        confidence_level = result.get("confidence_level", "Low")
        confidence_colors = {"High": "success", "Medium": "warning", "Low": "secondary"}
        confidence_badge = dbc.Badge(
            confidence_level,
            color=confidence_colors.get(confidence_level, "secondary")
        )

        evidence_quality = result.get("evidence_quality", "Limited")
        evidence_colors = {"Strong": "success", "Moderate": "info", "Limited": "secondary"}
        evidence_badge = dbc.Badge(
            evidence_quality,
            color=evidence_colors.get(evidence_quality, "secondary")
        )

        table_rows.append(
            html.Tr([
                html.Td(result.get("incident_id", "N/A")),
                html.Td(result.get("facility", "N/A")),
                html.Td(
                    html.Div(result.get("effective_action", "")[:60] + "..."
                            if len(result.get("effective_action", "")) > 60
                            else result.get("effective_action", "")),
                    style={"whiteSpace": "normal", "wordBreak": "break-word"},
                ),
                html.Td(
                    html.Div(result.get("why_effective", "No explanation provided")[:50] + "..."
                            if len(result.get("why_effective", "")) > 50
                            else result.get("why_effective", "No explanation provided")),
                    style={"whiteSpace": "normal", "wordBreak": "break-word"},
                ),
                html.Td(str(result.get("usage_frequency", 0))),
                html.Td([confidence_badge, html.Br(), evidence_badge]),
            ])
        )

    return html.Div([
        *export_info,
        html.H5(f"Proven Effective Actions ({len(results)} found)", className="text-success mb-3"),
        dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Action Request"),
                    html.Th("Facility"),
                    html.Th("Effective Action"),
                    html.Th("Why It Works"),
                    html.Th("Usage Count"),
                    html.Th("Quality")
                ])
            ]),
            html.Tbody(table_rows),
        ], striped=True, hover=True, responsive=True, size="sm"),
    ])


def create_solutions_table_with_export_info(results: List[Dict[str, Any]], export_path: str = None) -> html.Div:
    """Solutions table with export info"""
    if not results:
        return dbc.Alert("No solution precedents found for these keywords", color="warning")

    # Export notification
    export_info = []
    if export_path:
        export_info = [
            dbc.Alert([
                html.I(className="fas fa-download me-2"),
                f"Results exported to: {export_path.split('/')[-1]}"
            ], color="success", className="mb-3")
        ]

    # Create table rows
    table_rows = []
    for result in results[:10]:
        confidence_level = result.get("confidence_level", "Low")
        confidence_colors = {"High": "success", "Medium": "warning", "Low": "secondary"}
        confidence_badge = dbc.Badge(
            confidence_level,
            color=confidence_colors.get(confidence_level, "secondary")
        )

        table_rows.append(
            html.Tr([
                html.Td(result.get("incident_id", "N/A")),
                html.Td(result.get("facility", "N/A")),
                html.Td(
                    html.Div(result.get("problem_description", "")[:50] + "..."
                            if len(result.get("problem_description", "")) > 50
                            else result.get("problem_description", "")),
                    style={"whiteSpace": "normal", "wordBreak": "break-word"},
                ),
                html.Td(
                    html.Div(result.get("proven_solution", "")[:50] + "..."
                            if len(result.get("proven_solution", "")) > 50
                            else result.get("proven_solution", "")),
                    style={"whiteSpace": "normal", "wordBreak": "break-word"},
                ),
                html.Td(confidence_badge),
            ])
        )

    return html.Div([
        *export_info,
        html.H5(f"Solution Precedents ({len(results)} found)", className="text-primary mb-3"),
        dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Action Request"),
                    html.Th("Facility"),
                    html.Th("Problem Description"),
                    html.Th("Proven Solution"),
                    html.Th("Confidence"),
                ])
            ]),
            html.Tbody(table_rows),
        ], striped=True, hover=True, responsive=True, size="sm"),
    ])


def create_expertise_table_with_export_info(results: List[Dict[str, Any]], export_path: str = None) -> html.Div:
    """Expertise table with export info"""
    if not results:
        return dbc.Alert("No department expertise data found", color="warning")

    # Export notification
    export_info = []
    if export_path:
        export_info = [
            dbc.Alert([
                html.I(className="fas fa-download me-2"),
                f"Results exported to: {export_path.split('/')[-1]}"
            ], color="success", className="mb-3")
        ]

    # Create table rows
    table_rows = []
    for result in results[:10]:
        success_rate = result.get("success_rate", 0)
        badge_color = (
            "success" if success_rate >= 80 else "warning" if success_rate >= 60 else "secondary"
        )

        table_rows.append(
            html.Tr([
                html.Td(result.get("initiating_department", "N/A")),
                html.Td(result.get("receiving_department", "N/A")),
                html.Td(result.get("facility", "N/A")),
                html.Td(result.get("location", "N/A")),
                html.Td(
                    f"{result.get('successful_resolutions', 0)}/{result.get('contamination_cases', 0)}"
                ),
                html.Td(html.Span(f"{success_rate}%", className=f"badge bg-{badge_color}")),
            ])
        )

    return html.Div([
        *export_info,
        html.H5(f"Expert Departments ({len(results)} found)", className="text-info mb-3"),
        dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Initiating Dept"),
                    html.Th("Receiving Dept"),
                    html.Th("Facility"),
                    html.Th("Location"),
                    html.Th("Success Record"),
                    html.Th("Success Rate"),
                ])
            ]),
            html.Tbody(table_rows),
        ], striped=True, hover=True, responsive=True, size="sm"),
    ])


def create_timeline_table_with_export_info(results: List[Dict[str, Any]], export_path: str = None) -> html.Div:
    """Timeline table with export info"""
    if not results:
        return dbc.Alert("No timeline data found for these repairs", color="warning")

    # Export notification
    export_info = []
    if export_path:
        export_info = [
            dbc.Alert([
                html.I(className="fas fa-download me-2"),
                f"Results exported to: {export_path.split('/')[-1]}"
            ], color="success", className="mb-3")
        ]

    # Create table rows
    table_rows = []
    for result in results[:10]:
        avg_days = result.get("average_days", 0)
        badge_color = "success" if avg_days <= 3 else "warning" if avg_days <= 7 else "danger"

        table_rows.append(
            html.Tr([
                html.Td(result.get("incident_id", "N/A")),
                html.Td(result.get("facility", "N/A")),
                html.Td(
                    html.Div(result.get("repair_type", "N/A")[:40] + "..."
                            if len(result.get("repair_type", "")) > 40
                            else result.get("repair_type", "N/A")),
                    style={"whiteSpace": "normal", "wordBreak": "break-word"},
                ),
                html.Td(html.Span(f"{avg_days:.1f} days", className=f"badge bg-{badge_color}")),
                html.Td(f"{result.get('fastest_completion', 0)} days"),
                html.Td(f"{result.get('longest_completion', 0)} days"),
                html.Td(result.get("repair_instances", 0)),
                html.Td(f"{result.get('average_planned_days', 0):.1f} days"),
            ])
        )

    return html.Div([
        *export_info,
        html.H5(f"Timeline Analysis ({len(results)} repair types)", className="text-warning mb-3"),
        dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Action Request"),
                    html.Th("Facility"),
                    html.Th("Repair Type"),
                    html.Th("Avg Duration"),
                    html.Th("Fastest"),
                    html.Th("Longest"),
                    html.Th("Instances"),
                    html.Th("Planned Avg"),
                ])
            ]),
            html.Tbody(table_rows),
        ], striped=True, hover=True, responsive=True, size="sm"),
    ])


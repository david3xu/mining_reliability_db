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
    """Complete stakeholder journey interface with single input and five outputs"""

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Complete Stakeholder Journey", className="mb-3"),
                    html.P("Single input → Five automatic answers for complete incident investigation",
                           className="text-muted mb-3"),

                    # Single input interface
                    dbc.InputGroup(
                        [
                            dbc.Input(
                                id="stakeholder-journey-input",
                                placeholder="Describe your incident: excavator motor contamination...",
                                className="form-control-lg"
                            ),
                            dbc.Button("Start Complete Journey", id="journey-search-btn",
                                     color="primary", size="lg", className="me-2"),
                            dbc.Button("Export Results", id="journey-export-btn",
                                     color="secondary", outline=True, disabled=True)
                        ],
                        className="mb-4"
                    ),

                    # Journey status and results
                    html.Div(id="journey-status", className="mb-3"),
                    html.Div(id="journey-results-container"),
                ]
            )
        ],
        className="mb-4"
    )

def create_complete_stakeholder_journey():
    """Complete stakeholder journey interface with single input and five outputs"""

    return dbc.Card([
        dbc.CardBody([
            html.H4("Complete Stakeholder Journey", className="mb-3"),
            html.P("Single input → Five automatic answers for complete incident investigation",
                   className="text-muted mb-3"),

            # Single input interface
            dbc.InputGroup([
                dbc.Input(
                    id="stakeholder-journey-input",
                    placeholder="Describe your incident: excavator motor contamination...",
                    className="form-control-lg"
                ),
                dbc.Button("Start Complete Journey", id="journey-search-btn",
                         color="primary", size="lg", className="me-2"),
                dbc.Button("Export Results", id="journey-export-btn",
                         color="secondary", outline=True, disabled=True)
            ], className="mb-4"),

            # Journey status and results
            html.Div(id="journey-status", className="mb-3"),
            html.Div(id="journey-results-container"),
        ])
    ], className="mb-4")

def create_journey_results_display(journey_data: Dict[str, Any]) -> html.Div:
    """Create display for complete journey results"""

    if not journey_data or not journey_data.get("metadata", {}).get("success"):
        return html.Div([
            dbc.Alert("No results found or search failed. Please try different keywords.",
                     color="warning")
        ], className="mt-3")

    metadata = journey_data.get("metadata", {})
    results_sections = []

    # Journey header
    journey_header = dbc.Row([
        dbc.Col([
            html.H5(f"Journey Results for: '{metadata.get('user_input', 'N/A')}'"),
            html.P(f"Keywords: {', '.join(metadata.get('keywords_used', []))}",
                   className="text-muted"),
            html.P(f"Total Results: {metadata.get('total_results', 0)}",
                   className="text-success fw-bold")
        ])
    ], className="mb-4")

    results_sections.append(journey_header)

    # Five journey questions
    journey_questions = [
        ("why_did_this_happen", "🔍 Why did this happen?", "danger"),
        ("how_do_i_figure_out_whats_wrong", "🔬 How do I figure out what's wrong?", "warning"),
        ("who_can_help_me", "👥 Who can help me?", "info"),
        ("what_should_i_check_first", "📋 What should I check first?", "primary"),
        ("how_do_i_fix_it", "🔧 How do I fix it?", "success")
    ]

    for question_key, question_title, color in journey_questions:
        section_data = journey_data.get(question_key, {})
        section_results = section_data.get("results", [])
        section_count = section_data.get("count", 0)

        # Create table content for results
        table_content = []

        if section_count > 0 and section_results:
            # Determine table structure based on question type
            if question_key == "why_did_this_happen":
                table_content = [create_why_table(section_results)]
            elif question_key == "how_do_i_figure_out_whats_wrong":
                table_content = [create_investigation_table(section_results)]
            elif question_key == "who_can_help_me":
                table_content = [create_experts_table(section_results)]
            elif question_key == "what_should_i_check_first":
                table_content = [create_checklist_table(section_results)]
            elif question_key == "how_do_i_fix_it":
                table_content = [create_solutions_table(section_results)]
            else:
                table_content = [create_generic_table(section_results)]
        else:
            table_content = [
                dbc.Alert("No historical data found for this question type.",
                         color="light", className="mb-0")
            ]

        # Create section card
        section_card = dbc.Card([
            dbc.CardHeader([
                html.H6(f"{question_title}", className=f"text-{color} mb-0"),
                dbc.Badge(f"{section_count} results", color=color, className="ms-auto")
            ], className="d-flex justify-content-between align-items-center"),
            dbc.CardBody(table_content)
        ], className="mb-3")

        results_sections.append(section_card)

    return html.Div(results_sections)

def create_why_table(results: List[Dict]) -> dbc.Table:
    """Create table for 'Why did this happen?' results"""
    headers = ["Action Request", "Facility", "Root Cause", "Frequency", "Success Rate"]

    # Filter out results with None or empty root causes and symptoms
    valid_results = [
        result for result in results
        if (result.get("identified_root_cause") is not None and str(result.get("identified_root_cause", "")).strip() != "") or
           (result.get("similar_symptoms") is not None and str(result.get("similar_symptoms", "")).strip() != "")
    ]

    rows = []
    for result in valid_results[:10]:  # Limit to top 10
        # Use multiple possible field names for root cause
        root_cause = (result.get("identified_root_cause") or
                     result.get("root_cause") or
                     result.get("similar_symptoms") or "N/A")
        root_cause = str(root_cause)
        if len(root_cause) > 60:
            root_cause = root_cause[:60] + "..."

        # Extract action request and facility
        action_request = result.get("action_request_id") or result.get("incident_id") or "N/A"
        facility = result.get("facility") or result.get("facilities") or result.get("operating_centre") or "N/A"

        rows.append(html.Tr([
            html.Td(action_request),
            html.Td(facility),
            html.Td(root_cause),
            html.Td(result.get("pattern_frequency") or result.get("frequency", 0)),
            html.Td(f"{result.get('success_rate', 0)}%")
        ]))

    return dbc.Table([
        html.Thead([html.Tr([html.Th(h) for h in headers])]),
        html.Tbody(rows)
    ], striped=True, hover=True, responsive=True, size="sm")

def create_investigation_table(results: List[Dict]) -> dbc.Table:
    """Create table for investigation approaches"""
    headers = ["Action Request", "Facility", "Investigation Approach", "Success Cases", "Effectiveness"]

    # Filter out results with None or empty investigation data
    valid_results = [
        result for result in results
        if (result.get("symptoms") is not None and str(result.get("symptoms", "")).strip() != "") or
           (result.get("identified_cause") is not None and str(result.get("identified_cause", "")).strip() != "") or
           (result.get("evidence_found") is not None and str(result.get("evidence_found", "")).strip() != "")
    ]

    rows = []
    for result in valid_results[:10]:
        # Use symptoms or identified cause as investigation approach
        approach = (result.get("symptoms") or
                   result.get("identified_cause") or
                   result.get("evidence_found") or "N/A")
        approach = str(approach)
        if len(approach) > 50:
            approach = approach[:50] + "..."

        # Extract action request and facility
        action_request = result.get("action_request_id") or result.get("incident_id") or "N/A"
        facility = result.get("facility") or result.get("facilities") or result.get("operating_centre") or "N/A"

        rows.append(html.Tr([
            html.Td(action_request),
            html.Td(facility),
            html.Td(approach),
            html.Td(result.get("success_cases", 1)),
            html.Td(f"{result.get('effectiveness_rate', 100)}%")
        ]))

    return dbc.Table([
        html.Thead([html.Tr([html.Th(h) for h in headers])]),
        html.Tbody(rows)
    ], striped=True, hover=True, responsive=True, size="sm")

def create_experts_table(results: List[Dict]) -> dbc.Table:
    """Create table for expert departments"""
    headers = ["Action Request", "Facility", "Department", "Location", "Success Rate", "Expertise Areas"]

    # Filter out results with None or empty department information
    valid_results = [
        result for result in results
        if (result.get("initiating_department") is not None and str(result.get("initiating_department", "")).strip() != "") or
           (result.get("receiving_department") is not None and str(result.get("receiving_department", "")).strip() != "")
    ]

    rows = []
    for result in valid_results[:10]:
        # Extract action request and facility
        action_request = result.get("action_request_id") or result.get("incident_id") or "N/A"
        facility = result.get("facility") or result.get("facilities") or result.get("operating_centre") or "N/A"

        init_dept = result.get('initiating_department', 'N/A')
        rec_dept = result.get('receiving_department', 'N/A')
        department_flow = f"{init_dept} → {rec_dept}"

        expertise_list = result.get("expertise_areas", [])
        if isinstance(expertise_list, list) and expertise_list:
            expertise = ", ".join(expertise_list[:2])
        else:
            expertise = "N/A"

        if len(expertise) > 50:
            expertise = expertise[:50] + "..."

        rows.append(html.Tr([
            html.Td(action_request),
            html.Td(facility),
            html.Td(department_flow),
            html.Td(result.get("location", "N/A")),
            html.Td(f"{result.get('success_rate', 0)}%"),
            html.Td(expertise)
        ]))

    return dbc.Table([
        html.Thead([html.Tr([html.Th(h) for h in headers])]),
        html.Tbody(rows)
    ], striped=True, hover=True, responsive=True, size="sm")

def create_checklist_table(results: List[Dict]) -> dbc.Table:
    """Create table for prioritized investigation steps"""
    headers = ["Action Request", "Facility", "Priority", "Investigation Step", "Success Rate", "Time to Resolution"]

    # Filter out results with None or empty investigation steps
    valid_results = [
        result for result in results
        if result.get("investigation_step") is not None and str(result.get("investigation_step", "")).strip() != "" and len(str(result.get("investigation_step", ""))) > 10
    ]

    rows = []
    for i, result in enumerate(valid_results[:10], 1):
        # Extract action request and facility
        action_request = result.get("action_request_id") or result.get("incident_id") or "N/A"
        facility = result.get("facility") or result.get("facilities") or result.get("operating_centre") or "N/A"

        step = str(result.get("investigation_step", "N/A"))
        if len(step) > 70:
            step = step[:70] + "..."

        # Calculate estimated success rate from frequency and available data
        frequency = result.get("step_frequency", 1)
        success_rate = min(frequency * 20, 100)  # Rough estimate based on frequency

        rows.append(html.Tr([
            html.Td(action_request),
            html.Td(facility),
            html.Td(dbc.Badge(str(i), color="primary")),
            html.Td(step),
            html.Td(f"{success_rate}%"),
            html.Td(f"{result.get('avg_resolution_days', 'Variable')} days")
        ]))

    return dbc.Table([
        html.Thead([html.Tr([html.Th(h) for h in headers])]),
        html.Tbody(rows)
    ], striped=True, hover=True, responsive=True, size="sm")

def create_solutions_table(results: List[Dict]) -> dbc.Table:
    """Create table for proven solutions"""
    headers = ["Action Request", "Facility", "Solution", "Effectiveness", "Implementation", "Verification"]

    # Filter out results with None or empty solutions
    valid_results = [
        result for result in results
        if (result.get("proven_solution") is not None and str(result.get("proven_solution", "")).strip() != "") or
           (result.get("similar_symptoms") is not None and str(result.get("similar_symptoms", "")).strip() != "") or
           (result.get("root_cause_addressed") is not None and str(result.get("root_cause_addressed", "")).strip() != "")
    ]

    rows = []
    for result in valid_results[:10]:
        # Extract action request and facility
        action_request = result.get("action_request_id") or result.get("incident_id") or "N/A"
        facility = result.get("facility") or result.get("facilities") or result.get("operating_centre") or "N/A"

        # Use proven solution, or fall back to root cause addressed
        solution = (result.get("proven_solution") or
                   result.get("root_cause_addressed") or
                   result.get("similar_symptoms") or "N/A")
        solution = str(solution)
        if len(solution) > 60:
            solution = solution[:60] + "..."

        # Determine verification status
        has_proof = result.get("effectiveness_proof") is not None
        has_timeline = result.get("solution_timeline") is not None
        verification = "Yes" if (has_proof or has_timeline) else "Pending"

        verification_badge = (
            dbc.Badge("Verified", color="success") if verification == "Yes"
            else dbc.Badge("Pending", color="warning")
        )

        rows.append(html.Tr([
            html.Td(action_request),
            html.Td(facility),
            html.Td(solution),
            html.Td(f"{result.get('effectiveness_rate', 85)}%"),
            html.Td(result.get("implementation_complexity") or result.get("facility", "Standard")),
            html.Td(verification_badge)
        ]))

    return dbc.Table([
        html.Thead([html.Tr([html.Th(h) for h in headers])]),
        html.Tbody(rows)
    ], striped=True, hover=True, responsive=True, size="sm")

def create_generic_table(results: List[Dict]) -> dbc.Table:
    """Create generic table for unknown result types"""
    if not results:
        return html.Div("No results available")

    # Filter out completely empty results (where all values are None)
    valid_results = [
        result for result in results
        if any(value is not None and str(value).strip() != "" for value in result.values())
    ]

    if not valid_results:
        return html.Div("No valid results available")

    # Get all unique keys from all results
    all_keys = set()
    for result in valid_results:
        all_keys.update(result.keys())

    headers = list(all_keys)[:5]  # Limit to 5 columns

    rows = []
    for result in valid_results[:10]:
        row_cells = []
        for header in headers:
            value = str(result.get(header, "N/A"))
            # Truncate long values
            if len(value) > 50:
                value = value[:50] + "..."
            row_cells.append(html.Td(value))
        rows.append(html.Tr(row_cells))

    return dbc.Table([
        html.Thead([html.Tr([html.Th(h) for h in headers])]),
        html.Tbody(rows)
    ], striped=True, hover=True, responsive=True, size="sm")

def create_solutions_table_old(results: List[Dict[str, Any]]) -> html.Div:
    """Create table for proven solutions (legacy version)"""
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


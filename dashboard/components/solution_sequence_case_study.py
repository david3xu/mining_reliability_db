#!/usr/bin/env python3
"""
Solution Sequence Case Study Component
Demonstrates knowledge graph intelligence for engineering decision support.
"""

import logging
from typing import Any, Dict

import dash_bootstrap_components as dbc
from dash import html

from dashboard.adapters import get_data_adapter, handle_error_utility
from dashboard.components.layout_template import create_standard_layout
from dashboard.utils.styling import get_colors

logger = logging.getLogger(__name__)

__all__ = ["create_solution_sequence_case_study_layout"]


def create_solution_sequence_case_study_layout() -> html.Div:
    """Create solution sequence intelligence case study page"""
    try:
        data_adapter = get_data_adapter()
        case_study_data = data_adapter.get_solution_sequence_case_study()

        if "error" in case_study_data:
            return create_error_layout(case_study_data["error"])

        return create_standard_layout(
            title="Case Study: Solution Sequence Intelligence",
            content_cards=[
                create_case_study_header(case_study_data),
                create_approach_comparison(case_study_data),
                create_solution_sequence_detail(case_study_data),
                create_business_value_summary(),
            ],
        )

    except Exception as e:
        handle_error_utility(logger, e, "solution sequence case study layout")
        return create_error_layout("Case study unavailable")


def create_case_study_header(case_data: Dict[str, Any]) -> html.Div:
    """Create case study header with key details for multiple sequences"""
    colors = get_colors()

    # Handle both old single sequence format and new multiple sequences format
    solution_sequences = case_data.get("solution_sequences", [])
    action_request_number = case_data.get("action_request_number", "Unknown")
    total_sequences = case_data.get("total_sequences", 0)

    # Get facility from first sequence if available
    facility = "Unknown"
    if solution_sequences:
        facility = solution_sequences[0].get("facility", "Unknown")

    # Calculate total actions across all sequences
    total_actions = sum(seq.get("total_actions", 0) for seq in solution_sequences)

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2(
                                f"Case Study: Action Request {action_request_number}",
                                style={
                                    "color": colors.get("primary_color"),
                                    "marginBottom": "20px",
                                },
                            ),
                            html.P(
                                f"Action Request: {action_request_number}",
                                style={
                                    "fontSize": "16px",
                                    "fontWeight": "bold",
                                    "color": colors.get("text_primary"),
                                },
                            ),
                            html.P(
                                f"Facility: {facility}",
                                style={"fontSize": "16px", "color": colors.get("text_secondary")},
                            ),
                            html.P(
                                f"Solution Sequences: {total_sequences}",
                                style={"fontSize": "16px", "color": colors.get("info_color")},
                            ),
                            html.P(
                                f"Total Action Steps: {total_actions}",
                                style={"fontSize": "16px", "color": colors.get("text_primary")},
                            ),
                        ]
                    )
                ]
            )
        ],
        style={
            "backgroundColor": colors.get("background_secondary"),
            "padding": "20px",
            "borderRadius": "8px",
            "marginBottom": "20px",
        },
    )


def create_approach_comparison(case_data: Dict[str, Any]) -> html.Div:
    """Create traditional vs knowledge graph comparison using actual root cause data"""
    colors = get_colors()

    # Extract root cause tail extraction from the first sequence
    problem_text = "problem"  # Default fallback
    solution_sequences = case_data.get("solution_sequences", [])
    if solution_sequences:
        root_cause_tail = solution_sequences[0].get("root_cause_tail_extraction", "")
        if root_cause_tail and root_cause_tail.strip():
            problem_text = root_cause_tail.strip()
        else:
            # Fallback to regular root cause if tail extraction is not available
            root_cause = solution_sequences[0].get("root_cause", "")
            if root_cause and root_cause.strip():
                problem_text = root_cause.strip()

    traditional_box = dbc.Card(
        [
            dbc.CardHeader(html.H4("Traditional Approach", style={"margin": "0"})),
            dbc.CardBody(
                [
                    html.P(f"Engineer faces {problem_text}"),
                    html.Ul(
                        [
                            html.Li("❓ Which solution first?"),
                            html.Li("❓ Will it work?"),
                            html.Li("❓ What's next if it fails?"),
                        ]
                    ),
                    html.P(
                        "Trial and error approach", style={"fontWeight": "bold", "color": "#dc3545"}
                    ),
                ]
            ),
        ],
        color="warning",
        outline=True,
    )

    knowledge_graph_box = dbc.Card(
        [
            dbc.CardHeader(html.H4("Knowledge Graph Approach", style={"margin": "0"})),
            dbc.CardBody(
                [
                    html.P("Engineer queries historical solutions"),
                    html.Ul(
                        [
                            html.Li("✓ Proven solution sequence", style={"color": "#28a745"}),
                            html.Li("✓ All steps verified effective", style={"color": "#28a745"}),
                            html.Li("✓ Immediate implementation", style={"color": "#28a745"}),
                        ]
                    ),
                    html.P(
                        "Systematic solution intelligence",
                        style={"fontWeight": "bold", "color": "#28a745"},
                    ),
                ]
            ),
        ],
        color="info",
        outline=True,
    )

    return html.Div(
        [
            html.H3("Approach Comparison", style={"marginBottom": "20px"}),
            dbc.Row(
                [
                    dbc.Col(traditional_box, md=5),
                    dbc.Col(
                        html.Div(
                            "→",
                            style={
                                "fontSize": "4rem",
                                "textAlign": "center",
                                "color": colors["accent"],
                                "lineHeight": "200px",
                            },
                        ),
                        md=2,
                    ),
                    dbc.Col(knowledge_graph_box, md=5),
                ]
            ),
        ],
        style={"marginBottom": "30px"},
    )


def create_solution_sequence_detail(case_data: Dict[str, Any]) -> html.Div:
    """Create detailed solution sequence display for multiple sequences"""
    colors = get_colors()

    # Handle both old single sequence format and new multiple sequences format
    solution_sequences = case_data.get("solution_sequences", [])
    if not solution_sequences and "action_sequence" in case_data:
        # Backward compatibility: convert old format to new format
        solution_sequences = [
            {
                "action_title": case_data.get("action_title", "Unknown"),
                "problem": case_data.get("problem", ""),
                "root_cause": case_data.get("root_cause", ""),
                "action_sequence": case_data.get("action_sequence", []),
            }
        ]

    all_sequence_cards = []

    for seq_idx, sequence in enumerate(solution_sequences, 1):
        # Create header for each sequence
        sequence_header = html.Div(
            [
                html.H4(
                    f"Sequence {seq_idx}: {sequence.get('action_title', 'Unknown Title')}",
                    style={"color": colors["primary"], "marginBottom": "10px"},
                ),
                html.P(
                    f"Problem: {sequence.get('problem', 'N/A')}",
                    style={
                        "fontSize": "14px",
                        "color": colors["text_secondary"],
                        "marginBottom": "5px",
                    },
                ),
                html.P(
                    f"Root Cause: {sequence.get('root_cause', 'N/A')}",
                    style={
                        "fontSize": "14px",
                        "color": colors["text_secondary"],
                        "marginBottom": "15px",
                    },
                ),
            ]
        )

        # Create action cards for this sequence
        action_cards = []
        for i, action in enumerate(sequence.get("action_sequence", []), 1):
            # Determine effectiveness status
            effectiveness = action.get("verification_status", "N/A")
            if effectiveness == "Yes":
                effectiveness_text = "Effective"
                effectiveness_color = "#28a745"
            elif effectiveness == "No":
                effectiveness_text = "Not Effective"
                effectiveness_color = "#dc3545"
            else:
                effectiveness_text = "N/A"
                effectiveness_color = colors["text_secondary"]

            action_card = dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        str(i),
                                        style={
                                            "backgroundColor": colors["primary"],
                                            "color": "white",
                                            "borderRadius": "50%",
                                            "width": "30px",
                                            "height": "30px",
                                            "display": "inline-flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "fontWeight": "bold",
                                            "marginRight": "15px",
                                        },
                                    ),
                                    html.Span(
                                        action.get("action_description", ""),
                                        style={"fontWeight": "bold", "fontSize": "16px"},
                                    ),
                                ]
                            ),
                            html.P(
                                f"Due: {action.get('due_date', 'N/A')} | Complete: {action.get('complete', 'N/A')}",
                                style={
                                    "margin": "5px 0 0 45px",
                                    "color": colors["text_secondary"],
                                    "fontSize": "14px",
                                },
                            ),
                            html.P(
                                f"Effectiveness: {effectiveness_text}",
                                style={
                                    "margin": "5px 0 0 45px",
                                    "color": effectiveness_color,
                                    "fontWeight": "bold",
                                },
                            ),
                        ]
                    )
                ],
                style={"marginBottom": "10px"},
            )
            action_cards.append(action_card)

        # Add sequence summary
        total_actions = len(sequence.get("action_sequence", []))
        effective_actions = sum(
            1
            for action in sequence.get("action_sequence", [])
            if action.get("verification_status") == "Yes"
        )

        if total_actions > 0:
            if effective_actions == total_actions:
                result_text = (
                    f"Result: All {total_actions} actions effective - Complete solution verified"
                )
                result_color = "#28a745"
            elif effective_actions > 0:
                result_text = f"Result: {effective_actions}/{total_actions} actions effective - Partial solution"
                result_color = "#ffc107"
            else:
                result_text = f"Result: No effective actions - Solution needs revision"
                result_color = "#dc3545"
        else:
            result_text = "Result: No actions defined"
            result_color = colors["text_secondary"]

        sequence_card = html.Div(
            [
                sequence_header,
                html.Div(action_cards),
                html.P(
                    result_text,
                    style={
                        "fontWeight": "bold",
                        "color": result_color,
                        "fontSize": "16px",
                        "marginTop": "15px",
                    },
                ),
            ],
            style={
                "backgroundColor": colors["card_background"],
                "padding": "20px",
                "borderRadius": "8px",
                "marginBottom": "20px",
                "border": f"1px solid {colors.get('border', '#dee2e6')}",
            },
        )

        all_sequence_cards.append(sequence_card)

    return html.Div(
        [
            html.H3(
                f"Solution Sequence Recipe ({len(solution_sequences)} sequences)",
                style={"marginBottom": "20px"},
            ),
            html.Div(all_sequence_cards),
        ]
    )


def create_business_value_summary() -> html.Div:
    """Create business value comparison"""
    colors = get_colors()

    return html.Div(
        [
            html.H3("Business Value", style={"marginBottom": "20px"}),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4("Before", style={"color": "#dc3545"}),
                            html.Ul(
                                [
                                    html.Li("Engineer guesses solution sequence"),
                                    html.Li("Multiple attempts to find what works"),
                                    html.Li("Extended downtime"),
                                    html.Li("Knowledge lost after resolution"),
                                ]
                            ),
                        ],
                        md=6,
                    ),
                    dbc.Col(
                        [
                            html.H4("After", style={"color": "#28a745"}),
                            html.Ul(
                                [
                                    html.Li("Engineer applies proven solution recipe"),
                                    html.Li("Immediate systematic implementation"),
                                    html.Li("Reduced resolution time"),
                                    html.Li(
                                        "Solution intelligence captured",
                                        style={"fontWeight": "bold", "color": "#28a745"},
                                    ),
                                ]
                            ),
                        ],
                        md=6,
                    ),
                ]
            ),
            html.Div(
                [
                    html.H4("Core Insight", style={"textAlign": "center", "marginTop": "30px"}),
                    html.P(
                        "Transform individual problem-solving into systematic solution intelligence",
                        style={
                            "fontSize": "18px",
                            "fontWeight": "bold",
                            "textAlign": "center",
                            "color": colors["primary"],
                        },
                    ),
                    html.P(
                        "Historical action sequences become proven implementation recipes",
                        style={"textAlign": "center", "fontSize": "16px"},
                    ),
                ],
                style={
                    "backgroundColor": "#e7f3ff",
                    "padding": "20px",
                    "borderRadius": "8px",
                    "marginTop": "20px",
                },
            ),
        ],
        style={
            "backgroundColor": colors["card_background"],
            "padding": "20px",
            "borderRadius": "8px",
        },
    )


def create_error_layout(error_message: str) -> html.Div:
    """Create error display layout"""
    return create_standard_layout(
        title="Case Study Error",
        content_cards=[
            html.Div([html.H4("Case Study Unavailable"), html.P(f"Error: {error_message}")])
        ],
    )

#!/usr/bin/env python3
"""
Atomized Workflow Analysis - Two-Tier Architecture
Core workflow stages + supporting entities with clean visual hierarchy.
"""

import logging
from typing import Any, Dict, List

import dash_bootstrap_components as dbc
from dash import dcc, html

# Pure adapter dependencies
from dashboard.adapters import get_workflow_adapter, handle_error_utility
from dashboard.components.interactive_elements import create_interactive_metric_card
from dashboard.components.layout_template import create_standard_layout
from dashboard.components.micro.chart_base import create_bar_chart
from dashboard.components.micro.metric_card import create_metric_card
from dashboard.components.micro.table_base import create_data_table
from dashboard.utils.styling import (
    get_chart_layout_template,
    get_colors,
    get_fonts,
    get_table_style,
)

logger = logging.getLogger(__name__)

__all__ = [
    "create_workflow_metrics",
    "create_workflow_analysis_layout",
    "create_core_workflow_section",
    "create_supporting_entities_section",
    "create_config_driven_stage_card",
    "create_supporting_entity_card",
    "create_core_workflow_section_comprehensive",
    "create_comprehensive_stage_card",
    "create_supporting_entities_section_comprehensive",
    "create_comprehensive_supporting_card",
]


def create_workflow_metrics() -> html.Div:
    """Pure workflow metrics - 15 lines"""
    try:
        adapter = get_workflow_adapter()
        colors = get_colors()
        schema_data = adapter.get_workflow_schema_analysis()
        mapping_data = adapter.get_field_mapping_counts()

        metrics = [
            create_metric_card(schema_data.total_entities, "Entity Types"),
            create_metric_card(mapping_data.total_fields, "Mapped Fields", False, None),
            create_metric_card(schema_data.analytical_dimensions, "Analysis Dimensions"),
            create_metric_card(schema_data.field_categories, "Field Categories"),
        ]

        return html.Div(
            [
                html.H3("Workflow Schema Analysis", className="text-center mb-4"),
                html.Div(metrics, className="d-flex justify-content-center gap-3"),
            ],
            style={
                "backgroundColor": colors.get("background_dark"),
                "color": colors.get("text_light"),
                "borderRadius": "8px",
                "padding": "20px",
            },
        )
    except Exception as e:
        handle_error_utility(logger, e, "workflow metrics creation")
        return _create_fallback_metrics()


def create_core_workflow_section() -> html.Div:
    """Pure adapter dependency - zero config access"""
    try:
        adapter = get_workflow_adapter()
        colors = get_colors()

        # Receive processed data from adapter
        workflow_stages = adapter.get_enriched_workflow_stages()

        if not workflow_stages:  # Check if data is available
            return _create_static_core_flow()

        # Create large stage cards using the new config-driven function
        stage_cards = []
        for stage in workflow_stages:
            card = create_config_driven_stage_card(stage)  # Pure rendering
            stage_cards.append(
                html.Div(card, className="d-inline-block")
            )  # Keep inline-block styling

        # Add flow arrows
        flow_elements = []
        for i, card in enumerate(stage_cards):
            flow_elements.append(card)
            if i < len(stage_cards) - 1:
                flow_elements.append(
                    html.Div(
                        [
                            html.I(
                                className="fas fa-arrow-right fa-2x",
                                style={"color": colors.get("primary_color"), "margin": "0 15px"},
                            )
                        ],
                        className="d-inline-block align-middle",
                    )
                )

        return html.Div(
            [
                html.H4(
                    "Core Workflow Process",
                    className="text-center mb-4",
                    style={"color": colors.get("text_light")},
                ),
                html.Div(
                    flow_elements,
                    className="d-flex justify-content-center align-items-center flex-wrap",
                ),
            ],
            style={
                "backgroundColor": colors.get("background_dark"),
                "color": colors.get("text_light"),
                "borderRadius": "8px",
                "padding": "30px",
                "marginBottom": "30px",
            },
        )

    except Exception as e:
        handle_error_utility(logger, e, "core workflow section creation")
        return _create_static_core_flow()


def create_supporting_entities_section() -> html.Div:
    """Config-driven supporting entities through adapter"""
    try:
        adapter = get_workflow_adapter()
        colors = get_colors()

        # Receive processed supporting entity data
        supporting_entities = adapter.get_enriched_supporting_entities()

        cards = []
        for entity in supporting_entities:
            card = create_supporting_entity_card(entity)  # Pure rendering
            cards.append(
                dbc.Col(card, width="auto", className="mb-2")
            )  # Retain dbc.Col and styling

        return html.Div(
            [
                html.H4(
                    "Supporting Data Context",
                    className="text-center mb-4",
                    style={"color": colors.get("text_light")},
                ),  # Retain styling
                dbc.Row(
                    cards, className="justify-content-center"
                ),  # Ensure no_gutters is gone, as I already removed it
            ],
            style={
                "backgroundColor": colors.get("background_dark"),
                "color": colors.get("text_light"),  # Retain styling
                "padding": "20px",
                "borderRadius": "8px",
            },
        )

    except Exception as e:
        handle_error_utility(logger, e, "supporting entities section creation")
        return html.Div(
            [
                html.H4("Supporting Data Context"),
                html.P("Supporting entities data unavailable"),  # More generic error
            ],
            style={"padding": "20px"},
        )


def create_config_driven_stage_card(stage_data: dict) -> html.Div:
    """Pure component with field count header and truncated names"""
    stage_number = stage_data.get("stage_number", 1)
    title = stage_data.get("title", "Unknown")
    field_count = stage_data.get("field_count", 0)
    field_names = stage_data.get("business_fields", [])
    completion_rate = stage_data.get("completion_rate", 0.0)
    color = stage_data.get("card_color", "#4A90E2")

    content = html.Div(
        [
            # Field count header
            html.P(
                f"{field_count} Fields",
                style={
                    "fontSize": "14px",
                    "fontWeight": "bold",
                    "margin": "10px 0 8px 0",
                    "textAlign": "center",
                },
            ),
            # Truncated field names list
            html.Div(
                [
                    html.P(
                        field,
                        style={
                            "fontSize": "11px",
                            "margin": "1px 0",
                            "opacity": "0.8",
                            "textAlign": "left",
                        },
                    )
                    for field in field_names
                ],
                style={"marginBottom": "15px"},
            ),
            # Completion percentage
            html.Div(
                [
                    html.Span(
                        f"{completion_rate:.1f}% Complete",
                        style={
                            "padding": "6px 12px",
                            "borderRadius": "12px",
                            "backgroundColor": "rgba(255,255,255,0.2)",
                            "fontSize": "12px",
                        },
                    )
                ],
                style={"textAlign": "center"},
            ),
        ],
        style={"padding": "15px"},
    )

    return html.Div(
        [
            html.Div(
                [
                    html.H5(f"STAGE {stage_number}", style={"fontSize": "16px", "margin": "0"}),
                    html.H3(title, style={"fontSize": "18px", "margin": "8px 0"}),
                ],
                style={"backgroundColor": color, "color": "#FFFFFF", "padding": "12px"},
            ),
            content,
        ],
        style={
            "backgroundColor": color,
            "color": "#FFFFFF",
            "borderRadius": "8px",
            "minHeight": "400px",
            "width": "220px",
            "margin": "10px",
        },
    )


def create_supporting_entity_card(entity_data: dict) -> dbc.Card:
    """Supporting card with completion percentage"""
    name = entity_data.get("name")
    field_count = entity_data.get("field_count")
    completion_rate = entity_data.get("completion_rate", 0.0)
    fields = entity_data.get("fields", [])

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6(name, style={"fontSize": "12px", "fontWeight": "bold"}),
                    html.P(f"{field_count} Fields", style={"fontSize": "10px", "color": "#666"}),
                    html.P(
                        f"{completion_rate:.1f}% Complete",
                        style={"fontSize": "10px", "color": "#007bff"},
                    ),
                    html.Div(
                        [
                            html.P(
                                field[:30] + "..." if len(field) > 30 else field,
                                style={"fontSize": "9px", "margin": "1px 0"},
                            )
                            for field in fields[:3]  # Show first 3 fields
                        ]
                    ),
                ]
            )
        ],
        style={"minHeight": "100px", "backgroundColor": "#F8F9FA"},
    )


def create_workflow_analysis_layout() -> html.Div:
    """Updated layout with comprehensive completion analysis"""
    return create_standard_layout(
        title="Workflow Analysis",
        content_cards=[
            create_workflow_metrics(),
            create_core_workflow_section_comprehensive(),
            create_supporting_entities_section_comprehensive(),
            _create_instruction_section(),
        ],
    )


# Helper Functions


def _create_fallback_metrics() -> html.Div:
    """Fallback metrics when data unavailable"""
    return html.Div(
        [
            html.H3("Workflow Analysis", className="text-center mb-4"),
            html.P("Initializing workflow intelligence...", className="text-center"),
            html.Div(
                [
                    create_metric_card(5, "Core Stages"),
                    create_metric_card(41, "Expected Fields"),
                    create_metric_card(4, "Analysis Types"),
                    create_metric_card(5, "Field Categories"),
                ],
                className="d-flex justify-content-center gap-3",
            ),
        ],
        style={"padding": "20px"},
    )


def _create_static_core_flow() -> html.Div:
    """Fallback core workflow when data unavailable"""
    colors = get_colors()
    static_stages = [
        {
            "stage_number": 1,
            "title": "Incident Reporting",
            "field_count": 10,
            "color": "#4A90E2",
            "entity_name": "ActionRequest",
            "business_fields": [
                "Action Request Number:",
                "Title",
                "Initiation Date",
                "Action Types",
                "Categories",
                "Requested Response Time",
                "Past Due Status",
                "Days Past Due",
                "Operating Centre",
                "Stage",
            ],
        },
        {
            "stage_number": 2,
            "title": "Problem Definition",
            "field_count": 2,
            "color": "#F5A623",
            "entity_name": "Problem",
            "business_fields": ["What happened?", "Requirement"],
        },
        {
            "stage_number": 3,
            "title": "Causal Analysis",
            "field_count": 3,
            "color": "#7ED321",
            "entity_name": "RootCause",
            "business_fields": ["Root Cause", "Obj. Evidence", "Root Cause (tail extraction)"],
        },
        {
            "stage_number": 4,
            "title": "Resolution Planning",
            "field_count": 11,
            "color": "#B57EDC",
            "entity_name": "ActionPlan",
            "business_fields": [
                "Action Plan",
                "Recom.Action",
                "Immd. Contain. Action or Comments",
                "Due Date",
                "Complete",
                "Completion Date",
                "Comments",
                "Response Date",
                "Response Revision Date",
                "Did this action plan require a change to the equipment management strategy ?",
                "If yes, are there any corrective actions to update the strategy in APSS, eAM, ASM and BOM as required ?",
            ],
        },
        {
            "stage_number": 5,
            "title": "Effectiveness Check",
            "field_count": 4,
            "color": "#D32F2F",
            "entity_name": "Verification",
            "business_fields": [
                "Effectiveness Verification Due Date",
                "IsActionPlanEffective",
                "Action Plan Eval Comment",
                "Action Plan Verification Date:",
            ],
        },
    ]

    stage_cards = [
        create_config_driven_stage_card(stage) for stage in static_stages
    ]  # Changed to create_config_driven_stage_card

    flow_elements = []
    for i, card in enumerate(stage_cards):
        flow_elements.append(html.Div(card, className="d-inline-block"))
        if i < len(stage_cards) - 1:
            flow_elements.append(
                html.Div(
                    [
                        html.I(
                            className="fas fa-arrow-right fa-2x",
                            style={"color": get_colors().get("primary_color"), "margin": "0 15px"},
                        )
                    ],
                    className="d-inline-block align-middle",
                )
            )

    return html.Div(
        [
            html.H4("Core Workflow Process", className="text-center mb-4"),
            html.Div(
                flow_elements,
                className="d-flex justify-content-center align-items-center flex-wrap",
            ),
        ],
        style={
            "backgroundColor": colors.get("background_dark"),
            "padding": "30px",
            "borderRadius": "8px",
            "marginBottom": "30px",
        },
    )


def _create_instruction_section() -> html.Div:
    """User guidance section"""
    colors = get_colors()
    return html.Div(
        [
            html.P(
                "Core stages show incident workflow progression. Supporting entities provide operational context.",
                className="text-center text-muted mt-4 fst-italic",
            )
        ],
        style={
            "backgroundColor": colors.get("background_dark"),
            "padding": "20px",
            "borderRadius": "8px",
        },
    )


def create_core_workflow_section_comprehensive() -> html.Div:
    """Core workflow section with comprehensive completion data"""
    try:
        adapter = get_workflow_adapter()
        colors = get_colors()

        # Get comprehensive workflow data from adapter
        workflow_stages = adapter.get_enriched_workflow_stages_comprehensive()

        if not workflow_stages:
            return _create_static_core_flow()

        stage_cards = []
        for stage in workflow_stages:
            card = create_comprehensive_stage_card(stage)
            stage_cards.append(html.Div(card, className="d-inline-block"))

        # Add flow arrows
        flow_elements = []
        for i, card in enumerate(stage_cards):
            flow_elements.append(card)
            if i < len(stage_cards) - 1:
                flow_elements.append(
                    html.Div(
                        [
                            html.I(
                                className="fas fa-arrow-right fa-2x",
                                style={"color": colors.get("primary_color"), "margin": "0 15px"},
                            )
                        ],
                        className="d-inline-block align-middle",
                    )
                )

        return html.Div(
            [
                html.H4("Core Workflow Process", className="text-center mb-4"),
                html.Div(
                    flow_elements,
                    className="d-flex justify-content-center align-items-center flex-wrap",
                ),
            ],
            style={
                "backgroundColor": colors.get("background_dark"),
                "padding": "30px",
                "borderRadius": "8px",
                "marginBottom": "30px",
            },
        )

    except Exception as e:
        handle_error_utility(logger, e, "comprehensive core workflow section")
        return _create_static_core_flow()


def create_comprehensive_stage_card(stage_data: dict) -> html.Div:
    """Stage card with comprehensive 41-field completion analysis"""
    stage_number = stage_data.get("stage_number", 1)
    title = stage_data.get("title", "Unknown")
    field_count = stage_data.get("actual_field_count", 0)
    field_names = stage_data.get("business_fields", [])
    completion_rate = stage_data.get("completion_rate", 0.0)
    color = stage_data.get("dynamic_color", "#4A90E2")

    # Truncate field names for display
    display_fields = []
    for field in field_names:
        if len(field) > 35:
            display_fields.append(field[:32] + "...")
        else:
            display_fields.append(field)

    content = html.Div(
        [
            # Field count header
            html.P(
                f"{field_count} Fields",
                style={
                    "fontSize": "14px",
                    "fontWeight": "bold",
                    "margin": "10px 0 8px 0",
                    "textAlign": "center",
                },
            ),
            # Field names (show first 8)
            html.Div(
                [
                    html.P(
                        field,
                        style={
                            "fontSize": "11px",
                            "margin": "1px 0",
                            "opacity": "0.8",
                            "textAlign": "left",
                        },
                    )
                    for field in display_fields[:8]
                ]
                + (
                    [
                        html.P(
                            f"... +{len(display_fields)-8} more",
                            style={"fontSize": "10px", "fontStyle": "italic"},
                        )
                    ]
                    if len(display_fields) > 8
                    else []
                ),
                style={"marginBottom": "15px"},
            ),
            # Comprehensive completion percentage
            html.Div(
                [
                    html.Span(
                        f"{completion_rate:.1f}% Complete",
                        style={
                            "padding": "6px 12px",
                            "borderRadius": "12px",
                            "backgroundColor": "rgba(255,255,255,0.2)",
                            "fontSize": "12px",
                        },
                    )
                ],
                style={"textAlign": "center"},
            ),
        ],
        style={"padding": "15px"},
    )

    return html.Div(
        [
            html.Div(
                [
                    html.H5(f"STAGE {stage_number}", style={"fontSize": "16px", "margin": "0"}),
                    html.H3(title, style={"fontSize": "18px", "margin": "8px 0"}),
                ],
                style={"backgroundColor": "rgba(0,0,0,0.3)", "padding": "12px"},
            ),
            content,
        ],
        style={
            "backgroundColor": color,
            "color": "#FFFFFF",
            "borderRadius": "8px",
            "minHeight": "400px",
            "width": "220px",
            "margin": "10px",
        },
    )


def create_supporting_entities_section_comprehensive() -> html.Div:
    """Supporting entities with comprehensive completion"""
    try:
        adapter = get_workflow_adapter()
        colors = get_colors()

        # Get comprehensive supporting data from adapter
        supporting_entities = adapter.get_enriched_supporting_entities_comprehensive()

        cards = []
        for entity in supporting_entities:
            card = create_comprehensive_supporting_card(entity)
            cards.append(dbc.Col(card, width="auto"))

        return html.Div(
            [
                html.H4("Supporting Data Context", className="text-center mb-4"),
                dbc.Row(cards, className="justify-content-center"),
            ],
            style={
                "backgroundColor": colors.get("background_dark"),
                "padding": "20px",
                "borderRadius": "8px",
            },
        )

    except Exception as e:
        handle_error_utility(logger, e, "comprehensive supporting entities")
        return html.Div("Supporting entities unavailable")


def create_comprehensive_supporting_card(entity_data: dict) -> dbc.Card:
    """Supporting card with comprehensive field completion"""
    name = entity_data.get("name")
    field_count = entity_data.get("field_count")
    completion_rate = entity_data.get("completion_rate", 0.0)
    fields = entity_data.get("fields", [])
    color = entity_data.get("dynamic_color", "#F8F9FA")  # Use dynamic color

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6(name, style={"fontSize": "12px", "fontWeight": "bold"}),
                    html.P(f"{field_count} Fields", style={"fontSize": "10px", "color": "#666"}),
                    html.P(
                        f"{completion_rate:.1f}% Complete",
                        style={"fontSize": "10px", "color": "#007bff"},
                    ),
                    html.Div(
                        [
                            html.P(
                                field[:30] + "..." if len(field) > 30 else field,
                                style={"fontSize": "9px", "margin": "1px 0"},
                            )
                            for field in fields[:3]
                        ]
                    ),
                ]
            )
        ],
        style={"minHeight": "100px", "backgroundColor": color},
    )

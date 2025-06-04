#!/usr/bin/env python3
"""
Stakeholder Questions Component - Professional Question Display System
Card-based layout with adaptive styling for systematic question organization.
"""

import logging
from typing import Any, Dict, List, Optional

import dash_bootstrap_components as dbc
from dash import html

from dashboard.adapters import get_config_adapter
from dashboard.components.layout_template import create_metric_card, create_standard_layout
from dashboard.utils.styling import get_colors, get_dashboard_styles

logger = logging.getLogger(__name__)

__all__ = [
    "create_stakeholder_questions_overview",
    "create_question_category_card",
    "create_question_detail_view",
    "create_questions_navigation",
    "get_question_category_metrics"
]


def create_question_category_card(
    category_id: str,
    category_name: str,
    questions: List[Dict],
    show_details: bool = False
) -> dbc.Card:
    """Create a professional card for a question category"""
    config_adapter = get_config_adapter()
    colors = get_colors()

    # Category color mapping for visual distinction
    category_colors = {
        "tech_impact": "#4A90E2",        # Blue - Strategic
        "operational_trends": "#50C878",  # Green - Operational
        "data_quality": "#E74C3C",       # Red - Critical
        "workflow_understanding": "#9B59B6", # Purple - Process
        "record_structure": "#F39C12",    # Orange - Architecture
        "category_classification": "#1ABC9C", # Teal - Analysis
        "field_relationships": "#95A5A6"  # Gray - Technical
    }

    card_color = category_colors.get(category_id, colors.get("primary"))
    question_count = len(questions)

    # Card header with metrics
    header_content = [
        html.Div([
            html.H4(category_name, className="text-white mb-1",
                   style={"fontWeight": "600", "fontSize": "18px"}),
            html.Div([
                html.Span(f"{question_count} Questions",
                         className="badge bg-light text-dark me-2"),
                html.Span("Pending Analysis",
                         className="badge bg-warning text-dark")
            ])
        ], className="d-flex justify-content-between align-items-start")
    ]

    # Question list - always show all questions
    question_items = []
    for i, question in enumerate(questions, 1):
        if show_details:
            # Detailed view with styling
            question_items.append(
                html.Div([
                    html.Strong(f"Q{i}: ", className="text-primary"),
                    html.Span(question.get("question_text", ""), className="text-muted")
                ], className="mb-2 p-2 bg-light rounded")
            )
        else:
            # Compact view - all questions listed
            question_items.append(
                html.Div([
                    html.Strong(f"Q{i}: ", className="text-primary me-1"),
                    html.Span(question.get("question_text", ""), className="text-muted")
                ], className="mb-2")
            )

    body_content = question_items

    return dbc.Card([
        dbc.CardHeader(header_content, style={"backgroundColor": card_color}),
        dbc.CardBody(body_content, style={"minHeight": "120px"})
    ], className="mb-3 shadow-sm", style={"borderLeft": f"4px solid {card_color}"})


def create_questions_grid(categories: List[Dict]) -> html.Div:
    """Create responsive grid of question category cards"""
    rows = []

    # Group categories into rows of 2-3 cards
    for i in range(0, len(categories), 3):
        category_batch = categories[i:i+3]
        cols = []

        for category in category_batch:
            col_width = 12 // len(category_batch) if len(category_batch) <= 2 else 4
            cols.append(
                dbc.Col([
                    create_question_category_card(
                        category.get("category_id", ""),
                        category.get("category_name", ""),
                        category.get("questions", [])
                    )
                ], width=col_width, className="mb-3")
            )

        rows.append(dbc.Row(cols))

    return html.Div(rows)


def create_stakeholder_questions_overview(questions_data: Dict) -> html.Div:
    """Main overview page for stakeholder questions"""
    categories = questions_data.get("question_categories", [])

    # Calculate summary metrics
    total_questions = sum(len(cat.get("questions", [])) for cat in categories)
    total_categories = len(categories)

    # Priority distribution (you can enhance this based on your data)
    high_priority_cats = ["tech_impact", "operational_trends", "workflow_understanding"]
    high_priority_count = sum(1 for cat in categories
                             if cat.get("category_id") in high_priority_cats)

    # Header metrics
    metrics_row = dbc.Row([
        dbc.Col([
            create_metric_card(total_questions, "Total Questions", "Across all categories")
        ], width=3),
        dbc.Col([
            create_metric_card(total_categories, "Question Categories", "Strategic areas")
        ], width=3),
        dbc.Col([
            create_metric_card(high_priority_count, "High Priority", "Categories requiring immediate attention")
        ], width=3),
        dbc.Col([
            create_metric_card("0", "Completed", "Analysis progress")
        ], width=3),
    ], className="mb-4")

    # Category grid
    categories_section = html.Div([
        html.H3("Question Categories", className="mb-3"),
        create_questions_grid(categories)
    ])

    return create_standard_layout(
        title="Stakeholder Questions Overview",
        content_cards=[metrics_row, categories_section]
    )


def create_question_detail_view(category_data: Dict) -> html.Div:
    """Detailed view for a specific question category"""
    category_name = category_data.get("category_name", "")
    questions = category_data.get("questions", [])

    # Detailed question cards
    question_cards = []
    for i, question in enumerate(questions, 1):
        question_card = dbc.Card([
            dbc.CardHeader([
                html.H5(f"Question {question.get('question_id', f'Q{i}')}",
                       className="mb-0 text-primary")
            ]),
            dbc.CardBody([
                html.P(question.get("question_text", ""),
                      className="lead mb-3"),
                html.Div([
                    dbc.Badge("Pending Analysis", color="warning", className="me-2"),
                    dbc.Badge("High Priority", color="info", className="me-2"),
                ]),
                html.Hr(),
                html.Div([
                    dbc.Button("Begin Analysis", color="primary", size="sm", className="me-2"),
                    dbc.Button("Add Notes", color="outline-secondary", size="sm", className="me-2"),
                    dbc.Button("Share", color="outline-info", size="sm")
                ])
            ])
        ], className="mb-3")
        question_cards.append(question_card)

    return create_standard_layout(
        title=category_name,
        content_cards=question_cards
    )


def get_question_category_metrics(questions_data: Dict) -> Dict[str, Any]:
    """Calculate metrics for question categories"""
    categories = questions_data.get("question_categories", [])

    return {
        "total_questions": sum(len(cat.get("questions", [])) for cat in categories),
        "total_categories": len(categories),
        "categories_by_priority": {
            "high": len([c for c in categories if c.get("category_id") in
                        ["tech_impact", "operational_trends", "workflow_understanding"]]),
            "medium": len([c for c in categories if c.get("category_id") in
                          ["record_structure", "category_classification", "field_relationships"]]),
            "critical": len([c for c in categories if c.get("category_id") in ["data_quality"]])
        },
        "completion_status": {
            "pending": len(categories),  # All pending for now
            "in_progress": 0,
            "completed": 0
        }
    }

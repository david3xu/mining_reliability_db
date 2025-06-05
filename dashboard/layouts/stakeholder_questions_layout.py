#!/usr/bin/env python3
"""
Stakeholder Questions Layout - Professional Question Management Interface
Systematic display and organization of stakeholder analysis questions.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

from dash import html

from dashboard.adapters import get_config_adapter
from dashboard.components.stakeholder_questions import (
    create_question_detail_view,
    create_stakeholder_questions_overview,
    get_question_category_metrics,
)
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

__all__ = ["create_stakeholder_questions_layout", "load_stakeholder_questions_data"]


def load_stakeholder_questions_data() -> Dict[str, Any]:
    """Load stakeholder questions from configuration"""
    try:
        config_adapter = get_config_adapter()

        # Load stakeholder questions schema using relative path
        project_root = Path(__file__).parent.parent.parent
        config_file = project_root / "configs" / "stakeholder_questions_schema.json"

        with open(config_file, "r") as f:
            questions_data = json.load(f)

        return questions_data

    except Exception as e:
        handle_error(logger, e, "loading stakeholder questions data")
        return {"question_categories": [], "error": "Failed to load stakeholder questions data"}


def create_stakeholder_questions_layout(category_id: str = None) -> html.Div:
    """Create stakeholder questions layout with optional category focus"""
    try:
        questions_data = load_stakeholder_questions_data()

        if "error" in questions_data:
            return html.Div(
                [
                    html.H2("Stakeholder Questions", className="text-danger"),
                    html.P("Error loading stakeholder questions data.", className="text-muted"),
                ]
            )

        if category_id:
            # Show detailed view for specific category
            categories = questions_data.get("question_categories", [])
            category_data = next(
                (cat for cat in categories if cat.get("category_id") == category_id), None
            )

            if category_data:
                return create_question_detail_view(category_data)
            else:
                return html.Div(
                    [
                        html.H2("Category Not Found", className="text-warning"),
                        html.P(f"Category '{category_id}' not found.", className="text-muted"),
                    ]
                )
        else:
            # Show overview of all categories
            return create_stakeholder_questions_overview(questions_data)

    except Exception as e:
        handle_error(logger, e, "creating stakeholder questions layout")
        return html.Div(
            [
                html.H2("Error", className="text-danger"),
                html.P("Failed to create stakeholder questions layout.", className="text-muted"),
            ]
        )


# Category metadata for enhanced display
CATEGORY_METADATA = {
    "tech_impact": {
        "icon": "🔧",
        "priority": "high",
        "description": "Analyze technological changes and equipment impacts",
        "stakeholders": ["Operations Management", "Maintenance Engineering", "Technology Planning"],
    },
    "operational_trends": {
        "icon": "📈",
        "priority": "high",
        "description": "Investigate operational patterns and business changes",
        "stakeholders": ["Operations Management", "Business Strategy", "Data Governance"],
    },
    "data_quality": {
        "icon": "🎯",
        "priority": "critical",
        "description": "Ensure data sampling and representativeness accuracy",
        "stakeholders": ["Data Science", "Analytics Team", "Quality Assurance"],
    },
    "workflow_understanding": {
        "icon": "🔄",
        "priority": "high",
        "description": "Map workflow progression and process documentation",
        "stakeholders": ["Process Owners", "Workflow Management", "Training Teams"],
    },
    "record_structure": {
        "icon": "🗂️",
        "priority": "medium",
        "description": "Understand record patterns and data architecture",
        "stakeholders": ["Data Architects", "Business Analysts", "System Designers"],
    },
    "category_classification": {
        "icon": "🏷️",
        "priority": "medium",
        "description": "Define categorization systems and classification accuracy",
        "stakeholders": ["Subject Matter Experts", "Data Governance", "Classification Specialists"],
    },
    "field_relationships": {
        "icon": "🔗",
        "priority": "medium",
        "description": "Analyze field interactions and data consistency",
        "stakeholders": ["Data Architects", "Workflow Designers", "Quality Assurance"],
    },
}

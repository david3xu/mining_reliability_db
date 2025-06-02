#!/usr/bin/env python3
"""
Atomized Workflow Analysis - Pure Adapter Dependencies
Micro-component composition for workflow intelligence with zero config coupling.
"""

import logging

import dash_bootstrap_components as dbc
from dash import dcc, html

# Pure adapter dependencies
from dashboard.adapters import get_workflow_adapter
from dashboard.components.micro.chart_base import create_bar_chart
from dashboard.components.micro.metric_card import create_metric_card
from dashboard.components.micro.table_base import create_data_table
from dashboard.components.micro.workflow_stage import create_workflow_stage_card
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


def create_workflow_metrics() -> html.Div:
    """Pure workflow metrics - 15 lines"""
    try:
        adapter = get_workflow_adapter()
        schema_data = adapter.get_workflow_schema_analysis()
        mapping_data = adapter.get_field_mapping_counts()

        metrics = [
            create_metric_card(schema_data.get("total_entities", 0), "Entity Types"),
            create_metric_card(
                mapping_data.get("total_fields", 0), "Mapped Fields", True, "/workflow-process"
            ),
            create_metric_card(schema_data.get("analytical_dimensions", 0), "Analysis Dimensions"),
            create_metric_card(schema_data.get("field_categories", 0), "Field Categories"),
        ]

        return html.Div(
            [
                html.H3("Workflow Schema Analysis", className="text-center mb-4"),
                html.Div(metrics, className="d-flex justify-content-center gap-3"),
            ]
        )
    except Exception as e:
        handle_error(logger, e, "workflow metrics creation")
        return html.Div("Workflow metrics unavailable")


def create_process_flow() -> html.Div:
    """Pure process flow diagram - 18 lines"""
    try:
        adapter = get_workflow_adapter()
        workflow_data = adapter.get_workflow_business_analysis_neo4j()

        if not workflow_data.get("workflow_stages"):
            return html.Div("Workflow stages unavailable")

        # Create stage cards
        stage_cards = []
        for stage in workflow_data["workflow_stages"]:
            stage_cards.append(create_workflow_stage_card(stage))

        # Add arrows between stages
        flow_elements = []
        for i, card in enumerate(stage_cards):
            flow_elements.append(html.Div(card, className="col-md"))
            if i < len(stage_cards) - 1:
                flow_elements.append(
                    html.Div(
                        [html.I(className="fas fa-arrow-right fa-2x text-primary")],
                        className="col-auto d-flex align-items-center",
                    )
                )

        return html.Div(
            [
                html.H5("Workflow Process Flow", className="text-center mb-4"),
                html.Div(flow_elements, className="row align-items-center"),
            ]
        )
    except Exception as e:
        handle_error(logger, e, "process flow creation")
        return html.Div("Process flow unavailable")


def create_entity_distribution_chart() -> dcc.Graph:
    """Pure entity distribution chart - 10 lines"""
    try:
        adapter = get_workflow_adapter()
        entity_data = adapter.get_entity_field_distribution()

        if not entity_data.get("entity_names"):
            return dcc.Graph(figure={})

        return create_bar_chart(
            entity_data["entity_names"], entity_data["field_counts"], "Entity Field Distribution"
        )
    except Exception as e:
        handle_error(logger, e, "entity distribution chart creation")
        return dcc.Graph(figure={})


def create_mapping_table() -> any:
    """Pure mapping analysis table - 12 lines"""
    try:
        adapter = get_workflow_adapter()
        mapping_data = adapter.get_field_mapping_analysis()

        if not mapping_data.get("mappings"):
            return html.Div("Mapping data unavailable")

        # Transform for table display
        table_data = [
            {
                "Entity": m["entity"],
                "Target Field": m["target_field"],
                "Source Field": m["source_field"],
                "Category": m["category"],
                "Critical": "Yes" if m["critical"] else "No",
            }
            for m in mapping_data["mappings"]
        ]

        return create_data_table(
            table_data, ["Entity", "Target Field", "Source Field", "Category", "Critical"]
        )
    except Exception as e:
        handle_error(logger, e, "mapping table creation")
        return html.Div("Mapping table unavailable")


def create_workflow_analysis_layout() -> html.Div:
    """Main workflow layout - 20 lines"""
    try:
        adapter = get_workflow_adapter()
        validation = adapter.validate_workflow_data()

        if not validation.get("workflow_schema", False):
            return dbc.Alert("Workflow data unavailable", color="warning")

        return html.Div(
            [
                create_workflow_metrics(),
                html.Div(
                    [
                        html.P(
                            "Click cards to explore detailed workflow analysis",
                            className="text-center text-muted my-4",
                        )
                    ]
                ),
                dbc.Row([dbc.Col([create_entity_distribution_chart()], md=12)]),
            ],
            className="container-fluid p-4",
        )
    except Exception as e:
        handle_error(logger, e, "workflow analysis layout creation")
        return dbc.Alert("Workflow analysis failed", color="danger")


def create_workflow_process_page() -> html.Div:
    """Dedicated workflow process page - 25 lines"""
    try:
        return html.Div(
            [
                dbc.Container(
                    [
                        dbc.Button(
                            "← Back to Workflow",
                            href="/workflow",
                            color="secondary",
                            size="sm",
                            className="mb-3",
                        ),
                        html.H2("Workflow Process Analysis", className="text-primary mb-4"),
                        # Process flow section
                        html.Div([create_process_flow()], className="mb-5"),
                        # Analysis sections
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5("Entity Distribution", className="mb-3"),
                                        create_entity_distribution_chart(),
                                    ],
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        html.H5("Field Mapping Details", className="mb-3"),
                                        create_mapping_table(),
                                    ],
                                    md=6,
                                ),
                            ]
                        ),
                    ],
                    fluid=True,
                )
            ],
            className="p-4",
        )
    except Exception as e:
        handle_error(logger, e, "workflow process page creation")
        return dbc.Alert("Workflow process page unavailable", color="danger")


# Legacy compatibility functions
def create_workflow_metrics_cards() -> html.Div:
    """Legacy compatibility"""
    return create_workflow_metrics()


def create_process_flow_diagram() -> html.Div:
    """Legacy compatibility"""
    return create_process_flow()


def create_stage_field_distribution() -> dcc.Graph:
    """Legacy compatibility"""
    return create_entity_distribution_chart()


def create_workflow_mapping_table() -> any:
    """Legacy compatibility"""
    return create_mapping_table()

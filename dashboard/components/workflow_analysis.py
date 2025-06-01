#!/usr/bin/env python3
"""
Workflow Understanding Component - Real Schema-Driven Implementation
Uses actual field mappings and entity definitions from configuration.
"""

import logging
from dash import dcc, html, dash_table
import plotly.graph_objects as go
from dashboard.components.layout_template import create_standard_layout, create_metric_card
from mine_core.shared.common import handle_error

# Real schema and configuration sources
from configs.environment import get_mappings, get_schema, get_entity_names
from mine_core.database.queries import get_root_cause_intelligence_summary, get_facilities

logger = logging.getLogger(__name__)

def create_workflow_metrics_cards() -> list:
    """Generate workflow metrics using real schema and data"""

    try:
        # Real schema data
        schema = get_schema()
        mappings = get_mappings()
        entity_names = get_entity_names()

        # Real field mapping counts
        entity_mappings = mappings.get("entity_mappings", {})
        total_fields = sum(len(fields) for fields in entity_mappings.values())

        # Real entity count from schema
        entities_count = len(entity_names)

        # Real analytical dimensions
        analytical_dimensions = schema.get("analytical_dimensions", {})

        cards = [
            create_metric_card(
                value=entities_count,
                label="Entity Types",
                detail="Schema-defined entities",
                color="#4A90E2"
            ),
            create_metric_card(
                value=total_fields,
                label="Mapped Fields",
                detail="Across all entities",
                color="#F5A623"
            ),
            create_metric_card(
                value=f"{len(analytical_dimensions)}",
                label="Analysis Dimensions",
                detail="Schema-driven analytics",
                color="#7ED321"
            ),
            create_metric_card(
                value=f"{len(mappings.get('field_categories', {}))}",
                label="Field Categories",
                detail="Classification types",
                color="#B57EDC"
            )
        ]

        return cards

    except Exception as e:
        handle_error(logger, e, "workflow metrics cards creation")
        return []

def create_process_flow_diagram() -> html.Div:
    """Create workflow visualization using real entity schema"""

    try:
        # Real entity order from schema
        schema = get_schema()
        entities = schema.get("entities", [])

        # Core workflow entities in order
        workflow_entities = [
            {"name": "ActionRequest", "title": "Incident Reporting", "stage": 1},
            {"name": "Problem", "title": "Problem Definition", "stage": 2},
            {"name": "RootCause", "title": "Causal Analysis", "stage": 3},
            {"name": "ActionPlan", "title": "Resolution Planning", "stage": 4},
            {"name": "Verification", "title": "Effectiveness Check", "stage": 5}
        ]

        # Get real entity definitions
        entity_dict = {e["name"]: e for e in entities}

        stage_boxes = []
        for workflow_entity in workflow_entities:
            entity_name = workflow_entity["name"]
            entity_def = entity_dict.get(entity_name, {})

            # Real field count from schema
            properties = entity_def.get("properties", {})
            field_count = len(properties)

            # Real required fields
            required_fields = sum(1 for prop in properties.values()
                                if prop.get("required", False))

            # Color based on field complexity
            if field_count >= 8:
                color = "#D0021B"  # Complex
            elif field_count >= 5:
                color = "#F5A623"  # Moderate
            else:
                color = "#7ED321"  # Simple

            stage_box = html.Div([
                html.Div([
                    html.H6(f"STAGE {workflow_entity['stage']}",
                           className="text-white mb-1"),
                    html.H5(entity_name, className="text-white mb-2"),
                    html.Hr(className="border-white"),
                    html.P(workflow_entity["title"],
                          className="text-white small mb-2"),
                    html.P(f"{field_count} Fields ({required_fields} required)",
                          className="text-white small mb-0")
                ], className="p-3 text-center")
            ],
            className="rounded shadow-sm mb-3",
            style={
                "backgroundColor": color,
                "minHeight": "150px",
                "display": "flex",
                "alignItems": "center"
            })

            stage_boxes.append(stage_box)

        # Create flow with arrows
        flow_elements = []
        for i, stage_box in enumerate(stage_boxes):
            flow_elements.append(
                html.Div([stage_box], className="col-md")
            )

            # Add arrow between stages (except last)
            if i < len(stage_boxes) - 1:
                flow_elements.append(
                    html.Div([
                        html.I(className="fas fa-arrow-right fa-2x text-primary")
                    ], className="col-auto d-flex align-items-center")
                )

        return html.Div([
            html.H5("Schema-Driven Workflow Process", className="text-center mb-4"),
            html.Div(flow_elements, className="row align-items-center")
        ])

    except Exception as e:
        handle_error(logger, e, "process flow diagram creation")
        return html.Div([html.P("Process flow diagram unavailable")])

def create_entity_field_distribution() -> dcc.Graph:
    """Entity field distribution using real schema data"""

    try:
        # Real schema data
        schema = get_schema()
        entities = schema.get("entities", [])

        if not entities:
            return dcc.Graph(figure={})

        entity_names = []
        field_counts = []
        required_counts = []

        for entity in entities:
            entity_name = entity["name"]
            properties = entity.get("properties", {})

            field_count = len(properties)
            required_count = sum(1 for prop in properties.values()
                               if prop.get("required", False))

            entity_names.append(entity_name)
            field_counts.append(field_count)
            required_counts.append(required_count)

        fig = go.Figure()

        # Total fields bar
        fig.add_trace(go.Bar(
            x=entity_names,
            y=field_counts,
            name="Total Fields",
            marker_color="#4A90E2",
            text=field_counts,
            textposition="outside"
        ))

        # Required fields bar
        fig.add_trace(go.Bar(
            x=entity_names,
            y=required_counts,
            name="Required Fields",
            marker_color="#D0021B",
            text=required_counts,
            textposition="inside"
        ))

        fig.update_layout(
            title="Entity Field Distribution - Real Schema Analysis",
            xaxis_title="Entity Type",
            yaxis_title="Number of Fields",
            height=400,
            barmode='overlay',
            showlegend=True,
            legend=dict(x=0.02, y=0.98),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        # Rotate x-axis labels for readability
        fig.update_xaxes(tickangle=-45)

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, "entity field distribution creation")
        return dcc.Graph(figure={})

def create_field_mapping_table() -> dash_table.DataTable:
    """Field mapping table using real configuration data"""

    try:
        # Real field mappings
        mappings = get_mappings()
        entity_mappings = mappings.get("entity_mappings", {})
        field_categories = mappings.get("field_categories", {})

        if not entity_mappings:
            return dash_table.DataTable(data=[])

        # Build field category lookup
        category_lookup = {}
        for category, fields in field_categories.items():
            for field in fields:
                category_lookup[field] = category.replace("_fields", "").title()

        table_data = []
        for entity_name, field_mapping in entity_mappings.items():
            for target_field, source_field in field_mapping.items():

                # Determine field category
                field_category = category_lookup.get(source_field, "General")

                # Determine if critical based on field name patterns
                critical_patterns = ["number", "id", "cause", "plan", "date"]
                is_critical = any(pattern in target_field.lower()
                                for pattern in critical_patterns)

                table_data.append({
                    "Entity": entity_name,
                    "Target Field": target_field,
                    "Source Field": source_field,
                    "Category": field_category,
                    "Critical": "Yes" if is_critical else "No"
                })

        return dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "Entity", "id": "Entity"},
                {"name": "Target Field", "id": "Target Field"},
                {"name": "Source Field", "id": "Source Field"},
                {"name": "Category", "id": "Category"},
                {"name": "Critical", "id": "Critical"}
            ],
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#4A90E2', 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': 'white'},
            style_data_conditional=[
                {
                    'if': {'filter_query': '{Critical} = Yes'},
                    'backgroundColor': '#FFF3CD',
                    'color': 'black'
                }
            ],
            sort_action="native",
            filter_action="native",
            page_size=15
        )

    except Exception as e:
        handle_error(logger, e, "field mapping table creation")
        return dash_table.DataTable(data=[])

def create_workflow_analysis_layout() -> html.Div:
    """Complete workflow analysis using real schema data"""

    try:
        return create_standard_layout(
            tab_id="workflow",
            metric_cards=create_workflow_metrics_cards(),
            left_component=create_process_flow_diagram(),
            right_component=create_entity_field_distribution(),
            summary_component=create_field_mapping_table(),
            summary_title="Schema-Driven Field Mapping Analysis"
        )

    except Exception as e:
        handle_error(logger, e, "workflow analysis layout creation")
        return html.Div([
            html.H3("Workflow Analysis Error"),
            html.P("Failed to load real workflow schema data")
        ])
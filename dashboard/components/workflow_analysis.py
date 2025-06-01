#!/usr/bin/env python3
"""
Workflow Understanding Component - Clean Adapter Pattern Implementation
Uses adapter layer for all data access, maintains separation of concerns.
"""

import logging
from typing import Dict, Any, List
from dash import dcc, html, dash_table
import plotly.graph_objects as go
from dashboard.components.layout_template import create_standard_layout, create_metric_card
from mine_core.shared.common import handle_error

# Clean adapter pattern - single point data access
from dashboard.adapters import get_data_adapter
from dashboard.utils.style_constants import (
    PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, WARNING_COLOR, DANGER_COLOR,
    HIGH_PRIORITY_BG, MEDIUM_PRIORITY_BG, LOW_PRIORITY_BG, LIGHT_BLUE
)

logger = logging.getLogger(__name__)

def create_workflow_metrics_cards() -> list:
    """Generate workflow metrics using adapter data access with clickable navigation"""

    try:
        # Clean adapter access
        adapter = get_data_adapter()
        workflow_data = adapter.get_workflow_schema_analysis()

        if not workflow_data:
            return []        # Real metrics from adapter
        entities_count = workflow_data.get("total_entities", 0)

        # Get field mapping counts using the adapter (clean architecture)
        mapping_data = adapter.get_field_mapping_counts()
        total_fields = mapping_data.get("total_fields", 0)

        analytical_dimensions = workflow_data.get("analytical_dimensions", 0)
        field_categories = workflow_data.get("field_categories", 0)

        # Create clean clickable metric card for mapped fields
        def create_clean_clickable_metric_card(value, label, detail, color, href=None):
            """Create clean metric card with optional click navigation"""

            display_value = f"{value:,}" if isinstance(value, int) and value > 999 else str(value)

            card_style = {
                "backgroundColor": color,
                "padding": "20px",
                "borderRadius": "8px",
                "textAlign": "center",
                "minWidth": "140px",
                "minHeight": "120px",
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
            }

            if href:
                card_style.update({
                    "cursor": "pointer",
                    "transition": "transform 0.2s ease, box-shadow 0.2s ease",
                    "textDecoration": "none"
                })
                hover_class = "metric-card-hover"
            else:
                hover_class = ""

            card_content = [
                html.H2(display_value, className="text-white mb-1",
                       style={"fontSize": "32px", "fontWeight": "bold"}),
                html.P(label, className="text-white mb-1",
                      style={"fontSize": "14px"}),
                html.Small(detail, className="text-white-50",
                          style={"fontSize": "12px"})
            ]

            if href:
                return html.A(card_content, href=href, style=card_style,
                             className=f"text-decoration-none {hover_class}")
            else:
                return html.Div(card_content, style=card_style)

        # Get styling configuration for consistent colors
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            colors = styling_config.get("chart_colors", [PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, DANGER_COLOR])
        except Exception:
            colors = [PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, DANGER_COLOR]

        cards = [
            create_metric_card(
                value=entities_count,
                label="Entity Types",
                detail="Schema-defined entities",
                color=colors[0]
            ),
            create_clean_clickable_metric_card(
                value=total_fields,
                label="Mapped Fields",
                detail="Click to explore process",
                color=colors[1],
                href="/workflow-process"
            ),
            create_metric_card(
                value=analytical_dimensions,
                label="Analysis Dimensions",
                detail="Schema-driven analytics",
                color=colors[2]
            ),
            create_metric_card(
                value=field_categories,
                label="Field Categories",
                detail="Classification types",
                color=colors[3]
            )
        ]

        return cards

    except Exception as e:
        handle_error(logger, e, "workflow metrics cards creation")
        return []

def create_process_flow_diagram() -> html.Div:
    """Create workflow visualization using adapter data access and configuration"""

    try:
        # Clean adapter access using the new Neo4j-driven method
        adapter = get_data_adapter()
        workflow_data = adapter.get_workflow_business_analysis_neo4j()

        if not workflow_data:
            return html.Div([html.P("Workflow data unavailable")])

        # Get global display configuration from workflow_stages.json
        display_config = workflow_data.get("display_config", {})

        # Get enriched workflow stages from adapter
        workflow_stages = workflow_data.get("workflow_stages", [])

        stage_boxes = []
        for stage in workflow_stages:
            # Create two-part card for each stage using our new function
            stage_box = create_two_part_stage_card(stage)

            stage_boxes.append(stage_box)

        # Create flow with arrows and stage titles
        flow_elements = []
        for i, stage in enumerate(workflow_stages):
            stage_title = stage.get("title", stage.get("entity_name", ""))
            stage_box = stage_boxes[i]

            # Create column with both the stage card and a title caption
            flow_elements.append(
                html.Div([
                    stage_box,
                    html.Div(
                        stage_title,
                        className="text-center mt-2 fw-bold",
                        style={"fontSize": display_config.get("font_sizes", {}).get("title", "16px")}
                    )
                ], className="col-md")
            )

            # Add arrow between stages (except last)
            if i < len(stage_boxes) - 1:
                flow_elements.append(
                    html.Div([
                        html.I(className="fas fa-arrow-right fa-2x text-primary")
                    ], className="col-auto d-flex align-items-center")
                )

        return html.Div([
            html.H4("Configuration-Driven Workflow Process",
                   className="text-center mb-4"),
            html.Div(flow_elements, className="row align-items-center")
        ])

    except Exception as e:
        handle_error(logger, e, "process flow diagram creation")
        return html.Div([html.P("Process flow diagram unavailable")])

def create_entity_field_distribution() -> dcc.Graph:
    """Entity field distribution using adapter data access"""

    try:
        # Clean adapter access
        adapter = get_data_adapter()
        entity_data = adapter.get_entity_field_distribution()

        if not entity_data:
            return dcc.Graph(figure={})

        entity_names = entity_data.get("entity_names", [])
        field_counts = entity_data.get("field_counts", [])

        if not entity_names:
            return dcc.Graph(figure={})

        fig = go.Figure()

        # Use configuration-driven styling
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            primary_color = styling_config.get("primary_color", PRIMARY_COLOR)
        except Exception:
            primary_color = PRIMARY_COLOR

        # Total fields bar
        fig.add_trace(go.Bar(
            x=entity_names,
            y=field_counts,
            name="Total Fields",
            marker_color=primary_color,
            text=field_counts,
            textposition="outside"
        ))

        fig.update_layout(
            title="Entity Field Distribution - Real Schema Analysis",
            xaxis_title="Entity Type",
            yaxis_title="Number of Fields",
            height=400,
            barmode='group',
            showlegend=False,
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
    """Field mapping table using adapter data access"""

    try:
        # Clean adapter access
        adapter = get_data_adapter()
        mapping_data = adapter.get_field_mapping_analysis()

        if not mapping_data:
            return dash_table.DataTable(data=[])

        mappings = mapping_data.get("mappings", [])

        if not mappings:
            return dash_table.DataTable(data=[])

        # Transform adapter data for table display
        table_data = []
        for mapping in mappings:
            table_data.append({
                "Entity": mapping["entity"],
                "Target Field": mapping["target_field"],
                "Source Field": mapping["source_field"],
                "Category": mapping["category"],
                "Critical": "Yes" if mapping["critical"] else "No"
            })

        # Use configuration-driven styling
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            primary_color = styling_config.get("primary_color", PRIMARY_COLOR)
        except Exception:
            primary_color = PRIMARY_COLOR

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
            style_header={'backgroundColor': primary_color, 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': 'white'},
            style_data_conditional=[
                {
                    'if': {'filter_query': '{Critical} = Yes'},
                    'backgroundColor': MEDIUM_PRIORITY_BG,
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

def create_workflow_process_page() -> html.Div:
    """Dedicated workflow process analysis page"""

    try:
        logger.info("Creating dedicated workflow process page")

        return html.Div([
            # Page header with navigation
            html.Div([
                html.Div([
                    html.A([
                        html.I(className="fas fa-arrow-left me-2"),
                        "Back to Workflow Overview"
                    ], href="/workflow", className="btn btn-outline-primary btn-sm"),
                    html.H3("Workflow Process Analysis", className="text-center mb-3 mt-3")
                ], className="col-12")
            ], className="row mb-4"),

            # Configuration summary
            html.Div([
                html.Div([
                    html.H4("Configuration Summary", className="mb-3"),
                    html.Div([
                        # JSON Source files
                        html.P([
                            html.Strong("Configuration Files: "),
                            "workflow_stages.json, entity_classification.json, entity_connections.json"
                        ], className="border-bottom pb-2"),

                        # Workflow stages info
                        html.P([
                            html.Strong("Workflow Stages: "),
                            html.Span(id="stages-count")
                        ]),
                        html.P([
                            html.Strong("Main Process Fields: "),
                            html.Span(id="fields-count")
                        ]),
                        html.P([
                            html.Strong("Main Process Completion: "),
                            html.Span(id="avg-completion")
                        ]),

                        # Supporting entities info
                        html.P([
                            html.Strong("Supporting Entities: "),
                            "7 (Facility, Department, Asset, etc.)"
                        ]),
                        html.P([
                            html.Strong("Architecture: "),
                            "Two-row layout with entity connections"
                        ])
                    ], className="p-3 bg-light rounded")
                ], className="col-12 mb-4")
            ], className="row"),

            # Process flow diagram (standard workflow stages only)
            html.Div([
                html.Div([
                    html.H5("Standard Workflow", className="mb-3"),
                    create_process_flow_diagram()
                ], className="col-12")
            ], className="row mb-4"),

            # Enhanced two-row visualization (workflow + supporting entities)
            html.Div([
                html.Div([
                    html.H5("Complete Entity Architecture", className="mb-3"),
                    create_complete_workflow_visualization()
                ], className="col-12")
            ], className="row mb-4"),

            # Entity distribution and field mapping side by side
            html.Div([
                html.Div([
                    html.H5("Entity Field Distribution", className="mb-3"),
                    create_entity_field_distribution()
                ], className="col-md-6"),
                html.Div([
                    html.H5("Field Mapping Details", className="mb-3"),
                    create_field_mapping_table()
                ], className="col-md-6")
            ], className="row")
        ], className="container-fluid p-4")

    except Exception as e:
        handle_error(logger, e, "workflow process page creation")
        return html.Div([
            html.H3("Workflow Process Error"),
            html.P("Failed to load workflow process analysis")
        ])

def create_workflow_analysis_layout() -> html.Div:
    """Clean workflow overview with clickable navigation to process details"""

    try:
        return html.Div([
            # Clean workflow metrics with clickable navigation
            html.Div([
                html.Div([
                    html.H3("Workflow Schema Analysis", className="text-center mb-4"),
                    html.P("Click cards to explore detailed analysis",
                          className="text-center text-muted mb-4")
                ], className="col-12")
            ], className="row mb-4"),

            # Workflow metrics cards
            html.Div([
                html.Div(create_workflow_metrics_cards(),
                        className="d-flex justify-content-center gap-3")
            ], className="row mb-4"),

            # High-level entity distribution (overview only)
            html.Div([
                html.Div([
                    html.H5("Entity Overview", className="mb-3"),
                    create_entity_field_distribution()
                ], className="col-12")
            ], className="row")
        ], className="container-fluid p-4")

    except Exception as e:
        handle_error(logger, e, "workflow analysis layout creation")
        return html.Div([
            html.H3("Workflow Analysis Error"),
            html.P("Failed to load workflow schema data through adapter")
        ])

# ALIAS FUNCTIONS (for compatibility with different naming conventions)
def create_stage_field_distribution() -> dcc.Graph:
    """Alias for create_entity_field_distribution"""
    return create_entity_field_distribution()

def create_workflow_mapping_table() -> dash_table.DataTable:
    """Alias for create_field_mapping_table"""
    return create_field_mapping_table()

def create_two_part_stage_card(stage_data: Dict[str, Any]) -> html.Div:
    """Configuration-driven two-section card: header + fields

    All display parameters come from workflow_stages.json configuration
    instead of being hardcoded in the component.
    """
    # Extract basic stage information
    entity_name = stage_data["entity_name"]
    stage_number = stage_data["stage_number"]
    source_fields = stage_data["source_fields"]
    completion_rate = stage_data["completion_rate"]

    # Get display title if available, otherwise fall back to entity name
    display_title = stage_data.get("title", entity_name)

    # Calculate unique field count to avoid counting duplicates
    unique_source_fields = list(dict.fromkeys(source_fields))
    field_count = len(unique_source_fields)

    # Use color from configuration with fallback
    color = stage_data.get("color", SUCCESS_COLOR)

    # Get display field limit from config with fallback
    max_fields_to_display = stage_data.get("max_fields_to_display", 6)

    # Format field text for display based on configuration
    if len(unique_source_fields) <= max_fields_to_display:
        field_text = ", ".join(unique_source_fields)
    else:
        shown_fields = unique_source_fields[:max_fields_to_display]
        remaining = len(unique_source_fields) - max_fields_to_display
        field_text = ", ".join(shown_fields) + f" + {remaining} more"

    # Get basic card display configurations
    card_min_height = stage_data.get("card_min_height", "300px")
    header_bg_opacity = stage_data.get("header_bg_opacity", 0.3)
    show_description = stage_data.get("show_description", False)
    description = stage_data.get("description", "")

    # Get adapter to access config
    adapter = get_data_adapter()
    workflow_config = adapter.get_workflow_business_analysis_neo4j()
    display_config = workflow_config.get("display_config", {})

    # Get font sizes from config
    font_sizes = display_config.get("font_sizes", {})
    stage_number_font_size = font_sizes.get("stage_number", "14px")
    title_font_size = font_sizes.get("title", "18px")

    # Build the header section with configurable styling
    header_section = html.Div([
        html.H6(f"STAGE {stage_number}",
                className="text-white mb-1",
                style={"fontSize": stage_number_font_size}),
        html.H4(display_title,
                className="text-white mb-0",
                style={"fontSize": title_font_size})
    ],
    className="p-2 text-center",
    style={"backgroundColor": f"rgba(0,0,0,{header_bg_opacity})", "borderRadius": "8px 8px 0 0"})

    # Get additional font sizes and styling from config
    field_count_font_size = font_sizes.get("field_count", "14px")
    field_list_font_size = font_sizes.get("field_list", "11px")
    description_font_size = font_sizes.get("description", "12px")

    # Get line height and other style parameters
    card_style = display_config.get("card_style", {})
    field_line_height = card_style.get("field_line_height", "1.3")
    completion_rate_padding = card_style.get("completion_rate_padding", "5px 10px")
    completion_rate_border_radius = card_style.get("completion_rate_border_radius", "10px")

    # Build the content section with configurable styling
    content_elements = [
        html.P(f"{field_count} Unique Fields:",
              className="text-white mb-2",
              style={"fontSize": field_count_font_size, "fontWeight": "bold"}),

        html.P(field_text,
              className="text-white",
              style={"fontSize": field_list_font_size, "lineHeight": field_line_height, "textAlign": "left"})
    ]

    # Add description if enabled in configuration
    if show_description and description:
        content_elements.insert(1, html.P(
            description,
            className="text-white mb-2 fst-italic",
            style={"fontSize": description_font_size}
        ))

    # Add completion rate badge with configurable styling
    content_elements.append(
        html.Div([
            html.Span(f"{completion_rate}% Data Completeness",
                      className="badge bg-light text-dark",
                      style={"padding": completion_rate_padding, "borderRadius": completion_rate_border_radius})
        ], className="mt-2")
    )

    # Assemble the card
    return html.Div([
        header_section,
        html.Div(content_elements, className="p-3")
    ],
    className="rounded shadow-sm mb-3",
    style={
        "backgroundColor": color,
        "minHeight": card_min_height,
        "display": "flex",
        "flexDirection": "column"
    })

def create_supporting_entity_card(entity_data: Dict[str, Any], connection_config: Dict[str, Any]) -> html.Div:
    """Create supporting entity card for second row of workflow visualization"""

    # Extract basic entity information
    entity_name = entity_data["entity_name"]
    field_count = entity_data["field_count"]
    completion_rate = entity_data["completion_rate"]
    connects_to = entity_data["connects_to"]
    color = entity_data.get("color", LIGHT_BLUE)

    # Get height from config with fallback
    card_height = f"{entity_data.get('card_height', 120)}px"

    # Get connection display config
    connection_symbol = connection_config.get("connection_symbol", "→")
    connection_style = connection_config.get("connection_style", "text-white-50")

    return html.Div([
        html.Div([
            html.H6(entity_name, className="text-white mb-1", style={"fontSize": "14px"}),
            html.P(f"{field_count} Fields", className="text-white mb-1", style={"fontSize": "12px"}),
            html.Small(f"{connection_symbol} {connects_to}",
                      className=connection_style,
                      style={"fontSize": "10px"}),
            html.Div([
                html.Span(f"{completion_rate}%",
                         className="badge bg-light text-dark",
                         style={"fontSize": "10px"})
            ], className="mt-1")
        ], className="p-2 text-center")
    ],
    className="rounded shadow-sm",
    style={
        "backgroundColor": color,
        "minHeight": card_height,
        "margin": "5px"
    })

def create_complete_workflow_visualization() -> html.Div:
    """Create enhanced two-row workflow visualization with supporting entities"""

    try:
        # Access complete workflow data through adapter
        adapter = get_data_adapter()
        complete_data = adapter.get_complete_workflow_analysis()

        if not complete_data:
            return html.Div([html.P("Complete workflow data unavailable")])

        # Get workflow stages and supporting entities
        workflow_stages = complete_data.get("workflow_stages", [])
        supporting_entities = complete_data.get("supporting_entities", [])

        # Get configuration
        layout_config = complete_data.get("layout_config", {})
        connection_config = complete_data.get("connection_config", {})
        display_config = complete_data.get("display_config", {})

        # Create workflow stages row (reusing existing stage cards)
        stage_boxes = []
        for stage in workflow_stages:
            # Use existing card creation function
            stage_box = create_two_part_stage_card(stage)
            stage_boxes.append(stage_box)

        # Create workflow row with arrows
        workflow_row_elements = []
        for i, stage in enumerate(workflow_stages):
            stage_title = stage.get("title", stage.get("entity_name", ""))
            stage_box = stage_boxes[i]

            # Create column with stage card and title
            workflow_row_elements.append(
                html.Div([
                    stage_box,
                    html.Div(
                        stage_title,
                        className="text-center mt-2 fw-bold",
                        style={"fontSize": display_config.get("font_sizes", {}).get("title", "16px")}
                    )
                ], className="col-md")
            )

            # Add arrow between stages (except last)
            if i < len(workflow_stages) - 1:
                workflow_row_elements.append(
                    html.Div([
                        html.I(className="fas fa-arrow-right fa-2x text-primary")
                    ], className="col-auto d-flex align-items-center")
                )

        # Create supporting entities row
        supporting_row_elements = []
        for entity in supporting_entities:
            entity_card = create_supporting_entity_card(entity, connection_config)
            supporting_row_elements.append(
                html.Div([entity_card], className="col-md-auto")
            )

        # Combine into two-row layout
        return html.Div([
            # Main title
            html.H4(layout_config.get("main_title", "Complete Entity Architecture"),
                   className="text-center mb-4"),

            # TOP ROW - Workflow Process
            html.Div([
                html.H5(layout_config.get("workflow_row_title", "Core Workflow Process"),
                       className="mb-3"),
                html.Div(workflow_row_elements, className="row align-items-center mb-5")
            ], className="mb-4"),

            # BOTTOM ROW - Supporting Entities
            html.Div([
                html.H5(layout_config.get("supporting_row_title", "Supporting Data Entities"),
                       className="mb-3"),
                html.Div(supporting_row_elements, className="row justify-content-center")
            ])
        ])

    except Exception as e:
        handle_error(logger, e, "complete workflow visualization creation")
        return html.Div([html.P("Complete workflow visualization unavailable")])

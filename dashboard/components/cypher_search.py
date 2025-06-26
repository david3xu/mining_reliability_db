"""
Cypher Search Component for Mining Reliability Database
Advanced graph query interface for power users with safety framework
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dash_table, dcc, html

from dashboard.adapters.config_adapter import ConfigAdapter
from dashboard.adapters.data_adapter import DataAdapter
from dashboard.components.layout_template import create_standard_layout

logger = logging.getLogger(__name__)


class CypherQueryValidator:
    """Safety framework for validating Cypher queries"""

    def __init__(self, safety_config: Dict[str, Any]):
        self.allowed_keywords = [kw.upper() for kw in safety_config.get("allowed_keywords", [])]
        self.forbidden_keywords = [kw.upper() for kw in safety_config.get("forbidden_keywords", [])]
        self.max_query_length = safety_config.get("max_query_length", 2000)
        self.require_return_clause = safety_config.get("require_return_clause", True)
        self.require_limit_clause = safety_config.get("require_limit_clause", True)
        self.default_limit = safety_config.get("default_limit", 100)

    def validate_query(self, query: str) -> Tuple[bool, str]:
        """Validate a Cypher query for safety and compliance"""
        if not query or not query.strip():
            return False, "Query cannot be empty"

        query_upper = query.upper()

        # Check query length
        if len(query) > self.max_query_length:
            return False, f"Query exceeds maximum length of {self.max_query_length} characters"

        # Check for forbidden keywords
        for forbidden in self.forbidden_keywords:
            if forbidden in query_upper:
                return False, f"Forbidden keyword detected: {forbidden}"

        # Check for required RETURN clause
        if self.require_return_clause and "RETURN" not in query_upper:
            return False, "Query must include a RETURN clause"

        # Check for LIMIT clause or add default
        if self.require_limit_clause and "LIMIT" not in query_upper:
            return False, f"Query must include a LIMIT clause (max {self.default_limit})"

        # Extract and validate LIMIT value
        limit_match = re.search(r"LIMIT\s+(\d+)", query_upper)
        if limit_match:
            limit_value = int(limit_match.group(1))
            if limit_value > self.default_limit:
                return (
                    False,
                    f"LIMIT value {limit_value} exceeds maximum allowed {self.default_limit}",
                )

        return True, "Query is valid"


def create_cypher_search_layout() -> html.Div:
    """Create the cypher search component layout"""

    try:
        # Load configuration
        config_adapter = ConfigAdapter()
        config = config_adapter.load_cypher_search_config()

        query_templates = config.get("query_templates", {})
        example_queries = config.get("example_queries", {})

        # Create template dropdown options
        template_options = [{"label": "Custom Query", "value": "custom"}]
        for template_id, template_info in query_templates.items():
            template_options.append(
                {"label": template_info.get("title", template_id), "value": template_id}
            )

        # Create example query options
        example_options = []
        for example_id, example_info in example_queries.items():
            example_options.append(
                {"label": example_info.get("title", example_id), "value": example_id}
            )

        content_cards = [
            # Query Builder Section
            html.Div(
                [
                    html.H4("Query Builder", className="mb-3"),
                    # Template Selection
                    html.Div(
                        [
                            html.Label("Query Template:", className="form-label"),
                            dcc.Dropdown(
                                id="cypher-template-dropdown",
                                options=template_options,
                                value="custom",
                                className="mb-3",
                            ),
                        ]
                    ),
                    # Template Parameters (dynamically populated)
                    html.Div(id="cypher-template-parameters", className="mb-3"),
                    # Query Input
                    html.Div(
                        [
                            html.Label("Cypher Query:", className="form-label"),
                            dcc.Textarea(
                                id="cypher-query-input",
                                placeholder="Enter your Cypher query here...\nExample: MATCH (n) RETURN n LIMIT 10",
                                style={"width": "100%", "height": "150px"},
                                className="form-control mb-2",
                            ),
                        ]
                    ),
                    # Query Validation Status
                    html.Div(id="cypher-validation-status", className="mb-3"),
                    # Execute Button
                    html.Div(
                        [
                            html.Button(
                                "Execute Query",
                                id="cypher-execute-button",
                                className="btn btn-primary me-2",
                                disabled=True,
                            ),
                            html.Button(
                                "Clear Query",
                                id="cypher-clear-button",
                                className="btn btn-secondary me-2",
                            ),
                            html.Button(
                                "Load Example", id="cypher-example-button", className="btn btn-info"
                            ),
                        ]
                    ),
                ],
                className="card-body",
            ),
            # Example Queries Section
            html.Div(
                [
                    html.H4("Example Queries", className="mb-3"),
                    dcc.Dropdown(
                        id="cypher-example-dropdown",
                        options=example_options,
                        placeholder="Select an example query to load...",
                        className="mb-3",
                    ),
                    html.Div(id="cypher-example-description", className="text-muted"),
                ],
                className="card-body",
            ),
            # Results Section
            html.Div(
                [
                    html.H4("Query Results", className="mb-3"),
                    html.Div(id="cypher-execution-status", className="mb-3"),
                    # Results Display Tabs
                    dcc.Tabs(
                        id="cypher-results-tabs",
                        value="table-tab",
                        children=[
                            dcc.Tab(label="Table View", value="table-tab"),
                            dcc.Tab(label="Graph View", value="graph-tab"),
                            dcc.Tab(label="Raw Data", value="raw-tab"),
                        ],
                    ),
                    # Results Content
                    html.Div(id="cypher-results-content", className="mt-3"),
                ],
                className="card-body",
            ),
        ]

        return create_standard_layout(title="Cypher Search Interface", content_cards=content_cards)

    except Exception as e:
        logger.error(f"Failed to create cypher search layout: {str(e)}")
        return html.Div(
            [
                html.H3("Cypher Search Component"),
                html.Div(f"Error loading component: {str(e)}", className="alert alert-danger"),
            ]
        )


# Callback for template selection
@callback(
    [Output("cypher-template-parameters", "children"), Output("cypher-query-input", "value")],
    Input("cypher-template-dropdown", "value"),
)
def update_template_selection(template_id):
    """Update template parameters and query based on selection"""

    if not template_id or template_id == "custom":
        return [], ""

    try:
        config_adapter = ConfigAdapter()
        config = config_adapter.load_cypher_search_config()

        templates = config.get("query_templates", {})
        template = templates.get(template_id, {})

        if not template:
            return [], ""

        # Create parameter inputs
        parameters = template.get("parameters", [])
        parameter_inputs = []

        for param in parameters:
            param_name = param.get("name", "")
            param_type = param.get("type", "text")
            param_desc = param.get("description", "")
            param_default = param.get("default", "")
            param_required = param.get("required", False)

            label_text = f"{param_name}"
            if param_required:
                label_text += " *"

            if param_type == "number":
                input_component = dcc.Input(
                    id={"type": "template-param", "param": param_name},
                    type="number",
                    value=param_default,
                    placeholder=param_desc,
                    className="form-control",
                )
            else:
                input_component = dcc.Input(
                    id={"type": "template-param", "param": param_name},
                    type="text",
                    value=param_default,
                    placeholder=param_desc,
                    className="form-control",
                )

            parameter_inputs.append(
                html.Div(
                    [
                        html.Label(label_text, className="form-label"),
                        input_component,
                        html.Small(param_desc, className="form-text text-muted"),
                    ],
                    className="mb-2",
                )
            )

        # Get template query
        template_query = template.get("template", "")

        return parameter_inputs, template_query

    except Exception as e:
        logger.error(f"Error updating template selection: {str(e)}")
        return [], ""


# Callback for query validation
@callback(
    [Output("cypher-validation-status", "children"), Output("cypher-execute-button", "disabled")],
    Input("cypher-query-input", "value"),
)
def validate_query(query):
    """Validate the entered Cypher query"""

    if not query or not query.strip():
        return html.Div("Enter a query to validate", className="text-muted"), True

    try:
        config_adapter = ConfigAdapter()
        config = config_adapter.load_cypher_search_config()

        validator = CypherQueryValidator(config.get("safety_framework", {}))
        is_valid, message = validator.validate_query(query)

        if is_valid:
            status_div = html.Div(
                [html.I(className="fas fa-check-circle text-success me-2"), message],
                className="text-success",
            )
            return status_div, False
        else:
            status_div = html.Div(
                [html.I(className="fas fa-exclamation-triangle text-danger me-2"), message],
                className="text-danger",
            )
            return status_div, True

    except Exception as e:
        logger.error(f"Error validating query: {str(e)}")
        return html.Div(f"Validation error: {str(e)}", className="text-danger"), True


# Callback for example query loading
@callback(
    [
        Output("cypher-example-description", "children"),
        Output("cypher-query-input", "value", allow_duplicate=True),
    ],
    [Input("cypher-example-dropdown", "value"), Input("cypher-example-button", "n_clicks")],
    prevent_initial_call=True,
)
def load_example_query(example_id, n_clicks):
    """Load an example query"""

    if not example_id:
        return "", dash.no_update

    try:
        config_adapter = ConfigAdapter()
        config = config_adapter.load_cypher_search_config()

        examples = config.get("example_queries", {})
        example = examples.get(example_id, {})

        if not example:
            return "Example not found", dash.no_update

        description = example.get("description", "")
        query = example.get("query", "")

        # Only update query if button was clicked
        triggered = dash.callback_context.triggered[0]["prop_id"]
        if "example-button" in triggered:
            return description, query
        else:
            return description, dash.no_update

    except Exception as e:
        logger.error(f"Error loading example query: {str(e)}")
        return f"Error: {str(e)}", dash.no_update


# Callback for query execution
@callback(
    Output("cypher-execution-status", "children"),
    Input("cypher-execute-button", "n_clicks"),
    State("cypher-query-input", "value"),
)
def execute_query(n_clicks, query):
    """Execute the Cypher query"""

    if not n_clicks or not query:
        return ""

    try:
        # Validate query again before execution
        config_adapter = ConfigAdapter()
        config = config_adapter.load_cypher_search_config()

        validator = CypherQueryValidator(config.get("safety_framework", {}))
        is_valid, message = validator.validate_query(query)

        if not is_valid:
            return html.Div(
                [
                    html.I(className="fas fa-exclamation-triangle text-danger me-2"),
                    f"Query validation failed: {message}",
                ],
                className="alert alert-danger",
            )

        # Execute query through data adapter
        data_adapter = DataAdapter()
        results = data_adapter.execute_cypher_query(query)

        if results is not None:
            result_count = len(results) if hasattr(results, "__len__") else 0
            return html.Div(
                [
                    html.I(className="fas fa-check-circle text-success me-2"),
                    f"Query executed successfully. {result_count} results returned.",
                ],
                className="alert alert-success",
            )
        else:
            return html.Div(
                [
                    html.I(className="fas fa-exclamation-triangle text-warning me-2"),
                    "Query executed but no results returned.",
                ],
                className="alert alert-warning",
            )

    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return html.Div(
            [
                html.I(className="fas fa-times-circle text-danger me-2"),
                f"Query execution failed: {str(e)}",
            ],
            className="alert alert-danger",
        )


# Callback for results display
@callback(
    Output("cypher-results-content", "children"),
    [Input("cypher-execution-status", "children"), Input("cypher-results-tabs", "value")],
    State("cypher-query-input", "value"),
)
def display_results(execution_status, active_tab, query):
    """Display query results in different formats"""

    if not execution_status or not query:
        return html.Div("No results to display", className="text-muted")

    try:
        # Check if execution was successful
        if not execution_status or "alert-success" not in str(execution_status):
            return html.Div("Query was not executed successfully", className="text-muted")

        # Execute query to get results for display
        data_adapter = DataAdapter()
        results = data_adapter.execute_cypher_query(query)

        if not results:
            return html.Div("No data to display", className="text-muted")

        # Convert results to DataFrame for easier handling
        if isinstance(results, list) and len(results) > 0:
            df = pd.DataFrame(results)
        else:
            return html.Div("Unable to format results", className="text-muted")

        if active_tab == "table-tab":
            return create_table_view(df)
        elif active_tab == "graph-tab":
            return create_graph_view(df)
        elif active_tab == "raw-tab":
            return create_raw_view(results)
        else:
            return html.Div("Unknown tab", className="text-muted")

    except Exception as e:
        logger.error(f"Error displaying results: {str(e)}")
        return html.Div(f"Error displaying results: {str(e)}", className="text-danger")


def create_table_view(df: pd.DataFrame) -> html.Div:
    """Create table view of results"""

    try:
        return dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=20,
            sort_action="native",
            filter_action="native",
            export_format="csv",
            style_cell={"textAlign": "left"},
            style_data={"whiteSpace": "normal", "height": "auto"},
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        )
    except Exception as e:
        return html.Div(f"Error creating table view: {str(e)}", className="text-danger")


def create_graph_view(df: pd.DataFrame) -> html.Div:
    """Create graph visualization of results"""

    try:
        # Simple bar chart if we have numeric columns
        numeric_cols = df.select_dtypes(include=["number"]).columns

        if len(numeric_cols) > 0:
            # Create a simple bar chart with first numeric column
            first_col = df.columns[0]
            first_numeric = numeric_cols[0]

            fig = px.bar(
                df.head(20),  # Limit to first 20 rows
                x=first_col,
                y=first_numeric,
                title=f"{first_numeric} by {first_col}",
            )

            return dcc.Graph(figure=fig)
        else:
            # Create a simple count chart
            first_col = df.columns[0]
            value_counts = df[first_col].value_counts().head(10)

            fig = px.bar(x=value_counts.index, y=value_counts.values, title=f"Count of {first_col}")

            return dcc.Graph(figure=fig)

    except Exception as e:
        return html.Div(f"Error creating graph view: {str(e)}", className="text-danger")


def create_raw_view(results: Any) -> html.Div:
    """Create raw data view"""

    try:
        return html.Pre(
            json.dumps(results, indent=2, default=str),
            style={"background": "#f8f9fa", "padding": "10px", "border-radius": "5px"},
        )
    except Exception as e:
        return html.Div(f"Error creating raw view: {str(e)}", className="text-danger")


# Callback for clearing query
@callback(
    Output("cypher-query-input", "value", allow_duplicate=True),
    Input("cypher-clear-button", "n_clicks"),
    prevent_initial_call=True,
)
def clear_query(n_clicks):
    """Clear the query input"""
    if n_clicks:
        return ""
    return dash.no_update

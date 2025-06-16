#!/usr/bin/env python3
"""
Interaction Handlers Adapter - Pure Callback Management
Clean interaction logic with adapter-driven URL generation.
"""

import logging
from typing import Any, Dict, List, Optional

import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, html
from dash.exceptions import PreventUpdate

from dashboard.adapters import get_data_adapter, get_facility_adapter
from dashboard.routing.url_manager import get_url_manager
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


class InteractionHandlers:
    """Pure interaction handling with adapter integration"""

    def __init__(self):
        self.facility_adapter = get_facility_adapter()
        self.data_adapter = get_data_adapter()
        self.url_manager = get_url_manager()
        self.last_results = None  # Store last query results for export
        self.last_journey_results = None  # Store last journey results for export

    def register_chart_interactions(self, app):
        """Register chart click callbacks"""

        @app.callback(
            Output("url-location", "pathname"),
            Input("facility-pie-chart", "clickData"),
            prevent_initial_call=True,
        )
        def handle_facility_chart_click(click_data):
            """Direct facility navigation from pie chart"""
            try:
                if not click_data:
                    raise PreventUpdate

                facility_name = click_data["points"][0]["label"]
                logger.info(f"Chart interaction: {facility_name}")

                # Validate facility exists
                if self.url_manager.validate_route(f"/facility/{facility_name}"):
                    return f"/facility/{facility_name}"

                raise PreventUpdate

            except Exception as e:
                handle_error(logger, e, "facility chart interaction")
                raise PreventUpdate

        @app.callback(
            Output("url-location", "pathname", allow_duplicate=True),
            Input("field-bar-chart", "clickData"),
            prevent_initial_call=True,
        )
        def handle_field_chart_click(click_data):
            """Direct field analysis navigation"""
            try:
                if not click_data:
                    raise PreventUpdate

                field_type = click_data["points"][0]["x"]
                logger.info(f"Field chart interaction: {field_type}")

                return "/data-types-distribution"

            except Exception as e:
                handle_error(logger, e, "field chart interaction")
                raise PreventUpdate

    def register_table_interactions(self, app):
        """Register table click callbacks"""

        @app.callback(
            Output("url-location", "pathname", allow_duplicate=True),
            Input("timeline-table", "active_cell"),
            prevent_initial_call=True,
        )
        def handle_table_interaction(active_cell):
            """Direct facility navigation from table"""
            try:
                if not active_cell:
                    raise PreventUpdate

                # Get table data through adapter
                timeline_data = self.facility_adapter.get_facility_list()

                if active_cell["row"] < len(timeline_data):
                    facility_id = timeline_data[active_cell["row"]]["facility_id"]
                    logger.info(f"Table interaction: {facility_id}")

                    return f"/facility/{facility_id}"

                raise PreventUpdate

            except Exception as e:
                handle_error(logger, e, "table interaction")
                raise PreventUpdate

    def register_navigation_interactions(self, app):
        """Register navigation state management"""

        @app.callback(
            Output("dashboard-state", "data"),
            Input("url-location", "pathname"),
            prevent_initial_call=True,
        )
        def update_navigation_state(pathname):
            """Track navigation state for breadcrumbs"""
            try:
                breadcrumbs = self.url_manager.get_breadcrumbs(pathname)

                return {
                    "current_path": pathname,
                    "breadcrumbs": breadcrumbs,
                    "timestamp": ctx.triggered[0]["prop_id"],
                }

            except Exception as e:
                handle_error(logger, e, "navigation state update")
                return {}

    def register_search_interactions(self, app):
        """Register search functionality callbacks"""

        @app.callback(
            [Output("search-results", "children"), Output("search-status", "children")],
            [Input("search-button", "n_clicks"), Input("clear-button", "n_clicks")],
            [State("search-input", "value")],
            prevent_initial_call=True,
        )
        def handle_search_interaction(search_clicks, clear_clicks, search_text):
            """Process search requests and display results"""
            try:
                if not ctx.triggered:
                    raise PreventUpdate

                trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

                if trigger_id == "clear-button":
                    return html.Div(), html.Div()

                if trigger_id == "search-button" and search_text:
                    return self._perform_search(search_text.strip())

                raise PreventUpdate

            except Exception as e:
                handle_error(logger, e, "search interaction")
                return html.Div("Search error occurred"), self._create_error_status("Search failed")

        @app.callback(
            Output("search-input", "placeholder"),
            Input("search-button", "n_clicks"),
            State("search-input", "value"),
            prevent_initial_call=True,
        )
        def update_search_placeholder(n_clicks, search_value):
            """Update placeholder to show last searched term"""
            if search_value:
                return f"Last searched: {search_value}"
            return "Enter search term"

    def _perform_search(self, search_text: str) -> tuple:
        """Execute search and format results"""
        try:
            if len(search_text) < 3:
                return html.Div(), self._create_status_message(
                    "Enter at least 3 characters", "warning"
                )

            # Execute search through data adapter
            results = self.data_adapter.search_problems_and_causes(search_text)

            if not results:
                no_results = html.Div(
                    [
                        html.P(f"No matching incidents found for '{search_text}'"),
                        html.P("Try different keywords or check spelling"),
                    ]
                )
                return no_results, self._create_status_message("No results found", "info")

            # Create results table
            results_table = self._create_search_results_table(results)
            status = self._create_status_message(
                f"Found {len(results)} incidents matching '{search_text}'", "success"
            )

            return results_table, status

        except Exception as e:
            error_display = html.Div(
                [
                    html.P(f"Search error: {str(e)}", style={"color": "red"}),
                    html.P(f"Search term: {search_text}", style={"color": "yellow"}),
                ]
            )
            return error_display, self._create_error_status("Search failed")

    def _create_search_results_table(self, results):
        """Format search results as table"""
        try:
            from dash import dash_table

            # Transform results for table display
            table_data = []
            for result in results:
                # Safely handle None values for string operations
                problem_desc = result.get("problem_description") or "N/A"
                root_cause = result.get("root_cause") or "N/A"
                initiation_date = result.get("initiation_date") or "N/A"

                table_data.append(
                    {
                        "Problem": problem_desc,
                        "Root Cause": root_cause,
                        "Facility": result.get("facility_id", "Unknown"),
                        "Date": initiation_date[:10] if initiation_date != "N/A" else "N/A",
                        "Status": result.get("status", "Unknown"),
                    }
                )

            columns = ["Problem", "Root Cause", "Facility", "Date", "Status"]

            return html.Div(
                [
                    html.H5(f"Search Results ({len(results)} incidents)", className="mb-3"),
                    dash_table.DataTable(
                        data=table_data,
                        columns=[
                            {"name": "Problem", "id": "Problem", "type": "text"},
                            {"name": "Root Cause", "id": "Root Cause", "type": "text"},
                            {"name": "Facility", "id": "Facility", "type": "text"},
                            {"name": "Date", "id": "Date", "type": "text"},
                            {"name": "Status", "id": "Status", "type": "text"},
                        ],
                        style_cell={
                            "textAlign": "left",
                            "padding": "10px",
                            "fontFamily": "Arial",
                            "fontSize": "14px",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "overflow": "visible",
                        },
                        style_cell_conditional=[
                            {
                                "if": {"column_id": "Problem"},
                                "minWidth": "300px",
                                "whiteSpace": "normal",
                                "height": "auto",
                            },
                            {
                                "if": {"column_id": "Root Cause"},
                                "minWidth": "250px",
                                "whiteSpace": "normal",
                                "height": "auto",
                            },
                            {
                                "if": {"column_id": "Facility"},
                                "minWidth": "120px",
                                "textAlign": "center",
                            },
                            {
                                "if": {"column_id": "Date"},
                                "minWidth": "110px",
                                "textAlign": "center",
                            },
                            {
                                "if": {"column_id": "Status"},
                                "minWidth": "130px",
                                "textAlign": "center",
                            },
                        ],
                        style_header={
                            "backgroundColor": "rgb(230, 230, 230)",
                            "fontWeight": "bold",
                            "textAlign": "center",
                        },
                        style_data={
                            "backgroundColor": "rgb(248, 248, 248)",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "lineHeight": "1.4",
                            "wordWrap": "break-word",
                        },
                        css=[
                            {
                                "selector": ".dash-table-tooltip",
                                "rule": "background-color: white; font-family: Arial; border: 1px solid grey; border-radius: 5px; padding: 10px; max-width: 500px",
                            }
                        ],
                        tooltip_data=[
                            {
                                column: {"value": str(row[column]), "type": "markdown"}
                                for column in ["Problem", "Root Cause", "Status"]
                            }
                            for row in table_data
                        ],
                        tooltip_duration=None,
                        page_size=10,
                        sort_action="native",
                    ),
                ]
            )

        except Exception as e:
            handle_error(logger, e, "search results table creation")
            return html.Div(f"Error displaying results: {str(e)}")

    def _create_status_message(self, message: str, alert_type: str):
        """Create status message with appropriate styling"""
        import dash_bootstrap_components as dbc

        return dbc.Alert(message, color=alert_type, dismissable=True, className="mb-2")

    def _create_error_status(self, message: str):
        """Create error status message"""
        import dash_bootstrap_components as dbc

        return dbc.Alert(message, color="danger", dismissable=True, className="mb-2")

    def get_chart_config(self) -> Dict[str, Any]:
        """Chart interaction configuration"""
        return {
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
            "displaylogo": False,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "mining_chart",
                "height": 500,
                "width": 700,
            },
        }

    def register_stakeholder_essentials_interactions(self, app):
        """Register callbacks for essential stakeholder questions with JSON export"""

        @app.callback(
            [Output("results-display", "children"), Output("export-status", "children")],
            [Input("search-btn", "n_clicks"), Input("question-tabs", "active_tab")],
            State("incident-keywords", "value"),
            prevent_initial_call=True,
        )
        def execute_essential_query(n_clicks, active_tab, keywords):
            """Execute essential stakeholder queries"""
            import dash_bootstrap_components as dbc
            from dash import Input, Output, State, ctx, dcc, html

            from dashboard.components.stakeholder_essentials import (
                create_effective_actions_table,
                create_expertise_table,
                create_solutions_table,
                create_timeline_table,
            )
            from mine_core.shared.common import handle_error

            if not n_clicks and not active_tab:
                raise PreventUpdate

            if not keywords:
                return [dbc.Alert("Please enter equipment and issue keywords", color="info")], ""

            try:
                # Process keywords
                keyword_list = [k.strip().lower() for k in keywords.split() if k.strip()]

                data_adapter = self.data_adapter  # Use the adapter initialized in __init__

                # Execute the appropriate query based on active tab and store results
                display = html.Div()
                if active_tab == "tab-1":
                    query_type = "what_could_be_causing_this"
                    results = data_adapter.execute_essential_stakeholder_query(
                        query_type, keyword_list
                    )
                    self.last_results = {
                        "type": query_type,
                        "data": results,
                        "keywords": keyword_list,
                    }
                    display = create_solutions_table(results)

                elif active_tab == "tab-2":
                    query_type = "who_has_diagnostic_experience"
                    results = data_adapter.execute_essential_stakeholder_query(
                        query_type, keyword_list
                    )
                    self.last_results = {
                        "type": query_type,
                        "data": results,
                        "keywords": keyword_list,
                    }
                    display = create_expertise_table(results)

                elif active_tab == "tab-3":
                    query_type = "what_should_i_check_first"
                    results = data_adapter.execute_essential_stakeholder_query(
                        query_type, keyword_list
                    )
                    self.last_results = {
                        "type": query_type,
                        "data": results,
                        "keywords": keyword_list,
                    }
                    display = create_timeline_table(results)

                elif active_tab == "tab-4":
                    query_type = "what_investigation_steps_worked"
                    results = data_adapter.execute_essential_stakeholder_query(
                        query_type, keyword_list
                    )
                    self.last_results = {
                        "type": query_type,
                        "data": results,
                        "keywords": keyword_list,
                    }
                    display = create_effective_actions_table(results)

                else:
                    return [dbc.Alert("Unknown question tab", color="danger")], ""

                return [display], ""

            except Exception as e:
                handle_error(logger, e, f"essential query for '{keywords}'")
                error_display = dbc.Alert(
                    [
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        f"Analysis failed: {str(e)}",
                    ],
                    color="danger",
                )

                return [error_display], ""

        @app.callback(
            [
                Output("results-display", "children", allow_duplicate=True),
                Output("export-status", "children", allow_duplicate=True),
            ],
            Input("export-json-btn", "n_clicks"),
            prevent_initial_call=True,
        )
        def export_json_results(n_clicks):
            """Export last query results to JSON"""
            import dash_bootstrap_components as dbc
            from dash import html, no_update

            from dashboard.adapters.data_adapter_json_export import get_json_export_adapter
            from dashboard.components.stakeholder_essentials import (
                create_effective_actions_table_with_export_info,
                create_expertise_table_with_export_info,
                create_solutions_table_with_export_info,
                create_timeline_table_with_export_info,
            )
            from mine_core.shared.common import handle_error

            if not n_clicks:
                raise PreventUpdate

            if not hasattr(self, "last_results") or not self.last_results:
                return no_update, dbc.Alert(
                    "No results to export. Run a search first.", color="warning"
                )

            try:
                query_type = self.last_results["type"]
                results = self.last_results["data"]
                keywords = self.last_results["keywords"]

                # Get JSON export adapter and export
                json_export_adapter = get_json_export_adapter()
                (
                    _,
                    export_path,
                ) = json_export_adapter.execute_essential_stakeholder_query_with_export(
                    query_type, keywords
                )

                # Update display with export info
                if query_type == "can_this_be_fixed":
                    display = create_solutions_table_with_export_info(results, export_path)
                elif query_type == "who_do_i_call":
                    display = create_expertise_table_with_export_info(results, export_path)
                elif query_type == "how_long_will_this_take":
                    display = create_timeline_table_with_export_info(results, export_path)
                elif query_type == "what_works_and_why":
                    display = create_effective_actions_table_with_export_info(results, export_path)
                else:
                    return no_update, dbc.Alert("Unknown query type", color="danger")

                status = dbc.Alert(
                    [
                        html.I(className="fas fa-check-circle me-2"),
                        f"Results exported to: {export_path.split('/')[-1]}",
                    ],
                    color="success",
                    dismissable=True,
                )

                return display, status

            except Exception as e:
                handle_error(logger, e, "JSON export")
                return no_update, dbc.Alert(f"Export failed: {str(e)}", color="danger")

        @app.callback(
            [
                Output("results-display", "children", allow_duplicate=True),
                Output("export-status", "children", allow_duplicate=True),
            ],
            Input("export-all-btn", "n_clicks"),
            State("incident-keywords", "value"),
            prevent_initial_call=True,
        )
        def export_comprehensive_results(n_clicks, keywords):
            """Export comprehensive analysis covering all 4 essential questions"""
            import dash_bootstrap_components as dbc
            from dash import html, no_update

            from dashboard.adapters.data_adapter_json_export import get_json_export_adapter
            from mine_core.shared.common import handle_error

            if not n_clicks:
                raise PreventUpdate

            if not keywords:
                return no_update, dbc.Alert("Please enter keywords first", color="warning")

            try:
                # Process keywords
                keyword_list = [k.strip().lower() for k in keywords.split() if k.strip()]

                # Get JSON export adapter and perform comprehensive export
                json_export_adapter = get_json_export_adapter()
                (
                    all_results,
                    export_path,
                ) = json_export_adapter.execute_comprehensive_stakeholder_export(keyword_list)

                if not export_path:
                    return no_update, dbc.Alert("Comprehensive export failed", color="danger")

                # Create comprehensive results display
                comprehensive_display = self._create_comprehensive_results_display(
                    all_results, export_path
                )

                status = dbc.Alert(
                    [
                        html.I(className="fas fa-check-circle me-2"),
                        f"Comprehensive analysis exported to: {export_path.split('/')[-1]}",
                    ],
                    color="success",
                    dismissable=True,
                )

                return comprehensive_display, status

            except Exception as e:
                handle_error(logger, e, "Comprehensive JSON export")
                return no_update, dbc.Alert(
                    f"Comprehensive export failed: {str(e)}", color="danger"
                )

    def _create_comprehensive_results_display(
        self, all_results: Dict[str, List[Dict]], export_path: str
    ) -> html.Div:
        """Create display for comprehensive results across all 4 questions"""
        import dash_bootstrap_components as dbc
        from dash import html

        # Calculate summary statistics
        total_results = sum(len(results) for results in all_results.values())

        # Create summary cards
        summary_cards = []
        question_titles = {
            "what_could_be_causing_this": (
                "What could be causing this?",
                "primary",
                "fas fa-search-plus",
            ),
            "who_has_diagnostic_experience": (
                "Who has diagnostic experience?",
                "info",
                "fas fa-user-md",
            ),
            "what_should_i_check_first": (
                "What should I check first?",
                "warning",
                "fas fa-list-ol",
            ),
            "what_investigation_steps_worked": (
                "What investigation steps worked?",
                "success",
                "fas fa-check-circle",
            ),
        }

        for question_id, results in all_results.items():
            if question_id in question_titles:
                title, color, icon = question_titles[question_id]

                summary_cards.append(
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                [html.I(className=f"{icon} me-2"), title],
                                                className=f"text-{color} mb-2",
                                            ),
                                            html.H4(str(len(results)), className=f"text-{color}"),
                                            html.P(
                                                "relevant records", className="text-muted small"
                                            ),
                                        ]
                                    )
                                ],
                                className=f"border-{color}",
                            )
                        ],
                        width=3,
                    )
                )

        # Export notification
        export_notification = dbc.Alert(
            [
                html.I(className="fas fa-download me-2"),
                f"Comprehensive analysis exported to: {export_path.split('/')[-1]}",
                html.Br(),
                html.Small(
                    f"Total records found: {total_results} across all 4 questions",
                    className="text-muted",
                ),
            ],
            color="success",
            className="mb-4",
        )

        # Create detailed results sections
        detailed_sections = []
        for question_id, results in all_results.items():
            if question_id in question_titles and results:
                title, color, icon = question_titles[question_id]

                # Create mini table for each question
                table_rows = []
                for result in results[:5]:  # Show top 5 results per question
                    if question_id == "what_investigation_steps_worked":
                        table_rows.append(
                            html.Tr(
                                [
                                    html.Td(result.get("incident_id", "N/A")),
                                    html.Td(
                                        result.get("approach_description", "")[:50] + "..."
                                        if len(result.get("approach_description", "")) > 50
                                        else result.get("approach_description", "")
                                    ),
                                    html.Td(
                                        dbc.Badge(
                                            f"{result.get('success_rate', 0)}%",
                                            color="success"
                                            if result.get("success_rate", 0) > 70
                                            else "secondary",
                                        )
                                    ),
                                ]
                            )
                        )
                    elif question_id == "who_has_diagnostic_experience":
                        table_rows.append(
                            html.Tr(
                                [
                                    html.Td(result.get("expert_department", "N/A")),
                                    html.Td(result.get("facility_name", "N/A")),
                                    html.Td(f"{result.get('diagnostic_success_rate', 0)}%"),
                                ]
                            )
                        )
                    elif question_id == "what_should_i_check_first":
                        table_rows.append(
                            html.Tr(
                                [
                                    html.Td(result.get("step_description", "N/A")),
                                    html.Td(result.get("priority_level", "N/A")),
                                    html.Td(result.get("instances", 0)),
                                ]
                            )
                        )
                    elif question_id == "what_could_be_causing_this":
                        table_rows.append(
                            html.Tr(
                                [
                                    html.Td(result.get("incident_id", "N/A")),
                                    html.Td(
                                        result.get("root_cause_analysis", "")[:40] + "..."
                                        if len(result.get("root_cause_analysis", "")) > 40
                                        else result.get("root_cause_analysis", "")
                                    ),
                                    html.Td(f"{result.get('similarity_score', 0):.1f}"),
                                ]
                            )
                        )

                if table_rows:
                    detailed_sections.append(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.I(className=f"{icon} me-2"),
                                        title,
                                        dbc.Badge(
                                            f"{len(results)} found", color=color, className="ms-2"
                                        ),
                                    ]
                                ),
                                dbc.CardBody(
                                    [
                                        dbc.Table(
                                            [html.Tbody(table_rows)],
                                            striped=True,
                                            hover=True,
                                            size="sm",
                                        ),
                                        html.P(
                                            f"Showing top 5 of {len(results)} results",
                                            className="text-muted small mt-2",
                                        ),
                                    ]
                                ),
                            ],
                            className="mb-3",
                        )
                    )

        return html.Div(
            [
                export_notification,
                html.H4("Comprehensive Stakeholder Analysis", className="mb-4"),
                dbc.Row(summary_cards, className="mb-4"),
                html.H5("Detailed Results by Question", className="mb-3"),
                html.Div(detailed_sections),
            ]
        )

    def register_stakeholder_journey_callbacks(self, app):
        """Register complete stakeholder journey callbacks"""

        @app.callback(
            [
                Output("journey-status", "children"),
                Output("journey-results-container", "children"),
                Output("journey-export-btn", "disabled"),
            ],
            Input("journey-search-btn", "n_clicks"),
            State("stakeholder-journey-input", "value"),
            prevent_initial_call=True,
        )
        def execute_complete_stakeholder_journey(n_clicks, user_input):
            """Execute complete stakeholder journey with single input"""
            try:
                if not n_clicks or not user_input or not user_input.strip():
                    raise PreventUpdate

                logger.info(f"Starting complete stakeholder journey for: {user_input}")

                # Show loading status
                loading_status = dbc.Alert(
                    [
                        dbc.Spinner(size="sm", spinner_class_name="me-2"),
                        f"Executing complete journey for: '{user_input}'...",
                    ],
                    color="info",
                    className="mb-0",
                )

                # Execute journey through data adapter
                journey_results = self.data_adapter.execute_complete_stakeholder_journey(user_input)

                # Store results for export
                self.last_journey_results = journey_results

                if journey_results.get("metadata", {}).get("success"):
                    # Success status
                    total_results = journey_results.get("metadata", {}).get("total_results", 0)
                    success_status = dbc.Alert(
                        [
                            html.I(className="fas fa-check-circle me-2"),
                            f"Journey completed successfully! Found {total_results} total results across all questions.",
                        ],
                        color="success",
                        className="mb-0",
                    )

                    # Create results display using the component function
                    from dashboard.components.stakeholder_essentials import (
                        create_journey_results_display,
                    )

                    results_display = create_journey_results_display(journey_results)

                    return success_status, results_display, False  # Enable export button
                else:
                    # Error status
                    error_msg = journey_results.get("metadata", {}).get("error", "Unknown error")
                    error_status = dbc.Alert(
                        [
                            html.I(className="fas fa-exclamation-triangle me-2"),
                            f"Journey failed: {error_msg}",
                        ],
                        color="danger",
                        className="mb-0",
                    )

                    return error_status, html.Div(), True  # Keep export disabled

            except Exception as e:
                handle_error(logger, e, "complete stakeholder journey callback")
                error_status = dbc.Alert(
                    [
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        f"Error executing journey: {str(e)}",
                    ],
                    color="danger",
                    className="mb-0",
                )

                return error_status, html.Div(), True

        @app.callback(
            [
                Output("journey-status", "children", allow_duplicate=True),
                Output("journey-export-btn", "disabled", allow_duplicate=True),
            ],
            Input("journey-export-btn", "n_clicks"),
            prevent_initial_call=True,
        )
        def export_journey_results(n_clicks):
            """Export complete journey results as JSON file"""
            try:
                if not n_clicks or not hasattr(self, "last_journey_results"):
                    raise PreventUpdate

                import json
                import os
                from datetime import datetime

                # Create export directory if it doesn't exist
                export_dir = "data/stakeholder_results"
                os.makedirs(export_dir, exist_ok=True)

                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"stakeholder_journey_{timestamp}.json"
                filepath = os.path.join(export_dir, filename)

                # Write results to file
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(self.last_journey_results, f, indent=2, default=str)

                # Show success message
                success_status = dbc.Alert(
                    [
                        html.I(className="fas fa-check-circle me-2"),
                        f"Journey results exported to: {filepath}",
                    ],
                    color="success",
                    dismissable=True,
                )

                return success_status, False

            except Exception as e:
                handle_error(logger, e, "journey results export")
                error_status = dbc.Alert(
                    [
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        f"Export failed: {str(e)}",
                    ],
                    color="danger",
                    dismissable=True,
                )
                return error_status, False


# Singleton pattern
_interaction_handlers = None


def get_interaction_handlers():
    """Get singleton interaction handlers instance"""
    global _interaction_handlers
    if _interaction_handlers is None:
        _interaction_handlers = InteractionHandlers()
    return _interaction_handlers

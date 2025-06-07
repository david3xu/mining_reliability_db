#!/usr/bin/env python3
"""
Interaction Handlers Adapter - Pure Callback Management
Clean interaction logic with adapter-driven URL generation.
"""

import logging
from typing import Any, Dict, Optional

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
        """Register callbacks for essential stakeholder questions"""

        @app.callback(
            [Output("results-display", "children")],
            [Input("search-btn", "n_clicks"), Input("question-tabs", "active_tab")],
            State("incident-keywords", "value"),
            prevent_initial_call=True,
        )
        def execute_essential_query(n_clicks, active_tab, keywords):
            """Execute essential stakeholder queries"""
            import dash_bootstrap_components as dbc
            from dash import Input, Output, State, ctx, dcc, html

            from dashboard.components.stakeholder_essentials import (
                create_expertise_table,
                create_solutions_table,
                create_timeline_table,
            )
            from mine_core.shared.common import handle_error

            if not n_clicks and not active_tab:
                raise PreventUpdate

            if not keywords:
                return [dbc.Alert("Please enter equipment and issue keywords", color="info")]

            try:
                # Show search in progress
                # This part will be handled by a separate output/status in the UI if needed

                # Process keywords
                keyword_list = [k.strip().lower() for k in keywords.split() if k.strip()]

                data_adapter = self.data_adapter  # Use the adapter initialized in __init__

                # Execute the appropriate query based on active tab
                display = html.Div()
                if active_tab == "tab-1":
                    # Can this be fixed?
                    results = data_adapter.execute_essential_stakeholder_query(
                        "can_this_be_fixed", keyword_list
                    )
                    display = create_solutions_table(results)

                elif active_tab == "tab-2":
                    # Who do I call?
                    results = data_adapter.execute_essential_stakeholder_query(
                        "who_do_i_call", keyword_list
                    )
                    display = create_expertise_table(results)

                elif active_tab == "tab-3":
                    # How long will this take?
                    results = data_adapter.execute_essential_stakeholder_query(
                        "how_long_will_this_take", keyword_list
                    )
                    display = create_timeline_table(results)
                else:
                    return [dbc.Alert("Unknown question tab", color="danger")]

                return [display]

            except Exception as e:
                handle_error(logger, e, f"essential query for '{keywords}'")
                error_display = dbc.Alert(
                    [
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        f"Analysis failed: {str(e)}",
                    ],
                    color="danger",
                )

                return [error_display]


# Singleton pattern
_interaction_handlers = None


def get_interaction_handlers():
    """Get singleton interaction handlers instance"""
    global _interaction_handlers
    if _interaction_handlers is None:
        _interaction_handlers = InteractionHandlers()
    return _interaction_handlers

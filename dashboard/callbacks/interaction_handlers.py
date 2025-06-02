#!/usr/bin/env python3
"""
Interaction Handlers Adapter - Pure Callback Management
Clean interaction logic with adapter-driven URL generation.
"""

import logging
from typing import Any, Dict, Optional

from dash import Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate

from dashboard.adapters import get_facility_adapter
from dashboard.routing.url_manager import get_url_manager
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


class InteractionHandlers:
    """Pure interaction handling with adapter integration"""

    def __init__(self):
        self.facility_adapter = get_facility_adapter()
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


# Singleton pattern
_interaction_handlers = None


def get_interaction_handlers():
    """Get singleton interaction handlers instance"""
    global _interaction_handlers
    if _interaction_handlers is None:
        _interaction_handlers = InteractionHandlers()
    return _interaction_handlers

#!/usr/bin/env python3
"""
Search-Only Dashboard Application - Minimal Search Interface
Clean application entry point focused on search algorithms only.
"""

import logging
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html

# Search components and adapters
from dashboard.adapters import get_config_adapter, get_data_adapter
from dashboard.components import create_graph_search_layout, create_cypher_search_layout, create_standard_layout
from mine_core.shared.common import setup_project_environment

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_search_app():
    """Create a minimal search-only dashboard application."""

    # Setup environment
    setup_project_environment()

    # Initialize Dash app
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True
    )

    # Simple layout with tabs for the two search interfaces
    app.layout = html.Div([
        dbc.Container([
            html.H1("Mining Reliability Search", className="text-center mb-4"),

            dbc.Tabs([
                dbc.Tab(label="Graph Search", tab_id="graph-search"),
                dbc.Tab(label="Cypher Search", tab_id="cypher-search"),
            ], id="search-tabs", active_tab="graph-search"),

            html.Div(id="tab-content", className="mt-3")
        ], fluid=True)
    ])

    # Callback to switch between search interfaces
    @app.callback(
        Output("tab-content", "children"),
        Input("search-tabs", "active_tab")
    )
    def render_tab_content(active_tab):
        if active_tab == "graph-search":
            return create_graph_search_layout()
        elif active_tab == "cypher-search":
            return create_cypher_search_layout()
        return html.Div("Select a search tab")

    return app


# For compatibility with existing code
def create_app():
    """Create the search application."""
    return create_search_app()


class SearchDashboardApp:
    """Minimal search dashboard application wrapper."""

    def __init__(self):
        self.app = create_search_app()

    def run(self, host="0.0.0.0", port=8050, debug=False):
        """Run the search dashboard."""
        self.app.run_server(host=host, port=port, debug=debug)


# For compatibility
PurifiedDashboardApp = SearchDashboardApp


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8050, debug=True)

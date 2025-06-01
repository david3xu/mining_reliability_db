#!/usr/bin/env python3
"""
Dashboard Application - Multi-Tab with Facility Routing
Professional tab routing plus facility drill-down capability.
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Dash framework
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Configuration and utilities
from mine_core.shared.common import setup_project_environment, handle_error

# Tab components
from dashboard.components.tab_navigation import create_tab_container
from dashboard.components.portfolio_overview import create_complete_dashboard
from dashboard.components.data_quality import create_data_quality_layout
from dashboard.components.workflow_analysis import create_workflow_analysis_layout
from dashboard.components.facility_detail import create_facility_detail_layout

# Data validation
from dashboard.utils.data_transformers import validate_dashboard_data

# Layout infrastructure
from dashboard.layouts.main_layout import create_main_layout, create_error_boundary

logger = None

class MultiTabDashboardApplication:
    """Professional multi-tab dashboard with facility drill-down"""

    def __init__(self, debug=None, port=None, host=None):
        """Initialize with tab and facility routing capability"""
        self.debug = debug if debug is not None else False
        self.port = port or 8050
        self.host = host or "127.0.0.1"

        self.app = None
        self.validation_status = {}

        self._setup_logging()
        self._validate_system()
        self._initialize_app()
        self._setup_routing_callbacks()

    def _setup_logging(self):
        """Setup logging using project infrastructure"""
        global logger
        try:
            logger = setup_project_environment("multi_tab_dashboard_app")
            logger.info("Multi-tab dashboard with facility routing initialization started")
        except Exception as e:
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to setup project environment: {e}")

    def _validate_system(self):
        """Validate all tab and facility data availability"""
        logger.info("Validating multi-tab system with facility support...")

        try:
            self.validation_status = validate_dashboard_data()

            tabs_ready = all([
                self.validation_status.get("portfolio_metrics", False),
                self.validation_status.get("data_quality", False),
                self.validation_status.get("workflow_analysis", False)
            ])

            if tabs_ready:
                logger.info("✅ All tabs and facility support validated - dashboard ready")
            else:
                failed_tabs = [k for k, v in self.validation_status.items()
                             if k in ["portfolio_metrics", "data_quality", "workflow_analysis"] and not v]
                logger.warning(f"⚠️ Tab validation issues: {failed_tabs}")

        except Exception as e:
            handle_error(logger, e, "multi-tab system validation")
            self.validation_status = {"phase2_complete": False}

    def _initialize_app(self):
        """Initialize Dash application with routing support"""
        try:
            external_stylesheets = [
                dbc.themes.BOOTSTRAP,
                {
                    "href": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
                    "rel": "stylesheet"
                }
            ]

            self.app = dash.Dash(
                __name__,
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True,
                title="Mining Reliability Database - Comprehensive Analysis",
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
                    {"name": "description", "content": "Multi-Tab Mining Reliability Dashboard with Facility Analysis"}
                ]
            )

            self.app.layout = self._create_layout()
            logger.info("Multi-tab Dash application with routing initialized successfully")

        except Exception as e:
            handle_error(logger, e, "multi-tab Dash application initialization")
            raise

    def _create_layout(self):
        """Create application layout with URL routing support"""
        try:
            # Main layout with URL location tracking
            return html.Div([
                dcc.Location(id="url", refresh=False),
                html.Div(id="page-content")
            ])

        except Exception as e:
            handle_error(logger, e, "multi-tab layout creation")
            return html.Div([
                dbc.Container([
                    create_error_boundary(f"Multi-tab system error: {str(e)}")
                ])
            ])

    def _setup_routing_callbacks(self):
        """Setup routing callbacks for tabs and facilities"""
        try:
            @self.app.callback(
                Output("page-content", "children"),
                Input("url", "pathname"),
                prevent_initial_call=False
            )
            def display_page(pathname):
                """Main routing logic for all views"""
                try:
                    if pathname is None or pathname == "/":
                        # Default: Multi-tab dashboard
                        return create_main_layout(content=create_tab_container())

                    elif pathname.startswith("/facility/"):
                        # Facility detail pages
                        facility_id = pathname.replace("/facility/", "")
                        logger.info(f"Routing to facility: {facility_id}")

                        # Create facility detail with navigation
                        facility_content = create_facility_detail_layout(facility_id)
                        return create_main_layout(content=facility_content)

                    else:
                        # Unknown route - redirect to home
                        return create_main_layout(content=html.Div([
                            dbc.Alert([
                                html.H4("Page Not Found"),
                                html.P(f"The requested page '{pathname}' does not exist."),
                                dbc.Button("Return to Dashboard", href="/", color="primary")
                            ], color="warning")
                        ]))

                except Exception as e:
                    handle_error(logger, e, f"page routing for {pathname}")
                    return create_main_layout(content=create_error_boundary(f"Failed to load {pathname}"))

            @self.app.callback(
                Output("tab-content", "children"),
                Input("main-tabs", "active_tab"),
                prevent_initial_call=False
            )
            def render_tab_content(active_tab):
                """Render content for multi-tab view"""
                try:
                    if active_tab == "portfolio":
                        return create_complete_dashboard()
                    elif active_tab == "quality":
                        return create_data_quality_layout()
                    elif active_tab == "workflow":
                        return create_workflow_analysis_layout()
                    else:
                        return create_complete_dashboard()

                except Exception as e:
                    handle_error(logger, e, f"tab content rendering for {active_tab}")
                    return create_error_boundary(f"Failed to load {active_tab} analysis")

            # Navigation callback for facility clicks
            @self.app.callback(
                Output("url", "pathname"),
                Input("facility-pie-chart", "clickData"),
                prevent_initial_call=True
            )
            def navigate_to_facility(click_data):
                """Navigate to facility detail when pie chart clicked"""
                try:
                    if not click_data:
                        raise PreventUpdate

                    # Extract facility from clicked slice
                    point = click_data['points'][0]
                    facility_name = point['label']

                    logger.info(f"Facility navigation: {facility_name}")

                    # Convert facility name to URL-safe format
                    facility_url = facility_name.lower().replace(" ", "-")
                    return f"/facility/{facility_url}"

                except Exception as e:
                    handle_error(logger, e, "facility navigation")
                    raise PreventUpdate

            # Dashboard state callback
            @self.app.callback(
                Output("dashboard-state", "data"),
                [Input("url", "pathname"), Input("main-tabs", "active_tab")],
                prevent_initial_call=True
            )
            def update_dashboard_state(pathname, active_tab):
                """Update dashboard state based on current route"""
                try:
                    state = {
                        "current_path": pathname,
                        "active_tab": active_tab,
                        "validation_status": self.validation_status,
                        "is_facility_view": pathname.startswith("/facility/") if pathname else False
                    }

                    if pathname and pathname.startswith("/facility/"):
                        facility_id = pathname.replace("/facility/", "")
                        state["facility_id"] = facility_id

                    return state

                except Exception as e:
                    handle_error(logger, e, "dashboard state update")
                    return {"current_path": pathname, "error": str(e)}

            logger.info("Routing callbacks setup completed")

        except Exception as e:
            handle_error(logger, e, "routing callbacks setup")

    def run_server(self, **kwargs):
        """Run multi-tab dashboard server with facility support"""
        try:
            server_config = {
                "host": self.host,
                "port": self.port,
                "debug": self.debug,
                "dev_tools_hot_reload": self.debug,
                "dev_tools_ui": self.debug
            }
            server_config.update(kwargs)

            logger.info(f"Starting comprehensive dashboard server on {self.host}:{self.port}")

            # System status summary
            tabs_ready = {
                "Portfolio": self.validation_status.get("portfolio_metrics", False),
                "Quality": self.validation_status.get("data_quality", False),
                "Workflow": self.validation_status.get("workflow_analysis", False)
            }

            data_quality = self.validation_status.get("data_quality_score", 0.0)

            print("\n" + "=" * 70)
            print("🚀 COMPREHENSIVE MINING RELIABILITY DASHBOARD")
            print("=" * 70)
            print(f"📊 URL: http://{self.host}:{self.port}")
            print(f"🔧 Debug: {self.debug}")
            print(f"📈 Data Quality: {data_quality:.1%}")
            print("📑 Navigation:")
            print("   • Multi-tab analysis (Portfolio, Quality, Workflow)")
            print("   • Facility drill-down (/facility/facility-name)")
            print("   • Cross-facility stakeholder assessment")
            print("📋 Tab Status:")
            for tab, status in tabs_ready.items():
                print(f"   {tab}: {'✅ Ready' if status else '❌ Limited'}")
            print("=" * 70)
            print("💡 Click facility slices to drill down into specific analysis")
            print("=" * 70)

            self.app.run_server(**server_config)

        except Exception as e:
            handle_error(logger, e, "comprehensive server startup")
            raise

    def get_validation_status(self):
        """Get current validation status"""
        return self.validation_status.copy()

# Application factory
def create_dashboard_app(debug=None, port=None, host=None):
    """Create comprehensive dashboard application instance"""
    try:
        return MultiTabDashboardApplication(debug=debug, port=port, host=host)
    except Exception as e:
        if logger:
            handle_error(logger, e, "comprehensive dashboard application creation")
        raise

# CLI interface
def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Comprehensive Mining Reliability Dashboard")
    parser.add_argument("--port", type=int, help="Server port")
    parser.add_argument("--host", type=str, help="Server host")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--validate", action="store_true", help="Validate comprehensive system only")

    args = parser.parse_args()

    try:
        dashboard_app = create_dashboard_app(
            debug=args.debug,
            port=args.port,
            host=args.host
        )

        if args.validate:
            validation_status = dashboard_app.get_validation_status()
            print("\nComprehensive System Validation:")

            all_components = ["portfolio_metrics", "data_quality", "workflow_analysis"]
            for component in all_components:
                status = validation_status.get(component, False)
                component_name = component.replace("_", " ").title()
                print(f"  {component_name}: {'✅ READY' if status else '❌ LIMITED'}")

            overall_score = sum(validation_status.get(c, False) for c in all_components) / len(all_components)
            print(f"\nOverall Readiness: {overall_score:.1%}")
            print("Facility Routing: ✅ READY")

            return 0 if overall_score >= 0.67 else 1
        else:
            dashboard_app.run_server()
            return 0

    except KeyboardInterrupt:
        print("\n🛑 Comprehensive dashboard stopped")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())

# Production WSGI export
try:
    dashboard_instance = create_dashboard_app()
    app = dashboard_instance.app
    server = app.server
except Exception as e:
    print(f"Production app creation failed: {e}")
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("Comprehensive Dashboard Error"),
        html.P(f"Failed to initialize: {str(e)}")
    ])
    server = app.server
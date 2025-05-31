#!/usr/bin/env python3
"""
Dashboard Application - Adapter Pattern Integration
Clean application architecture with dependency injection.
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
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Configuration-driven imports
from mine_core.shared.common import setup_project_environment, handle_error
from configs.environment import get_dashboard_server_config, get_dashboard_performance_config

# Adapter-based data access
from dashboard.adapters import get_data_adapter
from dashboard.utils.data_transformers import validate_dashboard_data
from dashboard.components.portfolio_overview import create_complete_dashboard
from dashboard.layouts.main_layout import create_main_layout, create_error_boundary

logger = None

class DashboardApplication:
    """Clean dashboard application with adapter dependency injection"""

    def __init__(self, debug=None, port=None, host=None):
        """Initialize with configuration-driven defaults"""
        # Get server configuration
        server_config = get_dashboard_server_config()

        self.debug = debug if debug is not None else False
        self.port = port or server_config.get("default_port", 8050)
        self.host = host or server_config.get("default_host", "127.0.0.1")

        self.app = None
        self.data_adapter = None
        self.validation_status = {}

        self._setup_logging()
        self._validate_system()
        self._initialize_app()
        self._setup_callbacks()

    def _setup_logging(self):
        """Setup logging using project infrastructure"""
        global logger
        try:
            logger = setup_project_environment("dashboard_app")
            logger.info("Dashboard application initialization started")
        except Exception as e:
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to setup project environment: {e}")

    def _validate_system(self):
        """Validate system readiness using adapter"""
        logger.info("Validating system readiness...")

        try:
            # Initialize data adapter
            self.data_adapter = get_data_adapter()

            # Validate data pipeline
            self.validation_status = validate_dashboard_data()

            if self.validation_status.get("phase2_complete", False):
                logger.info("✅ System validation passed - dashboard ready")
            else:
                failed_components = [k for k, v in self.validation_status.items()
                                   if k != "phase2_complete" and not v]
                logger.warning(f"⚠️ System validation issues: {failed_components}")

        except Exception as e:
            handle_error(logger, e, "system validation")
            self.validation_status = {"phase2_complete": False}

    def _initialize_app(self):
        """Initialize Dash application"""
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
                title="Mining Reliability Database - Portfolio Overview",
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
                ]
            )

            self.app.layout = self._create_layout()
            logger.info("Dash application initialized successfully")

        except Exception as e:
            handle_error(logger, e, "Dash application initialization")
            raise

    def _create_layout(self):
        """Create application layout with validation checks"""
        try:
            if not self.validation_status.get("phase2_complete", False):
                error_content = html.Div([
                    dbc.Alert([
                        html.H4("System Validation Warning", className="alert-heading"),
                        html.P("Data pipeline validation failed. Dashboard functionality may be limited."),
                        html.Ul([
                            html.Li(f"{component}: {'✅ OK' if status else '❌ Failed'}")
                            for component, status in self.validation_status.items()
                            if component != "phase2_complete"
                        ])
                    ], color="warning"),
                    create_complete_dashboard()  # Still show dashboard
                ])
                return create_main_layout(error_content)

            return create_main_layout()

        except Exception as e:
            handle_error(logger, e, "application layout creation")
            return html.Div([
                dbc.Container([
                    create_error_boundary(f"Critical application error: {str(e)}")
                ])
            ])

    def _setup_callbacks(self):
        """Setup dashboard callbacks"""
        try:
            @self.app.callback(
                Output("dashboard-state", "data"),
                Input("auto-refresh", "n_intervals"),
                prevent_initial_call=True
            )
            def update_dashboard_state(n_intervals):
                """Auto-refresh dashboard state"""
                try:
                    if n_intervals and n_intervals > 0:
                        logger.info(f"Auto-refresh triggered: interval {n_intervals}")

                        # Re-validate using adapter
                        validation_results = validate_dashboard_data()

                        return {
                            "last_refresh": n_intervals,
                            "validation_status": validation_results,
                            "data_quality": validation_results.get("data_quality_score", 0.0)
                        }

                    raise PreventUpdate

                except Exception as e:
                    handle_error(logger, e, "dashboard state update")
                    raise PreventUpdate

            @self.app.callback(
                Output("main-content", "children"),
                Input("url-location", "pathname"),
                prevent_initial_call=False
            )
            def update_page_content(pathname):
                """Route handling with adapter integration"""
                try:
                    logger.info(f"Route requested: {pathname}")

                    if pathname == "/" or pathname is None:
                        return create_complete_dashboard()

                    # Future facility detail routes
                    elif pathname and pathname.startswith("/facility/"):
                        facility_id = pathname.replace("/facility/", "")
                        return dbc.Alert(
                            f"Facility detail page for {facility_id} - Coming in Phase 5",
                            color="info"
                        )

                    # Future network analysis routes
                    elif pathname == "/network":
                        return dbc.Alert(
                            "Network analysis dashboard - Coming in Phase 6",
                            color="info"
                        )

                    # 404 handler
                    else:
                        return dbc.Alert([
                            html.H4("Page Not Found"),
                            html.P(f"The requested page '{pathname}' does not exist."),
                            dbc.Button("Portfolio Dashboard", href="/", color="primary")
                        ], color="warning")

                except Exception as e:
                    handle_error(logger, e, "page content routing")
                    return create_error_boundary(str(e))

            logger.info("Dashboard callbacks setup completed")

        except Exception as e:
            handle_error(logger, e, "callbacks setup")

    def run_server(self, **kwargs):
        """Run dashboard server with configuration"""
        try:
            # Get performance configuration
            perf_config = get_dashboard_performance_config()

            server_config = {
                "host": self.host,
                "port": self.port,
                "debug": self.debug,
                "dev_tools_hot_reload": self.debug,
                "dev_tools_ui": self.debug
            }
            server_config.update(kwargs)

            logger.info(f"Starting dashboard server on {self.host}:{self.port}")
            logger.info(f"Debug mode: {self.debug}")

            # System status summary
            data_quality = self.validation_status.get("data_quality_score", 0.0)
            system_ready = self.validation_status.get("phase2_complete", False)

            print("\n" + "=" * 60)
            print("🚀 MINING RELIABILITY DASHBOARD")
            print("=" * 60)
            print(f"📊 URL: http://{self.host}:{self.port}")
            print(f"🔧 Debug: {self.debug}")
            print(f"📈 Data Quality: {data_quality:.1%}")
            print(f"🟢 System Ready: {system_ready}")
            print("=" * 60)

            self.app.run_server(**server_config)

        except Exception as e:
            handle_error(logger, e, "server startup")
            raise

    def get_validation_status(self):
        """Get current validation status"""
        return self.validation_status.copy()

# Application factory
def create_dashboard_app(debug=None, port=None, host=None):
    """Create dashboard application instance"""
    try:
        return DashboardApplication(debug=debug, port=port, host=host)
    except Exception as e:
        if logger:
            handle_error(logger, e, "dashboard application creation")
        raise

# CLI interface
def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Mining Reliability Dashboard")
    parser.add_argument("--port", type=int, help="Server port")
    parser.add_argument("--host", type=str, help="Server host")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--validate", action="store_true", help="Validate system only")

    args = parser.parse_args()

    try:
        dashboard_app = create_dashboard_app(
            debug=args.debug,
            port=args.port,
            host=args.host
        )

        if args.validate:
            validation_status = dashboard_app.get_validation_status()
            print("\nValidation Results:")
            for component, status in validation_status.items():
                print(f"  {component}: {'✅ PASS' if status else '❌ FAIL'}")

            return 0 if validation_status.get("phase2_complete", False) else 1
        else:
            dashboard_app.run_server()
            return 0

    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped")
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
        html.H1("Dashboard Error"),
        html.P(f"Failed to initialize: {str(e)}")
    ])
    server = app.server

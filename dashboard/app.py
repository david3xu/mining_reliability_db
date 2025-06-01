#!/usr/bin/env python3
"""
Dashboard Application - Interactive Implementation
Clean application architecture with full interaction support.
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

# Configuration and utilities
from mine_core.shared.common import setup_project_environment, handle_error
from configs.environment import get_dashboard_server_config, get_dashboard_performance_config

# Interactive components
from dashboard.adapters import get_data_adapter
from dashboard.utils.data_transformers import validate_dashboard_data
from dashboard.components.portfolio_overview import create_complete_dashboard
from dashboard.layouts.main_layout import create_main_layout, create_error_boundary

# Interactive system
from dashboard.callbacks.interaction_handlers import interaction_manager

logger = None

class InteractiveDashboardApplication:
    """Enhanced dashboard application with full interaction support"""

    def __init__(self, debug=None, port=None, host=None):
        """Initialize with configuration-driven defaults"""
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
        self._setup_core_callbacks()
        self._register_interactions()

    def _setup_logging(self):
        """Setup logging using project infrastructure"""
        global logger
        try:
            logger = setup_project_environment("interactive_dashboard_app")
            logger.info("Interactive dashboard application initialization started")
        except Exception as e:
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to setup project environment: {e}")

    def _validate_system(self):
        """Validate system readiness using adapter"""
        logger.info("Validating interactive system readiness...")

        try:
            self.data_adapter = get_data_adapter()
            self.validation_status = validate_dashboard_data()

            if self.validation_status.get("phase2_complete", False):
                logger.info("✅ System validation passed - interactive dashboard ready")
            else:
                failed_components = [k for k, v in self.validation_status.items()
                                   if k != "phase2_complete" and not v]
                logger.warning(f"⚠️ System validation issues: {failed_components}")

        except Exception as e:
            handle_error(logger, e, "interactive system validation")
            self.validation_status = {"phase2_complete": False}

    def _initialize_app(self):
        """Initialize Dash application with interactive features"""
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
                title="Mining Reliability Database - Interactive Portfolio",
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
                    {"name": "description", "content": "Interactive Mining Reliability Dashboard"}
                ]
            )

            self.app.layout = self._create_layout()
            logger.info("Interactive Dash application initialized successfully")

        except Exception as e:
            handle_error(logger, e, "interactive Dash application initialization")
            raise

    def _create_layout(self):
        """Create application layout with interaction validation"""
        try:
            if not self.validation_status.get("phase2_complete", False):
                error_content = html.Div([
                    dbc.Alert([
                        html.H4("Interactive System Status", className="alert-heading"),
                        html.P("Interactive features may be limited due to data validation issues."),
                        html.Ul([
                            html.Li(f"{component}: {'✅ Ready' if status else '❌ Limited'}")
                            for component, status in self.validation_status.items()
                            if component != "phase2_complete"
                        ]),
                        html.P("Dashboard will function with reduced interactivity.", className="mb-0")
                    ], color="warning"),
                    create_complete_dashboard()
                ])
                return create_main_layout(error_content)

            return create_main_layout()

        except Exception as e:
            handle_error(logger, e, "interactive layout creation")
            return html.Div([
                dbc.Container([
                    create_error_boundary(f"Interactive system error: {str(e)}")
                ])
            ])

    def _setup_core_callbacks(self):
        """Setup core application callbacks"""
        try:
            @self.app.callback(
                Output("dashboard-state", "data"),
                Input("auto-refresh", "n_intervals"),
                prevent_initial_call=True
            )
            def update_dashboard_state(n_intervals):
                """Auto-refresh dashboard state with interaction tracking"""
                try:
                    if n_intervals and n_intervals > 0:
                        logger.info(f"Auto-refresh triggered: interval {n_intervals}")

                        validation_results = validate_dashboard_data()

                        return {
                            "last_refresh": n_intervals,
                            "validation_status": validation_results,
                            "data_quality": validation_results.get("data_quality_score", 0.0),
                            "interactive_mode": True
                        }

                    raise PreventUpdate

                except Exception as e:
                    handle_error(logger, e, "interactive dashboard state update")
                    raise PreventUpdate

            @self.app.callback(
                Output("main-content", "children"),
                Input("url-location", "pathname"),
                prevent_initial_call=False
            )
            def update_page_content(pathname):
                """Enhanced route handling with interaction support"""
                try:
                    logger.info(f"Interactive route requested: {pathname}")

                    if pathname == "/" or pathname is None:
                        return create_complete_dashboard()

                    elif pathname and pathname.startswith("/facility/"):
                        facility_id = pathname.replace("/facility/", "")
                        from dashboard.components.facility_detail import create_facility_detail_layout
                        return create_facility_detail_layout(facility_id)

                    elif pathname == "/network":
                        from dashboard.components.graph_visualizer import create_network_analysis_dashboard
                        return create_network_analysis_dashboard()

                    elif pathname.startswith("/detail/"):
                        # Future: Detail page implementation
                        return dbc.Alert(
                            "Detail pages coming soon - Enhanced analytics in development",
                            color="info"
                        )

                    else:
                        return dbc.Alert([
                            html.H4("Page Not Found"),
                            html.P(f"The requested page '{pathname}' does not exist."),
                            dbc.ButtonGroup([
                                dbc.Button("Portfolio Dashboard", href="/", color="primary", size="sm"),
                                dbc.Button("Network Analysis", href="/network", color="secondary", size="sm")
                            ])
                        ], color="warning")

                except Exception as e:
                    handle_error(logger, e, "interactive page content routing")
                    return create_error_boundary(str(e))

            logger.info("Core interactive callbacks setup completed")

        except Exception as e:
            handle_error(logger, e, "core callbacks setup")

    def _register_interactions(self):
        """Register interactive callback system"""
        try:
            logger.info("Registering interactive callback system...")

            # Register all interaction callbacks
            interaction_manager.register_callbacks(self.app)

            # Additional interaction feedback callback
            @self.app.callback(
                Output("interaction-toast", "is_open"),
                Output("interaction-toast", "children"),
                [Input("chart-interaction-store", "data"),
                 Input("table-interaction-store", "data"),
                 Input("card-interaction-store", "data")],
                prevent_initial_call=True
            )
            def show_interaction_feedback(chart_data, table_data, card_data):
                """Show feedback for user interactions"""
                try:
                    interaction_data = None

                    if dash.callback_context.triggered:
                        trigger_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

                        if trigger_id == 'chart-interaction-store' and chart_data:
                            interaction_data = chart_data
                        elif trigger_id == 'table-interaction-store' and table_data:
                            interaction_data = table_data
                        elif trigger_id == 'card-interaction-store' and card_data:
                            interaction_data = card_data

                    if interaction_data:
                        action = interaction_data.get('action', 'unknown')
                        target = interaction_data.get('facility_id') or interaction_data.get('detail_type', 'data')

                        feedback_messages = {
                            'navigate_facility': f"Navigating to {target} facility analysis...",
                            'explore_field_type': f"Analyzing {target} field distribution...",
                            'explore_records': f"Loading detailed {target} analysis...",
                            'explore_facilities': f"Opening {target} comparison view...",
                            'explore_timeline': f"Generating {target} analysis..."
                        }

                        message = feedback_messages.get(action, f"Loading {target} analysis...")

                        return True, [
                            html.Div([
                                html.I(className="fas fa-sync fa-spin me-2"),
                                message
                            ])
                        ]

                    return False, []

                except Exception as e:
                    handle_error(logger, e, "interaction feedback")
                    return False, []

            logger.info("Interactive callback system registered successfully")

        except Exception as e:
            handle_error(logger, e, "interaction system registration")

    def run_server(self, **kwargs):
        """Run interactive dashboard server"""
        try:
            perf_config = get_dashboard_performance_config()

            server_config = {
                "host": self.host,
                "port": self.port,
                "debug": self.debug,
                "dev_tools_hot_reload": self.debug,
                "dev_tools_ui": self.debug
            }
            server_config.update(kwargs)

            logger.info(f"Starting interactive dashboard server on {self.host}:{self.port}")

            # Enhanced system status
            data_quality = self.validation_status.get("data_quality_score", 0.0)
            system_ready = self.validation_status.get("phase2_complete", False)
            interactive_ready = all([
                system_ready,
                hasattr(self, 'data_adapter'),
                self.app is not None
            ])

            print("\n" + "=" * 70)
            print("🚀 INTERACTIVE MINING RELIABILITY DASHBOARD")
            print("=" * 70)
            print(f"📊 URL: http://{self.host}:{self.port}")
            print(f"🔧 Debug: {self.debug}")
            print(f"📈 Data Quality: {data_quality:.1%}")
            print(f"🟢 System Ready: {system_ready}")
            print(f"🎯 Interactive: {interactive_ready}")
            print("=" * 70)
            print("💡 Click dashboard elements to explore data")
            print("=" * 70)

            self.app.run_server(**server_config)

        except Exception as e:
            handle_error(logger, e, "interactive server startup")
            raise

    def get_validation_status(self):
        """Get current validation status"""
        return self.validation_status.copy()

# Application factory
def create_dashboard_app(debug=None, port=None, host=None):
    """Create interactive dashboard application instance"""
    try:
        return InteractiveDashboardApplication(debug=debug, port=port, host=host)
    except Exception as e:
        if logger:
            handle_error(logger, e, "interactive dashboard application creation")
        raise

# CLI interface
def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Interactive Mining Reliability Dashboard")
    parser.add_argument("--port", type=int, help="Server port")
    parser.add_argument("--host", type=str, help="Server host")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--validate", action="store_true", help="Validate interactive system only")

    args = parser.parse_args()

    try:
        dashboard_app = create_dashboard_app(
            debug=args.debug,
            port=args.port,
            host=args.host
        )

        if args.validate:
            validation_status = dashboard_app.get_validation_status()
            print("\nInteractive System Validation:")
            for component, status in validation_status.items():
                print(f"  {component}: {'✅ READY' if status else '❌ LIMITED'}")

            interactive_score = sum(validation_status.values()) / len(validation_status)
            print(f"\nInteractive Readiness: {interactive_score:.1%}")

            return 0 if validation_status.get("phase2_complete", False) else 1
        else:
            dashboard_app.run_server()
            return 0

    except KeyboardInterrupt:
        print("\n🛑 Interactive dashboard stopped")
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
        html.H1("Interactive Dashboard Error"),
        html.P(f"Failed to initialize: {str(e)}")
    ])
    server = app.server

#!/usr/bin/env python3
"""
Purified Dashboard Application - Pure Bootstrap Architecture
Clean application entry point with routing delegation and adapter validation.
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
from dash.exceptions import PreventUpdate

# Adapter validation
from dashboard.adapters import get_config_adapter, get_data_adapter
from dashboard.routing.navigation_builder import get_navigation_builder

# Pure routing and navigation
from dashboard.routing.url_manager import get_url_manager
from dashboard.utils.styling import get_dashboard_styles
from mine_core.shared.common import handle_error, setup_project_environment

logger = None


class PurifiedDashboardApp:
    """Clean application bootstrap with routing delegation"""

    def __init__(self, debug=None, port=None, host=None):
        self.debug = debug if debug is not None else False
        self.port = port or 8050
        self.host = host or "127.0.0.1"

        self._setup_logging()
        self._validate_adapters()
        self._initialize_app()
        self._setup_routing()

    def _setup_logging(self):
        """Initialize logging through project infrastructure"""
        global logger
        try:
            logger = setup_project_environment("purified_dashboard")
            logger.info("Purified dashboard initialization started")
        except Exception as e:
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.warning(f"Project environment setup failed: {e}")

    def _validate_adapters(self):
        """Validate adapter layer availability"""
        try:
            data_adapter = get_data_adapter()
            config_adapter = get_config_adapter()

            validation = data_adapter.get_data_quality_validation()
            if validation.overall_status:
                logger.info("✅ Adapter layer validated")
            else:
                logger.warning("⚠️ Adapter validation issues detected")

        except Exception as e:
            handle_error(logger, e, "adapter validation")

    def _initialize_app(self):
        """Initialize Dash application with clean architecture"""
        try:
            # Use centralized styling utility
            styling = get_dashboard_styles()

            self.app = dash.Dash(
                __name__,
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    {
                        "href": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
                        "rel": "stylesheet",
                    },
                    "/dashboard/assets/custom_styles.css",
                ],
                suppress_callback_exceptions=True,
                title="Mining Reliability Database",
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
                    {"name": "description", "content": "Professional Mining Reliability Analysis"},
                ],
            )

            self.app.layout = self._create_layout()
            logger.info("Purified application initialized")

        except Exception as e:
            handle_error(logger, e, "application initialization")
            raise

    def _create_layout(self):
        """Create application layout with navigation delegation"""
        navigation_builder = get_navigation_builder()
        # Use centralized styling utility for main layout background
        styling = get_dashboard_styles()

        return html.Div(
            [
                dcc.Location(id="url", refresh=False),
                navigation_builder.build_main_navigation(),
                html.Div(
                    id="page-content",
                    className="container-fluid p-4",
                    style=styling["main_container"],
                ),
            ]
        )

    def _setup_routing(self):
        """Setup routing through URL manager"""
        url_manager = get_url_manager()

        @self.app.callback(
            Output("page-content", "children"), Input("url", "pathname"), prevent_initial_call=False
        )
        def route_page(pathname):
            """Route pages through URL manager"""
            try:
                if not url_manager.validate_route(pathname):
                    return self._create_not_found_page(pathname)

                route_config = url_manager.resolve_route(pathname)
                return self._load_page_component(route_config)

            except Exception as e:
                handle_error(logger, e, f"routing for {pathname}")
                return self._create_error_page(str(e))

    def _load_page_component(self, route_config: dict):
        """Load page component based on route configuration"""
        component_name = route_config.get("component")

        try:
            if component_name == "portfolio_overview":
                from dashboard.components.portfolio_overview import create_complete_dashboard

                return create_complete_dashboard()

            elif component_name == "data_quality_layout":
                from dashboard.components.data_quality import create_data_quality_layout

                return create_data_quality_layout()

            elif component_name == "workflow_analysis_layout":
                from dashboard.components.workflow_analysis import create_workflow_analysis_layout

                return create_workflow_analysis_layout()

            elif component_name == "historical_records_page":
                from dashboard.components.portfolio_overview import create_historical_records_page

                return create_historical_records_page()

            elif component_name == "facilities_distribution_page":
                from dashboard.components.portfolio_overview import (
                    create_facilities_distribution_page,
                )

                return create_facilities_distribution_page()

            elif component_name == "data_types_distribution_page":
                from dashboard.components.portfolio_overview import (
                    create_data_types_distribution_page,
                )

                return create_data_types_distribution_page()

            elif component_name == "facility_detail_layout":
                facility_id = route_config.get("facility_id")
                from dashboard.components.facility_detail import create_facility_detail_layout

                return create_facility_detail_layout(facility_id)

            elif component_name == "facilities_summary":
                return self._create_facilities_summary()

            else:
                return self._create_not_found_page(route_config.get("page", "unknown"))

        except Exception as e:
            handle_error(logger, e, f"component loading for {component_name}")
            return self._create_error_page(f"Component {component_name} failed to load")

    def _create_not_found_page(self, pathname):
        """Create 404 page"""
        return dbc.Container(
            [
                dbc.Alert(
                    [
                        html.H4("Page Not Found"),
                        html.P(f"Route '{pathname}' does not exist"),
                        dbc.Button("Return to Portfolio", href="/", color="primary"),
                    ],
                    color="warning",
                )
            ]
        )

    def _create_error_page(self, error_message):
        """Create error page"""
        return dbc.Container(
            [
                dbc.Alert(
                    [
                        html.H4("Application Error"),
                        html.P(error_message),
                        dbc.Button("Return to Portfolio", href="/", color="secondary"),
                    ],
                    color="danger",
                )
            ]
        )

    def _create_facilities_summary(self):
        """Create facilities summary page"""
        try:
            data_adapter = get_data_adapter()
            portfolio_data = data_adapter.get_portfolio_metrics()
            facility_data = data_adapter.get_facility_breakdown()

            return html.Div(
                [
                    html.H2("Four Facilities Summary", className="text-primary mb-4"),
                    html.P(
                        f"Analysis across {facility_data.total_records:,} records from {len(facility_data.labels)} facilities"
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.H4(label, className="card-title"),
                                                    html.H2(f"{value:,}", className="text-success"),
                                                    html.P(
                                                        f"{percentage:.1f}% of total",
                                                        className="text-muted",
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                md=3,
                            )
                            for label, value, percentage in zip(
                                facility_data.labels,
                                facility_data.values,
                                facility_data.percentages,
                            )
                        ]
                    ),
                ]
            )

        except Exception as e:
            handle_error(logger, e, "facilities summary creation")
            return self._create_error_page("Facilities summary unavailable")

    def run_server(self, **kwargs):
        """Run dashboard server with status reporting"""
        try:
            server_config = {"host": self.host, "port": self.port, "debug": self.debug}
            server_config.update(kwargs)

            print("\n" + "=" * 60)
            print("🚀 PURIFIED MINING RELIABILITY DASHBOARD")
            print("=" * 60)
            print(f"📊 URL: http://{self.host}:{self.port}")
            print(f"🏗️ Architecture: Core → Adapter → Component")
            print(f"🔧 Debug Mode: {self.debug}")
            print("=" * 60)
            print("🧭 Navigation:")
            print("   📋 Portfolio Overview (/)")
            print("   🔍 Data Quality (/data-quality)")
            print("   🔄 Workflow Analysis (/workflow)")
            print("   📊 Summary (/summary)")
            print("   🏭 Facility Analysis (dynamic)")
            print("=" * 60)

            self.app.run_server(**server_config)

        except Exception as e:
            handle_error(logger, e, "server startup")
            raise


def create_app(debug=None, port=None, host=None):
    """Application factory"""
    try:
        return PurifiedDashboardApp(debug=debug, port=port, host=host)
    except Exception as e:
        if logger:
            handle_error(logger, e, "application creation")
        raise


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Purified Mining Reliability Dashboard")
    parser.add_argument("--port", type=int, help="Server port")
    parser.add_argument("--host", type=str, help="Server host")
    parser.add_argument("--debug", action="store_true", help="Debug mode")

    args = parser.parse_args()

    try:
        app = create_app(debug=args.debug, port=args.port, host=args.host)
        app.run_server()
        return 0

    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

# Production WSGI
try:
    production_app = create_app()
    app = production_app.app
    server = app.server
except Exception as e:
    print(f"Production app creation failed: {e}")
    app = dash.Dash(__name__)
    app.layout = html.Div("Production initialization failed")
    server = app.server

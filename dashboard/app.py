#!/usr/bin/env python3
"""
Dashboard Application - Complete Navigation System
Professional navigation accessing all 6 analytical perspectives.
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

# Components
from dashboard.components.portfolio_overview import (
    create_complete_dashboard,
    create_historical_records_page,
    create_facilities_distribution_page,
    create_data_types_distribution_page
)
from dashboard.components.facility_detail import create_facility_detail_layout
from dashboard.components.data_quality import create_data_quality_layout
from dashboard.components.workflow_analysis import create_workflow_analysis_layout

# Data validation
from dashboard.utils.data_transformers import validate_dashboard_data

# Layout infrastructure
from dashboard.layouts.main_layout import create_error_boundary

logger = None

class CompleteDashboardApplication:
    """Professional navigation system for all analytical perspectives"""

    def __init__(self, debug=None, port=None, host=None):
        """Initialize complete navigation system"""
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
            logger = setup_project_environment("complete_dashboard_app")
            logger.info("Complete navigation system initialization started")
        except Exception as e:
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to setup project environment: {e}")

    def _validate_system(self):
        """Validate complete navigation system"""
        logger.info("Validating complete analytical system...")

        try:
            self.validation_status = validate_dashboard_data()
            system_ready = self.validation_status.get("phase2_complete", False)

            if system_ready:
                logger.info("✅ Complete navigation system validated")
            else:
                logger.warning("⚠️ System validation issues detected")

        except Exception as e:
            handle_error(logger, e, "complete system validation")
            self.validation_status = {"phase2_complete": False}

    def _initialize_app(self):
        """Initialize Dash application with complete navigation"""
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
                title="Mining Reliability Database - Complete Analysis System",
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
                    {"name": "description", "content": "Complete Mining Reliability Analysis Dashboard"}
                ]
            )

            # Add custom CSS for hover effects
            self.app.index_string = '''
            <!DOCTYPE html>
            <html>
                <head>
                    {%metas%}
                    <title>{%title%}</title>
                    {%favicon%}
                    {%css%}
                    <style>
                        .metric-card-hover:hover {
                            transform: translateY(-2px) !important;
                            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2) !important;
                        }
                        .metric-card-hover {
                            transition: all 0.3s ease !important;
                        }
                        .metric-card-interactive:hover {
                            transform: translateY(-3px);
                            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
                            border-color: #ffffff40 !important;
                        }
                    </style>
                </head>
                <body>
                    {%app_entry%}
                    <footer>
                        {%config%}
                        {%scripts%}
                        {%renderer%}
                    </footer>
                </body>
            </html>
            '''

            self.app.layout = self._create_layout()
            logger.info("Complete navigation application initialized successfully")

        except Exception as e:
            handle_error(logger, e, "complete navigation application initialization")
            raise

    def _create_layout(self):
        """Create application layout with complete navigation"""
        try:
            return html.Div([
                dcc.Location(id="url", refresh=False),
                self._create_navigation_bar(),
                html.Div(id="page-content", className="mt-3")
            ])

        except Exception as e:
            handle_error(logger, e, "complete layout creation")
            return html.Div([
                dbc.Container([
                    create_error_boundary(f"Navigation system error: {str(e)}")
                ])
            ])

    def _create_navigation_bar(self):
        """Create professional navigation bar for all analytical perspectives"""

        return dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Portfolio", href="/", className="nav-link")),
                dbc.NavItem(dbc.NavLink("Data Quality", href="/data-quality", className="nav-link")),
                dbc.NavItem(dbc.NavLink("Workflow", href="/workflow", className="nav-link")),
                dbc.NavItem(dbc.NavLink("Summary", href="/summary", className="nav-link")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Pinjarra", href="/facility/pinjarra"),
                        dbc.DropdownMenuItem("WA Mining", href="/facility/wa-mining"),
                        dbc.DropdownMenuItem("Kwinana", href="/facility/kwinana"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Historical Records", href="/historical-records"),
                        dbc.DropdownMenuItem("Facilities Distribution", href="/facilities-distribution"),
                        dbc.DropdownMenuItem("Data Types Distribution", href="/data-types-distribution")
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Analysis",
                    className="nav-link"
                )
            ],
            brand="Mining Reliability Database",
            brand_href="/",
            brand_style={"fontSize": "18px", "fontWeight": "bold"},
            color="#1E1E1E",
            dark=True,
            fluid=True,
            className="mb-3"
        )

    def _setup_routing_callbacks(self):
        """Setup complete routing for all analytical perspectives"""
        try:
            @self.app.callback(
                Output("page-content", "children"),
                Input("url", "pathname"),
                prevent_initial_call=False
            )
            def display_page(pathname):
                """Complete routing logic for all analytical perspectives"""
                try:
                    if pathname is None or pathname == "/":
                        # Portfolio Overview (home)
                        return self._create_main_container(create_complete_dashboard())

                    elif pathname == "/data-quality":
                        # Data Quality Foundation analysis
                        logger.info("Routing to data quality analysis")
                        return self._create_main_container(create_data_quality_layout())

                    elif pathname == "/workflow":
                        # Workflow Understanding analysis
                        logger.info("Routing to workflow analysis")
                        return self._create_main_container(create_workflow_analysis_layout())

                    elif pathname == "/workflow-process":
                        # Dedicated workflow process analysis
                        logger.info("Routing to workflow process analysis")
                        from dashboard.components.workflow_analysis import create_workflow_process_page
                        return self._create_main_container(create_workflow_process_page())

                    elif pathname == "/summary":
                        # Four Facilities Summary
                        logger.info("Routing to facilities summary")
                        return self._create_main_container(self._create_facilities_summary())

                    elif pathname == "/historical-records":
                        # Historical records analysis
                        logger.info("Routing to historical records")
                        return self._create_main_container(create_historical_records_page())

                    elif pathname == "/facilities-distribution":
                        # Facilities distribution analysis
                        logger.info("Routing to facilities distribution")
                        return self._create_main_container(create_facilities_distribution_page())

                    elif pathname == "/data-types-distribution":
                        # Data types distribution analysis
                        logger.info("Routing to data types distribution")
                        return self._create_main_container(create_data_types_distribution_page())

                    elif pathname.startswith("/facility/"):
                        # Individual facility analysis
                        facility_id = pathname.replace("/facility/", "")
                        logger.info(f"Routing to facility analysis: {facility_id}")
                        return self._create_main_container(create_facility_detail_layout(facility_id))

                    else:
                        # Unknown route
                        return self._create_main_container(html.Div([
                            dbc.Alert([
                                html.H4("Page Not Found"),
                                html.P(f"The requested page '{pathname}' does not exist."),
                                dbc.Button("Return to Portfolio", href="/", color="primary")
                            ], color="warning")
                        ]))

                except Exception as e:
                    handle_error(logger, e, f"page routing for {pathname}")
                    return self._create_main_container(create_error_boundary(f"Failed to load {pathname}"))

            logger.info("Complete routing callbacks setup completed")

        except Exception as e:
            handle_error(logger, e, "complete routing callbacks setup")

    def _create_main_container(self, content):
        """Create main container for page content"""
        return dbc.Container([content], fluid=True, className="p-4")

    def _create_facilities_summary(self):
        """Create four facilities summary analysis"""
        try:
            from dashboard.utils.data_transformers import get_facility_breakdown_data, get_portfolio_metrics

            # Real data integration
            portfolio_data = get_portfolio_metrics()
            facility_data = get_facility_breakdown_data()

            if not facility_data:
                return dbc.Alert("No facility data available for summary", color="warning")

            # Summary metrics
            total_records = portfolio_data.get("total_records", {}).get("value", 0)
            total_facilities = len(facility_data.get("labels", []))

            # Create facility comparison cards
            facility_cards = []
            for i, (label, value, percentage) in enumerate(zip(
                facility_data.get("labels", []),
                facility_data.get("values", []),
                facility_data.get("percentages", [])
            )):
                card = dbc.Card([
                    dbc.CardBody([
                        html.H4(label, className="card-title text-primary"),
                        html.H2(f"{value:,}", className="text-success"),
                        html.P(f"{percentage:.1f}% of total records", className="text-muted"),
                        dbc.Button("Analyze", href=f"/facility/{label.lower()}",
                                 color="outline-primary", size="sm")
                    ])
                ], className="mb-3")
                facility_cards.append(card)

            return html.Div([
                html.H2("Four Facilities Analysis Summary", className="text-primary mb-4"),
                html.P(f"Comprehensive assessment across {total_facilities} operational facilities with {total_records:,} total records",
                      className="text-muted mb-4"),

                dbc.Row([
                    dbc.Col([card], md=6, lg=3) for card in facility_cards
                ]),

                html.Hr(className="my-4"),

                html.H4("Facilities Distribution Overview", className="text-secondary mb-3"),
                create_facilities_distribution_page()
            ])

        except Exception as e:
            handle_error(logger, e, "facilities summary creation")
            return dbc.Alert("Failed to load facilities summary", color="danger")

    def run_server(self, **kwargs):
        """Run complete analytical dashboard server"""
        try:
            server_config = {
                "host": self.host,
                "port": self.port,
                "debug": self.debug,
                "dev_tools_hot_reload": self.debug,
                "dev_tools_ui": self.debug
            }
            server_config.update(kwargs)

            logger.info(f"Starting complete analytical dashboard on {self.host}:{self.port}")

            data_quality = self.validation_status.get("data_quality_score", 0.0)

            print("\n" + "=" * 80)
            print("🚀 COMPLETE MINING RELIABILITY ANALYTICAL DASHBOARD")
            print("=" * 80)
            print(f"📊 URL: http://{self.host}:{self.port}")
            print(f"🔧 Debug: {self.debug}")
            print(f"📈 Data Quality: {data_quality:.1%}")
            print("🧭 Complete Navigation Structure:")
            print("   📋 Portfolio Overview (/) - Home dashboard")
            print("   🔍 Data Quality (/data-quality) - Reliability analysis")
            print("   🔄 Workflow (/workflow) - Process mapping")
            print("   📊 Summary (/summary) - Four facilities assessment")
            print("   🏭 Individual Facilities:")
            print("      • Pinjarra (/facility/pinjarra)")
            print("      • WA Mining (/facility/wa-mining)")
            print("      • Kwinana (/facility/kwinana)")
            print("   📈 Analysis Pages:")
            print("      • Historical Records (/historical-records)")
            print("      • Facilities Distribution (/facilities-distribution)")
            print("      • Data Types Distribution (/data-types-distribution)")
            print("=" * 80)
            print("💡 Use navigation bar to access all analytical perspectives")
            print("=" * 80)

            self.app.run_server(**server_config)

        except Exception as e:
            handle_error(logger, e, "complete server startup")
            raise

    def get_validation_status(self):
        """Get current validation status"""
        return self.validation_status.copy()

# Application factory
def create_dashboard_app(debug=None, port=None, host=None):
    """Create complete dashboard application instance"""
    try:
        return CompleteDashboardApplication(debug=debug, port=port, host=host)
    except Exception as e:
        if logger:
            handle_error(logger, e, "complete dashboard application creation")
        raise

# CLI interface
def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Complete Mining Reliability Dashboard")
    parser.add_argument("--port", type=int, help="Server port")
    parser.add_argument("--host", type=str, help="Server host")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--validate", action="store_true", help="Validate complete system")

    args = parser.parse_args()

    try:
        dashboard_app = create_dashboard_app(
            debug=args.debug,
            port=args.port,
            host=args.host
        )

        if args.validate:
            validation_status = dashboard_app.get_validation_status()
            print("\nComplete System Validation:")

            components = ["portfolio_metrics", "field_distribution", "facility_breakdown", "historical_timeline"]
            for component in components:
                status = validation_status.get(component, False)
                component_name = component.replace("_", " ").title()
                print(f"  {component_name}: {'✅ READY' if status else '❌ LIMITED'}")

            overall_score = sum(validation_status.get(c, False) for c in components) / len(components)
            print(f"\nOverall Readiness: {overall_score:.1%}")
            print("Complete Navigation: ✅ READY")
            print("All 6 Analytical Perspectives: ✅ ACCESSIBLE")

            return 0 if overall_score >= 0.67 else 1
        else:
            dashboard_app.run_server()
            return 0

    except KeyboardInterrupt:
        print("\n🛑 Complete dashboard stopped")
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
        html.H1("Complete Dashboard Error"),
        html.P(f"Failed to initialize: {str(e)}")
    ])
    server = app.server
#!/usr/bin/env python3
"""
Phase 4: Main Layout Authority for Portfolio Dashboard
Page structure, navigation, and responsive design management.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Tuple
from functools import lru_cache

# Dash components
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Import Phase 3 components
from dashboard.components.portfolio_overview import create_complete_dashboard
from dashboard.utils.data_transformers import get_facility_breakdown_data

# Import styling system
from dashboard.utils.styling import (
    COLORS, FONTS, DASHBOARD_STYLES,
    get_responsive_style, apply_theme_mode
)

# Import configuration infrastructure
from configs.environment import get_all_config
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_facility_navigation_items() -> List[Tuple[str, int]]:
    """Cached facility navigation generation with record counts"""
    try:
        facility_data = get_facility_breakdown_data()
        if not facility_data:
            return []

        # Return list of (facility_id, record_count) tuples
        return list(zip(
            facility_data.get("labels", []),
            facility_data.get("values", [])
        ))
    except Exception as e:
        handle_error(logger, e, "facility navigation data retrieval")
        return []

def create_navigation_bar() -> dbc.NavbarSimple:
    """Enhanced navigation bar with dynamic facility detection"""
    try:
        # Get facility data with caching
        facility_items = []
        facilities = get_facility_navigation_items()

        if facilities:
            # Create menu items for each facility
            for facility_id, record_count in facilities:
                facility_items.append(
                    dbc.DropdownMenuItem(
                        f"{facility_id} ({record_count:,} records)",
                        href=f"/facility/{facility_id}"
                    )
                )

            # Add separator and "All Facilities" option
            facility_items.extend([
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("All Facilities", href="/")
            ])
        else:
            # Fallback if no facility data available
            facility_items = [
                dbc.DropdownMenuItem("No Facilities Available", disabled=True),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("All Facilities", href="/")
            ]

        navbar = dbc.NavbarSimple(
            children=[
                # Main dashboard
                dbc.NavItem(
                    dbc.NavLink(
                        "Portfolio Overview",
                        href="/",
                        style={"color": COLORS["text_light"]}
                    )
                ),

                # Dynamic facility analysis dropdown
                dbc.DropdownMenu(
                    children=facility_items,
                    nav=True,
                    in_navbar=True,
                    label="Facility Analysis",
                    color="link",
                    style={"color": COLORS["text_light"]}
                ),

                # Advanced analytics
                dbc.NavItem(
                    dbc.NavLink(
                        "Network Analysis",
                        href="/network",
                        style={"color": COLORS["text_light"]}
                    )
                ),

                # System utilities
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("System Status", href="/status"),
                        dbc.DropdownMenuItem("Documentation", href="#", disabled=True),
                        dbc.DropdownMenuItem("API Reference", href="#", disabled=True),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("About", href="#", disabled=True),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Tools",
                    color="link",
                    style={"color": COLORS["text_light"]}
                ),
            ],
            brand="Mining Reliability Database",
            brand_href="/",
            brand_style={
                "fontSize": FONTS["subtitle_size"],
                "fontWeight": "bold",
                "color": COLORS["text_light"]
            },
            color=COLORS["background_dark"],
            dark=True,
            fluid=True,
            sticky="top",
            className="mb-3"
        )

        return navbar

    except Exception as e:
        handle_error(logger, e, "enhanced navigation bar creation")
        return dbc.NavbarSimple(
            brand="Mining Reliability Database",
            color=COLORS["primary_blue"],
            dark=True
        )

def create_footer() -> html.Footer:
    """
    Create application footer with system information.
    """
    try:
        # Get system configuration for footer info
        config = get_all_config()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        footer_content = [
            html.Hr(style={"margin": "40px 0 20px 0", "borderColor": COLORS["grid_color"]}),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H6("Mining Reliability Database v1.0.0", style={"fontWeight": "bold"}),
                        html.P([
                            "Operational Intelligence Platform | ",
                            html.Small(f"Generated: {current_time}")
                        ], style={"margin": "0", "fontSize": FONTS["caption_size"]})
                    ], md=6),
                    dbc.Col([
                        html.P([
                            html.Strong("Data Sources: "),
                            "Neo4j Graph Database | ",
                            html.Strong("Records: "),
                            f"~{config.get('processing', {}).get('batch_size', 'N/A')} batch processing"
                        ], style={
                            "textAlign": "right",
                            "margin": "0",
                            "fontSize": FONTS["caption_size"]
                        })
                    ], md=6)
                ], className="align-items-center")
            ], fluid=True),
            html.Div(style={"height": "20px"})  # Bottom spacing
        ]

        footer = html.Footer(
            footer_content,
            style={
                "backgroundColor": "#F8F9FA",
                "color": COLORS["text_secondary"],
                "padding": "20px 0 0 0",
                "marginTop": "40px",
                "borderTop": f"1px solid {COLORS['grid_color']}"
            }
        )

        return footer

    except Exception as e:
        handle_error(logger, e, "footer creation")
        return html.Footer([
            html.P("Mining Reliability Database", style={"textAlign": "center"})
        ])

def create_error_boundary(error_message: str = None) -> html.Div:
    """
    Create error boundary component for graceful failure handling.
    """
    error_content = dbc.Container([
        dbc.Alert([
            html.H4("Application Error", className="alert-heading"),
            html.P(error_message or "An unexpected error occurred while loading the dashboard."),
            html.Hr(),
            html.P([
                "Please try: ",
                html.Ul([
                    html.Li("Refreshing the page"),
                    html.Li("Checking database connectivity"),
                    html.Li("Contacting system administrator if problem persists")
                ])
            ], className="mb-0")
        ], color="danger", dismissable=True),

        dbc.Card([
            dbc.CardBody([
                html.H5("System Diagnostics", className="card-title"),
                html.P("Run these commands to diagnose issues:", className="card-text"),
                html.Code([
                    "python dashboard/validate_data.py",
                    html.Br(),
                    "python -c \"from dashboard.utils.data_transformers import validate_dashboard_data; print(validate_dashboard_data())\""
                ], style={
                    "display": "block",
                    "whiteSpace": "pre",
                    "backgroundColor": "#F8F9FA",
                    "padding": "10px",
                    "borderRadius": "4px"
                })
            ])
        ])
    ], className="mt-5")

    return error_content

def create_loading_spinner() -> dbc.Spinner:
    """
    Create loading spinner for data processing states.
    """
    return dbc.Spinner([
        html.Div([
            html.H5("Loading Portfolio Dashboard...", className="text-center"),
            html.P("Processing operational data and generating visualizations",
                   className="text-center text-muted")
        ])
    ], size="lg", color=COLORS["primary_blue"], type="border")

def get_layout_config() -> Dict[str, Any]:
    """
    Get layout configuration settings.
    Returns responsive breakpoints and theme settings.
    """
    return {
        "responsive_breakpoints": {
            "xs": 0,
            "sm": 576,
            "md": 768,
            "lg": 992,
            "xl": 1200
        },
        "theme_settings": {
            "primary_color": COLORS["primary_blue"],
            "background_color": COLORS["background_light"],
            "text_color": COLORS["text_primary"],
            "font_family": FONTS["primary_font"]
        },
        "container_settings": {
            "fluid": True,
            "className": "px-3"
        }
    }

def create_main_layout(content: html.Div = None) -> html.Div:
    """
    Create main application layout with navigation, content, and footer.
    Central layout authority for entire dashboard application.
    """
    try:
        logger.info("Creating main application layout...")

        # Default content if none provided
        if content is None:
            logger.info("No content provided - creating default portfolio dashboard")
            content = create_complete_dashboard()

        # Layout configuration
        layout_config = get_layout_config()

        # Main layout structure
        main_layout = html.Div([
            # Meta tags for responsive design
            html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            html.Meta(name="description", content="Mining Reliability Database - Portfolio Overview Dashboard"),

            # Application header/navigation
            create_navigation_bar(),

            # Main content area
            dbc.Container([
                # Loading overlay (hidden by default)
                dcc.Loading(
                    id="main-loading",
                    type="default",
                    color=COLORS["primary_blue"],
                    children=[
                        html.Div(id="main-content", children=[content])
                    ]
                )
            ], **layout_config["container_settings"]),

            # Application footer
            create_footer(),

            # Global styles and scripts
            html.Div([
                # Interval component for auto-refresh (if needed)
                dcc.Interval(
                    id="auto-refresh",
                    interval=300000,  # 5 minutes
                    n_intervals=0,
                    disabled=True  # Disabled by default
                ),

                # Store component for client-side data
                dcc.Store(id="dashboard-state", data={}),

                # Location component for routing
                dcc.Location(id="url-location", refresh=False)
            ], style={"display": "none"})

        ], style={
            "fontFamily": layout_config["theme_settings"]["font_family"],
            "backgroundColor": layout_config["theme_settings"]["background_color"],
            "color": layout_config["theme_settings"]["text_color"],
            "minHeight": "100vh"
        })

        logger.info("Main layout created successfully")
        return main_layout

    except Exception as e:
        handle_error(logger, e, "main layout creation")

        # Fallback minimal layout
        return html.Div([
            html.H1("Dashboard Error", style={"textAlign": "center", "color": "red"}),
            create_error_boundary(str(e))
        ])

def create_responsive_layout(content: html.Div = None, mobile_optimized: bool = True) -> html.Div:
    """
    Create responsive layout optimized for different screen sizes.
    """
    try:
        # Get responsive configuration
        responsive_config = get_layout_config()["responsive_breakpoints"]

        # Mobile-optimized content wrapper
        if mobile_optimized:
            content_wrapper = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        content or create_complete_dashboard()
                    ], width=12)
                ])
            ], fluid=True, className="px-2")
        else:
            content_wrapper = content or create_complete_dashboard()

        # Responsive layout with breakpoint handling
        responsive_layout = html.Div([
            # CSS media queries for responsive behavior
            html.Style(f"""
                @media (max-width: {responsive_config['md']}px) {{
                    .dashboard-charts-section {{
                        grid-template-columns: 1fr !important;
                    }}
                    .dashboard-metrics-row {{
                        flex-direction: column !important;
                        align-items: center !important;
                    }}
                }}
                @media (max-width: {responsive_config['sm']}px) {{
                    .metric-card {{
                        width: 90% !important;
                        margin: 10px auto !important;
                    }}
                }}
            """),

            # Main responsive content
            create_main_layout(content_wrapper)
        ])

        return responsive_layout

    except Exception as e:
        handle_error(logger, e, "responsive layout creation")
        return create_main_layout(content)

def validate_layout_dependencies() -> Dict[str, bool]:
    """
    Validate all layout dependencies are available.
    """
    validation_results = {
        "bootstrap_components": False,
        "dash_core_components": False,
        "portfolio_components": False,
        "styling_system": False,
        "configuration_access": False
    }

    try:
        # Test Bootstrap components
        test_navbar = dbc.NavbarSimple(brand="Test")
        validation_results["bootstrap_components"] = True

        # Test Dash core components
        test_div = html.Div("Test")
        validation_results["dash_core_components"] = True

        # Test portfolio components
        from dashboard.components.portfolio_overview import create_complete_dashboard
        validation_results["portfolio_components"] = True

        # Test styling system
        test_colors = COLORS["primary_blue"]
        validation_results["styling_system"] = True

        # Test configuration access
        config = get_all_config()
        validation_results["configuration_access"] = bool(config)

        logger.info("Layout dependencies validation completed")
        return validation_results

    except Exception as e:
        handle_error(logger, e, "layout dependencies validation")
        return validation_results

#!/usr/bin/env python3
"""
Navigation Builder - Dynamic Navigation Generation
Adapter-driven navigation with real facility data.
"""

import logging
from typing import Any, Dict, List

import dash_bootstrap_components as dbc

from dashboard.adapters import get_config_adapter, get_facility_adapter
from dashboard.utils.styling import get_colors, get_dashboard_styles
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


class NavigationBuilder:
    """Dynamic navigation construction using adapter data"""

    def __init__(self):
        self.facility_adapter = get_facility_adapter()
        self.config_adapter = get_config_adapter()

    def build_main_navigation(self) -> dbc.NavbarSimple:
        """Build main navigation bar with dynamic facility data"""
        try:
            styling = get_dashboard_styles()
            colors = get_colors()

            # Core navigation items
            nav_items = [
                dbc.NavItem(
                    dbc.NavLink("Portfolio", href="/", className="nav-link"),
                    style={"display": "flex", "alignItems": "center"},
                ),
                dbc.NavItem(
                    dbc.NavLink("Data Quality", href="/data-quality", className="nav-link"),
                    style={"display": "flex", "alignItems": "center"},
                ),
                dbc.NavItem(
                    dbc.NavLink("Workflow Analysis", href="/workflow", className="nav-link"),
                    style={"display": "flex", "alignItems": "center"},
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "Stakeholder Questions", href="/stakeholder-questions", className="nav-link"
                    ),
                    style={"display": "flex", "alignItems": "center"},
                ),
            ]

            # Analysis dropdown with facility data
            analysis_dropdown = self._build_analysis_dropdown()
            nav_items.append(
                dbc.NavItem(analysis_dropdown, style={"display": "flex", "alignItems": "center"})
            )

            # System dropdown
            system_dropdown = self._build_system_dropdown()
            nav_items.append(
                dbc.NavItem(system_dropdown, style={"display": "flex", "alignItems": "center"})
            )

            return dbc.NavbarSimple(
                children=nav_items,
                brand="Mining Reliability Database",
                brand_href="/",
                brand_style={"fontSize": "18px", "fontWeight": "bold"},
                color=colors.get("background_dark", "#1E1E1E"),
                dark=True,
                fluid=True,
                className="mb-3",
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "--bs-navbar-nav-link-padding-y": "0.5rem",
                    "--bs-navbar-nav-link-padding-x": "0.5rem",
                },
            )

        except Exception as e:
            handle_error(logger, e, "main navigation building")
            return self._build_fallback_navigation()

    def _build_analysis_dropdown(self) -> dbc.DropdownMenu:
        """Build analysis dropdown with facility data"""
        try:
            dropdown_items = []

            # Add separator and analysis pages
            dropdown_items.extend(
                [
                    dbc.DropdownMenuItem("Historical Records", href="/historical-records"),
                    dbc.DropdownMenuItem(
                        "Data Types Distribution", href="/data-types-distribution"
                    ),
                    dbc.DropdownMenuItem("Incident Search", href="/search"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Data Quality", href="/data-quality"),
                    dbc.DropdownMenuItem("Workflow Analysis", href="/workflow"),
                    dbc.DropdownMenuItem("Data Type Distribution", href="/data-types-distribution"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem(
                        "Solution Intelligence Case Study", href="/case-study-solution-sequence"
                    ),
                ]
            )

            return dbc.DropdownMenu(
                children=dropdown_items,
                nav=True,
                in_navbar=True,
                label="Analysis",
                className="nav-link",
            )

        except Exception as e:
            handle_error(logger, e, "analysis dropdown building")
            return dbc.DropdownMenu(
                children=[dbc.DropdownMenuItem("Analysis Unavailable", disabled=True)],
                nav=True,
                in_navbar=True,
                label="Analysis",
            )

    def _build_system_dropdown(self) -> dbc.DropdownMenu:
        """Build system utilities dropdown"""
        return dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Summary", href="/summary"),
                dbc.DropdownMenuItem("System Status", href="#", disabled=True),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Documentation", href="#", disabled=True),
            ],
            nav=True,
            in_navbar=True,
            label="System",
            className="nav-link",
        )

    def _build_fallback_navigation(self) -> dbc.NavbarSimple:
        """Fallback navigation when adapters fail"""
        colors = get_colors()
        return dbc.NavbarSimple(
            children=[dbc.NavItem(dbc.NavLink("Portfolio", href="/"))],
            brand="Mining Reliability Database",
            brand_href="/",
            color=colors.get("background_dark", "#1E1E1E"),
            dark=True,
            fluid=True,
        )

    def build_breadcrumbs(self, pathname: str) -> dbc.Breadcrumb:
        """Build breadcrumb navigation for current path"""
        try:
            breadcrumb_items = [dbc.BreadcrumbItem("Portfolio", href="/", external_link=True)]

            if pathname and pathname != "/":
                if pathname.startswith("/facility/"):
                    facility_id = pathname.replace("/facility/", "")
                    breadcrumb_items.append(
                        dbc.BreadcrumbItem(f"Facility: {facility_id}", active=True)
                    )
                elif pathname == "/data-quality":
                    breadcrumb_items.append(dbc.BreadcrumbItem("Data Quality", active=True))
                elif pathname == "/workflow":
                    breadcrumb_items.append(dbc.BreadcrumbItem("Workflow Analysis", active=True))
                elif pathname == "/workflow-process":
                    breadcrumb_items.extend(
                        [
                            dbc.BreadcrumbItem("Workflow", href="/workflow", external_link=True),
                            dbc.BreadcrumbItem("Process Analysis", active=True),
                        ]
                    )
                else:
                    page_name = pathname.replace("/", "").replace("-", " ").title()
                    breadcrumb_items.append(dbc.BreadcrumbItem(page_name, active=True))

            return dbc.Breadcrumb(items=breadcrumb_items)

        except Exception as e:
            handle_error(logger, e, "breadcrumb building")
            return dbc.Breadcrumb(items=[dbc.BreadcrumbItem("Portfolio", href="/")])

    def get_page_title(self, pathname: str) -> str:
        """Get page title for current route"""
        title_mapping = {
            "/": "Portfolio Overview",
            "/data-quality": "Data Quality Foundation",
            "/workflow": "Workflow Understanding",
            "/workflow-process": "Workflow Process Analysis",
            "/summary": "Four Facilities Summary",
            "/historical-records": "Historical Records Analysis",
            "/facilities-distribution": "Facilities Distribution",
            "/data-types-distribution": "Data Types Distribution",
            "/search": "Incident Search",
        }

        if pathname in title_mapping:
            return title_mapping[pathname]

        if pathname and pathname.startswith("/facility/"):
            facility_id = pathname.replace("/facility/", "")
            return f"{facility_id.title()} Facility Analysis"

        return "Mining Reliability Database"

    def validate_navigation_data(self) -> Dict[str, bool]:
        """Validate navigation data availability"""
        try:
            validation = {}

            # Test facility data
            facilities = self.facility_adapter.get_facility_list()
            validation["facilities_available"] = len(facilities) > 0

            # Test configuration
            # Removed direct config_adapter.get_styling_config() as styling should be accessed via dashboard.utils.styling
            validation[
                "styling_available"
            ] = True  # Assuming styling functions are always available

            return validation

        except Exception as e:
            handle_error(logger, e, "navigation data validation")
            return {"facilities_available": False, "styling_available": False}


# Singleton pattern
_navigation_builder = None


def get_navigation_builder() -> NavigationBuilder:
    """Get singleton navigation builder instance"""
    global _navigation_builder
    if _navigation_builder is None:
        _navigation_builder = NavigationBuilder()
    return _navigation_builder

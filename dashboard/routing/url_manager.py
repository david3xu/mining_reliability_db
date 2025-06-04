#!/usr/bin/env python3
"""
URL Manager - Clean Routing System
Direct URL management with adapter-driven route generation.
"""

import logging
from typing import Any, Dict, List, Optional

from dash import Input, Output, callback

# Pure adapter dependencies
from dashboard.adapters import get_data_adapter, get_facility_adapter
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)


class URLManager:
    """Direct URL routing with adapter integration"""

    def __init__(self):
        self.data_adapter = get_data_adapter()
        self.facility_adapter = get_facility_adapter()
        self.route_cache = {}

    def get_valid_routes(self) -> List[str]:
        """Get all valid application routes"""
        base_routes = [
            "/",
            "/data-quality",
            "/workflow",
            "/stakeholder-questions",
            "/summary",
            "/historical-records",
            "/facilities-distribution",
            "/data-types-distribution",
            "/search",
            "/case-study-solution-sequence",
        ]

        # Add dynamic facility routes
        facility_routes = self._get_facility_routes()

        return base_routes + facility_routes

    def _get_facility_routes(self) -> List[str]:
        """Generate facility routes from adapter data"""
        try:
            facilities = self.facility_adapter.get_facility_list()
            return [f"/facility/{f['facility_id']}" for f in facilities]
        except Exception as e:
            handle_error(logger, e, "facility routes generation")
            return []

    def resolve_route(self, pathname: str) -> Dict[str, Any]:
        """Resolve pathname to route configuration"""
        if not pathname or pathname == "/":
            return {"page": "portfolio", "component": "portfolio_overview"}

        if pathname == "/data-quality":
            return {"page": "data_quality", "component": "data_quality_layout"}

        if pathname == "/workflow":
            return {"page": "workflow", "component": "workflow_analysis_layout"}

        if pathname == "/stakeholder-questions":
            return {"page": "stakeholder_questions", "component": "stakeholder_questions_layout"}

        if pathname.startswith("/stakeholder-questions/"):
            category_id = pathname.replace("/stakeholder-questions/", "")
            return {
                "page": "stakeholder_questions",
                "component": "stakeholder_questions_layout",
                "category_id": category_id
            }

        if pathname == "/summary":
            return {"page": "summary", "component": "facilities_summary"}

        if pathname == "/historical-records":
            return {"page": "historical_records", "component": "historical_records_page"}

        if pathname == "/facilities-distribution":
            return {"page": "facilities_distribution", "component": "facilities_distribution_page"}

        if pathname == "/data-types-distribution":
            return {"page": "data_types", "component": "data_types_distribution_page"}

        if pathname == "/search":
            return {"page": "search", "component": "incident_search_layout"}

        if pathname == "/case-study-solution-sequence":
            return {"page": "case_study", "component": "solution_sequence_case_study_layout"}

        if pathname.startswith("/facility/"):
            facility_id = pathname.replace("/facility/", "")
            return {
                "page": "facility_detail",
                "component": "facility_detail_layout",
                "facility_id": facility_id,
            }

        return {"page": "not_found", "component": "error_page"}

    def validate_route(self, pathname: str) -> bool:
        """Validate route exists and is accessible"""
        if pathname in self.get_valid_routes():
            return True

        # Check facility routes dynamically
        if pathname.startswith("/facility/"):
            facility_id = pathname.replace("/facility/", "")
            validation = self.facility_adapter.validate_facility_data(facility_id)
            return validation.get("facility_exists", False)

        return False

    def get_breadcrumbs(self, pathname: str) -> List[Dict[str, str]]:
        """Generate breadcrumb navigation"""
        breadcrumbs = [{"label": "Portfolio", "url": "/"}]

        if pathname == "/":
            return breadcrumbs

        route_config = self.resolve_route(pathname)
        page_type = route_config.get("page")

        if page_type == "facility_detail":
            facility_id = route_config.get("facility_id", "Unknown")
            breadcrumbs.append({"label": f"Facility: {facility_id}", "url": pathname})
        elif page_type in ["data_quality", "workflow", "summary"]:
            breadcrumbs.append({"label": page_type.replace("_", " ").title(), "url": pathname})
        elif page_type in [
            "historical_records",
            "facilities_distribution",
            "data_types",
            "incident_search",
        ]:
            breadcrumbs.append({"label": "Analysis", "url": pathname})

        return breadcrumbs

    def get_page_title(self, pathname: str) -> str:
        """Get page title based on pathname"""
        title_mapping = {
            "/": "Portfolio Overview",
            "/data-quality": "Data Quality Foundation",
            "/workflow": "Workflow Understanding",
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
            validation = self.facility_adapter.validate_facility_data(facility_id)
            if validation.get("facility_exists", False):
                return f"Facility: {facility_id}"

        return "Not Found"


# Singleton pattern
_url_manager = None


def get_url_manager() -> URLManager:
    """Get singleton URL manager instance"""
    global _url_manager
    if _url_manager is None:
        _url_manager = URLManager()
    return _url_manager

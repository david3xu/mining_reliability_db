#!/usr/bin/env python3
"""
Dashboard Routing Package
URL management and navigation infrastructure.
"""

from dashboard.routing.navigation_builder import NavigationBuilder, get_navigation_builder
from dashboard.routing.url_manager import URLManager, get_url_manager

__all__ = ["URLManager", "get_url_manager", "NavigationBuilder", "get_navigation_builder"]

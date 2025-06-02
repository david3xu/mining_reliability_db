#!/usr/bin/env python3
"""
Routing Package - Page Routing & Navigation
URL managers and page navigation components.
"""

from dashboard.routing.navigation_builder import NavigationBuilder, get_navigation_builder
from dashboard.routing.url_manager import URLManager, get_url_manager

__all__ = [
    "URLManager",
    "get_url_manager",
    "NavigationBuilder",
    "get_navigation_builder",
]

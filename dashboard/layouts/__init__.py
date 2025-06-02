#!/usr/bin/env python3
"""
Dashboard Layouts Package
Layout infrastructure and navigation templates.
"""

from dashboard.layouts.main_layout import (
    create_error_boundary,
    create_footer,
    create_main_layout,
    create_navigation_bar,
    get_layout_config,
)

__all__ = [
    "create_main_layout",
    "create_navigation_bar",
    "create_footer",
    "create_error_boundary",
    "get_layout_config",
]

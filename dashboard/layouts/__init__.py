"""
Dashboard Layouts Package
Page structure and navigation components for dashboard application.
"""

from dashboard.layouts.main_layout import (
    create_main_layout,
    create_navigation_bar,
    create_footer,
    get_layout_config
)

__all__ = [
    'create_main_layout',
    'create_navigation_bar',
    'create_footer',
    'get_layout_config'
]

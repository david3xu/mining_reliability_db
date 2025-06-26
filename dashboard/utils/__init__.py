"""
Dashboard Utilities Package - Search-Only Version
Minimal utilities for search components only.
"""

from dashboard.utils.styling import (
    get_colors,
    get_dashboard_styles,
    get_fonts,
    COLORS,
    DASHBOARD_STYLES,
    FONTS,
)

__all__ = [
    # Only export styling utilities needed by search components
    "get_colors",
    "get_dashboard_styles",
    "get_fonts",
    "COLORS",
    "DASHBOARD_STYLES",
    "FONTS",
]

#!/usr/bin/env python3
"""
Dashboard Style Constants
Centralized constants for dashboard styling to eliminate hardcoded values.
"""

# Primary color constants (aligned with dashboard_config.json)
PRIMARY_COLOR = "#4A90E2"
SECONDARY_COLOR = "#F5A623"
SUCCESS_COLOR = "#7ED321"
DANGER_COLOR = "#D0021B"
WARNING_COLOR = "#F5A623"
INFO_COLOR = "#B57EDC"

# Extended colors
LIGHT_BLUE = "#7BB3F0"
DARK_BLUE = "#2E5C8A"
TEXT_COLOR = "#2C3E50"
GRID_COLOR = "#E5E5E5"
LINE_COLOR = "#CCCCCC"
BORDER_COLOR = "#FFFFFF"

# Priority background colors
HIGH_PRIORITY_BG = "#FFE6E6"
MEDIUM_PRIORITY_BG = "#FFF3CD"
LOW_PRIORITY_BG = "#E6F7E6"

# Chart color arrays
CHART_COLORS = [PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, INFO_COLOR]
TIMELINE_COLORS = [PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, INFO_COLOR, "#FF6B6B", "#4ECDC4"]

# Background colors
BACKGROUND_LIGHT = "#FFFFFF"
BACKGROUND_DARK = "#1E1E1E"
TEXT_PRIMARY = "#333333"
TEXT_SECONDARY = "#666666"
TEXT_LIGHT = "#FFFFFF"

def get_fallback_color(color_type: str) -> str:
    """Get fallback color value for given type"""
    fallback_map = {
        "primary_color": PRIMARY_COLOR,
        "secondary_color": SECONDARY_COLOR,
        "success_color": SUCCESS_COLOR,
        "danger_color": DANGER_COLOR,
        "warning_color": WARNING_COLOR,
        "info_color": INFO_COLOR,
        "text_color": TEXT_COLOR,
        "grid_color": GRID_COLOR,
        "line_color": LINE_COLOR,
        "border_color": BORDER_COLOR,
        "high_priority_bg": HIGH_PRIORITY_BG,
        "medium_priority_bg": MEDIUM_PRIORITY_BG,
        "low_priority_bg": LOW_PRIORITY_BG,
        "light_blue": LIGHT_BLUE
    }
    return fallback_map.get(color_type, PRIMARY_COLOR)

def get_fallback_colors(color_type: str) -> list:
    """Get fallback color array for given type"""
    if color_type == "chart_colors":
        return CHART_COLORS
    elif color_type == "timeline_colors":
        return TIMELINE_COLORS
    else:
        return CHART_COLORS

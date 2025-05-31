#!/usr/bin/env python3
"""
Configuration-Driven Styling System
Clean theme management using centralized configuration.
"""

from typing import Dict, Any
from configs.environment import get_dashboard_styling_config, get_dashboard_chart_config

def get_colors() -> Dict[str, str]:
    """Get color palette from configuration"""
    styling_config = get_dashboard_styling_config()

    return {
        # Primary colors from config
        "primary_blue": styling_config.get("primary_color", "#4A90E2"),
        "light_blue": styling_config.get("light_blue", "#7BB3F0"),
        "dark_blue": styling_config.get("dark_blue", "#2E5C8A"),

        # Chart colors from config
        "chart_colors": styling_config.get("chart_colors", ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"]),

        # Background and text from config
        "background_light": styling_config.get("background_light", "#FFFFFF"),
        "background_dark": styling_config.get("background_dark", "#1E1E1E"),
        "text_primary": styling_config.get("text_primary", "#333333"),
        "text_secondary": styling_config.get("text_secondary", "#666666"),
        "text_light": styling_config.get("text_light", "#FFFFFF"),

        # Grid and borders - fallback defaults
        "grid_color": "#E5E5E5",
        "border_color": "#CCCCCC"
    }

def get_fonts() -> Dict[str, Any]:
    """Get typography configuration"""
    chart_config = get_dashboard_chart_config()

    return {
        "primary_font": chart_config.get("font_family", "Arial, sans-serif"),
        "title_size": chart_config.get("title_font_size", 24),
        "subtitle_size": chart_config.get("subtitle_font_size", 18),
        "body_size": chart_config.get("body_font_size", 14),
        "caption_size": chart_config.get("caption_font_size", 12),
        "metric_size": 32,
        "metric_label_size": 14
    }

def get_layout_config() -> Dict[str, Any]:
    """Get layout dimensions from configuration"""
    chart_config = get_dashboard_chart_config()

    return {
        "container_padding": "20px",
        "component_margin": "15px",
        "card_padding": "20px",
        "metric_card_height": chart_config.get("metric_card_height", 120),
        "metric_card_width": chart_config.get("metric_card_width", 220),
        "chart_height": chart_config.get("default_height", 400),
        "table_height": chart_config.get("table_height", 300),
        "mobile_breakpoint": "768px"
    }

def get_metric_card_style(color=None):
    """Generate metric card styling from configuration"""
    colors = get_colors()
    layout = get_layout_config()

    card_color = color or colors["primary_blue"]

    return {
        "backgroundColor": card_color,
        "color": colors["text_light"],
        "padding": layout["card_padding"],
        "borderRadius": "8px",
        "textAlign": "center",
        "height": f"{layout['metric_card_height']}px",
        "width": f"{layout['metric_card_width']}px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
        "margin": layout["component_margin"],
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center"
    }

def get_chart_layout_template(title=""):
    """Generate chart layout from configuration"""
    colors = get_colors()
    fonts = get_fonts()
    layout = get_layout_config()

    return {
        "title": {
            "text": title,
            "font": {
                "family": fonts["primary_font"],
                "size": fonts["title_size"],
                "color": colors["text_primary"]
            },
            "x": 0.5,
            "xanchor": "center"
        },
        "paper_bgcolor": colors["background_light"],
        "plot_bgcolor": colors["background_light"],
        "font": {
            "family": fonts["primary_font"],
            "size": fonts["body_size"],
            "color": colors["text_primary"]
        },
        "margin": {"l": 60, "r": 30, "t": 60, "b": 60},
        "height": layout["chart_height"]
    }

def get_bar_chart_style():
    """Bar chart styling from configuration"""
    colors = get_colors()
    fonts = get_fonts()

    return {
        "marker": {
            "color": colors["chart_colors"],
            "line": {"color": colors["border_color"], "width": 1}
        },
        "textfont": {"size": fonts["caption_size"]},
        "textposition": "outside"
    }

def get_pie_chart_style():
    """Pie chart styling from configuration"""
    colors = get_colors()
    fonts = get_fonts()

    return {
        "marker": {
            "colors": colors["chart_colors"],
            "line": {"color": colors["background_light"], "width": 2}
        },
        "textfont": {"size": fonts["body_size"], "color": colors["text_light"]},
        "textposition": "inside",
        "textinfo": "label+percent",
        "hovertemplate": "<b>%{label}</b><br>Records: %{value}<br>Percentage: %{percent}<extra></extra>"
    }

def get_table_style():
    """Data table styling from configuration"""
    colors = get_colors()
    fonts = get_fonts()
    layout = get_layout_config()

    return {
        "style_cell": {
            "textAlign": "center",
            "padding": "12px",
            "fontFamily": fonts["primary_font"],
            "fontSize": fonts["body_size"],
            "border": f"1px solid {colors['border_color']}"
        },
        "style_header": {
            "backgroundColor": colors["primary_blue"],
            "color": colors["text_light"],
            "fontWeight": "bold",
            "border": f"1px solid {colors['primary_blue']}"
        },
        "style_data": {
            "backgroundColor": colors["background_light"],
            "color": colors["text_primary"]
        },
        "style_table": {
            "height": f"{layout['table_height']}px",
            "overflowY": "auto",
            "border": f"1px solid {colors['border_color']}",
            "borderRadius": "8px"
        }
    }

def get_dashboard_styles():
    """Complete dashboard styling from configuration"""
    colors = get_colors()
    fonts = get_fonts()
    layout = get_layout_config()

    return {
        "main_container": {
            "backgroundColor": colors["background_light"],
            "padding": layout["container_padding"],
            "fontFamily": fonts["primary_font"]
        },
        "header_section": {
            "textAlign": "center",
            "marginBottom": "30px",
            "padding": "20px",
            "backgroundColor": colors["background_dark"],
            "color": colors["text_light"],
            "borderRadius": "10px"
        },
        "metrics_row": {
            "display": "flex",
            "justifyContent": "space-around",
            "flexWrap": "wrap",
            "marginBottom": "30px",
            "gap": "15px"
        },
        "charts_section": {
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr",
            "gap": "30px",
            "marginBottom": "30px"
        },
        "table_section": {
            "marginTop": "30px",
            "backgroundColor": colors["background_light"],
            "borderRadius": "8px",
            "padding": "20px",
            "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
        }
    }

# Legacy compatibility - expose via CONSTANTS for existing code
COLORS = get_colors()
FONTS = get_fonts()
LAYOUT = get_layout_config()
DASHBOARD_STYLES = get_dashboard_styles()

# Utility functions
def apply_theme_mode(dark_mode=False):
    """Apply theme mode - updates configuration dynamically"""
    # In production, this would update the configuration source
    pass

def get_responsive_style(component_type, screen_size="desktop"):
    """Get responsive styling"""
    dashboard_styles = get_dashboard_styles()

    if screen_size == "mobile" and component_type in dashboard_styles:
        mobile_overrides = {
            "charts_section": {"gridTemplateColumns": "1fr"},
            "metrics_row": {"flexDirection": "column", "alignItems": "center"}
        }

        if component_type in mobile_overrides:
            style = dashboard_styles[component_type].copy()
            style.update(mobile_overrides[component_type])
            return style

    return dashboard_styles.get(component_type, {})

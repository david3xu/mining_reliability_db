#!/usr/bin/env python3
"""
Adapter-Based Styling Utilities - Configuration Access Layer
Direct styling configuration through adapter pattern.
"""

from typing import Any, Dict

from dashboard.adapters import get_config_adapter


def get_colors() -> Dict[str, str]:
    """Direct color configuration access"""
    config_adapter = get_config_adapter()
    styling = config_adapter.get_styling_config()

    return {
        "primary_blue": styling.get("primary_color", "#4A90E2"),
        "light_blue": styling.get("light_blue", "#7BB3F0"),
        "dark_blue": styling.get("dark_blue", "#2E5C8A"),
        "chart_colors": styling.get("chart_colors", ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"]),
        "background_light": styling.get("background_light", "#FFFFFF"),
        "background_dark": styling.get("background_dark", "#1E1E1E"),
        "text_primary": styling.get("text_primary", "#333333"),
        "text_secondary": styling.get("text_secondary", "#666666"),
        "text_light": styling.get("text_light", "#FFFFFF"),
        "grid_color": "#E5E5E5",
        "border_color": "#CCCCCC",
    }


def get_fonts() -> Dict[str, Any]:
    """Get fonts configuration"""
    config_adapter = get_config_adapter()
    chart = config_adapter.get_dashboard_chart_config()
    return {
        "family": chart.get("font_family", "Arial, sans-serif"),
        "size": chart.get("title_font_size", 12),
        "color": get_colors().get("text_primary"),
    }


def get_layout_dimensions() -> Dict[str, Any]:
    """Get layout dimensions configuration"""
    config_adapter = get_config_adapter()
    chart = config_adapter.get_dashboard_chart_config()
    return {
        "container_padding": chart.get("container_padding", "20px"),
        "metric_card_height": chart.get("metric_card_height", 120),
        "metric_card_width": chart.get("metric_card_width", 220),
        "chart_height": chart.get("default_height", 400),
        "table_height": chart.get("table_height", 300),
        "card_padding": chart.get("micro_component_configs", {})
        .get("metric_card", {})
        .get("dimensions", {})
        .get("padding", 20),
        "component_margin": chart.get("micro_component_configs", {}).get(
            "component_margin", "15px"
        ),
    }


def get_metric_card_style(color: str = None) -> Dict[str, Any]:
    """Standard metric card styling from configuration"""
    colors = get_colors()
    layout = get_layout_dimensions()

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
        "margin": layout.get("component_margin", "15px"),
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
    }


def get_chart_layout_template(title: str = "") -> Dict[str, Any]:
    """Standard chart layout from configuration"""
    colors = get_colors()
    fonts = get_fonts()
    layout = get_layout_dimensions()

    return {
        "title": {
            "text": title,
            "font": {
                "family": fonts["family"],
                "size": fonts["size"],
                "color": fonts["color"],
            },
            "x": 0.5,
            "xanchor": "center",
        },
        "paper_bgcolor": colors["background_light"],
        "plot_bgcolor": colors["background_light"],
        "font": {
            "family": fonts["family"],
            "size": fonts["size"],
            "color": fonts["color"],
        },
        "margin": {"l": 60, "r": 30, "t": 60, "b": 60},
        "height": layout["chart_height"],
    }


def get_bar_chart_style() -> Dict[str, Any]:
    """Bar chart styling configuration"""
    colors = get_colors()
    fonts = get_fonts()

    return {
        "marker": {
            "color": colors["chart_colors"],
            "line": {"color": colors["border_color"], "width": 1},
        },
        "textfont": {"size": fonts["size"]},
        "textposition": "outside",
    }


def get_pie_chart_style() -> Dict[str, Any]:
    """Pie chart styling configuration"""
    colors = get_colors()
    fonts = get_fonts()

    return {
        "marker": {
            "colors": colors["chart_colors"],
            "line": {"color": colors["background_light"], "width": 2},
        },
        "textfont": {"size": fonts["size"], "color": colors["text_light"]},
        "textposition": "inside",
        "textinfo": "label+percent",
        "hovertemplate": "<b>%{label}</b><br>Records: %{value}<br>Percentage: %{percent}<extra></extra>",
    }


def get_table_style() -> Dict[str, Any]:
    """Data table styling configuration"""
    colors = get_colors()
    fonts = get_fonts()
    layout = get_layout_dimensions()

    return {
        "style_cell": {
            "textAlign": "center",
            "padding": "12px",
            "fontFamily": fonts["family"],
            "fontSize": fonts["size"],
            "border": f"1px solid {colors['border_color']}",
        },
        "style_header": {
            "backgroundColor": colors["primary_blue"],
            "color": colors["text_light"],
            "fontWeight": "bold",
            "border": f"1px solid {colors['primary_blue']}",
        },
        "style_data": {
            "backgroundColor": colors["background_light"],
            "color": colors["text_primary"],
        },
        "style_table": {
            "height": f"{layout['table_height']}px",
            "overflowY": "auto",
            "border": f"1px solid {colors['border_color']}",
            "borderRadius": "8px",
        },
    }


def get_dashboard_styles() -> Dict[str, Any]:
    """Complete dashboard styling configuration"""
    colors = get_colors()
    fonts = get_fonts()
    layout = get_layout_dimensions()

    return {
        "main_container": {
            "backgroundColor": colors["background_light"],
            "padding": layout["container_padding"],
            "fontFamily": fonts["family"],
        },
        "header_section": {
            "textAlign": "center",
            "marginBottom": "30px",
            "padding": "20px",
            "backgroundColor": colors["background_dark"],
            "color": colors["text_light"],
            "borderRadius": "10px",
        },
        "metrics_row": {
            "display": "flex",
            "justifyContent": "space-around",
            "flexWrap": "wrap",
            "marginBottom": "30px",
            "gap": "15px",
        },
        "charts_section": {
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr",
            "gap": "30px",
            "marginBottom": "30px",
        },
        "table_section": {
            "marginTop": "30px",
            "backgroundColor": colors["background_light"],
            "borderRadius": "8px",
            "padding": "20px",
            "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
        },
    }


def get_responsive_style(component_type: str, screen_size: str = "desktop") -> Dict[str, Any]:
    """Responsive styling adjustments"""
    dashboard_styles = get_dashboard_styles()

    if screen_size == "mobile" and component_type in dashboard_styles:
        mobile_overrides = {
            "charts_section": {"gridTemplateColumns": "1fr"},
            "metrics_row": {"flexDirection": "column", "alignItems": "center"},
        }

        if component_type in mobile_overrides:
            style = dashboard_styles[component_type].copy()
            style.update(mobile_overrides[component_type])
            return style

    return dashboard_styles.get(component_type, {})


# Legacy compatibility exports
COLORS = get_colors()
FONTS = get_fonts()
LAYOUT = get_layout_dimensions()
DASHBOARD_STYLES = get_dashboard_styles()


def apply_theme_mode(dark_mode: bool = False):
    """Theme mode application"""
    pass  # Configuration-driven themes handled by adapter

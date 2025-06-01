#!/usr/bin/env python3
"""
Portfolio Overview Component - Interactive Navigation Hub
Clean home page with clickable metric cards and dedicated analysis pages.
"""

import logging
from typing import Dict, List, Any

# Dash components
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# Data pipeline
from dashboard.utils.data_transformers import (
    get_portfolio_metrics,
    get_field_distribution_data,
    get_facility_breakdown_data,
    get_historical_timeline_data,
    validate_dashboard_data,
    get_styling_config,
    get_chart_config
)

# Error handling
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

def create_clean_metric_card(value: Any, label: str, color: str, clickable: bool = False, href: str = None) -> html.Div:
    """Create clean metric card with optional click navigation"""

    display_value = f"{value:,}" if isinstance(value, int) and value > 999 else str(value)

    card_style = {
        "backgroundColor": color,
        "padding": "20px",
        "borderRadius": "8px",
        "textAlign": "center",
        "minWidth": "140px",
        "minHeight": "100px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
    }

    if clickable:
        card_style.update({
            "cursor": "pointer",
            "transition": "transform 0.2s ease, box-shadow 0.2s ease",
            "textDecoration": "none"
        })
        hover_class = "metric-card-hover"
    else:
        hover_class = ""

    card_content = [
        html.H2(display_value, className="text-white mb-1",
               style={"fontSize": "32px", "fontWeight": "bold"}),
        html.P(label, className="text-white mb-0",
              style={"fontSize": "14px"})
    ]

    if clickable and href:
        return html.A(card_content, href=href, style=card_style,
                     className=f"text-decoration-none {hover_class}")
    else:
        return html.Div(card_content, style=card_style)

def create_clean_metrics_section() -> html.Div:
    """Create clean portfolio metrics with clickable navigation"""

    try:
        logger.info("Creating clean metrics section...")

        # Real data from existing infrastructure
        metrics_data = get_portfolio_metrics()

        if not metrics_data:
            return html.Div([
                dbc.Alert("No metrics data available", color="warning")
            ])

        # Interactive metric cards with real values
        cards = [
            create_clean_metric_card(
                value=metrics_data["total_records"]["value"],
                label="Total Records",
                color="#4A90E2",
                clickable=True,
                href="/historical-records"
            ),
            create_clean_metric_card(
                value=metrics_data["data_fields"]["value"],
                label="Data Fields",
                color="#4A90E2",
                clickable=True,
                href="/data-types-distribution"
            ),
            create_clean_metric_card(
                value=metrics_data["facilities"]["value"],
                label="Facilities",
                color="#4A90E2",
                clickable=True,
                href="/facilities-distribution"
            ),
            create_clean_metric_card(
                value=metrics_data["years_coverage"]["value"],
                label="Years Coverage",
                color="#4A90E2"
            )
        ]

        # Dynamic description from real data
        year_detail = metrics_data["years_coverage"]["detail"]
        facilities_count = metrics_data["facilities"]["value"]

        return html.Div([
            # Header
            html.H3("Key Portfolio Metrics",
                   className="text-center text-white mb-4"),

            # Cards row
            html.Div(cards, className="d-flex justify-content-center gap-3 mb-3"),

            # Dynamic description
            html.H5(f"Comprehensive Analysis Across {facilities_count} Operational Facilities",
                   className="text-center text-white mb-2"),
            html.P(f"Data spans from {year_detail} with consistent field structure",
                  className="text-center text-white-50 mb-0")
        ], className="p-4 bg-dark rounded")

    except Exception as e:
        handle_error(logger, e, "clean metrics section creation")
        return html.Div([
            dbc.Alert("Failed to load metrics", color="danger")
        ])

def create_complete_dashboard() -> html.Div:
    """Clean home page with interactive metric cards"""

    try:
        logger.info("Creating clean interactive dashboard")

        # Validate data before rendering
        validation_results = validate_dashboard_data()

        if not validation_results.get("phase2_complete", False):
            logger.warning("Data validation failed - showing error state")
            return html.Div([
                dbc.Alert([
                    html.H4("Data Validation Error", className="alert-heading"),
                    html.P("Dashboard data pipeline validation failed."),
                    dbc.Button("Retry", href="/", color="primary", size="sm")
                ], color="warning", dismissable=True)
            ], className="p-4")

        # Clean layout with just metrics
        layout = html.Div([
            # Interactive metrics section
            create_clean_metrics_section(),

            # Simple instruction
            html.Div([
                html.P("Click metric cards to explore detailed analysis",
                      className="text-center text-muted mt-4",
                      style={"fontSize": "14px", "fontStyle": "italic"})
            ])
        ], className="container-fluid p-4")

        logger.info("Clean interactive dashboard created successfully")
        return layout

    except Exception as e:
        handle_error(logger, e, "clean dashboard creation")
        return html.Div([
            dbc.Container([
                dbc.Alert("Dashboard initialization error", color="danger")
            ])
        ])

# DEDICATED ANALYSIS PAGES

def create_historical_records_page() -> html.Div:
    """Enhanced historical records page with trend analysis"""

    try:
        # Real historical data from existing method
        timeline_data = get_historical_timeline_data()

        if not timeline_data:
            return html.Div([
                dbc.Container([
                    dbc.Alert("No historical data available", color="warning")
                ])
            ])

        return html.Div([
            dbc.Container([
                # Back button
                dbc.Button("← Back to Portfolio", href="/", color="secondary", size="sm", className="mb-3"),

                # Page header
                html.H2("Historical Records by Years", className="text-primary mb-4"),

                # Real data summary
                html.P(f"Total Records: {timeline_data['summary']['total_records']:,} | "
                      f"Years Covered: {timeline_data['summary']['year_span']} | "
                      f"Facilities: {timeline_data['summary']['facilities']}",
                      className="text-muted mb-4"),

                # Trend visualization section
                dbc.Row([
                    dbc.Col([
                        html.H4("Performance Trends", className="text-secondary mb-3"),
                        create_historical_trends_chart()
                    ], md=12, className="mb-4")
                ]),

                # Data table section
                html.H4("Detailed Records", className="text-secondary mb-3"),
                create_enhanced_historical_table()
            ], fluid=True)
        ], className="p-4")

    except Exception as e:
        handle_error(logger, e, "enhanced historical records page creation")
        return html.Div([
            dbc.Container([
                dbc.Alert("Failed to load historical records analysis", color="danger")
            ])
        ])

def create_facilities_distribution_page() -> html.Div:
    """Dedicated facilities distribution page using real data"""

    try:
        # Real facility data from existing method
        facility_data = get_facility_breakdown_data()

        if not facility_data:
            return html.Div([
                dbc.Container([
                    dbc.Alert("No facility data available", color="warning")
                ])
            ])

        return html.Div([
            dbc.Container([
                # Back button
                dbc.Button("← Back to Portfolio", href="/", color="secondary", size="sm", className="mb-3"),

                # Page header
                html.H2("Records Distribution by Site", className="text-primary mb-4"),

                # Real data summary
                html.P(f"Total Records: {facility_data['total_records']:,} across {len(facility_data['labels'])} facilities",
                      className="text-muted mb-4"),

                # Large pie chart using existing component
                html.Div([
                    create_enhanced_facility_pie_chart()
                ], className="d-flex justify-content-center")
            ], fluid=True)
        ], className="p-4")

    except Exception as e:
        handle_error(logger, e, "facilities distribution page creation")
        return html.Div([
            dbc.Container([
                dbc.Alert("Failed to load facilities distribution", color="danger")
            ])
        ])

def create_data_types_distribution_page() -> html.Div:
    """Dedicated data types distribution page using real data"""

    try:
        # Real field data from existing method
        field_data = get_field_distribution_data()

        if not field_data:
            return html.Div([
                dbc.Container([
                    dbc.Alert("No field data available", color="warning")
                ])
            ])

        return html.Div([
            dbc.Container([
                # Back button
                dbc.Button("← Back to Portfolio", href="/", color="secondary", size="sm", className="mb-3"),

                # Page header
                html.H2("Data Types Distribution", className="text-primary mb-4"),

                # Real data summary
                html.P(f"Total Fields: {field_data['total_fields']} across {len(field_data['labels'])} categories",
                      className="text-muted mb-4"),

                # Large bar chart using existing component
                html.Div([
                    create_enhanced_field_distribution_chart()
                ], className="d-flex justify-content-center")
            ], fluid=True)
        ], className="p-4")

    except Exception as e:
        handle_error(logger, e, "data types distribution page creation")
        return html.Div([
            dbc.Container([
                dbc.Alert("Failed to load data types distribution", color="danger")
            ])
        ])

# EXISTING CHART COMPONENTS (Keep for dedicated pages)

def create_enhanced_field_distribution_chart() -> dcc.Graph:
    """Create enhanced field distribution bar chart"""
    try:
        # Get data and styling
        field_data = get_field_distribution_data()
        styling_config = get_styling_config()
        chart_config = get_chart_config()

        if not field_data:
            return dcc.Graph(figure={})

        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=field_data.get("labels", []),
            y=field_data.get("values", []),
            text=[f"{p}%" for p in field_data.get("percentages", [])],
            textposition="outside",
            marker=dict(
                color=styling_config.get("primary_color", "#4A90E2"),
                line=dict(color=styling_config.get("border_color", "#CCCCCC"), width=1)
            ),
            hovertemplate="<b>%{x}</b><br>Count: %{y}<br>Percentage: %{text}<extra></extra>"
        ))

        fig.update_layout(
            title="Data Types Distribution",
            xaxis_title="Field Type Category",
            yaxis_title="Number of Fields",
            height=400,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, "enhanced field distribution chart creation")
        return dcc.Graph(figure={})

def create_enhanced_facility_pie_chart() -> dcc.Graph:
    """Create enhanced facility pie chart"""
    try:
        # Get data and styling
        facility_data = get_facility_breakdown_data()
        styling_config = get_styling_config()

        if not facility_data:
            return dcc.Graph(figure={})

        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=facility_data.get("labels", []),
            values=facility_data.get("values", []),
            textinfo="label+percent",
            textposition="auto",
            marker=dict(
                colors=styling_config.get("chart_colors", ["#4A90E2", "#F5A623", "#7ED321", "#B57EDC"]),
                line=dict(color='white', width=2)
            ),
            hovertemplate="<b>%{label}</b><br>Records: %{value}<br>Percentage: %{percent}<extra></extra>"
        ))

        fig.update_layout(
            title="Records Distribution by Site",
            height=400,
            showlegend=True,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, "enhanced facility pie chart creation")
        return dcc.Graph(figure={})

def create_enhanced_historical_table() -> dash_table.DataTable:
    """Create enhanced historical timeline table"""
    try:
        # Get data and styling
        timeline_data = get_historical_timeline_data()
        styling_config = get_styling_config()

        if not timeline_data:
            return dash_table.DataTable(data=[])

        columns = timeline_data.get("columns", [])
        rows = timeline_data.get("rows", [])

        # Create column definitions
        table_columns = []
        for col in columns:
            column_def = {
                "name": col.title(),
                "id": col,
                "type": "numeric" if col != "facility" else "text"
            }
            table_columns.append(column_def)

        return dash_table.DataTable(
            data=rows,
            columns=table_columns,
            style_cell={
                "textAlign": "center",
                "padding": "12px",
                "fontSize": "14px",
                "border": f"1px solid {styling_config.get('border_color', '#CCCCCC')}"
            },
            style_header={
                "backgroundColor": styling_config.get("primary_color", "#4A90E2"),
                "color": "white",
                "fontWeight": "bold"
            },
            style_data={
                "backgroundColor": "white",
                "color": styling_config.get("text_primary", "#333333")
            },
            style_data_conditional=[
                {
                    "if": {"row_index": len(rows) - 1},
                    "backgroundColor": styling_config.get("light_blue", "#7BB3F0"),
                    "color": "white",
                    "fontWeight": "bold"
                }
            ],
            sort_action="native",
            page_action="none",
            style_table={
                "height": "400px",
                "overflowY": "auto"
            }
        )

    except Exception as e:
        handle_error(logger, e, "enhanced historical table creation")
        return dash_table.DataTable(data=[])

def create_facility_trends_line_chart() -> dcc.Graph:
    """Create line chart showing facility trends over time"""
    try:
        # Get timeline data and styling
        timeline_data = get_historical_timeline_data()
        styling_config = get_styling_config()

        if not timeline_data:
            return dcc.Graph(figure={})

        import plotly.graph_objects as go

        rows = timeline_data.get("rows", [])
        year_range = timeline_data.get("summary", {}).get("min_year"), timeline_data.get("summary", {}).get("max_year")

        if not rows or not year_range[0] or not year_range[1]:
            return dcc.Graph(figure={})

        # Extract years from columns (skip 'facility' and 'total')
        columns = timeline_data.get("columns", [])
        years = [col for col in columns if col.isdigit()]

        # Color palette for facilities
        colors = ['#4A90E2', '#F5A623', '#7ED321', '#B57EDC', '#FF6B6B', '#4ECDC4']

        fig = go.Figure()

        # Add a line for each facility (exclude totals row)
        facility_rows = [row for row in rows if row.get("facility") != "Total"]

        for i, row in enumerate(facility_rows):
            facility_name = row.get("facility", "Unknown")
            y_values = [row.get(year, 0) for year in years]

            fig.add_trace(go.Scatter(
                x=years,
                y=y_values,
                mode='lines+markers',
                name=facility_name,
                line=dict(
                    color=colors[i % len(colors)],
                    width=3
                ),
                marker=dict(
                    size=8,
                    color=colors[i % len(colors)],
                    symbol='circle'
                ),
                hovertemplate=f"<b>{facility_name}</b><br>" +
                             "Year: %{x}<br>" +
                             "Records: %{y}<extra></extra>"
            ))

        fig.update_layout(
            title="Facility Records Trends Over Time",
            xaxis_title="Year",
            yaxis_title="Number of Records",
            height=450,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            )
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, "facility trends line chart creation")
        return dcc.Graph(figure={})

def create_historical_trends_chart() -> dcc.Graph:
    """Create professional line chart showing facility trends over time"""
    try:
        # Get timeline data and styling
        timeline_data = get_historical_timeline_data()
        styling_config = get_styling_config()

        if not timeline_data:
            return dcc.Graph(figure={})

        import plotly.graph_objects as go

        rows = timeline_data.get("rows", [])

        if not rows:
            return dcc.Graph(figure={})

        # Extract years from columns (skip 'facility' and 'total')
        columns = timeline_data.get("columns", [])
        years = [col for col in columns if col.isdigit()]

        # Professional color palette
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#1B998B', '#7209B7']

        fig = go.Figure()

        # Add a line for each facility (exclude totals row)
        facility_rows = [row for row in rows if row.get("facility") != "Total"]

        for i, row in enumerate(facility_rows):
            facility_name = row.get("facility", "Unknown")
            y_values = [row.get(year, 0) for year in years]

            fig.add_trace(go.Scatter(
                x=years,
                y=y_values,
                mode='lines+markers',
                name=facility_name,
                line=dict(
                    color=colors[i % len(colors)],
                    width=3
                ),
                marker=dict(
                    size=8,
                    color=colors[i % len(colors)],
                    symbol='circle'
                ),
                hovertemplate=f"<b>{facility_name}</b><br>" +
                             "Year: %{x}<br>" +
                             "Records: %{y:,}<extra></extra>"
            ))

        # Professional layout
        fig.update_layout(
            title={
                'text': "Historical Data Collection Trends by Facility",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2C3E50'}
            },
            xaxis=dict(
                title="Year",
                showgrid=True,
                gridwidth=1,
                gridcolor='#E5E5E5',
                linecolor='#CCCCCC',
                linewidth=1
            ),
            yaxis=dict(
                title="Number of Records",
                showgrid=True,
                gridwidth=1,
                gridcolor='#E5E5E5',
                linecolor='#CCCCCC',
                linewidth=1
            ),
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=60, r=40, t=60, b=80)
        )

        return dcc.Graph(figure=fig, config={'displayModeBar': False})

    except Exception as e:
        handle_error(logger, e, "historical trends chart creation")
        return dcc.Graph(figure={})

# Legacy compatibility functions (for backwards compatibility)
def create_metrics_cards() -> List[dbc.Card]:
    """Legacy compatibility wrapper"""
    return create_clean_metrics_section()

def create_field_distribution_chart() -> dcc.Graph:
    """Legacy compatibility wrapper"""
    return create_enhanced_field_distribution_chart()

def create_facility_pie_chart() -> dcc.Graph:
    """Legacy compatibility wrapper"""
    return create_enhanced_facility_pie_chart()

def create_historical_table() -> dash_table.DataTable:
    """Legacy compatibility wrapper"""
    return create_enhanced_historical_table()

def create_portfolio_layout() -> html.Div:
    """Legacy compatibility wrapper"""
    return create_complete_dashboard()
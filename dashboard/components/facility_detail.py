#!/usr/bin/env python3
"""
Dynamic Facility Detail Component - Real Data Implementation
Single component that adapts to any facility using real database queries.
"""

import logging
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dashboard.components.layout_template import create_standard_layout, create_metric_card
from mine_core.shared.common import handle_error

# Real data sources
from dashboard.adapters import get_data_adapter
from dashboard.utils.data_transformers import get_facility_analysis_data
from dashboard.utils.style_constants import (
    DANGER_COLOR, WARNING_COLOR, SUCCESS_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, INFO_COLOR,
    HIGH_PRIORITY_BG, MEDIUM_PRIORITY_BG, LOW_PRIORITY_BG, WHITE_COLOR
)

logger = logging.getLogger(__name__)

def create_facility_metrics_cards(facility_id: str) -> list:
    """Generate facility-specific metrics using real data"""

    try:
        # Real facility analysis data
        facility_data = get_facility_analysis_data(facility_id)

        if not facility_data:
            return []

        # Real comparison data
        adapter = get_data_adapter()
        comparison_data = adapter.get_facility_comparison_metrics(facility_id)

        total_records = facility_data.get("total_records", 0)
        categories_count = facility_data.get("categories_count", 0)

        # Calculate risk level based on real data
        avg_other_records = comparison_data.get("average_other_records", 0)
        risk_level = "High" if total_records > avg_other_records * 1.5 else "Medium" if total_records > avg_other_records else "Low"

        # Get risk colors from configuration
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            high_risk_color = styling_config.get("danger_color", DANGER_COLOR)
            medium_risk_color = styling_config.get("warning_color", WARNING_COLOR)
            low_risk_color = styling_config.get("success_color", SUCCESS_COLOR)
        except Exception:
            high_risk_color = DANGER_COLOR
            medium_risk_color = WARNING_COLOR
            low_risk_color = SUCCESS_COLOR

        risk_color = high_risk_color if risk_level == "High" else medium_risk_color if risk_level == "Medium" else low_risk_color

        # Performance vs others
        vs_average = comparison_data.get("vs_average", 0)
        performance_text = f"{vs_average:+.1f}% vs Others"

        # Get standard colors from configuration
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            primary_color = styling_config.get("primary_color", PRIMARY_COLOR)
            secondary_color = styling_config.get("secondary_color", SECONDARY_COLOR)
            info_color = styling_config.get("info_color", INFO_COLOR)
        except Exception:
            primary_color = PRIMARY_COLOR
            secondary_color = SECONDARY_COLOR
            info_color = INFO_COLOR

        cards = [
            create_metric_card(
                value=total_records,
                label="Total Records",
                detail=f"Facility incidents",
                color=primary_color
            ),
            create_metric_card(
                value=categories_count,
                label="Categories",
                detail="Issue types identified",
                color=secondary_color
            ),
            create_metric_card(
                value=risk_level,
                label="Risk Level",
                detail="Based on incident volume",
                color=risk_color
            ),
            create_metric_card(
                value=performance_text,
                label="Performance Rank",
                detail=f"Rank {comparison_data.get('performance_rank', 0)}/{comparison_data.get('total_facilities', 0)}",
                color=info_color
            )
        ]

        return cards

    except Exception as e:
        handle_error(logger, e, f"facility metrics cards for {facility_id}")
        return []

def create_facility_category_chart(facility_id: str) -> dcc.Graph:
    """Category distribution chart for specific facility"""

    try:
        # Real facility category data
        facility_data = get_facility_analysis_data(facility_id)

        if not facility_data:
            return dcc.Graph(figure={})

        category_distribution = facility_data.get("category_distribution", {})
        category_percentages = facility_data.get("category_percentages", {})

        if not category_distribution:
            return dcc.Graph(figure={})

        # Sort by count for better visualization
        sorted_categories = sorted(category_distribution.items(), key=lambda x: x[1], reverse=True)

        labels = [cat for cat, count in sorted_categories]
        values = [count for cat, count in sorted_categories]
        percentages = [category_percentages.get(cat, 0) for cat, count in sorted_categories]

        # Color mapping based on category risk using configuration
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            high_risk_color = styling_config.get("danger_color", DANGER_COLOR)
            medium_risk_color = styling_config.get("warning_color", WARNING_COLOR)
            low_risk_color = styling_config.get("success_color", SUCCESS_COLOR)
            border_color = styling_config.get("border_color", WHITE_COLOR)
        except Exception:
            high_risk_color = DANGER_COLOR
            medium_risk_color = WARNING_COLOR
            low_risk_color = SUCCESS_COLOR
            border_color = WHITE_COLOR

        colors = []
        for label in labels:
            if "Equipment" in label or "Production" in label:
                colors.append(high_risk_color)  # High risk
            elif "Safety" in label or "Plant Level" in label:
                colors.append(medium_risk_color)  # Medium risk
            else:
                colors.append(low_risk_color)  # Low risk

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=labels,
            values=values,
            text=[f"{p:.1f}%" for p in percentages],
            textinfo="label+text",
            textposition="auto",
            marker=dict(colors=colors, line=dict(color=border_color, width=2)),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{text}<extra></extra>"
        ))

        fig.update_layout(
            title=f"Category Distribution - {facility_id.title()} Facility",
            height=400,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, f"facility category chart for {facility_id}")
        return dcc.Graph(figure={})

def create_recurring_issues_analysis(facility_id: str) -> dcc.Graph:
    """Recurring issues analysis for specific facility"""

    try:
        # Real action requests for facility via adapter
        adapter = get_data_adapter()
        action_requests = adapter.get_action_requests(facility_id=facility_id, limit=10000)

        if not action_requests:
            return dcc.Graph(figure={})

        # Analyze recurring patterns from real data
        category_analysis = {}
        for request in action_requests:
            category = request.get('categories', 'Unknown')
            stage = request.get('stage', 'Unknown')

            if category not in category_analysis:
                category_analysis[category] = {
                    "total": 0,
                    "closed": 0,
                    "in_progress": 0
                }

            category_analysis[category]["total"] += 1

            if "Closed" in stage:
                category_analysis[category]["closed"] += 1
            elif "Progress" in stage or "Waiting" in stage:
                category_analysis[category]["in_progress"] += 1

        # Calculate recurring rates
        categories = list(category_analysis.keys())
        recurring_rates = []

        for category in categories:
            total = category_analysis[category]["total"]
            # Higher total indicates more recurring issues
            recurring_rate = (total / len(action_requests)) * 100 if total > 1 else 0
            recurring_rates.append(recurring_rate)

        # Create horizontal bar chart
        fig = go.Figure()

        # Color based on recurring rate using configuration
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            high_risk_color = styling_config.get("danger_color", DANGER_COLOR)
            medium_risk_color = styling_config.get("warning_color", WARNING_COLOR)
            low_risk_color = styling_config.get("success_color", SUCCESS_COLOR)
        except Exception:
            high_risk_color = DANGER_COLOR
            medium_risk_color = WARNING_COLOR
            low_risk_color = SUCCESS_COLOR

        colors = []
        for rate in recurring_rates:
            if rate > 30:
                colors.append(high_risk_color)  # High recurring
            elif rate > 15:
                colors.append(medium_risk_color)  # Medium recurring
            else:
                colors.append(low_risk_color)  # Low recurring

        fig.add_trace(go.Bar(
            x=recurring_rates,
            y=categories,
            orientation='h',
            marker=dict(color=colors),
            text=[f"{rate:.1f}%" for rate in recurring_rates],
            textposition='inside',
            hovertemplate="<b>%{y}</b><br>Recurring Rate: %{x:.1f}%<extra></extra>"
        ))

        fig.update_layout(
            title=f"Recurring Issues by Category - {facility_id.title()}",
            xaxis_title="Recurring Rate (%)",
            yaxis_title="Category",
            height=400,
            margin=dict(l=150, r=50, t=50, b=50),
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        handle_error(logger, e, f"recurring issues analysis for {facility_id}")
        return dcc.Graph(figure={})

def create_operating_centre_table(facility_id: str) -> dash_table.DataTable:
    """Operating centre breakdown table for facility"""

    try:
        # Real action requests data via adapter
        adapter = get_data_adapter()
        action_requests = adapter.get_action_requests(facility_id=facility_id, limit=10000)

        if not action_requests:
            return dash_table.DataTable(data=[])

        # Analyze by operating centre and category
        centre_analysis = {}

        for request in action_requests:
            operating_centre = request.get('stage', 'Unknown')  # Using stage as proxy for operating centre
            category = request.get('categories', 'Unknown')

            if operating_centre not in centre_analysis:
                centre_analysis[operating_centre] = {}

            if category not in centre_analysis[operating_centre]:
                centre_analysis[operating_centre][category] = 0

            centre_analysis[operating_centre][category] += 1

        # Build table data
        table_data = []

        for operating_centre, categories in centre_analysis.items():
            total_records = sum(categories.values())

            # Find dominant categories
            sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            primary_category = sorted_cats[0][0] if sorted_cats else "Unknown"
            primary_count = sorted_cats[0][1] if sorted_cats else 0
            primary_pct = (primary_count / total_records * 100) if total_records > 0 else 0

            # Priority based on volume
            if total_records > len(action_requests) * 0.3:
                priority = "High"
            elif total_records > len(action_requests) * 0.1:
                priority = "Medium"
            else:
                priority = "Low"

            table_data.append({
                "Operating Centre": operating_centre,
                "Total Records": total_records,
                "Primary Category": primary_category,
                "Primary %": f"{primary_pct:.1f}%",
                "Priority": priority
            })

        # Sort by total records descending
        table_data.sort(key=lambda x: x["Total Records"], reverse=True)

        # Get table styling from configuration
        try:
            from configs.environment import get_dashboard_styling_config
            styling_config = get_dashboard_styling_config()
            primary_color = styling_config.get("primary_color", PRIMARY_COLOR)
            high_bg = styling_config.get("high_priority_bg", HIGH_PRIORITY_BG)
            medium_bg = styling_config.get("medium_priority_bg", MEDIUM_PRIORITY_BG)
            low_bg = styling_config.get("low_priority_bg", LOW_PRIORITY_BG)
        except Exception:
            primary_color = PRIMARY_COLOR
            high_bg = HIGH_PRIORITY_BG
            medium_bg = MEDIUM_PRIORITY_BG
            low_bg = LOW_PRIORITY_BG

        return dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "Operating Centre", "id": "Operating Centre"},
                {"name": "Total Records", "id": "Total Records", "type": "numeric"},
                {"name": "Primary Category", "id": "Primary Category"},
                {"name": "Primary %", "id": "Primary %"},
                {"name": "Priority", "id": "Priority"}
            ],
            style_cell={'textAlign': 'center', 'padding': '12px'},
            style_header={'backgroundColor': primary_color, 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': 'white'},
            style_data_conditional=[
                {
                    'if': {'filter_query': '{Priority} = High'},
                    'backgroundColor': high_bg,
                    'color': 'black'
                },
                {
                    'if': {'filter_query': '{Priority} = Medium'},
                    'backgroundColor': medium_bg,
                    'color': 'black'
                },
                {
                    'if': {'filter_query': '{Priority} = Low'},
                    'backgroundColor': low_bg,
                    'color': 'black'
                }
            ],
            sort_action="native"
        )

    except Exception as e:
        handle_error(logger, e, f"operating centre table for {facility_id}")
        return dash_table.DataTable(data=[])

def create_facility_detail_layout(facility_id: str) -> html.Div:
    """
    Dynamic facility detail layout that adapts to any facility.
    Uses real database queries for facility-specific analysis.
    """

    try:
        logger.info(f"Creating facility detail layout for: {facility_id}")

        # Validate facility exists with real data
        facility_data = get_facility_analysis_data(facility_id)

        if not facility_data or facility_data.get("total_records", 0) == 0:
            # Facility not found or no data
            return html.Div([
                dbc.Container([
                    dbc.Alert([
                        html.H4("Facility Not Found", className="alert-heading"),
                        html.P(f"No data available for facility: {facility_id}"),
                        html.Hr(),
                        dbc.Button("Return to Portfolio Overview", href="/", color="primary")
                    ], color="warning")
                ])
            ])

        # Custom header for facility detail
        facility_header = html.Div([
            html.Div([
                dbc.Button("← Back to Portfolio", href="/", color="secondary", size="sm", className="mb-3"),
                html.H1(
                    f"{facility_id.title()} Facility - What are the specific issues?",
                    className="text-primary mb-2",
                    style={"fontSize": "28px", "fontWeight": "bold"}
                ),
                html.H4(
                    "Category Distribution & Recurring Issues",
                    className="text-muted mb-4",
                    style={"fontSize": "18px", "fontWeight": "normal"}
                )
            ], className="text-center")
        ],
        className="p-4 bg-dark text-white rounded mb-4"
        )

        # Create facility-specific content using standard layout
        facility_content = html.Div([
            facility_header,

            # Metrics row
            html.Div([
                html.Div(
                    create_facility_metrics_cards(facility_id),
                    className="d-flex justify-content-around flex-wrap gap-3 mb-4"
                )
            ]),

            # Main analysis grid
            dbc.Row([
                dbc.Col([
                    create_facility_category_chart(facility_id)
                ], md=6, className="mb-3"),
                dbc.Col([
                    create_recurring_issues_analysis(facility_id)
                ], md=6, className="mb-3")
            ], className="mb-4"),

            # Operating centre breakdown
            html.Div([
                html.H3("Operating Centre Analysis", className="mb-3 text-secondary"),
                create_operating_centre_table(facility_id)
            ], className="bg-light rounded p-4"),

            # Stakeholder questions
            html.Div([
                html.Hr(style={"margin": "40px 0 20px 0"}),
                html.H4("Stakeholder Questions", style={"color": SECONDARY_COLOR, "marginBottom": "20px"}),
                html.Ul([
                    html.Li(f"Equipment-Centric Operations at {facility_id.title()}",
                           style={"color": PRIMARY_COLOR, "fontSize": "16px", "marginBottom": "10px"}),
                    html.Li("Plant-Level Investigation Priorities",
                           style={"color": PRIMARY_COLOR, "fontSize": "16px", "marginBottom": "10px"}),
                    html.Li("Category-Specific Risk Assessment",
                           style={"color": PRIMARY_COLOR, "fontSize": "16px"})
                ])
            ])
        ], className="container-fluid")

        return facility_content

    except Exception as e:
        handle_error(logger, e, f"facility detail layout creation for {facility_id}")
        return html.Div([
            dbc.Container([
                dbc.Alert([
                    html.H4("Facility Analysis Error"),
                    html.P(f"Failed to load analysis for facility: {facility_id}"),
                    html.P(f"Error: {str(e)}"),
                    dbc.Button("Return to Portfolio Overview", href="/", color="secondary")
                ], color="danger")
            ])
        ])
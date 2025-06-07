#!/usr/bin/env python3
"""
Graph Search Component - Simple Neo4j Graph Exploration
Direct search interface for comprehensive graph data extraction.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import ALL, Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate

from dashboard.adapters.data_adapter import get_data_adapter
from dashboard.components.layout_template import create_standard_layout
from mine_core.shared.common import handle_error
from utils.json_recorder import JSONRecorder

logger = logging.getLogger(__name__)


def create_graph_search_layout():
    """Create simple graph search interface"""

    search_interface = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Graph Search", className="text-primary mb-3"),
                    html.P("Search all connected data in the mining reliability database"),
                    dbc.InputGroup(
                        [
                            dbc.Input(
                                id="graph-search-input",
                                placeholder="Search incidents, equipment, solutions... (e.g., 'excavator motor contamination')",
                                type="text",
                                value="",
                            ),
                            dbc.Button("Search Graph", id="search-graph-btn", color="primary"),
                        ],
                        className="mb-3",
                    ),
                    html.Div(id="search-status"),
                ]
            )
        ]
    )

    results_display = html.Div(id="graph-search-results")

    return create_standard_layout(
        title="Graph Search", content_cards=[search_interface, results_display]
    )


def create_results_display(search_results: Dict[str, Any]) -> dbc.Card:
    """Create comprehensive multi-dimensional results display with expandable sections"""

    incidents = search_results.get("incidents", [])
    solutions = search_results.get("solutions", [])
    facilities = search_results.get("facilities", [])
    metadata = search_results.get("metadata", {})

    # Create search performance summary
    performance_summary = create_search_performance_summary(metadata)

    tabs_content = []

    # Multi-Dimensional Incidents Tab with categorization
    if incidents:
        incidents_content = create_multi_dimensional_incidents_display(incidents)
        tabs_content.append(
            dbc.Tab(
                label=f"Incidents ({len(incidents)})",
                children=[incidents_content],
                tab_id="incidents-tab"
            )
        )

    # Enhanced Solutions Tab with effectiveness scoring
    if solutions:
        solutions_content = create_enhanced_solutions_display(solutions)
        tabs_content.append(
            dbc.Tab(
                label=f"Solutions ({len(solutions)})",
                children=[solutions_content],
                tab_id="solutions-tab"
            )
        )

    # Enhanced Facilities Tab with pattern insights
    if facilities:
        facilities_content = create_enhanced_facilities_display(facilities)
        tabs_content.append(
            dbc.Tab(
                label=f"Facilities ({len(facilities)})",
                children=[facilities_content],
                tab_id="facilities-tab"
            )
        )

    # Search Insights Tab
    if metadata:
        insights_content = create_search_insights_display(metadata)
        tabs_content.append(
            dbc.Tab(
                label="Search Insights",
                children=[insights_content],
                tab_id="insights-tab"
            )
        )

    if not tabs_content:
        return dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "No results found. Try different keywords or check spelling."
        ], color="warning")

    return dbc.Card([
        dbc.CardHeader([
            html.Div([
                html.H5("Multi-Dimensional Search Results", className="mb-1"),
                performance_summary
            ])
        ]),
        dbc.CardBody([dbc.Tabs(tabs_content, active_tab="incidents-tab")])
    ])


def create_search_performance_summary(metadata: Dict[str, Any]) -> html.Div:
    """Create search performance summary with dimension breakdown"""
    if not metadata:
        return html.Small("Standard search completed", className="text-muted")

    dimensions_executed = metadata.get("search_dimensions_executed", [])
    total_results = metadata.get("total_results", 0)
    dimension_results = metadata.get("search_performance", {})

    # Create dimension badges
    dimension_badges = []
    for dimension in dimensions_executed:
        count = dimension_results.get(dimension, 0)
        color = "success" if count > 0 else "secondary"
        dimension_name = dimension.replace("_", " ").title()

        dimension_badges.append(
            dbc.Badge(f"{dimension_name}: {count}", color=color, className="me-1")
        )

    return html.Small([
        html.Span(f"8-Dimensional Search: {total_results} total results | ", className="text-muted"),
        *dimension_badges
    ], className="d-block")


def create_multi_dimensional_incidents_display(incidents: List[Dict]) -> html.Div:
    """Create enhanced incidents display with dimensional categorization"""

    # Categorize incidents by relevance score and type
    high_relevance = [i for i in incidents if i.get("relevance_score", 0) >= 0.9]
    medium_relevance = [i for i in incidents if 0.7 <= i.get("relevance_score", 0) < 0.9]
    other_incidents = [i for i in incidents if i.get("relevance_score", 0) < 0.7]

    sections = []

    # High relevance section
    if high_relevance:
        sections.append(create_incidents_section(
            "Highly Relevant Matches",
            high_relevance,
            "success",
            "These incidents are highly relevant to your search with direct field matches."
        ))

    # Medium relevance section
    if medium_relevance:
        sections.append(create_incidents_section(
            "Pattern Matches",
            medium_relevance,
            "info",
            "These incidents match through equipment patterns, causal chains, or cross-facility patterns."
        ))

    # Other incidents section
    if other_incidents:
        sections.append(create_incidents_section(
            "Related Incidents",
            other_incidents,
            "light",
            "These incidents show temporal patterns, sequences, or cluster relationships."
        ))

    return html.Div(sections)


def create_incidents_section(title: str, incidents: List[Dict], color: str, description: str) -> dbc.Card:
    """Create an expandable section for incidents"""

    incident_rows = []
    for incident in incidents[:15]:  # Limit display
        # Add relevance indicator
        relevance_score = incident.get("relevance_score", 0)
        relevance_indicator = "🎯" if relevance_score >= 0.9 else "🔍" if relevance_score >= 0.7 else "📋"

        incident_rows.append(
            html.Tr([
                html.Td(relevance_indicator),
                html.Td(incident.get("incident_id", "N/A")),
                html.Td(incident.get("facility", "N/A")),
                html.Td(
                    html.Div(
                        incident.get("problem_description", "N/A")[:100] + "..."
                        if len(incident.get("problem_description", "")) > 100
                        else incident.get("problem_description", "N/A"),
                        title=incident.get("problem_description", "N/A")
                    )
                ),
                html.Td(incident.get("root_cause", "N/A")),
                html.Td(incident.get("solution", "N/A") if incident.get("solution") else "Not Available"),
            ])
        )

    incidents_table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th(""),
                html.Th("Incident ID"),
                html.Th("Facility"),
                html.Th("Problem Description"),
                html.Th("Root Cause"),
                html.Th("Solution")
            ])
        ]),
        html.Tbody(incident_rows)
    ], striped=True, hover=True, size="sm")

    return dbc.Card([
        dbc.CardHeader([
            dbc.Button([
                html.I(className="fas fa-chevron-down me-2"),
                f"{title} ({len(incidents)})"
            ], id=f"collapse-{title.lower().replace(' ', '-')}-button",
               color=color, variant="light", className="w-100 text-start"),
        ]),
        dbc.Collapse([
            dbc.CardBody([
                html.P(description, className="text-muted mb-3"),
                incidents_table
            ])
        ], id=f"collapse-{title.lower().replace(' ', '-')}", is_open=True)
    ], className="mb-3")


def create_enhanced_solutions_display(solutions: List[Dict]) -> html.Div:
    """Create enhanced solutions display with effectiveness analysis"""

    # Categorize solutions by effectiveness
    proven_solutions = [s for s in solutions if s.get("effective") is True]
    unproven_solutions = [s for s in solutions if s.get("effective") is False]
    unknown_solutions = [s for s in solutions if s.get("effective") is None]

    sections = []

    # Proven solutions section
    if proven_solutions:
        sections.append(create_solutions_section(
            "Proven Effective Solutions",
            proven_solutions,
            "success",
            "These solutions have been verified as effective and can be confidently recommended."
        ))

    # Unproven solutions section
    if unproven_solutions:
        sections.append(create_solutions_section(
            "Solutions with Mixed Results",
            unproven_solutions,
            "warning",
            "These solutions have been tried but verified as ineffective or partially effective."
        ))

    # Unknown effectiveness section
    if unknown_solutions:
        sections.append(create_solutions_section(
            "Solutions Pending Verification",
            unknown_solutions,
            "info",
            "These solutions are documented but lack effectiveness verification data."
        ))

    return html.Div(sections)


def create_solutions_section(title: str, solutions: List[Dict], color: str, description: str) -> dbc.Card:
    """Create an expandable section for solutions"""

    solution_rows = []
    for solution in solutions[:10]:  # Limit display
        effectiveness_icon = "✅" if solution.get("effective") is True else "❌" if solution.get("effective") is False else "❓"
        effectiveness_score = solution.get("effectiveness_score", 0)

        solution_rows.append(
            html.Tr([
                html.Td(effectiveness_icon),
                html.Td(
                    html.Div(
                        solution.get("solution", "N/A")[:150] + "..."
                        if len(solution.get("solution", "")) > 150
                        else solution.get("solution", "N/A"),
                        title=solution.get("solution", "N/A")
                    )
                ),
                html.Td(solution.get("facility", "N/A")),
                html.Td(solution.get("root_cause", "N/A")),
                html.Td(f"{effectiveness_score:.1f}" if effectiveness_score else "N/A"),
            ])
        )

    solutions_table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Status"),
                html.Th("Solution Description"),
                html.Th("Facility"),
                html.Th("Root Cause"),
                html.Th("Score")
            ])
        ]),
        html.Tbody(solution_rows)
    ], striped=True, hover=True, size="sm")

    return dbc.Card([
        dbc.CardHeader([
            dbc.Button([
                html.I(className="fas fa-chevron-down me-2"),
                f"{title} ({len(solutions)})"
            ], id=f"collapse-{title.lower().replace(' ', '-').replace('/', '-')}-button",
               color=color, variant="light", className="w-100 text-start"),
        ]),
        dbc.Collapse([
            dbc.CardBody([
                html.P(description, className="text-muted mb-3"),
                solutions_table
            ])
        ], id=f"collapse-{title.lower().replace(' ', '-').replace('/', '-')}", is_open=True)
    ], className="mb-3")


def create_enhanced_facilities_display(facilities: List[Dict]) -> html.Div:
    """Create enhanced facilities display with pattern insights"""

    facility_rows = []
    for facility in facilities:
        incident_count = facility.get("incident_count", 0)
        equipment_types = facility.get("equipment_types", [])

        # Create severity indicator
        severity_color = "danger" if incident_count > 20 else "warning" if incident_count > 10 else "success"
        severity_icon = "🔴" if incident_count > 20 else "🟡" if incident_count > 10 else "🟢"

        facility_rows.append(
            html.Tr([
                html.Td(severity_icon),
                html.Td(facility.get("facility_id", "N/A")),
                html.Td([
                    dbc.Badge(str(incident_count), color=severity_color, className="me-1"),
                    "incidents"
                ]),
                html.Td(", ".join(equipment_types[:3]) + ("..." if len(equipment_types) > 3 else "")),
                html.Td(facility.get("cluster_size", "N/A") if "cluster_size" in facility else "N/A"),
            ])
        )

    facilities_table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th(""),
                html.Th("Facility"),
                html.Th("Incident Count"),
                html.Th("Equipment Types"),
                html.Th("Cluster Size")
            ])
        ]),
        html.Tbody(facility_rows)
    ], striped=True, hover=True, size="sm")

    return dbc.Card([
        dbc.CardBody([
            html.H6("Facility Pattern Analysis", className="mb-3"),
            html.P("Facilities ranked by incident frequency and equipment failure clusters.",
                   className="text-muted mb-3"),
            facilities_table
        ])
    ])


def create_search_insights_display(metadata: Dict[str, Any]) -> html.Div:
    """Create search insights and analytics display"""

    dimensions_executed = metadata.get("search_dimensions_executed", [])
    dimension_results = metadata.get("search_performance", {})
    total_results = metadata.get("total_results", 0)

    # Create dimension performance chart data
    dimension_cards = []

    dimension_info = {
        "direct_field_matches": {
            "name": "Direct Field Matches",
            "description": "Exact keyword matches in incident descriptions and titles",
            "icon": "fas fa-search"
        },
        "equipment_patterns": {
            "name": "Equipment Patterns",
            "description": "Asset-specific failure patterns and equipment categories",
            "icon": "fas fa-cogs"
        },
        "causal_chains": {
            "name": "Causal Chains",
            "description": "Root cause analysis and solution pathways",
            "icon": "fas fa-link"
        },
        "cross_facility_patterns": {
            "name": "Cross-Facility Patterns",
            "description": "Knowledge sharing opportunities across facilities",
            "icon": "fas fa-building"
        },
        "temporal_patterns": {
            "name": "Temporal Patterns",
            "description": "Time-based trends and seasonal incident patterns",
            "icon": "fas fa-clock"
        },
        "recurring_sequences": {
            "name": "Recurring Sequences",
            "description": "Repeat incidents and maintenance cycles",
            "icon": "fas fa-sync"
        },
        "solution_effectiveness": {
            "name": "Solution Effectiveness",
            "description": "Proven solutions with verification data",
            "icon": "fas fa-check-circle"
        },
        "equipment_failure_clusters": {
            "name": "Equipment Failure Clusters",
            "description": "Asset vulnerability and failure concentrations",
            "icon": "fas fa-exclamation-triangle"
        }
    }

    for dimension in dimensions_executed:
        count = dimension_results.get(dimension, 0)
        info = dimension_info.get(dimension, {"name": dimension, "description": "", "icon": "fas fa-circle"})

        color = "success" if count > 5 else "info" if count > 0 else "secondary"

        dimension_cards.append(
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className=f"{info['icon']} fa-2x text-{color} mb-2"),
                            html.H6(info["name"], className="mb-1"),
                            html.H4(str(count), className=f"text-{color} mb-2"),
                            html.Small(info["description"], className="text-muted")
                        ], className="text-center")
                    ])
                ], className="h-100")
            ], md=3, className="mb-3")
        )

    return html.Div([
        html.H6("Search Dimension Performance", className="mb-3"),
        html.P(f"Multi-dimensional search executed across {len(dimensions_executed)} dimensions, "
               f"returning {total_results} total results.", className="text-muted mb-4"),
        dbc.Row(dimension_cards)
    ])


def create_comprehensive_search_layout(search_terms: str) -> html.Div:
    """Display comprehensive search results across all dimensions"""
    try:
        data_adapter = get_data_adapter()
        search_data = data_adapter.execute_comprehensive_graph_search(search_terms)

        search_sections = []
        total_results = 0

        # Create section for each search dimension
        dimensions = [
            ("direct_matches", "Direct Field Matches", "🎯", "Exact matches in incident descriptions, root causes, and solutions"),
            ("equipment_patterns", "Equipment Patterns", "⚙️", "Similar equipment types and failure patterns"),
            ("causal_chains", "Causal Relationship Chains", "🔗", "Related cause-effect relationships"),
            ("cross_facility_patterns", "Cross-Facility Patterns", "🏭", "Similar incidents across different facilities"),
            ("temporal_patterns", "Temporal Patterns", "⏰", "Time-based incident patterns"),
            ("recurring_sequences", "Recurring Problem Sequences", "🔄", "Repeated problem sequences"),
            ("solution_effectiveness", "Solution Effectiveness", "✅", "Proven solution effectiveness"),
            ("equipment_clusters", "Equipment Failure Clusters", "📊", "Equipment failure clustering patterns")
        ]

        for key, title, icon, description in dimensions:
            results = search_data.get(key, [])
            if results:
                total_results += len(results)
                search_sections.append(
                    create_search_dimension_section_enhanced(title, results, len(results), icon, description)
                )

        if not search_sections:
            return dbc.Container([
                dbc.Alert([
                    html.I(className="fas fa-search me-2"),
                    html.Strong("No results found"),
                    html.P(f"No matches found for '{search_terms}'. Try different keywords or check spelling.", className="mb-0 mt-2")
                ], color="warning")
            ])

        # Create search summary
        search_summary = dbc.Card([
            dbc.CardBody([
                html.H4([
                    html.I(className="fas fa-search me-2"),
                    f"Search Results for: '{search_terms}'"
                ], className="text-primary mb-3"),
                dbc.Row([
                    dbc.Col([
                        html.H5(str(total_results), className="text-success mb-0"),
                        html.Small("Total Results", className="text-muted")
                    ], width=3),
                    dbc.Col([
                        html.H5(str(len(search_sections)), className="text-info mb-0"),
                        html.Small("Dimensions Matched", className="text-muted")
                    ], width=3),
                    dbc.Col([
                        html.H5(str(search_data.get('search_coverage', 0)), className="text-warning mb-0"),
                        html.Small("Search Coverage", className="text-muted")
                    ], width=3),
                ])
            ])
        ], className="mb-4")

        return dbc.Container([
            search_summary,
            html.Div(search_sections)
        ])

    except Exception as e:
        handle_error(logger, e, "comprehensive search layout")
        return dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "Search temporarily unavailable. Please try again."
        ], color="danger")

def create_search_dimension_section(title: str, results: List[Dict], count: int) -> html.Div:
    """Create section for each search dimension, displaying formatted results."""
    display_results = []
    for i, result in enumerate(results[:5]): # Limit to 5 results per section for brevity
        item_details = []
        for key, value in result.items():
            if isinstance(value, str) and len(value) > 150: # Limit long strings
                item_details.append(html.Span(f"• {key}: {value[:150]}...", title=value, className="d-block mb-1"))
            elif isinstance(value, (str, int, float)):
                item_details.append(html.Span(f"• {key}: {value}", className="d-block mb-1"))
            elif isinstance(value, list) and len(value) > 0:
                if all(isinstance(item, str) for item in value):
                    list_display = ', '.join(value[:3])
                    if len(value) > 3:
                        list_display += f" (+{len(value)-3} more)"
                else:
                    list_display = ', '.join(str(item) for item in value[:3])
                    if len(value) > 3:
                        list_display += f" (+{len(value)-3} more)"
                item_details.append(html.Span(f"• {key}: {list_display}", title=str(value), className="d-block mb-1"))
            elif isinstance(value, dict) and len(value) > 0:
                # Format dictionary content properly
                dict_items = []
                for dict_key, dict_value in list(value.items())[:3]:  # Show first 3 items
                    if isinstance(dict_value, str) and len(dict_value) > 50:
                        dict_items.append(f"{dict_key}: {dict_value[:50]}...")
                    else:
                        dict_items.append(f"{dict_key}: {dict_value}")

                dict_display = "{ " + "; ".join(dict_items)
                if len(value) > 3:
                    dict_display += f" (+{len(value)-3} more fields)"
                dict_display += " }"

                item_details.append(html.Span(f"• {key}: {dict_display}", title=str(value), className="d-block mb-1"))

        if item_details:
            display_results.append(
                dbc.Card(
                    dbc.CardBody(
                        [html.H6(f"Result {i+1}", className="text-primary mb-2"),
                         html.Div(item_details, className="small")]
                    ),
                    className="mb-2 border-start border-3 border-primary"
                )
            )
        else:
            display_results.append(html.P(f"Result {i+1}: No displayable details.", className="text-muted"))

    return dbc.Card([
        dbc.CardHeader([
            html.H5(f"{title}", className="mb-0 text-primary"),
            html.Small(f"{count} results found", className="text-muted")
        ]),
        dbc.CardBody(display_results)
    ], className="mb-3")


def create_search_dimension_section_enhanced(title: str, results: List[Dict], count: int, icon: str, description: str) -> html.Div:
    """Create enhanced section for each search dimension with better formatting."""
    display_results = []
    for i, result in enumerate(results[:5]): # Limit to 5 results per section for brevity
        item_details = []

        # Prioritize important fields for display
        priority_fields = ['incident_id', 'problem_description', 'root_cause', 'solution', 'facility', 'equipment']
        other_fields = []

        # Sort fields by priority
        for key, value in result.items():
            if key.lower() in priority_fields:
                item_details.append((key, value, True))  # Priority field
            else:
                other_fields.append((key, value, False))  # Regular field

        # Add other fields after priority fields
        item_details.extend(other_fields)

        formatted_details = []
        for key, value, is_priority in item_details:
            key_display = key.replace('_', ' ').title()

            if isinstance(value, str) and len(value) > 200:
                formatted_details.append(
                    html.Div([
                        html.Strong(f"{key_display}: ", className="text-primary" if is_priority else "text-secondary"),
                        html.Span(f"{value[:200]}...", title=value)
                    ], className="d-block mb-2")
                )
            elif isinstance(value, (str, int, float)) and value:
                formatted_details.append(
                    html.Div([
                        html.Strong(f"{key_display}: ", className="text-primary" if is_priority else "text-secondary"),
                        html.Span(str(value))
                    ], className="d-block mb-2")
                )
            elif isinstance(value, list) and len(value) > 0:
                if all(isinstance(item, str) for item in value):
                    list_display = ', '.join(value[:3])
                    if len(value) > 3:
                        list_display += f" (+{len(value)-3} more)"
                else:
                    list_display = ', '.join(str(item) for item in value[:3])
                    if len(value) > 3:
                        list_display += f" (+{len(value)-3} more)"
                formatted_details.append(
                    html.Div([
                        html.Strong(f"{key_display}: ", className="text-secondary"),
                        html.Span(list_display, title=str(value))
                    ], className="d-block mb-2")
                )
            elif isinstance(value, dict) and len(value) > 0:
                # Format dictionary content properly
                dict_items = []
                for dict_key, dict_value in list(value.items())[:2]:  # Show first 2 items
                    if isinstance(dict_value, str) and len(dict_value) > 30:
                        dict_items.append(f"{dict_key}: {dict_value[:30]}...")
                    else:
                        dict_items.append(f"{dict_key}: {dict_value}")

                dict_display = "; ".join(dict_items)
                if len(value) > 2:
                    dict_display += f" (+{len(value)-2} more)"

                formatted_details.append(
                    html.Div([
                        html.Strong(f"{key_display}: ", className="text-secondary"),
                        html.Span(dict_display, title=str(value))
                    ], className="d-block mb-2")
                )

        if formatted_details:
            display_results.append(
                dbc.Card(
                    dbc.CardBody(
                        [html.H6(f"{icon} Result {i+1}", className="text-primary mb-3"),
                         html.Div(formatted_details)]
                    ),
                    className="mb-3 border-start border-4 border-primary"
                )
            )

    return dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    html.H5([
                        html.Span(icon, className="me-2"),
                        title
                    ], className="mb-1 text-primary"),
                    html.Small(description, className="text-muted")
                ], width=10),
                dbc.Col([
                    dbc.Badge(f"{count} results", color="primary", className="fs-6")
                ], width=2, className="text-end")
            ])
        ]),
        dbc.CardBody(display_results if display_results else [
            html.P("No detailed results available for this dimension.", className="text-muted text-center")
        ])
    ], className="mb-4")


@callback(
    [
        Output("search-status", "children", allow_duplicate=True),
        Output("graph-search-results", "children", allow_duplicate=True),
    ],
    Input("search-graph-btn", "n_clicks"),
    State("graph-search-input", "value"),
    prevent_initial_call=True,
)
def execute_graph_search(n_clicks, search_term):
    if not n_clicks or not search_term:
        raise PreventUpdate

    logger.info(f"Graph Search: Executing search for '{search_term}'")
    status_message = html.Div([
        dbc.Spinner(size="sm", color="primary"),
        html.Span(f" Searching graph for '{search_term}'...", className="ms-2 text-info")
    ])

    data_adapter = get_data_adapter()
    json_recorder = JSONRecorder()

    try:
        # Execute the comprehensive search and get raw data
        search_data = data_adapter.execute_comprehensive_graph_search(search_term)

        # Save search results to JSON file
        try:
            json_filepath = json_recorder.save_search_results(
                search_term=search_term,
                search_data=search_data,
                metadata={
                    "search_type": "comprehensive_graph_search",
                    "dashboard_version": "v1.0",
                    "user_session": "dashboard_session"
                }
            )
            logger.info(f"Search results saved to JSON: {json_filepath}")
        except Exception as json_error:
            logger.warning(f"Failed to save search results to JSON: {str(json_error)}")
            # Continue with search display even if JSON saving fails

        # Create the results display using the existing comprehensive layout
        results_display = create_comprehensive_search_layout(search_term)
        return "", results_display

    except Exception as e:
        handle_error(logger, e, f"graph search execution for '{search_term}'")
        return "", dbc.Alert(f"An error occurred during search: {str(e)}", color="danger")

# Register collapsible section callbacks for multi-dimensional search results

@callback(
    Output("incidents-collapse", "is_open"),
    Input("incidents-collapse-btn", "n_clicks"),
    State("incidents-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_incidents_section(n_clicks, is_open):
    """Toggle incidents section visibility"""
    if n_clicks:
        return not is_open
    return is_open

@callback(
    Output("solutions-collapse", "is_open"),
    Input("solutions-collapse-btn", "n_clicks"),
    State("solutions-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_solutions_section(n_clicks, is_open):
    """Toggle solutions section visibility"""
    if n_clicks:
        return not is_open
    return is_open

@callback(
    Output("facilities-collapse", "is_open"),
    Input("facilities-collapse-btn", "n_clicks"),
    State("facilities-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_facilities_section(n_clicks, is_open):
    """Toggle facilities section visibility"""
    if n_clicks:
        return not is_open
    return is_open

@callback(
    Output("search-insights-collapse", "is_open"),
    Input("search-insights-collapse-btn", "n_clicks"),
    State("search-insights-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_search_insights_section(n_clicks, is_open):
    """Toggle search insights section visibility"""
    if n_clicks:
        return not is_open
    return is_open

@callback(
    Output("performance-summary-collapse", "is_open"),
    Input("performance-summary-collapse-btn", "n_clicks"),
    State("performance-summary-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_performance_summary_section(n_clicks, is_open):
    """Toggle performance summary section visibility"""
    if n_clicks:
        return not is_open
    return is_open

# Dimension-specific result callbacks for progressive loading

@callback(
    Output("dimension-details-modal", "is_open"),
    [Input({"type": "dimension-detail-btn", "index": ALL}, "n_clicks")],
    [State("dimension-details-modal", "is_open")],
    prevent_initial_call=True,
)
def toggle_dimension_details_modal(n_clicks_list, is_open):
    """Show detailed view of specific search dimension results"""
    if any(n_clicks_list):
        return not is_open
    return is_open

@callback(
    [Output("dimension-details-modal-title", "children"),
     Output("dimension-details-modal-body", "children")],
    [Input({"type": "dimension-detail-btn", "index": ALL}, "n_clicks")],
    prevent_initial_call=True,
)
def update_dimension_details_modal(n_clicks_list):
    """Update modal content with dimension-specific details"""
    if not any(n_clicks_list):
        raise PreventUpdate

    # Get which button was clicked
    ctx_trigger = ctx.triggered[0]
    if not ctx_trigger["value"]:
        raise PreventUpdate

    try:
        # Extract dimension info from triggered button
        button_id = ctx_trigger["prop_id"].split(".")[0]
        button_data = eval(button_id)  # Parse the pattern match ID
        dimension = button_data["index"]

        # Create dimension-specific content
        title = f"{dimension.replace('_', ' ').title()} Search Results"

        content = html.Div([
            dbc.Alert(
                f"Detailed analysis for {dimension} dimension",
                color="info",
                className="mb-3"
            ),
            html.P("Loading detailed results..."),
            dbc.Spinner(color="primary")
        ])

        return title, content

    except Exception as e:
        logger.error(f"Error updating dimension details modal: {e}")
        return "Search Dimension Details", html.P("Error loading details")

# Search filter callbacks for advanced search functionality

@callback(
    Output("graph-search-results", "children"),
    [Input("search-filter-dropdown", "value"),
     Input("date-range-picker", "start_date"),
     Input("date-range-picker", "end_date"),
     Input("facility-filter-dropdown", "value"),
     Input("severity-filter-dropdown", "value")],
    [State("graph-search-results", "children")],
    prevent_initial_call=True,
)
def filter_search_results(dimension_filter, start_date, end_date, facility_filter, severity_filter, current_results):
    """Apply advanced filters to search results"""
    if not current_results:
        raise PreventUpdate

    try:
        # Apply filters to existing results (placeholder implementation)
        # In production, this would re-query with filters
        filtered_info = dbc.Alert(
            [
                html.I(className="fas fa-filter me-2"),
                f"Applied filters: {', '.join(filter(None, [dimension_filter, facility_filter, severity_filter]))}"
            ],
            color="info",
            className="mt-3"
        )

        # Return current results with filter notification
        if isinstance(current_results, list):
            return current_results + [filtered_info]
        else:
            return [current_results, filtered_info]

    except Exception as e:
        logger.error(f"Error filtering search results: {e}")
        return current_results

# Export functionality callbacks

@callback(
    Output("download-search-results", "data"),
    Input("export-search-results-btn", "n_clicks"),
    [State("graph-search-results", "children"),
     State("graph-search-input", "value")],
    prevent_initial_call=True,
)
def export_search_results(n_clicks, search_results, search_term):
    """Export search results to CSV/Excel format"""
    if not n_clicks or not search_results:
        raise PreventUpdate

    try:
        # Create export data structure
        export_data = {
            "search_term": search_term or "unknown",
            "timestamp": datetime.now().isoformat(),
            "dimensions_analyzed": [
                "direct_field_matches",
                "equipment_patterns",
                "causal_chains",
                "cross_facility_patterns",
                "temporal_patterns",
                "recurring_sequences",
                "solution_effectiveness",
                "equipment_failure_clusters"
            ],
            "summary": "Multi-dimensional graph search results export"
        }

        # Convert to CSV format
        import pandas as pd
        df = pd.DataFrame([export_data])

        return dcc.send_data_frame(
            df.to_csv,
            f"graph_search_results_{search_term or 'query'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            index=False
        )

    except Exception as e:
        logger.error(f"Error exporting search results: {e}")
        raise PreventUpdate

# Progressive loading callbacks for large result sets

@callback(
    Output("load-more-incidents-btn", "style"),
    Output("incidents-pagination-info", "children"),
    [Input("load-more-incidents-btn", "n_clicks")],
    [State("graph-search-results", "children")],
    prevent_initial_call=True,
)
def handle_load_more_incidents(n_clicks, current_results):
    """Handle progressive loading of incident results"""
    if not n_clicks:
        raise PreventUpdate

    try:
        # Hide load more button and show loading info
        hidden_style = {"display": "none"}
        loading_info = dbc.Spinner(
            [html.Small("Loading more incidents...")],
            size="sm",
            color="primary"
        )

        return hidden_style, loading_info

    except Exception as e:
        logger.error(f"Error handling load more incidents: {e}")
        raise PreventUpdate

@callback(
    Output("search-performance-chart", "figure"),
    Input("graph-search-results", "children"),
    prevent_initial_call=True,
)
def update_search_performance_chart(search_results):
    """Update performance visualization chart based on search results"""
    if not search_results:
        raise PreventUpdate

    try:
        # Create mock performance data for visualization
        dimensions = [
            "Direct Matches", "Equipment Patterns", "Causal Chains",
            "Cross-Facility", "Temporal Patterns", "Recurring Sequences",
            "Solution Effectiveness", "Failure Clusters"
        ]

        # Mock results count per dimension
        results_count = [15, 12, 8, 6, 10, 5, 18, 9]

        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=dimensions,
                y=results_count,
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                            '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'],
                text=results_count,
                textposition='auto',
            )
        ])

        fig.update_layout(
            title="Search Results by Dimension",
            xaxis_title="Search Dimensions",
            yaxis_title="Results Count",
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        return fig

    except Exception as e:
        logger.error(f"Error updating search performance chart: {e}")
        # Return empty figure on error
        return go.Figure()

# Real-time search suggestions callback

@callback(
    Output("search-suggestions-dropdown", "options"),
    Input("graph-search-input", "value"),
    prevent_initial_call=True,
)
def update_search_suggestions(search_input):
    """Provide real-time search suggestions based on input"""
    if not search_input or len(search_input) < 2:
        return []

    try:
        # Mock search suggestions based on common mining equipment and issues
        suggestions = [
            "conveyor belt failure",
            "pump malfunction",
            "crusher breakdown",
            "electrical fault",
            "hydraulic system",
            "bearing replacement",
            "motor overheating",
            "valve leakage",
            "sensor calibration",
            "maintenance schedule"
        ]

        # Filter suggestions based on input
        filtered_suggestions = [
            {"label": suggestion, "value": suggestion}
            for suggestion in suggestions
            if search_input.lower() in suggestion.lower()
        ]

        return filtered_suggestions[:5]  # Limit to 5 suggestions

    except Exception as e:
        logger.error(f"Error updating search suggestions: {e}")
        return []

#!/usr/bin/env python3
"""
Graph Search Component - Simple Neo4j Graph Exploration
Direct search interface for comprehensive graph data extraction.
"""

import logging
from typing import Any, Dict, List

import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html

from dashboard.adapters.data_adapter import get_data_adapter
from dashboard.components.layout_template import create_standard_layout
from mine_core.shared.common import handle_error

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
    """Create comprehensive results display"""

    incidents = search_results.get("incidents", [])
    solutions = search_results.get("solutions", [])
    facilities = search_results.get("facilities", [])

    tabs_content = []

    # Incidents Tab
    if incidents:
        incident_rows = []
        for incident in incidents[:20]:
            incident_rows.append(
                html.Tr(
                    [
                        html.Td(incident.get("incident_id", "N/A")),
                        html.Td(incident.get("facility", "N/A")),
                        html.Td(incident.get("problem_description", "N/A")),
                        html.Td(incident.get("root_cause", "N/A")),
                        html.Td(incident.get("solution", "N/A")),
                    ]
                )
            )

        incidents_table = dbc.Table(
            [
                html.Thead(
                    [
                        html.Tr(
                            [
                                html.Th("Incident ID"),
                                html.Th("Facility"),
                                html.Th("Problem"),
                                html.Th("Root Cause"),
                                html.Th("Solution"),
                            ]
                        )
                    ]
                ),
                html.Tbody(incident_rows),
            ],
            striped=True,
            hover=True,
            size="sm",
        )

        tabs_content.append(
            dbc.Tab(label=f"Incidents ({len(incidents)})", children=[incidents_table])
        )

    # Solutions Tab
    if solutions:
        solution_rows = []
        for solution in solutions[:15]:
            effectiveness = "✅" if solution.get("effective") else "❌"
            solution_rows.append(
                html.Tr(
                    [
                        html.Td(effectiveness),
                        html.Td(solution.get("solution", "N/A")),
                        html.Td(solution.get("facility", "N/A")),
                        html.Td(solution.get("root_cause", "N/A")),
                    ]
                )
            )

        solutions_table = dbc.Table(
            [
                html.Thead(
                    [
                        html.Tr(
                            [
                                html.Th("Effective"),
                                html.Th("Solution"),
                                html.Th("Facility"),
                                html.Th("Root Cause"),
                            ]
                        )
                    ]
                ),
                html.Tbody(solution_rows),
            ],
            striped=True,
            hover=True,
            size="sm",
        )

        tabs_content.append(
            dbc.Tab(label=f"Solutions ({len(solutions)})", children=[solutions_table])
        )

    # Facilities Tab
    if facilities:
        facility_rows = []
        for facility in facilities:
            facility_rows.append(
                html.Tr(
                    [
                        html.Td(facility.get("facility_id", "N/A")),
                        html.Td(facility.get("incident_count", 0)),
                        html.Td(", ".join(facility.get("equipment_types", [])[:3])),
                    ]
                )
            )

        facilities_table = dbc.Table(
            [
                html.Thead(
                    [
                        html.Tr(
                            [html.Th("Facility"), html.Th("Incidents"), html.Th("Equipment Types")]
                        )
                    ]
                ),
                html.Tbody(facility_rows),
            ],
            striped=True,
            hover=True,
            size="sm",
        )

        tabs_content.append(
            dbc.Tab(label=f"Facilities ({len(facilities)})", children=[facilities_table])
        )

    if not tabs_content:
        return dbc.Alert("No results found", color="warning")

    return dbc.Card(
        [
            dbc.CardHeader([html.H5("Search Results", className="mb-0")]),
            dbc.CardBody([dbc.Tabs(tabs_content)]),
        ]
    )


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
    """Execute comprehensive graph search"""
    if not n_clicks or not search_term:
        return "", ""

    try:
        # Show search in progress
        status = dbc.Alert(
            [
                dbc.Spinner(size="sm", spinnerClassName="me-2"),
                f"Searching graph for '{search_term}'...",
            ],
            color="info",
        )

        # Execute search
        data_adapter = get_data_adapter()
        results = data_adapter.execute_comprehensive_graph_search(search_term)

        # Update status
        total_results = sum(
            len(results.get(key, [])) for key in ["incidents", "solutions", "facilities"]
        )
        status = dbc.Alert(
            [
                html.I(className="fas fa-check-circle me-2"),
                f"Found {total_results} related records",
            ],
            color="success",
        )

        # Create results display
        results_display = create_results_display(results)

        return status, results_display

    except Exception as e:
        handle_error(logger, e, f"graph search for '{search_term}'")
        error_status = dbc.Alert(
            [html.I(className="fas fa-exclamation-triangle me-2"), f"Search failed: {str(e)}"],
            color="danger",
        )

        return error_status, ""

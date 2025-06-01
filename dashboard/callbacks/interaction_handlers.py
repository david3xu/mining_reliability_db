#!/usr/bin/env python3
"""
Dashboard Interaction Handlers - Core Callback Logic
Centralized interaction management for dashboard components.
"""

import logging
import json
from typing import Dict, Any, Optional, List
from dash import Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate

from dashboard.adapters import get_data_adapter
from dashboard.utils.url_builders import build_facility_url, build_detail_url
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

class InteractionManager:
    """Centralized interaction handling for dashboard components"""

    def __init__(self):
        self.adapter = get_data_adapter()

    def register_callbacks(self, app):
        """Register all interaction callbacks with the Dash app"""
        self._register_chart_interactions(app)
        self._register_table_interactions(app)
        self._register_card_interactions(app)
        self._register_navigation_interactions(app)

    def _register_chart_interactions(self, app):
        """Register chart click interactions"""

        @app.callback(
            Output('chart-interaction-store', 'data'),
            Input('facility-pie-chart', 'clickData'),
            prevent_initial_call=True
        )
        def handle_pie_chart_click(click_data):
            """Handle pie chart slice clicks for facility navigation"""
            try:
                if not click_data:
                    raise PreventUpdate

                # Extract facility from clicked slice
                point = click_data['points'][0]
                facility_name = point['label']

                logger.info(f"Pie chart clicked: {facility_name}")

                return {
                    'action': 'navigate_facility',
                    'facility_id': facility_name,
                    'url': build_facility_url(facility_name),
                    'timestamp': ctx.triggered[0]['prop_id']
                }

            except Exception as e:
                handle_error(logger, e, "pie chart click handling")
                raise PreventUpdate

        @app.callback(
            Output('chart-interaction-store', 'data', allow_duplicate=True),
            Input('field-bar-chart', 'clickData'),
            prevent_initial_call=True
        )
        def handle_bar_chart_click(click_data):
            """Handle bar chart clicks for field type exploration"""
            try:
                if not click_data:
                    raise PreventUpdate

                point = click_data['points'][0]
                field_type = point['x']
                field_count = point['y']

                logger.info(f"Bar chart clicked: {field_type}")

                return {
                    'action': 'explore_field_type',
                    'field_type': field_type,
                    'count': field_count,
                    'url': build_detail_url('fields', field_type),
                    'timestamp': ctx.triggered[0]['prop_id']
                }

            except Exception as e:
                handle_error(logger, e, "bar chart click handling")
                raise PreventUpdate

    def _register_table_interactions(self, app):
        """Register table row click interactions"""

        @app.callback(
            Output('table-interaction-store', 'data'),
            Input('historical-timeline-table', 'active_cell'),
            prevent_initial_call=True
        )
        def handle_table_cell_click(active_cell):
            """Handle table cell clicks for facility navigation"""
            try:
                if not active_cell:
                    raise PreventUpdate

                # Get table data to identify clicked facility
                timeline_data = self.adapter.get_historical_timeline()

                row_index = active_cell['row']
                column_id = active_cell['column_id']

                if row_index < len(timeline_data.rows):
                    clicked_row = timeline_data.rows[row_index]
                    facility_id = clicked_row.get('facility')

                    if facility_id and facility_id != 'Total':
                        logger.info(f"Table clicked: {facility_id}, column: {column_id}")

                        return {
                            'action': 'navigate_facility',
                            'facility_id': facility_id,
                            'column': column_id,
                            'url': build_facility_url(facility_id),
                            'timestamp': ctx.triggered[0]['prop_id']
                        }

                raise PreventUpdate

            except Exception as e:
                handle_error(logger, e, "table click handling")
                raise PreventUpdate

    def _register_card_interactions(self, app):
        """Register metric card click interactions"""

        @app.callback(
            Output('card-interaction-store', 'data'),
            [Input('total-records-card', 'n_clicks'),
             Input('data-fields-card', 'n_clicks'),
             Input('facilities-card', 'n_clicks'),
             Input('years-card', 'n_clicks')],
            prevent_initial_call=True
        )
        def handle_metric_card_clicks(records_clicks, fields_clicks,
                                    facilities_clicks, years_clicks):
            """Handle metric card clicks for detailed exploration"""
            try:
                if not any([records_clicks, fields_clicks, facilities_clicks, years_clicks]):
                    raise PreventUpdate

                # Determine which card was clicked
                triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

                card_actions = {
                    'total-records-card': {
                        'action': 'explore_records',
                        'detail_type': 'records',
                        'url': build_detail_url('records', 'all')
                    },
                    'data-fields-card': {
                        'action': 'explore_fields',
                        'detail_type': 'fields',
                        'url': build_detail_url('fields', 'distribution')
                    },
                    'facilities-card': {
                        'action': 'explore_facilities',
                        'detail_type': 'facilities',
                        'url': build_detail_url('facilities', 'overview')
                    },
                    'years-card': {
                        'action': 'explore_timeline',
                        'detail_type': 'timeline',
                        'url': build_detail_url('timeline', 'analysis')
                    }
                }

                if triggered_id in card_actions:
                    action_data = card_actions[triggered_id]
                    logger.info(f"Metric card clicked: {triggered_id}")

                    return {
                        **action_data,
                        'timestamp': ctx.triggered[0]['prop_id']
                    }

                raise PreventUpdate

            except Exception as e:
                handle_error(logger, e, "metric card click handling")
                raise PreventUpdate

    def _register_navigation_interactions(self, app):
        """Register navigation callback for interaction results"""

        @app.callback(
            Output('url-location', 'pathname'),
            [Input('chart-interaction-store', 'data'),
             Input('table-interaction-store', 'data'),
             Input('card-interaction-store', 'data')],
            prevent_initial_call=True
        )
        def handle_navigation_from_interactions(chart_data, table_data, card_data):
            """Navigate based on interaction data"""
            try:
                # Get the triggered interaction
                interaction_data = None

                if ctx.triggered:
                    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

                    if trigger_id == 'chart-interaction-store' and chart_data:
                        interaction_data = chart_data
                    elif trigger_id == 'table-interaction-store' and table_data:
                        interaction_data = table_data
                    elif trigger_id == 'card-interaction-store' and card_data:
                        interaction_data = card_data

                if interaction_data and interaction_data.get('url'):
                    target_url = interaction_data['url']
                    logger.info(f"Navigating to: {target_url}")
                    return target_url

                raise PreventUpdate

            except Exception as e:
                handle_error(logger, e, "navigation from interactions")
                raise PreventUpdate

def get_enhanced_chart_config():
    """Get chart configuration with interaction support"""
    return {
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
        'displaylogo': False,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'mining_reliability_chart',
            'height': 500,
            'width': 700,
            'scale': 1
        }
    }

def get_enhanced_table_config():
    """Get table configuration with interaction support"""
    return {
        'row_selectable': 'single',
        'selected_rows': [],
        'cell_selectable': True,
        'sort_action': 'native',
        'filter_action': 'native'
    }

def create_interaction_tooltip(component_type: str, data: Dict[str, Any]) -> str:
    """Generate interaction tooltips for components"""
    tooltips = {
        'pie_slice': f"Click to explore {data.get('facility_name', 'facility')} details",
        'bar_segment': f"Click to analyze {data.get('field_type', 'field')} distribution",
        'metric_card': f"Click for detailed {data.get('metric_type', 'metric')} breakdown",
        'table_row': f"Click to view {data.get('facility_name', 'facility')} analysis"
    }

    return tooltips.get(component_type, "Click for more details")

# Export interaction manager instance
interaction_manager = InteractionManager()

#!/usr/bin/env python3
"""
Micro-Component: Table Base - Standardized Table Component
20-line atomic component for consistent data table display.
"""

from dash import dash_table

from dashboard.adapters import get_config_adapter


def create_data_table(
    data: list, columns: list, table_id: str = "data-table"
) -> dash_table.DataTable:
    """Pure data table component - 16 lines of logic"""
    config = get_config_adapter().get_styling_config()

    # Generate column definitions
    table_columns = [{"name": col, "id": col} for col in columns]

    return dash_table.DataTable(
        id=table_id,
        data=data,
        columns=table_columns,
        style_cell={
            "textAlign": "center",
            "padding": "12px",
            "fontFamily": "Arial, sans-serif",
            "fontSize": "14px",
            "border": f"1px solid {config.get('border_color', '#CCCCCC')}",
        },
        style_header={
            "backgroundColor": config.get("primary_color", "#4A90E2"),
            "color": "#FFFFFF",
            "fontWeight": "bold",
        },
        style_data={"backgroundColor": "#FFFFFF"},
        sort_action="native",
        page_size=10,
    )

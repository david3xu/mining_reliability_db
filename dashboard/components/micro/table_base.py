#!/usr/bin/env python3
"""
Micro-Component: Table Base - Standardized Table Component
20-line atomic component for consistent data table display.
"""

from dash import dash_table, dcc

from dashboard.adapters import get_config_adapter


def create_data_table(
    data: list, columns: list, table_id: str = "data-table", link_column: str = None
) -> dash_table.DataTable:
    """Pure data table component - 16 lines of logic"""
    config = get_config_adapter().get_styling_config()

    # Generate column definitions
    table_columns = []
    for col in columns:
        col_def = {"name": col, "id": col}
        if col == link_column:
            col_def["presentation"] = "markdown"
        table_columns.append(col_def)

    # Format data for markdown links if link_column is present
    if link_column:
        for row in data:
            if row.get(link_column) != "Total":
                if link_column in row and isinstance(row[link_column], str):
                    facility_display_name = row[link_column]
                    facility_id_for_link = row.get("facility_id_raw", facility_display_name)
                    row[
                        link_column
                    ] = f"[{facility_display_name}](/facility/{facility_id_for_link})"
            elif row.get(link_column) == "Total":
                # For the 'Total' row, ensure it's just the display name without a link
                row[link_column] = row.get(link_column)
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
        markdown_options={"link_target": "_self"},
        style_data_conditional=[{"if": {"column_id": link_column}, "textDecoration": "none"}]
        if link_column
        else [],
    )

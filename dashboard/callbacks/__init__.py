"""
Callbacks Package - Interaction Handlers
Dashboard interaction callbacks and event handlers.
"""

from dashboard.callbacks.interaction_handlers import (
    register_chart_interactions,
    register_table_interactions,
)

__all__ = [
    "register_chart_interactions",
    "register_table_interactions",
]

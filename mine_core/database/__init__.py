"""
Schema-driven database layer using model_schema.json
"""

from mine_core.database.connection import get_connection
from mine_core.database.db import get_database
from mine_core.database.queries import (
    get_facilities,
    get_facility,
    get_action_requests,
    get_action_request,
    get_incident_chain,
    get_department,
    get_assets,
    get_incident_counts_by_category,
    get_root_cause_frequency,
    get_effectiveness_stats
)
"""
Schema-driven entity definitions using model_schema.json
"""

from mine_core.entities.definitions import (
    create_entity_from_dict,
    get_entity_definitions,
    get_schema_manager,
)

__all__ = ["get_entity_definitions", "create_entity_from_dict", "get_schema_manager"]

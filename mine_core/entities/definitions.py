#!/usr/bin/env python3
"""
Schema-driven entity definitions using model_schema.json
"""

import logging
from typing import Any, Dict, List, Optional

from configs.environment import get_schema

__all__ = [
    "SchemaEntityManager",
    "get_schema_manager",
    "get_entity_definitions",
    "create_entity_from_dict",
    "get_primary_key",
    "get_required_fields",
]

logger = logging.getLogger(__name__)


class SchemaEntityManager:
    """Manages entities using schema definition only"""

    def __init__(self, schema=None):
        """Initialize from schema"""
        self.schema = schema or get_schema()
        self.entities = {e["name"]: e for e in self.schema.get("entities", [])}

    def get_entity_names(self) -> List[str]:
        """Get all entity names from schema"""
        return list(self.entities.keys())

    def get_entity_properties(self, entity_name: str) -> Dict[str, Any]:
        """Get entity properties from schema"""
        return self.entities.get(entity_name, {}).get("properties", {})

    def get_primary_key(self, entity_name: str) -> Optional[str]:
        """Get primary key field from schema"""
        properties = self.get_entity_properties(entity_name)
        for prop_name, prop_info in properties.items():
            if prop_info.get("primary_key", False):
                return prop_name
        return None

    def get_required_fields(self, entity_name: str) -> List[str]:
        """Get required fields from schema"""
        properties = self.get_entity_properties(entity_name)
        return [
            prop_name
            for prop_name, prop_info in properties.items()
            if prop_info.get("required", False)
        ]


# Global schema manager instance
_schema_manager = None


def get_schema_manager() -> SchemaEntityManager:
    """Get global schema manager"""
    global _schema_manager
    if _schema_manager is None:
        _schema_manager = SchemaEntityManager()
    return _schema_manager


def get_entity_definitions() -> Dict[str, Any]:
    """Get entity definitions from schema"""
    manager = get_schema_manager()
    return {name: manager.entities[name] for name in manager.get_entity_names()}


def create_entity_from_dict(entity_type: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create entity from dict using schema validation"""
    manager = get_schema_manager()

    if entity_type not in manager.entities:
        logger.error(f"Unknown entity type: {entity_type}")
        return None

    return data

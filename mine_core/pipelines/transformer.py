#!/usr/bin/env python3
"""
Schema-driven data transformer using model_schema.json
"""

import logging
from typing import Dict, List, Any, Optional, Union
from configs.environment import get_mappings, get_schema

logger = logging.getLogger(__name__)

class DataTransformer:
    """Schema-driven transformer"""

    def __init__(self, mappings=None, schema=None, use_config=True):
        """Initialize from schema and mappings"""
        if use_config:
            self.mappings = mappings or get_mappings()
            self.schema = schema or get_schema()
        else:
            self.mappings = mappings or {}
            self.schema = schema or {}

        self.list_fields = self.mappings.get("list_fields", [])
        self.field_mappings = self.mappings.get("entity_mappings", {})
        self.list_field_extraction = self.mappings.get("list_field_extraction", {"default": "head"})

        # Get entity info from schema
        self.entities = {entity["name"]: entity for entity in self.schema.get("entities", [])}
        self.entity_order = self._determine_entity_order()

    def _determine_entity_order(self) -> List[str]:
        """Determine entity processing order from schema relationships"""
        if not self.schema.get("relationships"):
            return list(self.entities.keys())

        # Build dependency graph from relationships
        dependencies = {entity_name: set() for entity_name in self.entities.keys()}

        for rel in self.schema.get("relationships", []):
            from_entity = rel["from"]
            to_entity = rel["to"]
            if from_entity in dependencies and to_entity in dependencies:
                dependencies[from_entity].add(to_entity)

        # Topological sort
        ordered = []
        remaining = set(dependencies.keys())

        while remaining:
            ready = [e for e in remaining if not (dependencies[e] & remaining)]
            if not ready:
                ready = list(remaining)

            for entity in ready:
                ordered.append(entity)
                remaining.remove(entity)

        logger.info(f"Entity processing order from schema: {ordered}")
        return ordered

    def transform_facility_data(self, facility_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform using schema-defined entities"""
        facility_id = facility_data.get("facility_id", "unknown")
        records = facility_data.get("records", [])

        # Build entities dict from schema
        entities_dict = {entity_name: [] for entity_name in self.entities.keys()}

        transformed = {
            "facility": {
                "facility_id": facility_id,
                "facility_name": facility_id.replace("_", " ").title(),
                "active": True
            },
            "entities": entities_dict
        }

        for record in records:
            self._transform_record(record, facility_id, transformed)

        for entity_type, entities in transformed["entities"].items():
            logger.info(f"Transformed {len(entities)} {entity_type} entities")

        return transformed

    def _transform_record(self, record: Dict[str, Any], facility_id: str, transformed: Dict[str, Any]) -> None:
        """Transform record using schema"""
        action_request_number = record.get("Action Request Number:")
        if not action_request_number:
            return

        entity_ids = self._generate_entity_ids(action_request_number)

        # Process entities in schema order
        for entity_name in self.entity_order:
            if entity_name == "Facility":
                continue

            entity_data = self._transform_entity(record, entity_name)
            if not entity_data:
                continue

            # Add primary key
            primary_key = self._get_primary_key(entity_name)
            if primary_key and primary_key in entity_ids:
                entity_data[primary_key] = entity_ids[primary_key]

            # Add foreign keys based on relationships
            self._add_foreign_keys(entity_name, entity_data, entity_ids, facility_id)

            # Add if has required data
            if self._has_required_data(entity_name, record):
                transformed["entities"][entity_name].append(entity_data)

    def _get_primary_key(self, entity_name: str) -> Optional[str]:
        """Get primary key field from schema"""
        entity = self.entities.get(entity_name, {})
        properties = entity.get("properties", {})

        for prop_name, prop_info in properties.items():
            if prop_info.get("primary_key", False):
                return prop_name
        return None

    def _add_foreign_keys(self, entity_name: str, entity_data: Dict, entity_ids: Dict, facility_id: str) -> None:
        """Add foreign keys based on schema relationships"""
        if entity_name == "ActionRequest":
            entity_data["facility_id"] = facility_id
            return

        # Find relationships where this entity is the 'from' entity
        for rel in self.schema.get("relationships", []):
            if rel["from"] == entity_name:
                to_entity = rel["to"]
                to_primary_key = self._get_primary_key(to_entity)
                if to_primary_key and to_primary_key in entity_ids:
                    entity_data[to_primary_key] = entity_ids[to_primary_key]

    def _has_required_data(self, entity_name: str, record: Dict) -> bool:
        """Check if record has data for this entity type"""
        mappings = self.field_mappings.get(entity_name, {})
        if not mappings:
            return False

        # Check if any mapped fields have data
        for target_field, source_field in mappings.items():
            if record.get(source_field):
                return True
        return False

    def _generate_entity_ids(self, action_request_number: str) -> Dict[str, str]:
        """Generate IDs for all entities from schema"""
        request_id = action_request_number.replace('-', '').lower()

        entity_ids = {}
        for entity_name in self.entities.keys():
            primary_key = self._get_primary_key(entity_name)
            if primary_key:
                prefix = entity_name.lower()[:4]
                entity_ids[primary_key] = f"{prefix}-{request_id}"

        return entity_ids

    def _transform_entity(self, record: Dict[str, Any], entity_type: str) -> Dict[str, Any]:
        """Transform entity using field mappings"""
        entity = {}
        field_mappings = self.field_mappings.get(entity_type, {})

        for target_field, source_field in field_mappings.items():
            if source_field in record:
                value = record[source_field]

                if source_field in self.list_fields:
                    value = self._extract_list_field_value(source_field, value)

                if value is not None and (not isinstance(value, str) or value.strip()):
                    entity[target_field] = value

        return entity

    def _extract_list_field_value(self, field_name: str, value: Union[str, List[str]]) -> Optional[str]:
        """Extract value from list fields using config"""
        if not isinstance(value, list) or not value:
            return value

        extraction_method = self.list_field_extraction.get(field_name,
                                                          self.list_field_extraction.get("default", "head"))

        if extraction_method == "tail" and len(value) > 1:
            return value[1]
        else:
            return value[0]
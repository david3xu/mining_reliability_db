#!/usr/bin/env python3
"""
Schema-driven loader using model_schema.json relationships
"""

import logging
from typing import Dict, List, Any, Optional
from mine_core.database.db import get_database
from configs.environment import get_schema

logger = logging.getLogger(__name__)

class Neo4jLoader:
    """Schema-driven loader"""

    def __init__(self, uri=None, user=None, password=None, schema=None):
        """Initialize with schema"""
        self.db = get_database(uri, user, password)
        self.schema = schema or get_schema()

        # Extract entities and relationships from schema
        self.entities = {e["name"]: e for e in self.schema.get("entities", [])}
        self.relationships = self.schema.get("relationships", [])
        self.entity_order = self._determine_load_order()

    def _determine_load_order(self) -> List[str]:
        """Determine entity load order from schema dependencies"""
        # Build dependency graph
        dependencies = {entity_name: set() for entity_name in self.entities.keys()}

        # Add dependencies based on relationships
        for rel in self.relationships:
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

        logger.info(f"Entity load order from schema: {ordered}")
        return ordered

    def close(self):
        """Close database connection"""
        self.db.close()

    def load_data(self, transformed_data: Dict[str, Any]) -> bool:
        """Load data using schema-defined order"""
        try:
            facility = transformed_data.get("facility", {})
            entities = transformed_data.get("entities", {})

            # Load facility first
            self._load_facility(facility)

            # Load entities in schema-determined order
            for entity_type in self.entity_order:
                if entity_type in entities:
                    self._load_entities(entities[entity_type], entity_type)

            # Create relationships from schema
            self._create_schema_relationships(entities)

            logger.info("Data loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False

    def _load_facility(self, facility: Dict[str, Any]):
        """Load facility entity"""
        if facility:
            self.db.create_entity("Facility", facility)
            logger.info(f"Loaded facility: {facility.get('facility_id')}")

    def _load_entities(self, entities: List[Dict[str, Any]], entity_type: str):
        """Load entities of specific type"""
        if entities:
            self.db.batch_create_entities(entity_type, entities)
            logger.info(f"Loaded {len(entities)} {entity_type} entities")

    def _create_schema_relationships(self, entities: Dict[str, List[Dict[str, Any]]]):
        """Create relationships defined in schema"""
        for rel_config in self.relationships:
            from_type = rel_config["from"]
            to_type = rel_config["to"]
            rel_type = rel_config["type"]

            from_entities = entities.get(from_type, [])
            if not from_entities:
                continue

            # Get primary keys from schema
            from_pk = self._get_primary_key(from_type)
            to_pk = self._get_primary_key(to_type)

            if not from_pk or not to_pk:
                logger.warning(f"Missing primary keys for {from_type}-{to_type} relationship")
                continue

            self._create_relationship_batch(from_type, from_pk, rel_type, to_type, to_pk, from_entities)

    def _get_primary_key(self, entity_name: str) -> Optional[str]:
        """Get primary key from schema"""
        entity = self.entities.get(entity_name, {})
        properties = entity.get("properties", {})

        for prop_name, prop_info in properties.items():
            if prop_info.get("primary_key", False):
                return prop_name
        return None

    def _create_relationship_batch(self, from_type, from_field, rel_type, to_type, to_field, entities):
        """Create relationships in batch"""
        relationship_count = 0

        for entity in entities:
            from_id = entity.get(from_field)
            to_id = entity.get(to_field, from_id)

            if from_id and to_id:
                if self.db.create_relationship(from_type, from_id, rel_type, to_type, to_id):
                    relationship_count += 1

        if relationship_count > 0:
            logger.info(f"Created {relationship_count} {from_type}-[{rel_type}]->{to_type} relationships")
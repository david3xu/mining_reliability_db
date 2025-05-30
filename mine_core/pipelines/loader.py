#!/usr/bin/env python3
"""
Data Loader for Mining Reliability Database
Loads transformed data into Neo4j.
"""

import logging
from typing import Dict, List, Any
from mine_core.database.db import get_database

logger = logging.getLogger(__name__)

class Neo4jLoader:
    """Loads transformed data into Neo4j database"""

    def __init__(self, uri=None, user=None, password=None):
        """Initialize loader with database connection"""
        self.db = get_database(uri, user, password)

    def close(self):
        """Close database connection"""
        self.db.close()

    def load_data(self, transformed_data: Dict[str, Any]) -> bool:
        """Load transformed data into Neo4j"""
        try:
            facility = transformed_data.get("facility", {})
            entities = transformed_data.get("entities", {})

            # Load facility
            self._load_facility(facility)

            # Load entities in hierarchical order
            entity_order = [
                "ActionRequest", "Problem", "RootCause", "ActionPlan",
                "Verification", "Department", "Asset", "RecurringStatus",
                "AmountOfLoss", "Review", "EquipmentStrategy"
            ]

            for entity_type in entity_order:
                self._load_entities(entities.get(entity_type, []), entity_type)

            # Create relationships
            self._create_relationships(entities)
            return True

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False

    def _load_facility(self, facility: Dict[str, Any]):
        """Load facility node"""
        if not facility:
            logger.warning("No facility data to load")
            return

        self.db.create_entity("Facility", facility)
        logger.info(f"Loaded facility: {facility.get('facility_id')}")

    def _load_entities(self, entities: List[Dict[str, Any]], entity_type: str):
        """Load entities of a specific type"""
        if not entities:
            return

        self.db.batch_create_entities(entity_type, entities)
        logger.info(f"Loaded {len(entities)} {entity_type} entities")

    def _create_relationships(self, entities: Dict[str, List[Dict[str, Any]]]):
        """Create relationships between entities"""
        # Fixed relationship configurations with correct fields and directions
        relationship_configs = [
            # Core hierarchical chain
            ("ActionRequest", "facility_id", "BELONGS_TO", "Facility", "facility_id"),
            ("Problem", "action_request_id", "IDENTIFIED_IN", "ActionRequest", "action_request_id"),
            ("RootCause", "problem_id", "ANALYZES", "Problem", "problem_id"),
            ("ActionPlan", "root_cause_id", "RESOLVES", "RootCause", "cause_id"),
            ("Verification", "action_plan_id", "VALIDATES", "ActionPlan", "plan_id"),

            # Supporting relationships
            ("Asset", "problem_id", "INVOLVED_IN", "Problem", "problem_id"),
            ("AmountOfLoss", "problem_id", "QUANTIFIES", "Problem", "problem_id"),
            ("RecurringStatus", "problem_id", "CLASSIFIES", "Problem", "problem_id"),
            ("Department", "action_request_id", "ASSIGNED_TO", "ActionRequest", "action_request_id"),
            ("Review", "action_plan_id", "EVALUATES", "ActionPlan", "plan_id"),
            ("EquipmentStrategy", "action_plan_id", "MODIFIES", "ActionPlan", "plan_id")
        ]

        for from_type, from_field, rel_type, to_type, to_field in relationship_configs:
            self._create_relationship_batch(from_type, from_field, rel_type,
                                          to_type, to_field, entities.get(from_type, []))

    def _create_relationship_batch(self, from_type, from_field, rel_type, to_type, to_field, entities):
        """Create relationships in batch with proper ID resolution"""
        if not entities:
            return

        # Get primary key field names for both entity types
        from_pk_field = self._get_primary_key_field(from_type)
        to_pk_field = self._get_primary_key_field(to_type)

        relationship_count = 0
        for entity in entities:
            # Get the source entity's primary key
            from_id = entity.get(from_pk_field)

            # Get the target entity's ID that this entity references
            to_id = entity.get(from_field)

            if from_id and to_id:
                if self.db.create_relationship(from_type, from_id, rel_type, to_type, to_id):
                    relationship_count += 1

        if relationship_count > 0:
            logger.info(f"Created {relationship_count} {from_type}-[{rel_type}]->{to_type} relationships")

    def _get_primary_key_field(self, entity_type):
        """Get primary key field name for entity type"""
        # Maps entity types to their actual primary key field names
        pk_mapping = {
            "RootCause": "cause_id",
            "ActionPlan": "plan_id",
            "RecurringStatus": "recurring_id",
            "AmountOfLoss": "loss_id",
            "EquipmentStrategy": "strategy_id",
            "Department": "dept_id"
        }
        return pk_mapping.get(entity_type, f"{entity_type.lower()}_id")

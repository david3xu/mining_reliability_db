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
        # Get database connection from unified interface
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
            self._load_entities(entities.get("ActionRequest", []), "ActionRequest")
            self._load_entities(entities.get("Problem", []), "Problem")
            self._load_entities(entities.get("RootCause", []), "RootCause")
            self._load_entities(entities.get("ActionPlan", []), "ActionPlan")
            self._load_entities(entities.get("Verification", []), "Verification")

            # Load supporting entities
            self._load_entities(entities.get("Department", []), "Department")
            self._load_entities(entities.get("Asset", []), "Asset")
            self._load_entities(entities.get("RecurringStatus", []), "RecurringStatus")
            self._load_entities(entities.get("AmountOfLoss", []), "AmountOfLoss")
            self._load_entities(entities.get("Review", []), "Review")
            self._load_entities(entities.get("EquipmentStrategy", []), "EquipmentStrategy")

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
            logger.info(f"No {entity_type} entities to load")
            return

        # Use batch creation for efficiency
        self.db.batch_create_entities(entity_type, entities)
        logger.info(f"Loaded {len(entities)} {entity_type} entities")

    def _create_relationships(self, entities: Dict[str, List[Dict[str, Any]]]):
        """Create relationships between entities"""
        # Create hierarchical chain relationships
        self._create_relationship_batch("ActionRequest", "facility_id", "BELONGS_TO", "Facility", "facility_id",
                                       entities.get("ActionRequest", []))

        self._create_relationship_batch("Problem", "action_request_id", "IDENTIFIED_IN", "ActionRequest", "action_request_id",
                                       entities.get("Problem", []))

        self._create_relationship_batch("RootCause", "problem_id", "ANALYZES", "Problem", "problem_id",
                                       entities.get("RootCause", []))

        self._create_relationship_batch("ActionPlan", "root_cause_id", "RESOLVES", "RootCause", "cause_id",
                                       entities.get("ActionPlan", []))

        self._create_relationship_batch("Verification", "action_plan_id", "VALIDATES", "ActionPlan", "plan_id",
                                       entities.get("Verification", []))

        # Create supporting entity relationships
        self._create_relationship_batch("Asset", "problem_id", "INVOLVED_IN", "Problem", "problem_id",
                                       entities.get("Asset", []))

        self._create_relationship_batch("AmountOfLoss", "problem_id", "QUANTIFIES", "Problem", "problem_id",
                                       entities.get("AmountOfLoss", []))

        self._create_relationship_batch("RecurringStatus", "problem_id", "CLASSIFIES", "Problem", "problem_id",
                                       entities.get("RecurringStatus", []))

        self._create_relationship_batch("Department", "action_request_id", "ASSIGNED_TO", "ActionRequest", "action_request_id",
                                       entities.get("Department", []))

        self._create_relationship_batch("Review", "action_plan_id", "EVALUATES", "ActionPlan", "plan_id",
                                       entities.get("Review", []))

        self._create_relationship_batch("EquipmentStrategy", "action_plan_id", "MODIFIES", "ActionPlan", "plan_id",
                                       entities.get("EquipmentStrategy", []))

    def _create_relationship_batch(self, from_type, from_field, rel_type, to_type, to_field, entities):
        """Create relationships in batch"""
        if not entities:
            return

        relationship_count = 0

        # Create individual relationships
        for entity in entities:
            from_id = entity.get(from_field)
            to_id = entity.get(to_field, from_id)  # Default to from_id if to_field not in entity

            if from_id and to_id:
                if self.db.create_relationship(from_type, from_id, rel_type, to_type, to_id):
                    relationship_count += 1

        if relationship_count > 0:
            logger.info(f"Created {relationship_count} {from_type}-[{rel_type}]->{to_type} relationships")

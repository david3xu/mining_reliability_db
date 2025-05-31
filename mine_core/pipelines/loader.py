#!/usr/bin/env python3
"""
Simplified Data Loader for Mining Reliability Database
Clean implementation without backwards compatibility pollution.
"""

import logging
from typing import Dict, List, Any
from mine_core.database.db import get_database
from mine_core.shared.constants import ENTITY_LOAD_ORDER, RELATIONSHIP_CONFIGS
from mine_core.shared.common import handle_error
from mine_core.shared.field_utils import (
    has_real_value,
    is_missing_data_indicator
)

logger = logging.getLogger(__name__)

class SimplifiedLoader:
    """Streamlined loader for clean single-value datasets"""

    def __init__(self, uri=None, user=None, password=None):
        """Initialize loader with database connection"""
        self.db = get_database(uri, user, password)

    def close(self):
        """Close database connection"""
        self.db.close()

    def load_data(self, transformed_data: Dict[str, Any]) -> bool:
        """Load simplified transformed data into Neo4j"""
        try:
            facility = transformed_data.get("facility", {})
            entities = transformed_data.get("entities", {})

            # Load facility first
            if not self._load_facility(facility):
                return False

            # Load entities with dynamic labeling support
            if not self._load_all_entities(entities):
                return False

            # Create relationships
            if not self._create_all_relationships(entities):
                return False

            logger.info("Simplified data loading completed successfully")
            return True

        except Exception as e:
            handle_error(logger, e, "simplified data loading")
            return False

    def _load_facility(self, facility: Dict[str, Any]) -> bool:
        """Load facility node"""
        if not facility:
            logger.warning("No facility data to load")
            return True

        if self.db.create_entity_with_dynamic_label("Facility", facility):
            logger.info(f"Loaded facility: {facility.get('facility_id')}")
            return True
        return False

    def _load_all_entities(self, entities: Dict[str, List[Dict[str, Any]]]) -> bool:
        """Load all entities in hierarchical order"""
        for entity_type in ENTITY_LOAD_ORDER:
            entity_list = entities.get(entity_type, [])
            if not self._load_entities_with_labeling(entity_list, entity_type):
                return False
        return True

    def _load_entities_with_labeling(self, entities: List[Dict[str, Any]], entity_type: str) -> bool:
        """Load entities with dynamic label support"""
        if not entities:
            logger.debug(f"No {entity_type} entities to load")
            return True

        # Handle conditional creation for entities that might not have required data
        conditional_entities = ["Problem", "RootCause", "ActionPlan", "Verification"]

        if entity_type in conditional_entities:
            success_count = 0
            for entity in entities:
                if self._create_entity_conditionally(entity_type, entity.copy()):
                    success_count += 1

            if success_count > 0:
                logger.info(f"Loaded {success_count}/{len(entities)} {entity_type} entities")
            return True
        else:
            # Batch create for non-conditional entities
            if self.db.batch_create_entities_with_labels(entity_type, entities):
                logger.info(f"Loaded {len(entities)} {entity_type} entities")
                return True
            return False

    def _create_entity_conditionally(self, entity_type: str, entity_data: Dict[str, Any]) -> bool:
        """Create entity only if it has meaningful data"""
        # Extract dynamic label if present
        dynamic_label = entity_data.pop("_dynamic_label", None)

        # Check if entity has enough meaningful data using centralized validation
        if not self._has_sufficient_data(entity_data, entity_type):
            logger.debug(f"Skipping {entity_type} - insufficient data")
            return True  # Success, but no entity created

        return self.db.create_entity_with_dynamic_label(entity_type, entity_data, dynamic_label)

    def _has_sufficient_data(self, entity_data: Dict[str, Any], entity_type: str) -> bool:
        """Check if entity has sufficient data for creation using centralized validation"""
        # Define critical fields per entity type
        critical_fields = {
            "ActionRequest": ["action_request_number"],
            "Problem": ["what_happened"],
            "RootCause": ["root_cause"],
            "ActionPlan": ["action_plan"],
            "Verification": ["is_action_plan_effective"]
        }

        required_fields = critical_fields.get(entity_type, [])

        # Check if any critical field has real data using centralized validation
        for field in required_fields:
            value = entity_data.get(field)
            if has_real_value(value):
                return True

        # For entities without specific critical fields, check overall data completeness
        if not required_fields:
            meaningful_fields = sum(1 for value in entity_data.values()
                                  if has_real_value(value))
            return meaningful_fields >= 1

        return False

    def _create_all_relationships(self, entities: Dict[str, List[Dict[str, Any]]]) -> bool:
        """Create all entity relationships"""
        for config in RELATIONSHIP_CONFIGS:
            from_type, from_field, rel_type, to_type, to_field = config
            if not self._create_relationship_batch(from_type, from_field, rel_type,
                                                 to_type, to_field, entities.get(from_type, [])):
                return False
        return True

    def _create_relationship_batch(self, from_type: str, from_field: str, rel_type: str,
                                 to_type: str, to_field: str, entities: List[Dict[str, Any]]) -> bool:
        """Create relationships in batch for entity type"""
        if not entities:
            return True

        relationship_count = 0
        failed_count = 0

        for entity in entities:
            from_id = entity.get(from_field)
            to_id = entity.get(to_field, from_id)

            if from_id and to_id:
                if self.db.create_relationship(from_type, from_id, rel_type, to_type, to_id):
                    relationship_count += 1
                else:
                    failed_count += 1

        if relationship_count > 0:
            logger.info(f"Created {relationship_count} {from_type}-[{rel_type}]->{to_type} relationships")

        if failed_count > 0:
            logger.warning(f"Failed to create {failed_count} {from_type}-[{rel_type}]->{to_type} relationships")

        # Allow some failures but not total failure
        return failed_count < len(entities)

    def load_facility_data_complete(self, facility_id: str, transformed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Load facility data and return loading statistics"""
        stats = {
            "facility_id": facility_id,
            "entities_loaded": {},
            "relationships_created": 0,
            "load_success": False
        }

        try:
            # Load data
            success = self.load_data(transformed_data)
            stats["load_success"] = success

            if success:
                # Calculate loading statistics
                entities = transformed_data.get("entities", {})
                for entity_type, entity_list in entities.items():
                    stats["entities_loaded"][entity_type] = len(entity_list)

                # Estimate relationships created
                total_entities = sum(len(entity_list) for entity_list in entities.values())
                stats["relationships_created"] = max(0, total_entities - 1)  # Approximate

                logger.info(f"Successfully loaded facility {facility_id} with {total_entities} total entities")

        except Exception as e:
            handle_error(logger, e, f"loading facility {facility_id}")
            stats["load_success"] = False

        return stats

    def validate_loading_integrity(self, transformed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data integrity after loading"""
        validation_results = {
            "facility_check": False,
            "entity_counts": {},
            "relationship_validation": False,
            "causal_chain_integrity": False
        }

        try:
            facility_id = transformed_data.get("facility", {}).get("facility_id")

            if facility_id:
                # Check facility exists
                facility_check = self.db.execute_query(
                    "MATCH (f:Facility {facility_id: $facility_id}) RETURN count(f) AS count",
                    facility_id=facility_id
                )
                validation_results["facility_check"] = facility_check[0]["count"] > 0

                # Check entity counts
                entities = transformed_data.get("entities", {})
                for entity_type, entity_list in entities.items():
                    if entity_list:
                        actual_count = self.db.execute_query(
                            f"MATCH (e:{entity_type}) WHERE e.facility_id = $facility_id OR e.actionrequest_id CONTAINS $facility_id RETURN count(e) AS count",
                            facility_id=facility_id
                        )
                        validation_results["entity_counts"][entity_type] = actual_count[0]["count"]

                # Check causal chain integrity (ActionRequest -> Problem -> RootCause -> ActionPlan)
                causal_chain_check = self.db.execute_query(
                    """
                    MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility {facility_id: $facility_id})
                    MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)<-[:RESOLVES]-(ap:ActionPlan)
                    RETURN count(*) AS causal_chains
                    """,
                    facility_id=facility_id
                )
                validation_results["causal_chain_integrity"] = causal_chain_check[0]["causal_chains"] > 0

        except Exception as e:
            handle_error(logger, e, "validation")

        return validation_results

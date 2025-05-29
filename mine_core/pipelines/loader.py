#!/usr/bin/env python3
"""
Data Loader for Mining Reliability Database
Loads transformed data into Neo4j.
"""

import os
import logging
from typing import Dict, List, Any
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class Neo4jLoader:
    """Loads transformed data into Neo4j database"""

    def __init__(self, uri=None, user=None, password=None):
        """Initialize with Neo4j connection parameters"""
        # Use environment variables if parameters not provided
        self.uri = uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.environ.get("NEO4J_USER", "neo4j")
        self.password = password or os.environ.get("NEO4J_PASSWORD", "password")

        # Create driver on demand (lazy loading)
        self._driver = None

    @property
    def driver(self):
        """Get Neo4j driver, creating it if necessary"""
        if self._driver is None:
            logger.info(f"Connecting to Neo4j at {self.uri}")
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
        return self._driver

    def close(self):
        """Close Neo4j connection"""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")

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

        with self.driver.session() as session:
            query = """
            MERGE (f:Facility {facility_id: $facility_id})
            SET f.facility_name = $facility_name,
                f.active = $active
            """

            session.run(query, **facility)
            logger.info(f"Loaded facility: {facility.get('facility_id')}")

    def _load_entities(self, entities: List[Dict[str, Any]], entity_type: str):
        """Load entities of a specific type"""
        if not entities:
            logger.info(f"No {entity_type} entities to load")
            return

        with self.driver.session() as session:
            # Prepare batch parameters for the query
            batch_params = {"entities": entities}

            # Create query to merge entities of this type
            id_field = f"{entity_type.lower()}_id"

            # Build SET clause dynamically based on first entity's properties
            if entities:
                # Get all properties excluding ID (already in MERGE)
                sample_entity = entities[0]
                properties = [k for k in sample_entity.keys() if k != id_field]

                # Build the query
                if properties:
                    # Build SET clause
                    set_clause = ", ".join([
                        f"e.{prop} = entity.{prop}" for prop in properties
                    ])

                    query = f"""
                    UNWIND $entities AS entity
                    MERGE (e:{entity_type} {{{id_field}: entity.{id_field}}})
                    SET {set_clause}
                    """
                else:
                    # No properties to set
                    query = f"""
                    UNWIND $entities AS entity
                    MERGE (e:{entity_type} {{{id_field}: entity.{id_field}}})
                    """

                # Execute the query
                result = session.run(query, **batch_params)
                logger.info(f"Loaded {len(entities)} {entity_type} entities")

    def _create_relationships(self, entities: Dict[str, List[Dict[str, Any]]]):
        """Create relationships between entities"""
        with self.driver.session() as session:
            # Create hierarchical chain relationships
            self._create_relationship(session,
                "ActionRequest", "BELONGS_TO", "Facility",
                "action_request_id", "facility_id", "facility_id")

            self._create_relationship(session,
                "Problem", "IDENTIFIED_IN", "ActionRequest",
                "problem_id", "action_request_id", "action_request_id")

            self._create_relationship(session,
                "RootCause", "ANALYZES", "Problem",
                "cause_id", "problem_id", "problem_id")

            self._create_relationship(session,
                "ActionPlan", "RESOLVES", "RootCause",
                "plan_id", "root_cause_id", "cause_id")

            self._create_relationship(session,
                "Verification", "VALIDATES", "ActionPlan",
                "verification_id", "action_plan_id", "plan_id")

            # Create supporting entity relationships
            self._create_relationship(session,
                "Problem", "INVOLVES", "Asset",
                "problem_id", "problem_id", "asset_id")

            self._create_relationship(session,
                "Problem", "QUANTIFIES", "AmountOfLoss",
                "problem_id", "problem_id", "loss_id")

            self._create_relationship(session,
                "Problem", "CLASSIFIES", "RecurringStatus",
                "problem_id", "problem_id", "recurring_id")

            self._create_relationship(session,
                "ActionRequest", "ASSIGNS", "Department",
                "action_request_id", "action_request_id", "dept_id")

            self._create_relationship(session,
                "ActionPlan", "EVALUATES", "Review",
                "plan_id", "plan_id", "review_id")

            self._create_relationship(session,
                "ActionPlan", "MODIFIES", "EquipmentStrategy",
                "plan_id", "plan_id", "strategy_id")

    def _create_relationship(self, session, from_entity, rel_type, to_entity,
                            from_key, join_key, to_key):
        """Create relationship between two entity types"""
        query = f"""
        MATCH (from:{from_entity}), (to:{to_entity})
        WHERE from.{from_key} = to.{join_key}
        MERGE (from)-[:{rel_type}]->(to)
        """
        try:
            result = session.run(query)
            summary = result.consume()
            logger.info(f"Created {summary.counters.relationships_created} {from_entity}-[{rel_type}]->{to_entity} relationships")
        except Exception as e:
            logger.error(f"Error creating {from_entity}-[{rel_type}]->{to_entity} relationships: {e}")

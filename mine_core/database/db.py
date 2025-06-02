#!/usr/bin/env python3
"""
Simplified Database Interface for Mining Reliability Database
Clean implementation without backwards compatibility pollution.
"""

import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

from neo4j import GraphDatabase

from configs.environment import (
    get_connection_timeout,
    get_db_config,
    get_entity_primary_key,
    get_max_retries,
)
from mine_core.shared.common import handle_error
from mine_core.shared.field_utils import clean_label, has_real_value

logger = logging.getLogger(__name__)


class SimplifiedDatabase:
    """Streamlined database interface for clean dataset processing"""

    def __init__(self, uri=None, user=None, password=None):
        """Initialize database connection"""
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    @property
    def driver(self):
        """Get Neo4j driver with lazy initialization"""
        if self._driver is None:
            self._connect()
        return self._driver

    def _connect(self):
        """Establish Neo4j connection using unified configuration"""
        if not all([self._uri, self._user, self._password]):
            config = get_db_config()
            self._uri = config["uri"]
            self._user = config["user"]
            self._password = config["password"]

        logger.info(f"Connecting to Neo4j at {self._uri}")

        try:
            self._driver = GraphDatabase.driver(
                self._uri,
                auth=(self._user, self._password),
                connection_timeout=get_connection_timeout(),
            )
            self._driver.verify_connectivity()
            logger.info("Neo4j connection verified")
        except Exception as e:
            handle_error(logger, e, "Neo4j connection")
            self._driver = None
            raise

    def close(self):
        """Close database connection"""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")

    @contextmanager
    def session(self):
        """Session context manager"""
        session = self.driver.session()
        try:
            yield session
        finally:
            session.close()

    def execute_query(self, query: str, **params):
        """Execute query with parameters"""
        try:
            with self.session() as session:
                result = session.run(query, **params)
                return result.data()
        except Exception as e:
            handle_error(logger, e, f"Query execution: {query[:100]}...")
            raise

    def create_entity_with_dynamic_label(
        self, entity_type: str, properties: Dict[str, Any], dynamic_label: str = None
    ) -> bool:
        """Create entity with dynamic labeling support"""
        primary_key = get_entity_primary_key(entity_type)
        if not primary_key:
            logger.error(f"No primary key found for {entity_type}")
            return False

        id_value = properties.get(primary_key)
        if not id_value:
            logger.error(f"Missing primary key {primary_key} for {entity_type}")
            return False

        # Determine labels to apply
        labels = [entity_type]  # Always include entity type
        if dynamic_label and dynamic_label != entity_type:
            clean_dynamic = clean_label(dynamic_label)
            if clean_dynamic and clean_dynamic != entity_type:
                labels.append(clean_dynamic)

        # Filter out None values and missing indicators
        valid_props = {
            k: v
            for k, v in properties.items()
            if v is not None and not self._is_missing_indicator(v)
        }

        # Build label string and SET clause
        label_string = ":".join(labels)
        set_props = [f"n.{k} = ${k}" for k in valid_props.keys()]
        set_clause = f"SET {', '.join(set_props)}" if set_props else ""

        query = f"MERGE (n:{label_string} {{{primary_key}: ${primary_key}}}) {set_clause}"

        try:
            with self.session() as session:
                session.run(query, **valid_props)
            return True
        except Exception as e:
            handle_error(
                logger, e, f"Creating entity {entity_type} with dynamic label {dynamic_label}"
            )
            return False

    def batch_create_entities_with_labels(
        self, entity_type: str, entities_list: List[Dict[str, Any]]
    ) -> bool:
        """Batch create entities with dynamic labeling"""
        if not entities_list:
            return True

        primary_key = get_entity_primary_key(entity_type)
        if not primary_key:
            logger.error(f"No primary key found for {entity_type}")
            return False

        # Validate all entities have primary key
        for entity in entities_list:
            if primary_key not in entity:
                logger.error(f"Missing primary key {primary_key} in entity")
                return False

        try:
            with self.session() as session:
                for entity in entities_list:
                    dynamic_label = entity.pop("_dynamic_label", None)
                    self._create_single_entity_with_label(
                        session, entity_type, entity, primary_key, dynamic_label
                    )
            return True
        except Exception as e:
            handle_error(logger, e, f"Batch creating {entity_type}")
            return False

    def _create_single_entity_with_label(
        self,
        session,
        entity_type: str,
        entity: Dict[str, Any],
        primary_key: str,
        dynamic_label: str = None,
    ):
        """Create single entity with optional dynamic label"""
        # Determine labels
        labels = [entity_type]
        if dynamic_label and dynamic_label != entity_type:
            clean_dynamic = clean_label(dynamic_label)
            if clean_dynamic and clean_dynamic != entity_type:
                labels.append(clean_dynamic)

        # Filter meaningful properties
        meaningful_props = {
            k: v for k, v in entity.items() if v is not None and not self._is_missing_indicator(v)
        }

        # Build query
        label_string = ":".join(labels)
        properties = list(meaningful_props.keys())
        other_props = [p for p in properties if p != primary_key]

        set_clause = ""
        if other_props:
            set_props = [f"n.{p} = $entity.{p}" for p in other_props]
            set_clause = f"SET {', '.join(set_props)}"

        query = f"""
        MERGE (n:{label_string} {{{primary_key}: $entity.{primary_key}}})
        {set_clause}
        """

        session.run(query, entity=meaningful_props)

    def create_relationship(
        self, from_type: str, from_id: str, rel_type: str, to_type: str, to_id: str
    ) -> bool:
        """Create relationship using schema primary keys with validation"""
        from_pk = get_entity_primary_key(from_type)
        to_pk = get_entity_primary_key(to_type)

        if not from_pk or not to_pk:
            logger.error(f"Missing primary keys for {from_type}-{to_type}")
            return False

        query = f"""
        MATCH (from:{from_type} {{{from_pk}: $from_id}})
        MATCH (to:{to_type} {{{to_pk}: $to_id}})
        MERGE (from)-[r:{rel_type}]->(to)
        RETURN count(r) AS relationships_created
        """

        try:
            with self.session() as session:
                result = session.run(query, from_id=from_id, to_id=to_id)
                record = result.single()

                if record and record["relationships_created"] > 0:
                    return True
                else:
                    logger.warning(
                        f"No relationship created: {from_type}({from_id}) -[{rel_type}]-> {to_type}({to_id})"
                    )
                    return False

        except Exception as e:
            handle_error(logger, e, f"Creating relationship {from_type}-[{rel_type}]->{to_type}")
            return False

    def get_causal_intelligence_summary(self, facility_id: str = None) -> Dict[str, Any]:
        """Get summary of causal intelligence data for operational insights"""
        facility_filter = "WHERE f.facility_id = $facility_id" if facility_id else ""
        params = {"facility_id": facility_id} if facility_id else {}

        query = f"""
        MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
        {facility_filter}
        OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)<-[:ANALYZES]-(rc:RootCause)
        WITH rc.root_cause AS primary_cause, rc.root_cause_tail_extraction AS secondary_cause, count(*) AS frequency
        WHERE primary_cause IS NOT NULL
        RETURN primary_cause, secondary_cause, frequency
        ORDER BY frequency DESC
        LIMIT 20
        """

        results = self.execute_query(query, **params)

        return {
            "causal_patterns": results,
            "total_incidents_analyzed": len(results),
            "facility_scope": facility_id or "all_facilities",
        }

    def validate_data_integrity(self) -> Dict[str, Any]:
        """Validate overall database integrity"""
        integrity_checks = {}

        try:
            # Check entity counts
            for entity_type in ["Facility", "ActionRequest", "Problem", "RootCause", "ActionPlan"]:
                count_query = f"MATCH (n:{entity_type}) RETURN count(n) AS count"
                result = self.execute_query(count_query)
                integrity_checks[f"{entity_type}_count"] = result[0]["count"]

            # Check relationship integrity
            relationship_query = """
            MATCH (ar:ActionRequest)-[:BELONGS_TO]->(f:Facility)
            OPTIONAL MATCH (ar)<-[:IDENTIFIED_IN]-(p:Problem)
            OPTIONAL MATCH (p)<-[:ANALYZES]-(rc:RootCause)
            OPTIONAL MATCH (rc)<-[:RESOLVES]-(ap:ActionPlan)
            RETURN count(ar) AS total_requests,
                   count(p) AS problems_identified,
                   count(rc) AS causes_analyzed,
                   count(ap) AS plans_created
            """
            result = self.execute_query(relationship_query)
            integrity_checks["workflow_integrity"] = result[0]

            # Check causal intelligence completeness
            causal_query = """
            MATCH (rc:RootCause)
            WITH count(rc) AS total_causes,
                 count(CASE WHEN rc.root_cause IS NOT NULL AND rc.root_cause <> 'DATA_NOT_AVAILABLE' THEN 1 END) AS causes_with_data,
                 count(CASE WHEN rc.root_cause_tail IS NOT NULL AND rc.root_cause_tail <> 'NOT_SPECIFIED' THEN 1 END) AS causes_with_tail
            RETURN total_causes, causes_with_data, causes_with_tail,
                   toFloat(causes_with_data) / total_causes AS primary_completeness,
                   toFloat(causes_with_tail) / total_causes AS causal_intelligence_ratio
            """
            result = self.execute_query(causal_query)
            integrity_checks["causal_intelligence"] = result[0] if result else {}

        except Exception as e:
            handle_error(logger, e, "integrity validation")
            integrity_checks["validation_error"] = str(e)

        return integrity_checks

    def _is_missing_indicator(self, value: Any) -> bool:
        """Check if value is a missing data indicator"""
        if isinstance(value, str):
            return value in {"DATA_NOT_AVAILABLE", "NOT_SPECIFIED", "NOT_APPLICABLE"}
        return False

    def optimize_performance(self) -> bool:
        """Create performance optimization indexes"""
        optimization_queries = [
            "CREATE INDEX facility_id_index IF NOT EXISTS FOR (f:Facility) ON (f.facility_id)",
            "CREATE INDEX action_request_number_index IF NOT EXISTS FOR (ar:ActionRequest) ON (ar.action_request_number)",
            "CREATE INDEX root_cause_index IF NOT EXISTS FOR (rc:RootCause) ON (rc.root_cause)",
            "CREATE INDEX categories_index IF NOT EXISTS FOR (ar:ActionRequest) ON (ar.categories)",
            "CREATE INDEX stage_index IF NOT EXISTS FOR (ar:ActionRequest) ON (ar.stage)",
        ]

        try:
            with self.session() as session:
                for query in optimization_queries:
                    session.run(query)
            logger.info("Performance optimization indexes created")
            return True
        except Exception as e:
            handle_error(logger, e, "performance optimization")
            return False


# Singleton instance
_db_instance = None


def get_database(uri=None, user=None, password=None):
    """Get singleton database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = SimplifiedDatabase(uri, user, password)
    return _db_instance


def close_database():
    """Close singleton database connection"""
    global _db_instance
    if _db_instance is not None:
        _db_instance.close()
        _db_instance = None

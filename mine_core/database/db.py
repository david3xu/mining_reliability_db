#!/usr/bin/env python3
"""
Unified Database Interface
Single entry point for Neo4j operations.
"""

import logging
from contextlib import contextmanager
from neo4j import GraphDatabase
from configs.environment import get_db_config

logger = logging.getLogger(__name__)

class Database:
    """Unified interface for Neo4j database operations"""

    def __init__(self, uri=None, user=None, password=None):
        """Initialize with Neo4j connection parameters"""
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    @property
    def uri(self):
        """Get URI for backward compatibility"""
        return self._uri

    @property
    def user(self):
        """Get user for backward compatibility"""
        return self._user

    @property
    def password(self):
        """Get password for backward compatibility"""
        return self._password

    @property
    def driver(self):
        """Get Neo4j driver, creating it if necessary"""
        if self._driver is None:
            if not (self._uri and self._user and self._password):
                # Use environment configuration
                config = get_db_config()
                self._uri = config["uri"]
                self._user = config["user"]
                self._password = config["password"]

            logger.info(f"Connecting to Neo4j at {self._uri}")
            self._driver = GraphDatabase.driver(
                self._uri,
                auth=(self._user, self._password)
            )

            try:
                self._driver.verify_connectivity()
                logger.info("Neo4j connection verified")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                self._driver = None
                raise

        return self._driver

    def close(self):
        """Close Neo4j connection"""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")

    @contextmanager
    def session(self):
        """Context manager for Neo4j session"""
        session = self.driver.session()
        try:
            yield session
        finally:
            session.close()

    def execute_query(self, query, **params):
        """Execute a Cypher query with parameters"""
        with self.session() as session:
            result = session.run(query, **params)
            return result.data()

    def create_entity(self, entity_type, properties):
        """Create entity node with properties"""
        id_field = f"{entity_type.lower()}_id"
        id_value = properties.get(id_field)

        if not id_value:
            logger.error(f"Missing primary key {id_field} for {entity_type}")
            return False

        valid_props = {k: v for k, v in properties.items() if v is not None}
        props = [f"n.{k} = ${k}" for k in valid_props.keys()]
        set_clause = ", ".join(props) if props else ""

        query = f"MERGE (n:{entity_type} {{{id_field}: ${id_field}}})"
        if set_clause:
            query += f" SET {set_clause}"

        try:
            with self.session() as session:
                session.run(query, **valid_props)
            return True
        except Exception as e:
            logger.error(f"Error creating {entity_type}: {e}")
            return False

    def create_relationship(self, from_type, from_id, rel_type, to_type, to_id):
        """Create relationship between two nodes"""
        from_field = f"{from_type.lower()}_id"
        to_field = f"{to_type.lower()}_id"

        query = f"""
        MATCH (from:{from_type} {{{from_field}: $from_id}})
        MATCH (to:{to_type} {{{to_field}: $to_id}})
        MERGE (from)-[r:{rel_type}]->(to)
        """

        try:
            with self.session() as session:
                session.run(query, from_id=from_id, to_id=to_id)
            return True
        except Exception as e:
            logger.error(f"Error creating relationship {from_type}-[{rel_type}]->{to_type}: {e}")
            return False

    def batch_create_entities(self, entity_type, entities_list):
        """Create multiple entities in a batch"""
        if not entities_list:
            return True

        id_field = f"{entity_type.lower()}_id"
        for entity in entities_list:
            if id_field not in entity:
                logger.error(f"Missing primary key {id_field} in entity")
                return False

        sample_entity = entities_list[0]
        properties = list(sample_entity.keys())
        other_props = [p for p in properties if p != id_field]

        set_clause = ""
        if other_props:
            set_props = [f"n.{p} = entity.{p}" for p in other_props]
            set_clause = f"SET {', '.join(set_props)}"

        query = f"""
        UNWIND $entities AS entity
        MERGE (n:{entity_type} {{{id_field}: entity.{id_field}}})
        {set_clause}
        """

        try:
            with self.session() as session:
                session.run(query, entities=entities_list)
            return True
        except Exception as e:
            logger.error(f"Error batch creating {entity_type} entities: {e}")
            return False

# Singleton instance
_db_instance = None

def get_database(uri=None, user=None, password=None):
    """Get singleton database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(uri, user, password)
    return _db_instance

# Backward compatibility
class DatabaseConnection:
    """Legacy database connection wrapper"""
    def __init__(self):
        self.db = get_database()

def get_connection():
    """Legacy connection getter"""
    return get_database()

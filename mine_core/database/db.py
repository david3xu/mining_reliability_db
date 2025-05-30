#!/usr/bin/env python3
"""
Schema-driven database interface using model_schema.json
"""

import logging
from contextlib import contextmanager
from typing import Optional
from neo4j import GraphDatabase
from configs.environment import get_db_config, get_schema

logger = logging.getLogger(__name__)

class Database:
    """Schema-driven Neo4j interface"""

    def __init__(self, uri=None, user=None, password=None, schema=None):
        """Initialize with schema"""
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None
        self.schema = schema or get_schema()

        # Extract entity info from schema
        self.entities = {e["name"]: e for e in self.schema.get("entities", [])}

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
        """Get Neo4j driver"""
        if self._driver is None:
            if not (self._uri and self._user and self._password):
                config = get_db_config()
                self._uri = config["uri"]
                self._user = config["user"]
                self._password = config["password"]

            logger.info(f"Connecting to Neo4j at {self._uri}")
            self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

            try:
                self._driver.verify_connectivity()
                logger.info("Neo4j connection verified")
            except Exception as e:
                logger.error(f"Failed to connect: {e}")
                self._driver = None
                raise

        return self._driver

    def close(self):
        """Close connection"""
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

    def execute_query(self, query, **params):
        """Execute query"""
        with self.session() as session:
            result = session.run(query, **params)
            return result.data()

    def create_entity(self, entity_type, properties):
        """Create entity using schema primary key"""
        primary_key = self._get_primary_key(entity_type)
        if not primary_key:
            logger.error(f"No primary key found for {entity_type}")
            return False

        id_value = properties.get(primary_key)
        if not id_value:
            logger.error(f"Missing primary key {primary_key} for {entity_type}")
            return False

        valid_props = {k: v for k, v in properties.items() if v is not None}
        props = [f"n.{k} = ${k}" for k in valid_props.keys()]
        set_clause = ", ".join(props) if props else ""

        query = f"MERGE (n:{entity_type} {{{primary_key}: ${primary_key}}})"
        if set_clause:
            query += f" SET {set_clause}"

        try:
            with self.session() as session:
                session.run(query, **valid_props)
            return True
        except Exception as e:
            logger.error(f"Error creating {entity_type}: {e}")
            return False

    def _get_primary_key(self, entity_type: str) -> Optional[str]:
        """Get primary key from schema"""
        entity = self.entities.get(entity_type, {})
        properties = entity.get("properties", {})

        for prop_name, prop_info in properties.items():
            if prop_info.get("primary_key", False):
                return prop_name
        return None

    def batch_create_entities(self, entity_type, entities_list):
        """Batch create using schema primary key"""
        if not entities_list:
            return True

        primary_key = self._get_primary_key(entity_type)
        if not primary_key:
            logger.error(f"No primary key found for {entity_type}")
            return False

        for entity in entities_list:
            if primary_key not in entity:
                logger.error(f"Missing primary key {primary_key}")
                return False

        sample_entity = entities_list[0]
        properties = list(sample_entity.keys())
        other_props = [p for p in properties if p != primary_key]

        set_clause = ""
        if other_props:
            set_props = [f"n.{p} = entity.{p}" for p in other_props]
            set_clause = f"SET {', '.join(set_props)}"

        query = f"""
        UNWIND $entities AS entity
        MERGE (n:{entity_type} {{{primary_key}: entity.{primary_key}}})
        {set_clause}
        """

        try:
            with self.session() as session:
                session.run(query, entities=entities_list)
            return True
        except Exception as e:
            logger.error(f"Error batch creating {entity_type}: {e}")
            return False

    def create_relationship(self, from_type, from_id, rel_type, to_type, to_id):
        """Create relationship using schema primary keys"""
        from_pk = self._get_primary_key(from_type)
        to_pk = self._get_primary_key(to_type)

        if not from_pk or not to_pk:
            logger.error(f"Missing primary keys for {from_type}-{to_type}")
            return False

        query = f"""
        MATCH (from:{from_type} {{{from_pk}: $from_id}})
        MATCH (to:{to_type} {{{to_pk}: $to_id}})
        MERGE (from)-[r:{rel_type}]->(to)
        """

        try:
            with self.session() as session:
                session.run(query, from_id=from_id, to_id=to_id)
            return True
        except Exception as e:
            logger.error(f"Error creating relationship: {e}")
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
#!/usr/bin/env python3
"""
Neo4j Database Connection Manager
Handles connection to Neo4j graph database.
"""

import os
import logging
from contextlib import contextmanager
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Neo4j database connection manager"""

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

            # Verify connectivity
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

# Singleton instance
_connection = None

def get_connection(uri=None, user=None, password=None):
    """Get singleton database connection"""
    global _connection
    if _connection is None:
        _connection = DatabaseConnection(uri, user, password)
    return _connection

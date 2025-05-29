#!/usr/bin/env python3
"""
Neo4j Database Connection Manager
Backward compatibility layer for database connections.
"""

import logging
from mine_core.database.db import get_database, Database

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Compatibility wrapper for Neo4j database connection"""

    def __init__(self, uri=None, user=None, password=None):
        """Initialize with Neo4j connection parameters"""
        # Use the centralized database interface
        self.db = get_database(uri, user, password)

    @property
    def driver(self):
        """Get Neo4j driver from the database interface"""
        return self.db.driver

    def close(self):
        """Close Neo4j connection"""
        self.db.close()

    def session(self):
        """Get Neo4j session"""
        return self.db.session()

    def execute_query(self, query, **params):
        """Execute a Cypher query with parameters"""
        return self.db.execute_query(query, **params)

# Singleton instance function for backward compatibility
def get_connection(uri=None, user=None, password=None):
    """Get database connection (backward compatibility)"""
    # This now uses the centralized database interface
    return get_database(uri, user, password)

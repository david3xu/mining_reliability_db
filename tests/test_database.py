#!/usr/bin/env python3
"""
Tests for unified database interface and queries
"""

import unittest
from unittest.mock import patch, MagicMock
from mine_core.database.db import Database, get_database, DatabaseConnection, get_connection, _db_instance
from mine_core.database.queries import get_facilities, get_action_requests

class TestUnifiedDatabase(unittest.TestCase):
    """Tests for unified Database interface"""

    def setUp(self):
        global _db_instance
        _db_instance = None

    @patch('neo4j.GraphDatabase.driver')
    @patch('configs.environment.get_db_config')
    def test_database_initialization_with_config(self, mock_get_config, mock_driver):
        """Test database initialization using environment config"""
        # Setup mocks
        mock_get_config.return_value = {
            "uri": "bolt://localhost:7687",
            "user": "neo4j",
            "password": "password"
        }
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        # Create database instance
        db = Database()

        # Access driver to trigger initialization
        driver = db.driver

        # Verify configuration was used
        mock_get_config.assert_called_once()
        mock_driver.assert_called_once_with(
            "bolt://localhost:7687",
            auth=("neo4j", "password")
        )

    @patch('neo4j.GraphDatabase.driver')
    def test_database_initialization_with_params(self, mock_driver):
        """Test database initialization with explicit parameters"""
        # Setup mock
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        # Create database with custom parameters
        db = Database(
            uri="bolt://custom:7687",
            user="custom_user",
            password="custom_password"
        )

        # Access driver to trigger initialization
        driver = db.driver

        # Verify parameters were used
        mock_driver.assert_called_once_with(
            "bolt://custom:7687",
            auth=("custom_user", "custom_password")
        )

    @patch('neo4j.GraphDatabase.driver')
    def test_singleton_pattern(self, mock_driver):
        """Test get_database returns singleton instance"""
        # Setup mock
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        # Get database instances
        db1 = get_database()
        db2 = get_database()

        # Verify singleton pattern
        self.assertIs(db1, db2)

    @patch('neo4j.GraphDatabase.driver')
    def test_execute_query(self, mock_driver):
        """Test execute_query method"""
        # Setup mocks
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.data.return_value = [{"test": "result"}]

        mock_session.run.return_value = mock_result
        mock_driver_instance = MagicMock()
        mock_driver_instance.session.return_value = mock_session
        mock_driver.return_value = mock_driver_instance

        # Create database and execute query
        db = Database("bolt://localhost:7687", "neo4j", "password")
        result = db.execute_query("TEST QUERY", param1="value1")

        # Verify query execution
        mock_session.run.assert_called_once_with("TEST QUERY", param1="value1")
        self.assertEqual(result, [{"test": "result"}])

class TestBackwardCompatibility(unittest.TestCase):
    """Tests for backward compatibility layer"""

    def setUp(self):
        global _db_instance
        _db_instance = None

    @patch('mine_core.database.db.get_database')
    def test_connection_wrapper(self, mock_get_database):
        """Test DatabaseConnection wrapper works with unified interface"""
        # Setup mock
        mock_db = MagicMock()
        mock_get_database.return_value = mock_db

        # Create connection wrapper
        conn = DatabaseConnection()

        # Test wrapper delegates to unified interface
        self.assertIs(conn.db, mock_db)
        mock_get_database.assert_called_once()

    @patch('mine_core.database.db.get_database')
    def test_get_connection_compatibility(self, mock_get_database):
        """Test get_connection function compatibility"""
        # Setup mock
        mock_db = MagicMock()
        mock_get_database.return_value = mock_db

        # Test compatibility function
        result = get_connection()

        # Verify it returns unified interface
        self.assertIs(result, mock_db)
        mock_get_database.assert_called_once()

class TestQueries(unittest.TestCase):
    """Tests for database queries with unified interface"""

    def setUp(self):
        global _db_instance
        _db_instance = None

    @patch('mine_core.database.db.get_database')
    def test_get_facilities(self, mock_get_database):
        """Test get_facilities query"""
        # Setup mock
        mock_db = MagicMock()
        mock_db.execute_query.return_value = [
            {"id": "facility1", "name": "Facility 1", "active": True},
            {"id": "facility2", "name": "Facility 2", "active": False}
        ]
        mock_get_database.return_value = mock_db

        # Execute query
        result = get_facilities()

        # Verify query execution
        mock_db.execute_query.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "facility1")
        self.assertEqual(result[1]["name"], "Facility 2")

    @patch('mine_core.database.db.get_database')
    def test_get_action_requests(self, mock_get_database):
        """Test get_action_requests query"""
        # Setup mock
        mock_db = MagicMock()
        mock_db.execute_query.return_value = [
            {"id": "req1", "number": "AR-001", "title": "Request 1"},
            {"id": "req2", "number": "AR-002", "title": "Request 2"}
        ]
        mock_get_database.return_value = mock_db

        # Execute query with facility filter
        result = get_action_requests(facility_id="facility1", limit=10)

        # Verify query execution
        mock_db.execute_query.assert_called_once()
        call_args = mock_db.execute_query.call_args[1]
        self.assertEqual(call_args["facility_id"], "facility1")
        self.assertEqual(call_args["limit"], 10)

        # Verify result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "req1")
        self.assertEqual(result[1]["title"], "Request 2")

if __name__ == '__main__':
    unittest.main()

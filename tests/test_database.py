#!/usr/bin/env python3
"""
Tests for database connection and queries
"""

import unittest
from unittest.mock import patch, MagicMock
from mine_core.database.connection import DatabaseConnection, get_connection
from mine_core.database.queries import get_facilities, get_action_requests

class TestDatabaseConnection(unittest.TestCase):
    """Tests for DatabaseConnection class"""

    @patch('neo4j.GraphDatabase.driver')
    def test_connection_initialization(self, mock_driver):
        """Test connection initialization with default parameters"""
        # Setup mock
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        # Create connection
        conn = DatabaseConnection()

        # Access driver to trigger initialization
        driver = conn.driver

        # Check driver creation
        mock_driver.assert_called_once()
        self.assertEqual(conn.uri, "bolt://localhost:7687")
        self.assertEqual(conn.user, "neo4j")
        self.assertEqual(conn.password, "password")

    @patch('neo4j.GraphDatabase.driver')
    def test_connection_custom_parameters(self, mock_driver):
        """Test connection initialization with custom parameters"""
        # Setup mock
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        # Create connection
        conn = DatabaseConnection(
            uri="bolt://custom:7687",
            user="custom_user",
            password="custom_password"
        )

        # Access driver to trigger initialization
        driver = conn.driver

        # Check driver creation with custom parameters
        mock_driver.assert_called_once_with(
            "bolt://custom:7687",
            auth=("custom_user", "custom_password")
        )

    @patch('neo4j.GraphDatabase.driver')
    def test_connection_singleton(self, mock_driver):
        """Test get_connection returns singleton instance"""
        # Setup mock
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        # Get connection twice
        conn1 = get_connection()
        conn2 = get_connection()

        # Check that the same instance is returned
        self.assertIs(conn1, conn2)

        # Check driver creation called only once
        mock_driver.assert_called_once()

    @patch('neo4j.GraphDatabase.driver')
    def test_execute_query(self, mock_driver):
        """Test execute_query method"""
        # Setup mock
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.data.return_value = [{"test": "result"}]

        mock_session.run.return_value = mock_result
        mock_driver_instance = MagicMock()
        mock_driver_instance.session.return_value = mock_session
        mock_driver.return_value = mock_driver_instance

        # Create connection and execute query
        conn = DatabaseConnection()
        result = conn.execute_query("TEST QUERY", param1="value1")

        # Check query execution
        mock_session.run.assert_called_once_with("TEST QUERY", param1="value1")
        self.assertEqual(result, [{"test": "result"}])

class TestQueries(unittest.TestCase):
    """Tests for database queries"""

    @patch('mine_core.database.connection.get_connection')
    def test_get_facilities(self, mock_get_connection):
        """Test get_facilities query"""
        # Setup mock
        mock_conn = MagicMock()
        mock_conn.execute_query.return_value = [
            {"id": "facility1", "name": "Facility 1", "active": True},
            {"id": "facility2", "name": "Facility 2", "active": False}
        ]
        mock_get_connection.return_value = mock_conn

        # Execute query
        result = get_facilities()

        # Check query execution
        mock_conn.execute_query.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "facility1")
        self.assertEqual(result[1]["name"], "Facility 2")

    @patch('mine_core.database.connection.get_connection')
    def test_get_action_requests(self, mock_get_connection):
        """Test get_action_requests query"""
        # Setup mock
        mock_conn = MagicMock()
        mock_conn.execute_query.return_value = [
            {"id": "req1", "number": "AR-001", "title": "Request 1"},
            {"id": "req2", "number": "AR-002", "title": "Request 2"}
        ]
        mock_get_connection.return_value = mock_conn

        # Execute query with facility filter
        result = get_action_requests(facility_id="facility1", limit=10)

        # Check query execution
        mock_conn.execute_query.assert_called_once()
        call_args = mock_conn.execute_query.call_args[1]
        self.assertEqual(call_args["facility_id"], "facility1")
        self.assertEqual(call_args["limit"], 10)

        # Check result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "req1")
        self.assertEqual(result[1]["title"], "Request 2")

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""
Tests for unified database interface
Verifies database operations through the centralized interface.
"""

import unittest
from unittest.mock import patch, MagicMock
from mine_core.database.db import Database, get_database

class TestDatabaseInterface(unittest.TestCase):
    """Tests for Database interface class"""

    @patch('neo4j.GraphDatabase.driver')
    def test_initialization(self, mock_driver):
        """Test database initialization with default parameters"""
        # Setup mock
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        # Create database
        db = Database()

        # Access driver to trigger initialization
        driver = db.driver

        # Check driver creation
        mock_driver.assert_called_once()
        self.assertEqual(db.uri, "bolt://localhost:7687")
        self.assertEqual(db.user, "neo4j")
        self.assertEqual(db.password, "password")

    @patch('neo4j.GraphDatabase.driver')
    def test_singleton_pattern(self, mock_driver):
        """Test get_database returns singleton instance"""
        # Setup mock
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        # Get database instances
        db1 = get_database()
        db2 = get_database()

        # Access driver to trigger initialization
        driver1 = db1.driver
        driver2 = db2.driver

        # Check singleton pattern
        self.assertIs(db1, db2)
        mock_driver.assert_called_once()

    @patch('neo4j.GraphDatabase.driver')
    def test_create_entity(self, mock_driver):
        """Test create_entity method"""
        # Setup mocks
        mock_session = MagicMock()
        mock_driver_instance = MagicMock()
        mock_driver_instance.session.return_value = mock_session
        mock_driver.return_value = mock_driver_instance

        # Create database and entity
        db = Database()
        entity_type = "TestEntity"
        properties = {
            "testentity_id": "test-123",
            "name": "Test Entity",
            "active": True
        }

        # Call create_entity
        result = db.create_entity(entity_type, properties)

        # Check result and session calls
        self.assertTrue(result)
        mock_session.run.assert_called_once()

        # Check query contains expected merge pattern
        call_args = mock_session.run.call_args[0]
        query = call_args[0]
        self.assertIn(f"MERGE (n:{entity_type} {{testentity_id: $testentity_id}})", query)
        self.assertIn("n.name = $name", query)
        self.assertIn("n.active = $active", query)

    @patch('neo4j.GraphDatabase.driver')
    def test_batch_create_entities(self, mock_driver):
        """Test batch_create_entities method"""
        # Setup mocks
        mock_session = MagicMock()
        mock_driver_instance = MagicMock()
        mock_driver_instance.session.return_value = mock_session
        mock_driver.return_value = mock_driver_instance

        # Create database and entities
        db = Database()
        entity_type = "TestEntity"
        entities = [
            {"testentity_id": "test-1", "name": "Test 1"},
            {"testentity_id": "test-2", "name": "Test 2"}
        ]

        # Call batch_create_entities
        result = db.batch_create_entities(entity_type, entities)

        # Check result and session calls
        self.assertTrue(result)
        mock_session.run.assert_called_once()

        # Check query contains expected batch pattern
        call_args = mock_session.run.call_args
        query = call_args[0][0]
        self.assertIn("UNWIND $entities AS entity", query)
        self.assertIn(f"MERGE (n:{entity_type} {{testentity_id: entity.testentity_id}})", query)
        self.assertIn("SET n.name = entity.name", query)

        # Check entities parameter
        params = call_args[1]
        self.assertEqual(params["entities"], entities)

    @patch('neo4j.GraphDatabase.driver')
    def test_create_relationship(self, mock_driver):
        """Test create_relationship method"""
        # Setup mocks
        mock_session = MagicMock()
        mock_driver_instance = MagicMock()
        mock_driver_instance.session.return_value = mock_session
        mock_driver.return_value = mock_driver_instance

        # Create database
        db = Database()

        # Call create_relationship
        result = db.create_relationship(
            from_type="FromEntity",
            from_id="from-123",
            rel_type="RELATES_TO",
            to_type="ToEntity",
            to_id="to-456"
        )

        # Check result and session calls
        self.assertTrue(result)
        mock_session.run.assert_called_once()

        # Check query contains expected pattern
        call_args = mock_session.run.call_args
        query = call_args[0][0]
        self.assertIn("MATCH (from:FromEntity {fromentity_id: $from_id})", query)
        self.assertIn("(to:ToEntity {toentity_id: $to_id})", query)
        self.assertIn("MERGE (from)-[r:RELATES_TO]->(to)", query)

        # Check parameters
        params = call_args[1]
        self.assertEqual(params["from_id"], "from-123")
        self.assertEqual(params["to_id"], "to-456")

if __name__ == '__main__':
    unittest.main()

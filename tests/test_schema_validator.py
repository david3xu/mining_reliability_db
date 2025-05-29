#!/usr/bin/env python3
"""
Tests for schema validation utilities
Verifies validation functions against schema.
"""

import unittest
from unittest.mock import patch, mock_open
import json
from pathlib import Path

from mine_core.helpers.schema_validator import (
    load_schema,
    validate_entity,
    validate_relationship,
    validate_entity_chain
)

class TestSchemaValidator(unittest.TestCase):
    """Tests for schema validation utilities"""

    def setUp(self):
        """Set up test schema"""
        self.test_schema = {
            "entities": [
                {
                    "name": "TestEntity",
                    "properties": {
                        "test_id": {"type": "string", "primary_key": True, "required": True},
                        "name": {"type": "string", "required": True},
                        "count": {"type": "integer"},
                        "active": {"type": "boolean", "default": True},
                        "description": {"type": "text"}
                    }
                }
            ],
            "relationships": [
                {
                    "from": "TestEntity",
                    "to": "RelatedEntity",
                    "type": "RELATES_TO",
                    "cardinality": "one_to_many"
                }
            ]
        }

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_schema(self, mock_json_load, mock_file_open):
        """Test schema loading"""
        # Setup mock
        mock_json_load.return_value = self.test_schema

        # Load schema
        schema = load_schema(Path("/fake/path/schema.json"))

        # Check schema loaded correctly
        self.assertEqual(schema, self.test_schema)
        mock_file_open.assert_called_once_with(Path("/fake/path/schema.json"), 'r')

    def test_validate_entity_valid(self):
        """Test entity validation with valid data"""
        # Valid entity data
        data = {
            "test_id": "test-123",
            "name": "Test Entity",
            "count": 42,
            "active": True,
            "description": "This is a test entity"
        }

        # Validate against schema
        valid, errors = validate_entity("TestEntity", data, self.test_schema)

        # Check validation result
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

    def test_validate_entity_missing_required(self):
        """Test entity validation with missing required property"""
        # Invalid entity data (missing required name)
        data = {
            "test_id": "test-123",
            "count": 42
        }

        # Validate against schema
        valid, errors = validate_entity("TestEntity", data, self.test_schema)

        # Check validation result
        self.assertFalse(valid)
        self.assertEqual(len(errors), 1)
        self.assertIn("Missing required property: name", errors)

    def test_validate_entity_wrong_type(self):
        """Test entity validation with wrong property type"""
        # Invalid entity data (wrong types)
        data = {
            "test_id": "test-123",
            "name": "Test Entity",
            "count": "not-an-integer",  # Should be integer
            "active": "not-a-boolean"   # Should be boolean
        }

        # Validate against schema
        valid, errors = validate_entity("TestEntity", data, self.test_schema)

        # Check validation result
        self.assertFalse(valid)
        self.assertEqual(len(errors), 2)
        self.assertIn("Property count should be integer", errors[0])
        self.assertIn("Property active should be boolean", errors[1])

    def test_validate_entity_unknown_type(self):
        """Test entity validation with unknown entity type"""
        # Valid entity data
        data = {
            "test_id": "test-123",
            "name": "Test Entity"
        }

        # Validate against schema with unknown entity type
        valid, errors = validate_entity("UnknownEntity", data, self.test_schema)

        # Check validation result
        self.assertFalse(valid)
        self.assertEqual(len(errors), 1)
        self.assertIn("Entity type 'UnknownEntity' not found in schema", errors)

    def test_validate_relationship_valid(self):
        """Test relationship validation with valid relationship"""
        # Validate relationship
        valid, errors = validate_relationship(
            "TestEntity", "RelatedEntity", "RELATES_TO", self.test_schema
        )

        # Check validation result
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

    def test_validate_relationship_invalid(self):
        """Test relationship validation with invalid relationship"""
        # Validate relationship with wrong type
        valid, errors = validate_relationship(
            "TestEntity", "RelatedEntity", "WRONG_TYPE", self.test_schema
        )

        # Check validation result
        self.assertFalse(valid)
        self.assertEqual(len(errors), 1)
        self.assertIn("Relationship TestEntity-[WRONG_TYPE]->RelatedEntity not defined in schema", errors)

    def test_validate_entity_chain(self):
        """Test validation of entity chain"""
        # Entity chain with one valid and one invalid entity
        entities = {
            "TestEntity": [
                {
                    "test_id": "test-123",
                    "name": "Valid Entity"
                },
                {
                    "test_id": "test-456",
                    # Missing required name
                }
            ]
        }

        # Validate entity chain
        valid, errors = validate_entity_chain(entities, self.test_schema)

        # Check validation result
        self.assertFalse(valid)
        self.assertIn("TestEntity", errors)
        self.assertEqual(len(errors["TestEntity"]), 1)
        self.assertIn("Missing required property: name", errors["TestEntity"][0])

if __name__ == '__main__':
    unittest.main()

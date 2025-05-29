#!/usr/bin/env python3
"""
Tests for field mapping configuration
Verifies transformer's use of configuration-based mappings.
"""

import unittest
import json
from unittest.mock import patch, mock_open
from mine_core.pipelines.transformer import DataTransformer

class TestFieldMappings(unittest.TestCase):
    """Tests for field mapping configuration"""

    @patch('configs.environment.get_mappings')
    def test_config_based_initialization(self, mock_get_mappings):
        """Test transformer initialization with config-based mappings"""
        # Setup mock configuration
        mock_mappings = {
            "list_fields": ["Field1", "Field2"],
            "entity_mappings": {
                "EntityType": {
                    "target_field": "source_field"
                }
            },
            "list_field_extraction": {
                "Field1": "tail",
                "default": "head"
            }
        }
        mock_get_mappings.return_value = mock_mappings

        # Create transformer with mocked config
        transformer = DataTransformer()

        # Check mappings loaded from config
        self.assertEqual(transformer.list_fields, ["Field1", "Field2"])
        self.assertEqual(transformer.field_mappings, {"EntityType": {"target_field": "source_field"}})
        self.assertEqual(transformer.list_field_extraction, {"Field1": "tail", "default": "head"})

    @patch('configs.environment.get_mappings')
    def test_extract_list_field_value(self, mock_get_mappings):
        """Test list field extraction logic based on configuration"""
        # Setup mock configuration
        mock_mappings = {
            "list_fields": ["Field1", "Field2"],
            "list_field_extraction": {
                "Field1": "tail",
                "default": "head"
            }
        }
        mock_get_mappings.return_value = mock_mappings

        # Create transformer with mocked config
        transformer = DataTransformer()

        # Test tail extraction
        value1 = ["First", "Second", "Third"]
        result1 = transformer._extract_list_field_value("Field1", value1)
        self.assertEqual(result1, "Second")  # Tail is second item for this field

        # Test head extraction (default)
        value2 = ["First", "Second", "Third"]
        result2 = transformer._extract_list_field_value("Field2", value2)
        self.assertEqual(result2, "First")   # Head is first item (default)

        # Test non-list value
        value3 = "String value"
        result3 = transformer._extract_list_field_value("Field1", value3)
        self.assertEqual(result3, "String value")  # Return as is if not list

        # Test empty list
        value4 = []
        result4 = transformer._extract_list_field_value("Field1", value4)
        self.assertEqual(result4, [])  # Return as is if empty list

    @patch('configs.environment.get_mappings')
    def test_transform_entity(self, mock_get_mappings):
        """Test entity transformation with field mappings"""
        # Setup mock configuration
        mock_mappings = {
            "list_fields": ["ListField"],
            "entity_mappings": {
                "TestEntity": {
                    "target_field1": "SourceField1",
                    "target_field2": "SourceField2",
                    "target_list_field": "ListField"
                }
            },
            "list_field_extraction": {
                "default": "head"
            }
        }
        mock_get_mappings.return_value = mock_mappings

        # Create transformer with mocked config
        transformer = DataTransformer()

        # Create test record
        record = {
            "SourceField1": "Value1",
            "SourceField2": "Value2",
            "ListField": ["Item1", "Item2"],
            "UnmappedField": "ShouldNotBeMapped"
        }

        # Transform entity
        entity = transformer._transform_entity(record, "TestEntity")

        # Check transformed entity
        self.assertEqual(entity["target_field1"], "Value1")
        self.assertEqual(entity["target_field2"], "Value2")
        self.assertEqual(entity["target_list_field"], "Item1")  # Head of list
        self.assertNotIn("UnmappedField", entity)  # Unmapped field not included

    @patch('configs.environment.get_mappings')
    def test_fallback_behavior(self, mock_get_mappings):
        """Test transformer behavior when mappings not available"""
        # Setup mock to return empty mappings
        mock_get_mappings.return_value = {}

        # Create transformer with empty config
        transformer = DataTransformer()

        # Check fallback behavior
        self.assertEqual(transformer.list_fields, [])
        self.assertEqual(transformer.field_mappings, {})
        self.assertEqual(transformer.list_field_extraction, {"default": "head"})

    @patch('configs.environment.get_mappings')
    def test_missing_mappings_handling(self, mock_get_mappings):
        """Test transformer behavior when get_mappings returns None"""
        # Setup mock to return None
        mock_get_mappings.return_value = None

        # Create transformer with None config
        transformer = DataTransformer()

        # Check fallback behavior
        self.assertEqual(transformer.list_fields, [])
        self.assertEqual(transformer.field_mappings, {})
        self.assertEqual(transformer.list_field_extraction, {"default": "head"})

if __name__ == '__main__':
    unittest.main()

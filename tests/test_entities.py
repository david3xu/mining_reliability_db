#!/usr/bin/env python3
"""
Tests for schema-driven entity definitions
Verifies schema loading and entity creation from schema.
"""

import unittest
import json
from pathlib import Path
from unittest.mock import patch, mock_open

from mine_core.entities.definitions import (
    get_entity_definitions, create_entity_from_dict, get_schema_manager
)


class TestSchemaManager(unittest.TestCase):
    """Tests for schema-driven entity management"""

    def test_schema_manager_creation(self):
        """Test that schema manager can be created"""
        manager = get_schema_manager()
        self.assertIsNotNone(manager)
        self.assertTrue(hasattr(manager, 'entities'))

    def test_entity_creation_from_dict(self):
        """Test creating entity from dictionary using schema"""
        # Test data for a facility
        facility_data = {
            "id": "test-id",
            "facility_id": "facility1",
            "facility_name": "Test Facility",
            "location": "Test Location",
            "active": True
        }

        entity = create_entity_from_dict("Facility", facility_data)

        # Check that entity was created with correct attributes
        self.assertEqual(entity.id, "test-id")
        self.assertEqual(entity.facility_id, "facility1")
        self.assertEqual(entity.facility_name, "Test Facility")
        self.assertEqual(entity.location, "Test Location")
        self.assertTrue(entity.active)

    def test_action_request_creation(self):
        """Test creating ActionRequest entity from dictionary"""
        request_data = {
            "id": "test-id",
            "action_request_id": "ar-001",
            "facility_id": "facility1",
            "action_request_number": "AR-001",
            "title": "Test Request",
            "initiation_date": "2023-01-01",
            "action_types": "Corrective",
            "categories": "Safety",
            "stage": "In Progress"
        }

        entity = create_entity_from_dict("ActionRequest", request_data)

        # Check attributes
        self.assertEqual(entity.id, "test-id")
        self.assertEqual(entity.action_request_id, "ar-001")
        self.assertEqual(entity.facility_id, "facility1")
        self.assertEqual(entity.action_request_number, "AR-001")
        self.assertEqual(entity.title, "Test Request")

    def test_problem_creation(self):
        """Test creating Problem entity from dictionary"""
        problem_data = {
            "id": "test-id",
            "problem_id": "prob-001",
            "action_request_id": "ar-001",
            "what_happened": "Test incident occurred",
            "requirement": "Fix the issue"
        }

        entity = create_entity_from_dict("Problem", problem_data)

        # Check attributes
        self.assertEqual(entity.id, "test-id")
        self.assertEqual(entity.problem_id, "prob-001")
        self.assertEqual(entity.action_request_id, "ar-001")
        self.assertEqual(entity.what_happened, "Test incident occurred")
        self.assertEqual(entity.requirement, "Fix the issue")

    def test_schema_driven_entity_definitions(self):
        """Test that entity definitions come from schema"""
        manager = get_schema_manager()

        # Check that we have entities defined in schema
        self.assertIn('entities', manager.schema)
        entities = manager.schema['entities']

        # Should have core entities
        entity_names = [entity['name'] for entity in entities]
        self.assertIn('Facility', entity_names)
        self.assertIn('ActionRequest', entity_names)
        self.assertIn('Problem', entity_names)
        self.assertIn('RootCause', entity_names)
        self.assertIn('ActionPlan', entity_names)

    def test_entity_relationships_from_schema(self):
        """Test that entity relationships are defined in schema"""
        manager = get_schema_manager()

        # Check that relationships are defined
        self.assertIn('relationships', manager.schema)
        relationships = manager.schema['relationships']

        # Should have key relationships
        relationship_names = [rel['name'] for rel in relationships]
        self.assertIn('facility_action_requests', relationship_names)
        self.assertIn('action_request_problems', relationship_names)

    def test_invalid_entity_type(self):
        """Test handling of invalid entity types"""
        data = {"id": "test-id", "name": "Test"}

        # Should return None for unknown entity type
        entity = create_entity_from_dict("InvalidEntityType", data)
        self.assertIsNone(entity)

    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        # Missing required facility_id field
        incomplete_data = {
            "id": "test-id",
            "facility_name": "Test Facility"
        }

        # Should still create entity but may have None values
        entity = create_entity_from_dict("Facility", incomplete_data)
        self.assertIsNotNone(entity)
        self.assertEqual(entity.id, "test-id")
        self.assertEqual(entity.facility_name, "Test Facility")


class TestSchemaValidation(unittest.TestCase):
    """Tests for schema validation and loading"""

    def test_schema_file_loading(self):
        """Test that schema file can be loaded"""
        manager = get_schema_manager()

        # Should have loaded schema successfully
        self.assertIsNotNone(manager.schema)
        self.assertIn('entities', manager.schema)
        self.assertIn('relationships', manager.schema)

    def test_entity_definitions_from_schema(self):
        """Test that entity definitions are generated from schema"""
        entity_defs = get_entity_definitions()

        # Should have definitions for all entities in schema
        manager = get_schema_manager()
        schema_entities = [entity['name'] for entity in manager.schema['entities']]

        for entity_name in schema_entities:
            self.assertIn(entity_name, entity_defs)
            # Each definition should be a callable class
            self.assertTrue(callable(entity_defs[entity_name]))

    def test_schema_structure_validation(self):
        """Test basic schema structure validation"""
        manager = get_schema_manager()
        schema = manager.schema

        # Basic structure checks
        self.assertIsInstance(schema['entities'], list)
        self.assertIsInstance(schema['relationships'], list)

        # Each entity should have required fields
        for entity in schema['entities']:
            self.assertIn('name', entity)
            self.assertIn('properties', entity)
            self.assertIsInstance(entity['properties'], dict)


class TestEntityFactory(unittest.TestCase):
    """Tests for dynamic entity creation"""

    def test_entity_factory_with_all_entity_types(self):
        """Test creating all entity types using factory"""
        manager = get_schema_manager()

        # Test data for each entity type
        test_data = {
            "Facility": {
                "id": "test-id",
                "facility_id": "fac-001",
                "facility_name": "Test Facility"
            },
            "ActionRequest": {
                "id": "test-id",
                "action_request_id": "ar-001",
                "facility_id": "fac-001",
                "title": "Test Request"
            },
            "Problem": {
                "id": "test-id",
                "problem_id": "prob-001",
                "action_request_id": "ar-001"
            },
            "RootCause": {
                "id": "test-id",
                "cause_id": "cause-001",
                "problem_id": "prob-001"
            },
            "ActionPlan": {
                "id": "test-id",
                "plan_id": "plan-001",
                "root_cause_id": "cause-001"
            }
        }

        # Test creating each entity type
        for entity_name, data in test_data.items():
            with self.subTest(entity_type=entity_name):
                entity = create_entity_from_dict(entity_name, data)
                self.assertIsNotNone(entity, f"Failed to create {entity_name}")
                self.assertEqual(entity.id, "test-id")

    def test_entity_attribute_access(self):
        """Test that created entities have proper attribute access"""
        facility_data = {
            "id": "test-id",
            "facility_id": "fac-001",
            "facility_name": "Test Facility",
            "location": "Test Location",
            "active": True
        }

        entity = create_entity_from_dict("Facility", facility_data)

        # Test attribute access
        self.assertTrue(hasattr(entity, 'id'))
        self.assertTrue(hasattr(entity, 'facility_id'))
        self.assertTrue(hasattr(entity, 'facility_name'))
        self.assertTrue(hasattr(entity, 'location'))
        self.assertTrue(hasattr(entity, 'active'))

        # Test attribute values
        self.assertEqual(entity.id, "test-id")
        self.assertEqual(entity.facility_id, "fac-001")
        self.assertEqual(entity.facility_name, "Test Facility")
        self.assertEqual(entity.location, "Test Location")
        self.assertTrue(entity.active)


class TestSchemaManagerIntegration(unittest.TestCase):
    """Integration tests for schema manager functionality"""

    def test_real_schema_loading(self):
        """Test loading the actual schema file"""
        manager = get_schema_manager()

        # Should successfully load the real schema
        self.assertIsNotNone(manager.schema)

        # Check for expected entities from real schema
        entity_names = [entity['name'] for entity in manager.schema['entities']]
        expected_entities = [
            'Facility', 'ActionRequest', 'Department', 'Problem',
            'Asset', 'RecurringStatus', 'AmountOfLoss', 'RootCause',
            'ActionPlan', 'Review', 'EquipmentStrategy', 'Verification'
        ]

        for expected in expected_entities:
            self.assertIn(expected, entity_names)

    def test_all_schema_entities_creatable(self):
        """Test that all entities in schema can be created"""
        manager = get_schema_manager()

        # Test creating each entity type from schema
        for entity_def in manager.schema['entities']:
            entity_name = entity_def['name']

            # Create minimal test data
            test_data = {"id": f"test-{entity_name.lower()}"}

            # Add primary key if defined
            for prop_name, prop_def in entity_def['properties'].items():
                if prop_def.get('primary_key'):
                    test_data[prop_name] = f"test-{prop_name}"

            with self.subTest(entity_type=entity_name):
                entity = create_entity_from_dict(entity_name, test_data)
                self.assertIsNotNone(entity, f"Failed to create {entity_name}")
                self.assertEqual(entity.id, f"test-{entity_name.lower()}")


if __name__ == '__main__':
    unittest.main()

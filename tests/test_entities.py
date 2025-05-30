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

class TestEntityBase(unittest.TestCase):
    """Tests for Entity base class"""


    def test_entity_from_dict(self):
        """Test entity creation from dictionary"""
        # Test data for entity creation
        data = {
            "id": "test-id",
            "facility_id": "facility-123",
            "facility_name": "Test Facility",
            "location": "Test Location",
            "active": True,
            "extra_field": "Should be ignored"  # This should not be included
        }

        # Create entity from dictionary
        facility = Facility.from_dict(data)

        # Check entity properties
        self.assertEqual(facility.id, "test-id")
        self.assertEqual(facility.facility_id, "facility-123")
        self.assertEqual(facility.facility_name, "Test Facility")
        self.assertEqual(facility.location, "Test Location")
        self.assertTrue(facility.active)

        # Ensure extra field was not included
        self.assertFalse(hasattr(facility, "extra_field"))

    def test_create_entity_from_dict(self):
        """Test dynamic entity creation from type name and dictionary"""
        # Test data for entity creation
        data = {
            "id": "test-id",
            "problem_id": "prob-123",
            "action_request_id": "ar-456",
            "what_happened": "Test incident",
            "requirement": "Test requirement"
        }

        # Create entity using factory function
        problem = create_entity_from_dict("Problem", data)

        # Check entity type and properties
        self.assertIsInstance(problem, Problem)
        self.assertEqual(problem.id, "test-id")
        self.assertEqual(problem.problem_id, "prob-123")
        self.assertEqual(problem.action_request_id, "ar-456")
        self.assertEqual(problem.what_happened, "Test incident")
        self.assertEqual(problem.requirement, "Test requirement")

        # Test with unknown entity type
        unknown = create_entity_from_dict("UnknownType", data)
        self.assertIsNone(unknown)

class TestEntityDefinitions(unittest.TestCase):
    """Tests for entity class definitions"""

    def test_facility_entity(self):
        """Test Facility entity structure"""
        facility = Facility(
            id="test-id",
            facility_id="facility1",
            facility_name="Facility 1",
            location="Test Location",
            active=True
        )

        # Check attributes
        self.assertEqual(facility.id, "test-id")
        self.assertEqual(facility.facility_id, "facility1")
        self.assertEqual(facility.facility_name, "Facility 1")
        self.assertEqual(facility.location, "Test Location")
        self.assertTrue(facility.active)

    def test_action_request_entity(self):
        """Test ActionRequest entity structure"""
        request = ActionRequest(
            id="test-id",
            action_request_id="ar-001",
            facility_id="facility1",
            action_request_number="AR-001",
            title="Test Request",
            initiation_date="2023-01-01",
            action_types="Corrective",
            categories="Safety",
            requested_response_time="1 week",
            stage="In Progress",
            operating_centre="Test Centre",
            past_due_status="Not Due",
            days_past_due=0
        )

        # Check attributes
        self.assertEqual(request.id, "test-id")
        self.assertEqual(request.action_request_id, "ar-001")
        self.assertEqual(request.facility_id, "facility1")
        self.assertEqual(request.action_request_number, "AR-001")
        self.assertEqual(request.title, "Test Request")
        self.assertEqual(request.initiation_date, "2023-01-01")
        self.assertEqual(request.action_types, "Corrective")
        self.assertEqual(request.categories, "Safety")
        self.assertEqual(request.requested_response_time, "1 week")
        self.assertEqual(request.stage, "In Progress")
        self.assertEqual(request.operating_centre, "Test Centre")
        self.assertEqual(request.past_due_status, "Not Due")
        self.assertEqual(request.days_past_due, 0)

    def test_problem_entity(self):
        """Test Problem entity structure"""
        problem = Problem(
            id="test-id",
            problem_id="prob-001",
            action_request_id="ar-001",
            what_happened="Test incident occurred",
            requirement="Fix the issue"
        )

        # Check attributes
        self.assertEqual(problem.id, "test-id")
        self.assertEqual(problem.problem_id, "prob-001")
        self.assertEqual(problem.action_request_id, "ar-001")
        self.assertEqual(problem.what_happened, "Test incident occurred")
        self.assertEqual(problem.requirement, "Fix the issue")

    def test_root_cause_entity(self):
        """Test RootCause entity structure"""
        root_cause = RootCause(
            id="test-id",
            cause_id="cause-001",
            problem_id="prob-001",
            root_cause="Test root cause",
            objective_evidence="Test evidence"
        )

        # Check attributes
        self.assertEqual(root_cause.id, "test-id")
        self.assertEqual(root_cause.cause_id, "cause-001")
        self.assertEqual(root_cause.problem_id, "prob-001")
        self.assertEqual(root_cause.root_cause, "Test root cause")
        self.assertEqual(root_cause.objective_evidence, "Test evidence")

    def test_action_plan_entity(self):
        """Test ActionPlan entity structure"""
        action_plan = ActionPlan(
            id="test-id",
            plan_id="plan-001",
            root_cause_id="cause-001",
            action_plan="Test action plan",
            recommended_action="Test recommendation",
            immediate_containment="Test containment",
            due_date="2023-02-01",
            complete=True,
            completion_date="2023-01-15",
            comments="Test comments",
            response_date="2023-01-05",
            response_revision_date="2023-01-10",
            did_plan_require_strategy_change=True,
            are_there_corrective_actions_to_update=False
        )

        # Check attributes
        self.assertEqual(action_plan.id, "test-id")
        self.assertEqual(action_plan.plan_id, "plan-001")
        self.assertEqual(action_plan.root_cause_id, "cause-001")
        self.assertEqual(action_plan.action_plan, "Test action plan")
        self.assertEqual(action_plan.recommended_action, "Test recommendation")
        self.assertEqual(action_plan.immediate_containment, "Test containment")
        self.assertEqual(action_plan.due_date, "2023-02-01")
        self.assertTrue(action_plan.complete)
        self.assertEqual(action_plan.completion_date, "2023-01-15")
        self.assertEqual(action_plan.comments, "Test comments")
        self.assertEqual(action_plan.response_date, "2023-01-05")
        self.assertEqual(action_plan.response_revision_date, "2023-01-10")
        self.assertTrue(action_plan.did_plan_require_strategy_change)
        self.assertFalse(action_plan.are_there_corrective_actions_to_update)

class TestEntityLoading(unittest.TestCase):
    """Tests for entity loading from schema"""

    @patch('pathlib.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_get_entity_definitions(self, mock_json_load, mock_file_open, mock_exists):
        """Test get_entity_definitions function"""
        # Setup mocks
        mock_exists.return_value = True

        # Mock schema data
        mock_schema = {
            "entities": [
                {
                    "name": "Facility",
                    "properties": {
                        "facility_id": {"type": "string", "primary_key": True},
                        "facility_name": {"type": "string", "required": True},
                        "location": {"type": "string"},
                        "active": {"type": "boolean", "default": True}
                    }
                },
                {
                    "name": "ActionRequest",
                    "properties": {
                        "action_request_id": {"type": "string", "primary_key": True},
                        "facility_id": {"type": "string", "required": True},
                        "action_request_number": {"type": "string", "required": True},
                        "title": {"type": "string", "required": True}
                    }
                }
            ]
        }
        mock_json_load.return_value = mock_schema

        # Call function
        entity_defs = get_entity_definitions()

        # Check results
        self.assertIn("Facility", entity_defs)
        self.assertIn("ActionRequest", entity_defs)
        self.assertEqual(entity_defs["Facility"], Facility)
        self.assertEqual(entity_defs["ActionRequest"], ActionRequest)

    @patch('pathlib.Path.exists')
    def test_get_entity_definitions_fallback(self, mock_exists):
        """Test get_entity_definitions fallback when schema not found"""
        # Setup mocks
        mock_exists.return_value = False

        # Call function
        entity_defs = get_entity_definitions()

        # Check results - should fall back to built-in definitions
        self.assertIn("Facility", entity_defs)
        self.assertIn("ActionRequest", entity_defs)
        self.assertEqual(entity_defs["Facility"], Facility)
        self.assertEqual(entity_defs["ActionRequest"], ActionRequest)

if __name__ == '__main__':
    unittest.main()

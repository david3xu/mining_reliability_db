#!/usr/bin/env python3
"""
Tests for the DataTransformer class
Verifies list field extraction logic and transformation process.
"""

import unittest
from mine_core.pipelines.transformer import DataTransformer

class TestDataTransformer(unittest.TestCase):
    """Tests for the DataTransformer class"""

    def setUp(self):
        """Set up test cases"""
        self.transformer = DataTransformer()

        # Sample record with list field variations
        self.sample_record = {
            "Action Request Number:": "RCA-2023-00001",
            "Title": "Test incident",
            "Initiation Date": "2023-01-01",
            "What happened?": "Test incident description",
            "Requirement": "Fix the issue",

            # List fields with different patterns
            "Obj. Evidence": [
                "Evidence item 1",
                "Evidence item 2"
            ],
            "Recom.Action": [
                "Action item 1",
                "Action item 2",
                "Action item 3"
            ],
            "Immd. Contain. Action or Comments": [
                "Containment action"
            ],
            "Root Cause": [
                "Initial cause",
                "Underlying cause"  # Should be extracted as the root cause
            ],
            "Action Plan Eval Comment": [
                "Evaluation comment 1",
                "Evaluation comment 2"
            ]
        }

    def test_extract_list_field_value(self):
        """Test list field extraction logic"""
        # Root Cause should use tail (second) item if available
        root_cause = self.transformer._extract_list_field_value(
            "Root Cause",
            self.sample_record["Root Cause"]
        )
        self.assertEqual(root_cause, "Underlying cause")

        # Other list fields should use head (first) item
        evidence = self.transformer._extract_list_field_value(
            "Obj. Evidence",
            self.sample_record["Obj. Evidence"]
        )
        self.assertEqual(evidence, "Evidence item 1")

        action = self.transformer._extract_list_field_value(
            "Recom.Action",
            self.sample_record["Recom.Action"]
        )
        self.assertEqual(action, "Action item 1")

        containment = self.transformer._extract_list_field_value(
            "Immd. Contain. Action or Comments",
            self.sample_record["Immd. Contain. Action or Comments"]
        )
        self.assertEqual(containment, "Containment action")

        eval_comment = self.transformer._extract_list_field_value(
            "Action Plan Eval Comment",
            self.sample_record["Action Plan Eval Comment"]
        )
        self.assertEqual(eval_comment, "Evaluation comment 1")

    def test_transform_entity(self):
        """Test entity transformation with list field handling"""
        # Transform RootCause entity
        root_cause = self.transformer._transform_entity(self.sample_record, "RootCause")

        # Check list field extraction applied correctly
        self.assertEqual(root_cause["root_cause"], "Underlying cause")
        self.assertEqual(root_cause["objective_evidence"], "Evidence item 1")

        # Transform ActionPlan entity
        action_plan = self.transformer._transform_entity(self.sample_record, "ActionPlan")

        # Check list field extraction applied correctly
        self.assertEqual(action_plan["recommended_action"], "Action item 1")
        self.assertEqual(action_plan["immediate_containment"], "Containment action")

    def test_transform_record(self):
        """Test full record transformation"""
        # Create a minimal transformed structure
        transformed = {
            "facility": {"facility_id": "TEST"},
            "entities": {
                "ActionRequest": [],
                "Problem": [],
                "RootCause": [],
                "ActionPlan": [],
                "Verification": [],
                "Department": [],
                "Asset": [],
                "RecurringStatus": [],
                "AmountOfLoss": [],
                "Review": [],
                "EquipmentStrategy": []
            }
        }

        # Transform the record
        self.transformer._transform_record(self.sample_record, "TEST", transformed)

        # Check ActionRequest was created
        self.assertEqual(len(transformed["entities"]["ActionRequest"]), 1)

        # Check Problem was created
        self.assertEqual(len(transformed["entities"]["Problem"]), 1)

        # Check RootCause was created with correct extraction
        self.assertEqual(len(transformed["entities"]["RootCause"]), 1)
        root_cause = transformed["entities"]["RootCause"][0]
        self.assertEqual(root_cause["root_cause"], "Underlying cause")

if __name__ == '__main__':
    unittest.main()

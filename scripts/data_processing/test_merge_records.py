#!/usr/bin/env python3
"""
Test script for the record merge process.

This script validates the merge functionality with sample data
and ensures the merge strategies work correctly.
"""

import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from scripts.data_processing.merge_records import RecordMerger


class TestRecordMerger(unittest.TestCase):
    """Test cases for the RecordMerger class."""

    def setUp(self):
        """Set up test fixtures."""
        self.merger = RecordMerger()

        # Sample duplicate records for testing
        self.sample_duplicates = [
            {
                "Action Request Number:": "2021-06400",
                "Title": "Equipment Maintenance Issue",
                "Action Plan": ["Standardize work instructions for lubrication"],
                "Root Cause": ["Inadequate clearance for shaft"],
                "Stage": "Open - Receiver Proposing Action Plan",
                "Comments": "Initial assessment completed",
                "Complete": "No",
                "Days Past Due": 5,
                "Completion Date": "2021-06-15",
                "Amount of Loss": 1000,
                "Is Resp Satisfactory?": "No",
                "_source_file": "file1.xlsx",
                "_line_number": 10,
            },
            {
                "Action Request Number:": "2021-06400",
                "Title": "Equipment Maintenance Issue",
                "Action Plan": ["Update inspection checklist", "Add brake system inspection"],
                "Root Cause": ["Undersized bolts for PLC assembly", "Fatigue and wear"],
                "Stage": "Action Plan Implemented - Actions Effective - Closed",
                "Comments": "Follow-up investigation completed",
                "Complete": "Yes",
                "Days Past Due": 10,
                "Completion Date": "2021-06-20",
                "Amount of Loss": 1500,
                "Is Resp Satisfactory?": "Yes",
                "_source_file": "file2.xlsx",
                "_line_number": 25,
            },
        ]

    def test_merge_lists(self):
        """Test merging of list fields."""
        values = [["item1", "item2"], ["item2", "item3"], ["item4"]]
        result = self.merger.merge_lists(values)
        expected = "item1 | item2 | item3 | item4"
        self.assertEqual(result, expected)

    def test_merge_lists_with_strings(self):
        """Test merging lists that include string values."""
        values = [["item1"], "item2", ["item2", "item3"]]
        result = self.merger.merge_lists(values)
        expected = "item1 | item2 | item3"
        self.assertEqual(result, expected)

    def test_concatenate_strings(self):
        """Test string concatenation with deduplication."""
        values = ["First comment", "Second comment", "First comment", None]
        result = self.merger.concatenate_strings(values)
        expected = "First comment | Second comment"
        self.assertEqual(result, expected)

    def test_get_latest_date(self):
        """Test getting the latest date."""
        values = ["2021-06-15", "2021-06-20", "2021-06-10"]
        result = self.merger.get_latest_date(values)
        self.assertEqual(result, "2021-06-20")

    def test_prioritize_status_stage(self):
        """Test status prioritization for Stage field."""
        values = [
            "Open - Receiver Proposing Action Plan",
            "Action Plan Implemented - Actions Effective - Closed",
            "Action Plan Proposed - Waiting on Action Plan Implementation",
        ]
        result = self.merger.prioritize_status(values, "Stage")
        expected = "Action Plan Implemented - Actions Effective - Closed"
        self.assertEqual(result, expected)

    def test_prioritize_status_complete(self):
        """Test status prioritization for Complete field."""
        values = ["No", "Yes", "Cancelled"]
        result = self.merger.prioritize_status(values, "Complete")
        expected = "Yes"
        self.assertEqual(result, expected)

    def test_get_max_numeric(self):
        """Test getting maximum numeric value."""
        values = [5, 10, 3, None, "15"]
        result = self.merger.get_max_numeric(values)
        self.assertEqual(result, 15.0)

    def test_prioritize_yes(self):
        """Test prioritizing 'Yes' values."""
        values = ["No", "Yes", "Maybe"]
        result = self.merger.prioritize_yes(values)
        self.assertEqual(result, "Yes")

    def test_prioritize_yes_no_yes_found(self):
        """Test prioritize_yes when no 'Yes' value is found."""
        values = ["No", "Maybe", "Unknown"]
        result = self.merger.prioritize_yes(values)
        self.assertEqual(result, "No")

    def test_get_first_non_null(self):
        """Test getting first non-null value."""
        values = [None, "", "First value", "Second value"]
        result = self.merger.get_first_non_null(values)
        self.assertEqual(result, "First value")

    def test_detect_field_differences(self):
        """Test difference detection between records."""
        differences = self.merger.detect_field_differences(self.sample_duplicates)

        # Should detect differences in Action Plan, Root Cause, Stage, etc.
        self.assertIn("Action Plan", differences)
        self.assertIn("Root Cause", differences)
        self.assertIn("Stage", differences)

        # Check difference details
        action_plan_diff = differences["Action Plan"]
        self.assertEqual(action_plan_diff["unique_count"], 2)
        self.assertIn("merge_strategy", action_plan_diff)
        self.assertIn("confidence", action_plan_diff)

    def test_determine_merge_strategy(self):
        """Test dynamic merge strategy determination."""
        # Test date field detection
        strategy = self.merger._determine_merge_strategy(
            "Completion Date", ["2021-01-01", "2021-01-02"]
        )
        self.assertEqual(strategy, "latest_date")

        # Test status field detection
        strategy = self.merger._determine_merge_strategy("Stage", ["Open", "Closed"])
        self.assertEqual(strategy, "prioritize_status")

        # Test list field detection
        strategy = self.merger._determine_merge_strategy("Action Plan", [["item1"], ["item2"]])
        self.assertEqual(strategy, "merge_lists")

        # Test numeric field detection
        strategy = self.merger._determine_merge_strategy("Amount", [100, 200])
        self.assertEqual(strategy, "max_numeric")

        # Test comment field detection
        strategy = self.merger._determine_merge_strategy("Comments", ["comment1", "comment2"])
        self.assertEqual(strategy, "concatenate_strings")

    def test_calculate_merge_confidence(self):
        """Test merge confidence calculation."""
        # High confidence for consistent date values
        confidence = self.merger._calculate_merge_confidence(
            "Completion Date", ["2021-01-01", "2021-01-02"]
        )
        self.assertGreater(confidence, 0.7)

        # Lower confidence for mixed data types
        confidence = self.merger._calculate_merge_confidence("Mixed Field", ["text", 123, True])
        self.assertLess(confidence, 0.8)

    def test_analyze_merge_complexity(self):
        """Test merge complexity analysis."""
        complexity = self.merger.analyze_merge_complexity(self.sample_duplicates)

        self.assertIn("complexity", complexity)
        self.assertIn("differences", complexity)
        self.assertIn("recommendations", complexity)
        self.assertIn("field_count", complexity)

        # Should detect multiple differences
        self.assertGreater(complexity["field_count"], 0)

        # Should have some complexity score
        self.assertGreater(complexity["score"], 0)

    def test_enhanced_merge_duplicate_records(self):
        """Test enhanced merging with metadata."""
        merged = self.merger.merge_duplicate_records(self.sample_duplicates)

        # Test enhanced metadata
        self.assertIn("_merge_complexity", merged)
        self.assertIn("_merge_score", merged)
        self.assertIn("_differing_fields", merged)
        self.assertIn("_high_risk_fields", merged)
        self.assertIn("_merge_decisions", merged)

        # Test merge decisions tracking
        merge_decisions = merged["_merge_decisions"]
        self.assertIn("Action Plan", merge_decisions)
        self.assertIn("strategy", merge_decisions["Action Plan"])
        self.assertIn("confidence", merge_decisions["Action Plan"])

    def test_merge_field_values_correctly(self):
        """Test that field values are merged correctly."""
        merged = self.merger.merge_duplicate_records(self.sample_duplicates)

        # Test that Action Request Number is preserved
        self.assertEqual(merged["Action Request Number:"], "2021-06400")

        # Test that Action Plans are merged
        expected_action_plan = [
            "Standardize work instructions for lubrication",
            "Update inspection checklist",
            "Add brake system inspection",
        ]
        self.assertEqual(merged["Action Plan"], expected_action_plan)

        # Test that Root Causes are merged
        expected_root_cause = [
            "Inadequate clearance for shaft",
            "Undersized bolts for PLC assembly",
            "Fatigue and wear",
        ]
        self.assertEqual(merged["Root Cause"], expected_root_cause)

        # Test status prioritization (should pick most advanced)
        self.assertEqual(merged["Stage"], "Action Plan Implemented - Actions Effective - Closed")
        self.assertEqual(merged["Complete"], "Yes")

        # Test string concatenation
        expected_comments = "Initial assessment completed | Follow-up investigation completed"
        self.assertEqual(merged["Comments"], expected_comments)

        # Test numeric maximum
        self.assertEqual(merged["Days Past Due"], 10)
        self.assertEqual(merged["Amount of Loss"], 1500)

        # Test latest date
        self.assertEqual(merged["Completion Date"], "2021-06-20")

        # Test yes prioritization
        self.assertEqual(merged["Is Resp Satisfactory?"], "Yes")

        # Test metadata
        self.assertEqual(merged["_merged_from_count"], 2)
        self.assertIn("_merge_timestamp", merged)

    def test_analyze_dataset_differences(self):
        """Test dataset difference analysis functionality."""
        # Create temporary input file with test data
        test_data = [
            {
                "Action Request Number:": "TEST-001",
                "Title": "Test Issue 1",
                "Action Plan": ["Action 1"],
                "Stage": "Open - Receiver Proposing Action Plan",
                "Amount": 100,
            },
            {
                "Action Request Number:": "TEST-001",
                "Title": "Test Issue 1",
                "Action Plan": ["Action 2"],
                "Stage": "Action Plan Implemented - Actions Effective - Closed",
                "Amount": 200,
            },
            {
                "Action Request Number:": "TEST-002",
                "Title": "Test Issue 2",
                "Action Plan": ["Single Action"],
                "Stage": "Open - Receiver Proposing Action Plan",
                "Amount": 150,
            },
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as input_file:
            json.dump(test_data, input_file)
            input_path = input_file.name

        try:
            # Analyze the dataset
            analysis = self.merger.analyze_dataset_differences(input_path)

            # Verify analysis structure
            self.assertIn("total_records", analysis)
            self.assertIn("unique_action_requests", analysis)
            self.assertIn("duplicate_groups", analysis)
            self.assertIn("field_difference_patterns", analysis)
            self.assertIn("strategy_recommendations", analysis)
            self.assertIn("complexity_analysis", analysis)

            # Verify analysis results
            self.assertEqual(analysis["total_records"], 3)
            self.assertEqual(analysis["unique_action_requests"], 2)
            self.assertEqual(analysis["duplicate_groups"], 1)

            # Should detect differences in Action Plan, Stage, Amount
            self.assertIn("Action Plan", analysis["field_difference_patterns"])
            self.assertIn("Stage", analysis["field_difference_patterns"])
            self.assertIn("Amount", analysis["field_difference_patterns"])

        finally:
            # Clean up
            Path(input_path).unlink(missing_ok=True)

    def test_single_record_merge(self):
        """Test that single records are returned unchanged."""
        single_record = self.sample_duplicates[0]
        result = self.merger.merge_duplicate_records([single_record])

        # Should be the same record (reference equality)
        self.assertEqual(result, single_record)

    def test_empty_record_list(self):
        """Test that empty record list raises error."""
        with self.assertRaises(ValueError):
            self.merger.merge_duplicate_records([])

    def test_process_data_integration(self):
        """Test the complete data processing workflow."""
        # Create temporary input file
        test_data = [
            {
                "Action Request Number:": "TEST-001",
                "Title": "Test Issue 1",
                "Action Plan": ["Action 1"],
                "Stage": "Open - Receiver Proposing Action Plan",
            },
            {
                "Action Request Number:": "TEST-001",
                "Title": "Test Issue 1",
                "Action Plan": ["Action 2"],
                "Stage": "Action Plan Implemented - Actions Effective - Closed",
            },
            {
                "Action Request Number:": "TEST-002",
                "Title": "Test Issue 2",
                "Action Plan": ["Single Action"],
                "Stage": "Open - Receiver Proposing Action Plan",
            },
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as input_file:
            json.dump(test_data, input_file)
            input_path = input_file.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as output_file:
            output_path = output_file.name

        try:
            # Process the data
            stats = self.merger.process_data(input_path, output_path)

            # Verify statistics
            self.assertEqual(stats["original_records"], 3)
            self.assertEqual(stats["unique_action_requests"], 2)
            self.assertEqual(stats["duplicates_found"], 1)
            self.assertEqual(stats["duplicates_merged"], 1)
            self.assertEqual(stats["final_records"], 2)

            # Verify output file content
            with open(output_path, "r") as f:
                result_data = json.load(f)

            self.assertEqual(len(result_data), 2)

            # Find the merged record
            merged_record = None
            single_record = None
            for record in result_data:
                if record.get("_merged_from_count"):
                    merged_record = record
                else:
                    single_record = record

            self.assertIsNotNone(merged_record)
            self.assertIsNotNone(single_record)

            # Verify merged record
            self.assertEqual(merged_record["Action Request Number:"], "TEST-001")
            self.assertEqual(merged_record["Action Plan"], ["Action 1", "Action 2"])
            self.assertEqual(
                merged_record["Stage"], "Action Plan Implemented - Actions Effective - Closed"
            )
            self.assertEqual(merged_record["_merged_from_count"], 2)

            # Verify single record remains unchanged
            self.assertEqual(single_record["Action Request Number:"], "TEST-002")
            self.assertEqual(single_record["Action Plan"], ["Single Action"])

        finally:
            # Clean up temporary files
            Path(input_path).unlink(missing_ok=True)
            Path(output_path).unlink(missing_ok=True)


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()

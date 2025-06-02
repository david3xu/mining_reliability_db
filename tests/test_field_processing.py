#!/usr/bin/env python3
"""
Simplified Test Suite for Field Processing Components
Focused testing for clean single-value dataset processing with root cause intelligence.
"""

import os
import sys

import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mine_core.pipelines.transformer import DataTransformer
from mine_core.shared.field_utils import (
    clean_label,
    extract_root_cause_tail,
    get_causal_intelligence_fields,
    get_missing_indicator,
    has_real_value,
)


class TestSimplifiedFieldUtils:
    """Test simplified field utility functions"""

    def test_has_real_value(self):
        """Test real value detection for clean datasets"""
        assert has_real_value("Motor failure") == True
        assert has_real_value("") == False
        assert has_real_value(None) == False
        assert has_real_value("DATA_NOT_AVAILABLE") == False
        assert has_real_value("NOT_SPECIFIED") == False
        assert has_real_value(42) == True
        assert has_real_value(False) == True  # Boolean false is still a real value

    def test_get_missing_indicator(self):
        """Test missing data indicator assignment"""
        assert get_missing_indicator("Due Date") == "DATA_NOT_AVAILABLE"
        assert get_missing_indicator("Comments", "optional") == "NOT_APPLICABLE"
        assert get_missing_indicator("Description") == "NOT_SPECIFIED"
        assert get_missing_indicator("Root Cause") == "DATA_NOT_AVAILABLE"

    def test_clean_label(self):
        """Test label cleaning for Neo4j compatibility"""
        assert clean_label("Motor Failure") == "Motor_Failure"
        assert clean_label("Root Cause #1") == "Root_Cause_1"
        assert clean_label("123 Equipment") == "_123_Equipment"
        assert clean_label("") == "UnknownValue"

        # Test length limit
        long_text = "Very_Long_Equipment_Name_That_Exceeds_Fifty_Characters_Limit"
        assert len(clean_label(long_text)) == 50

    def test_extract_root_cause_tail(self):
        """Test root cause tail extraction for causal intelligence"""
        # Single cause - should return original
        assert extract_root_cause_tail("Equipment failure") == "Equipment failure"

        # Multiple causes with semicolon
        assert extract_root_cause_tail("Equipment failure; Poor maintenance") == "Poor maintenance"

        # Multiple causes with comma
        assert (
            extract_root_cause_tail("Heat damage, Inadequate ventilation, Design flaw")
            == "Design flaw"
        )

        # Multiple causes with 'and'
        assert (
            extract_root_cause_tail("Mechanical wear and insufficient lubrication")
            == "insufficient lubrication"
        )

        # Empty/None cases
        assert extract_root_cause_tail("") == "NOT_SPECIFIED"
        assert extract_root_cause_tail(None) == "NOT_SPECIFIED"

    def test_get_causal_intelligence_fields(self):
        """Test causal intelligence field extraction"""
        record = {
            "Root Cause": "Equipment overheating; Poor maintenance schedule",
            "Obj. Evidence": "Temperature logs show excessive heat",
            "Other Field": "Some other data",
        }

        causal_fields = get_causal_intelligence_fields(record)

        assert causal_fields["primary_cause"] == "Equipment overheating; Poor maintenance schedule"
        assert causal_fields["secondary_cause"] == "Poor maintenance schedule"
        assert causal_fields["evidence"] == "Temperature logs show excessive heat"


class TestDataTransformer:
    """Test simplified transformation logic with causal intelligence"""

    def setup_method(self):
        """Setup test environment"""
        self.sample_mappings = {
            "entity_mappings": {
                "ActionRequest": {
                    "action_request_number": "Action Request Number:",
                    "title": "Title",
                    "categories": "Categories",
                },
                "Problem": {"what_happened": "What happened?", "requirement": "Requirement"},
                "RootCause": {
                    "root_cause": "Root Cause",
                    "root_cause_tail": "Root Cause",
                    "objective_evidence": "Obj. Evidence",
                },
            },
            "cascade_labeling": {
                "ActionRequest": {
                    "label_priority": ["Title", "Action Request Number:"],
                    "required_fields": ["Action Request Number:"],
                    "entity_type": "ActionRequest",
                },
                "RootCause": {
                    "label_priority": ["Root Cause"],
                    "required_fields": ["Root Cause"],
                    "entity_type": "RootCause",
                },
            },
        }

        self.transformer = DataTransformer(self.sample_mappings, use_config=False)

    def test_transform_facility_data(self):
        """Test complete facility data transformation"""
        facility_data = {
            "facility_id": "TEST_FACILITY",
            "records": [
                {
                    "Action Request Number:": "AR-001",
                    "Title": "Conveyor System Failure",
                    "Categories": "Mechanical",
                    "What happened?": "Belt conveyor stopped during shift",
                    "Root Cause": "Motor bearing failure; Insufficient lubrication schedule",
                }
            ],
        }

        result = self.transformer.transform_facility_data(facility_data)

        # Check structure
        assert "facility" in result
        assert "entities" in result

        # Check facility
        assert result["facility"]["facility_id"] == "TEST_FACILITY"

        # Check entities were created
        assert len(result["entities"]["ActionRequest"]) == 1
        assert len(result["entities"]["Problem"]) == 1
        assert len(result["entities"]["RootCause"]) == 1

    def test_root_cause_intelligence_enhancement(self):
        """Test root cause tail extraction in transformation"""
        record = {
            "Action Request Number:": "AR-002",
            "Title": "Equipment Issue",
            "Root Cause": "Primary cause; Secondary contributing factor",
            "Obj. Evidence": "Maintenance logs and inspection reports",
        }

        base_id = "test_facility_ar002"
        root_cause = self.transformer._create_root_cause_with_intelligence(record, base_id)

        # Verify both primary and tail cause are captured
        assert root_cause["root_cause"] == "Primary cause; Secondary contributing factor"
        assert root_cause["root_cause_tail"] == "Secondary contributing factor"
        assert root_cause["objective_evidence"] == "Maintenance logs and inspection reports"

    def test_cascade_labeling_application(self):
        """Test cascade labeling with clean data"""
        entity_data = {
            "actionrequest_id": "ar-test001",
            "action_request_number": "AR-001",
            "title": "Equipment Malfunction",
            "categories": "Mechanical",
        }

        label = self.transformer._apply_cascade_labeling(entity_data, "ActionRequest")
        assert label == "Equipment_Malfunction"  # Should use title as first priority

    def test_missing_data_handling(self):
        """Test proper missing data indicator assignment"""
        record = {
            "Action Request Number:": "AR-003",
            "Title": "Test Issue"
            # Categories missing - should get indicator
        }

        entity = self.transformer._create_entity_with_labeling(record, "ActionRequest", "test_base")

        assert entity["action_request_number"] == "AR-003"
        assert entity["title"] == "Test Issue"
        assert entity["categories"] == "DATA_NOT_AVAILABLE"  # Missing field indicator

    def test_entity_creation_conditions(self):
        """Test conditional entity creation logic"""
        # Record with required data for RootCause
        record_with_cause = {
            "Action Request Number:": "AR-004",
            "Root Cause": "Actual equipment failure cause",
        }
        assert self.transformer._has_required_data("RootCause", record_with_cause) == True

        # Record without required data for RootCause
        record_without_cause = {
            "Action Request Number:": "AR-005",
            "Title": "Some issue"
            # No Root Cause field
        }
        assert self.transformer._has_required_data("RootCause", record_without_cause) == False


class TestCausalIntelligenceWorkflow:
    """Test complete causal intelligence workflow"""

    def setup_method(self):
        """Setup causal intelligence test environment"""
        self.causal_config = {
            "entity_mappings": {
                "ActionRequest": {
                    "action_request_number": "Action Request Number:",
                    "title": "Title",
                    "categories": "Categories",
                },
                "Problem": {"what_happened": "What happened?"},
                "RootCause": {
                    "root_cause": "Root Cause",
                    "root_cause_tail": "Root Cause",
                    "objective_evidence": "Obj. Evidence",
                },
                "ActionPlan": {"action_plan": "Action Plan"},
                "Verification": {"is_action_plan_effective": "IsActionPlanEffective"},
            },
            "cascade_labeling": {
                "ActionRequest": {
                    "label_priority": ["Title"],
                    "required_fields": ["Action Request Number:"],
                    "entity_type": "ActionRequest",
                },
                "Problem": {
                    "label_priority": ["What happened?"],
                    "required_fields": ["What happened?"],
                    "entity_type": "Problem",
                },
                "RootCause": {
                    "label_priority": ["Root Cause"],
                    "required_fields": ["Root Cause"],
                    "entity_type": "RootCause",
                },
                "ActionPlan": {
                    "label_priority": ["Action Plan"],
                    "required_fields": ["Action Plan"],
                    "entity_type": "ActionPlan",
                },
                "Verification": {
                    "label_priority": ["IsActionPlanEffective"],
                    "required_fields": ["IsActionPlanEffective"],
                    "entity_type": "Verification",
                },
            },
        }

    def test_complete_causal_workflow(self):
        """Test complete incident workflow with causal intelligence"""
        transformer = DataTransformer(self.causal_config, use_config=False)

        facility_data = {
            "facility_id": "CAUSAL_TEST",
            "records": [
                {
                    "Action Request Number:": "AR-CAUSAL-001",
                    "Title": "Motor Failure Analysis",
                    "Categories": "Equipment",
                    "What happened?": "Primary motor failed during operation",
                    "Root Cause": "Bearing deterioration; Inadequate maintenance frequency; Poor lubrication quality",
                    "Obj. Evidence": "Bearing inspection report and maintenance logs",
                    "Action Plan": "Replace bearings and improve maintenance schedule",
                    "IsActionPlanEffective": "true",
                }
            ],
        }

        result = transformer.transform_facility_data(facility_data)

        # Verify complete workflow chain
        assert len(result["entities"]["ActionRequest"]) == 1
        assert len(result["entities"]["Problem"]) == 1
        assert len(result["entities"]["RootCause"]) == 1
        assert len(result["entities"]["ActionPlan"]) == 1
        assert len(result["entities"]["Verification"]) == 1

        # Verify causal intelligence enhancement
        root_cause = result["entities"]["RootCause"][0]
        assert "root_cause" in root_cause
        assert "root_cause_tail" in root_cause
        assert root_cause["root_cause_tail"] == "Poor lubrication quality"  # Tail extraction

        # Verify dynamic labeling
        action_request = result["entities"]["ActionRequest"][0]
        assert action_request["_dynamic_label"] == "Motor_Failure_Analysis"

    def test_causal_intelligence_edge_cases(self):
        """Test causal intelligence with edge cases"""
        transformer = DataTransformer(self.causal_config, use_config=False)

        # Test various root cause formats
        test_cases = [
            {
                "input": "Single cause without delimiters",
                "expected_tail": "Single cause without delimiters",
            },
            {"input": "First cause, Second cause, Final cause", "expected_tail": "Final cause"},
            {
                "input": "Equipment failure - maintenance issue",
                "expected_tail": "maintenance issue",
            },
            {"input": "", "expected_tail": "NOT_SPECIFIED"},
        ]

        for test_case in test_cases:
            result = transformer._extract_tail_value(test_case["input"])
            assert result == test_case["expected_tail"]


class TestDataQualityValidation:
    """Test data quality validation for simplified processing"""

    def test_missing_data_completeness(self):
        """Test missing data indicator consistency"""
        from mine_core.shared.field_utils import is_missing_data_indicator

        # Valid missing indicators
        assert is_missing_data_indicator("DATA_NOT_AVAILABLE") == True
        assert is_missing_data_indicator("NOT_SPECIFIED") == True
        assert is_missing_data_indicator("NOT_APPLICABLE") == True

        # Real data values
        assert is_missing_data_indicator("Equipment failure") == False
        assert is_missing_data_indicator("Motor bearing issue") == False
        assert is_missing_data_indicator("123") == False

    def test_field_categorization(self):
        """Test field category detection for analytics"""
        from mine_core.shared.field_utils import get_field_category

        assert get_field_category("Due Date") == "temporal"
        assert get_field_category("Action Request Number:") == "identifier"
        assert get_field_category("Categories") == "categorical"
        assert get_field_category("What happened?") == "descriptive"
        assert get_field_category("Complete") == "boolean"
        assert get_field_category("Amount of Loss") == "quantitative"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

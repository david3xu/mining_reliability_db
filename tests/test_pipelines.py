#!/usr/bin/env python3
"""
Simplified Pipeline Integration Tests for Mining Reliability Database
End-to-end testing of clean dataset processing with causal intelligence.
"""

import pytest
import sys
import os
import tempfile
import json
from unittest.mock import Mock, patch

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mine_core.pipelines.extractor import FacilityDataExtractor
from mine_core.pipelines.transformer import SimplifiedTransformer
from mine_core.pipelines.loader import SimplifiedLoader

class TestSimplifiedETLPipeline:
    """Test streamlined ETL pipeline for clean datasets"""

    def setup_method(self):
        """Setup test environment"""
        self.test_config = {
            "entity_mappings": {
                "ActionRequest": {
                    "action_request_number": "Action Request Number:",
                    "title": "Title",
                    "categories": "Categories"
                },
                "Problem": {
                    "what_happened": "What happened?",
                    "requirement": "Requirement"
                },
                "RootCause": {
                    "root_cause": "Root Cause",
                    "root_cause_tail": "Root Cause",
                    "objective_evidence": "Obj. Evidence"
                },
                "ActionPlan": {
                    "action_plan": "Action Plan",
                    "complete": "Complete"
                },
                "Verification": {
                    "is_action_plan_effective": "IsActionPlanEffective"
                }
            },
            "cascade_labeling": {
                "ActionRequest": {
                    "label_priority": ["Title", "Categories"],
                    "required_fields": ["Action Request Number:"],
                    "entity_type": "ActionRequest"
                },
                "Problem": {
                    "label_priority": ["What happened?"],
                    "required_fields": ["What happened?"],
                    "entity_type": "Problem"
                },
                "RootCause": {
                    "label_priority": ["Root Cause"],
                    "required_fields": ["Root Cause"],
                    "entity_type": "RootCause"
                },
                "ActionPlan": {
                    "label_priority": ["Action Plan"],
                    "required_fields": ["Action Plan"],
                    "entity_type": "ActionPlan"
                },
                "Verification": {
                    "label_priority": ["IsActionPlanEffective"],
                    "required_fields": ["IsActionPlanEffective"],
                    "entity_type": "Verification"
                }
            }
        }

        self.sample_clean_data = {
            "facility_id": "CLEAN_TEST",
            "records": [
                {
                    "Action Request Number:": "AR-CLEAN-001",
                    "Title": "Conveyor Belt Issue",
                    "Categories": "Mechanical",
                    "What happened?": "Conveyor belt tore during operation",
                    "Root Cause": "Material fatigue; Excessive load; Poor maintenance",
                    "Obj. Evidence": "Belt inspection revealed multiple stress fractures",
                    "Action Plan": "Replace belt with higher grade material",
                    "Complete": "true",
                    "IsActionPlanEffective": "true"
                },
                {
                    "Action Request Number:": "AR-CLEAN-002",
                    "Title": "Electrical System Fault",
                    "Categories": "Electrical",
                    "What happened?": "Power interruption to primary systems",
                    "Root Cause": "Circuit breaker malfunction",
                    "Action Plan": "Replace faulty circuit breaker",
                    "IsActionPlanEffective": "true"
                }
            ]
        }

    def test_extractor_clean_data_handling(self):
        """Test extractor with clean single-value data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test data file
            test_file = os.path.join(temp_dir, "clean_facility.json")
            with open(test_file, 'w') as f:
                json.dump(self.sample_clean_data, f)

            # Test extraction
            extractor = FacilityDataExtractor(temp_dir)
            extracted_data = extractor.extract_facility_data("clean_facility")

            assert extracted_data["facility_id"] == "clean_facility"
            assert len(extracted_data["records"]) == 2
            assert "Action Request Number:" in extracted_data["records"][0]

    def test_transformer_causal_intelligence(self):
        """Test transformer with causal intelligence enhancement"""
        transformer = SimplifiedTransformer(self.test_config, use_config=False)
        transformed = transformer.transform_facility_data(self.sample_clean_data)

        # Verify structure
        assert "facility" in transformed
        assert "entities" in transformed

        # Verify entities created
        assert len(transformed["entities"]["ActionRequest"]) == 2
        assert len(transformed["entities"]["Problem"]) == 2
        assert len(transformed["entities"]["RootCause"]) == 2
        assert len(transformed["entities"]["ActionPlan"]) == 2
        assert len(transformed["entities"]["Verification"]) == 2

        # Verify causal intelligence - first record has complex root cause
        root_cause_1 = transformed["entities"]["RootCause"][0]
        assert root_cause_1["root_cause"] == "Material fatigue; Excessive load; Poor maintenance"
        assert root_cause_1["root_cause_tail"] == "Poor maintenance"  # Tail extraction

        # Verify causal intelligence - second record has simple root cause
        root_cause_2 = transformed["entities"]["RootCause"][1]
        assert root_cause_2["root_cause"] == "Circuit breaker malfunction"
        assert root_cause_2["root_cause_tail"] == "Circuit breaker malfunction"  # Same as primary

        # Verify dynamic labeling
        ar1 = transformed["entities"]["ActionRequest"][0]
        ar2 = transformed["entities"]["ActionRequest"][1]
        assert ar1["_dynamic_label"] == "Conveyor_Belt_Issue"
        assert ar2["_dynamic_label"] == "Electrical_System_Fault"

    @patch('mine_core.database.db.get_database')
    def test_loader_simplified_processing(self, mock_get_db):
        """Test loader with simplified clean data processing"""
        # Setup mock database
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        mock_db.create_entity_with_dynamic_label.return_value = True
        mock_db.batch_create_entities_with_labels.return_value = True
        mock_db.create_relationship.return_value = True

        # Prepare test data
        transformer = SimplifiedTransformer(self.test_config, use_config=False)
        transformed_data = transformer.transform_facility_data(self.sample_clean_data)

        # Test loading
        loader = SimplifiedLoader()
        result = loader.load_data(transformed_data)

        assert result == True

        # Verify database operations were called
        mock_db.create_entity_with_dynamic_label.assert_called()  # Facility
        mock_db.batch_create_entities_with_labels.assert_called()  # Entities

    def test_end_to_end_clean_pipeline(self):
        """Test complete ETL pipeline with clean data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test data file
            test_file = os.path.join(temp_dir, "e2e_clean.json")
            with open(test_file, 'w') as f:
                json.dump(self.sample_clean_data, f)

            # Mock database for loading phase
            with patch('mine_core.database.db.get_database') as mock_get_db:
                mock_db = Mock()
                mock_get_db.return_value = mock_db
                mock_db.create_entity_with_dynamic_label.return_value = True
                mock_db.batch_create_entities_with_labels.return_value = True
                mock_db.create_relationship.return_value = True

                # Execute pipeline
                extractor = FacilityDataExtractor(temp_dir)
                transformer = SimplifiedTransformer(self.test_config, use_config=False)
                loader = SimplifiedLoader()

                # Extract
                extracted_data = extractor.extract_facility_data("e2e_clean")
                assert extracted_data["facility_id"] == "e2e_clean"

                # Transform
                transformed_data = transformer.transform_facility_data(extracted_data)
                assert len(transformed_data["entities"]["ActionRequest"]) == 2

                # Load
                load_result = loader.load_data(transformed_data)
                assert load_result == True

    def test_causal_intelligence_workflow_integrity(self):
        """Test causal intelligence preservation through complete workflow"""
        causal_test_data = {
            "facility_id": "CAUSAL_INTEGRITY_TEST",
            "records": [
                {
                    "Action Request Number:": "AR-CI-001",
                    "Title": "Complex Causal Analysis",
                    "Categories": "Multi-factor",
                    "What happened?": "System failure with multiple contributing factors",
                    "Root Cause": "Primary hardware failure; Secondary software conflict; Tertiary operator error",
                    "Obj. Evidence": "Hardware diagnostics, software logs, and operator interviews",
                    "Action Plan": "Multi-phase corrective action addressing all factors",
                    "IsActionPlanEffective": "true"
                }
            ]
        }

        transformer = SimplifiedTransformer(self.test_config, use_config=False)
        transformed = transformer.transform_facility_data(causal_test_data)

        # Verify causal intelligence preservation
        root_cause = transformed["entities"]["RootCause"][0]
        assert "root_cause" in root_cause
        assert "root_cause_tail" in root_cause
        assert "objective_evidence" in root_cause

        # Verify tail extraction logic
        assert root_cause["root_cause_tail"] == "Tertiary operator error"
        assert "Primary hardware failure" in root_cause["root_cause"]

    def test_missing_data_handling_in_pipeline(self):
        """Test pipeline handling of missing data with indicators"""
        missing_data_test = {
            "facility_id": "MISSING_DATA_TEST",
            "records": [
                {
                    "Action Request Number:": "AR-MISS-001",
                    "Title": "Minimal Data Issue"
                    # Most fields missing - should still create basic structure
                }
            ]
        }

        transformer = SimplifiedTransformer(self.test_config, use_config=False)
        transformed = transformer.transform_facility_data(missing_data_test)

        # Should create ActionRequest despite missing data
        assert len(transformed["entities"]["ActionRequest"]) == 1

        # Should not create Problem/RootCause without required fields
        assert len(transformed["entities"]["Problem"]) == 0
        assert len(transformed["entities"]["RootCause"]) == 0

        # ActionRequest should have missing indicators for absent fields
        action_request = transformed["entities"]["ActionRequest"][0]
        assert action_request["title"] == "Minimal Data Issue"
        assert action_request["categories"] == "DATA_NOT_AVAILABLE"

    def test_performance_with_moderate_dataset(self):
        """Test pipeline performance with moderate-sized clean dataset"""
        # Generate moderate test dataset
        moderate_dataset = {
            "facility_id": "PERFORMANCE_TEST",
            "records": []
        }

        for i in range(50):  # 50 clean records
            record = {
                "Action Request Number:": f"AR-PERF-{i:03d}",
                "Title": f"Performance Test Issue {i}",
                "Categories": "Testing",
                "What happened?": f"Test incident {i} with clean data",
                "Root Cause": f"Primary cause {i}; Secondary factor {i}",
                "Action Plan": f"Resolution plan {i}",
                "IsActionPlanEffective": "true" if i % 2 == 0 else "false"
            }
            moderate_dataset["records"].append(record)

        transformer = SimplifiedTransformer(self.test_config, use_config=False)

        # Should complete transformation efficiently
        transformed = transformer.transform_facility_data(moderate_dataset)

        assert len(transformed["entities"]["ActionRequest"]) == 50
        assert len(transformed["entities"]["Problem"]) == 50
        assert len(transformed["entities"]["RootCause"]) == 50

        # Verify causal intelligence processing for all records
        for root_cause in transformed["entities"]["RootCause"]:
            assert "root_cause" in root_cause
            assert "root_cause_tail" in root_cause
            # Tail should be extracted properly
            assert "Secondary factor" in root_cause["root_cause_tail"]

class TestCausalIntelligenceIntegration:
    """Test causal intelligence integration across pipeline"""

    def test_causal_pattern_consistency(self):
        """Test consistent causal pattern processing"""
        causal_patterns = [
            "Single cause",
            "Primary; Secondary",
            "First, Second, Third",
            "Cause A - Cause B",
            "Factor 1 / Factor 2",
            "Issue and Related Problem"
        ]

        config = {
            "entity_mappings": {
                "RootCause": {
                    "root_cause": "Root Cause",
                    "root_cause_tail": "Root Cause"
                }
            },
            "cascade_labeling": {
                "RootCause": {
                    "label_priority": ["Root Cause"],
                    "required_fields": ["Root Cause"],
                    "entity_type": "RootCause"
                }
            }
        }

        transformer = SimplifiedTransformer(config, use_config=False)

        expected_tails = [
            "Single cause",      # No delimiter
            "Secondary",         # Semicolon
            "Third",            # Comma
            "Cause B",          # Dash
            "Factor 2",         # Slash
            "Related Problem"   # And
        ]

        for i, pattern in enumerate(causal_patterns):
            result = transformer._extract_tail_value(pattern)
            assert result == expected_tails[i]

    def test_operational_intelligence_data_flow(self):
        """Test data flow for operational intelligence analytics"""
        operational_data = {
            "facility_id": "OPERATIONAL_INTELLIGENCE",
            "records": [
                {
                    "Action Request Number:": "AR-OP-001",
                    "Title": "Operational Intelligence Test",
                    "Categories": "Equipment",
                    "What happened?": "Equipment degradation observed",
                    "Root Cause": "Wear and tear; Inadequate preventive maintenance",
                    "Obj. Evidence": "Inspection reports and maintenance history",
                    "Action Plan": "Implement enhanced maintenance protocol",
                    "Complete": "true",
                    "IsActionPlanEffective": "true"
                }
            ]
        }

        config = {
            "entity_mappings": {
                "ActionRequest": {
                    "action_request_number": "Action Request Number:",
                    "title": "Title",
                    "categories": "Categories"
                },
                "Problem": {
                    "what_happened": "What happened?"
                },
                "RootCause": {
                    "root_cause": "Root Cause",
                    "root_cause_tail": "Root Cause",
                    "objective_evidence": "Obj. Evidence"
                },
                "ActionPlan": {
                    "action_plan": "Action Plan",
                    "complete": "Complete"
                },
                "Verification": {
                    "is_action_plan_effective": "IsActionPlanEffective"
                }
            },
            "cascade_labeling": {
                "ActionRequest": {"label_priority": ["Title"], "required_fields": ["Action Request Number:"], "entity_type": "ActionRequest"},
                "Problem": {"label_priority": ["What happened?"], "required_fields": ["What happened?"], "entity_type": "Problem"},
                "RootCause": {"label_priority": ["Root Cause"], "required_fields": ["Root Cause"], "entity_type": "RootCause"},
                "ActionPlan": {"label_priority": ["Action Plan"], "required_fields": ["Action Plan"], "entity_type": "ActionPlan"},
                "Verification": {"label_priority": ["IsActionPlanEffective"], "required_fields": ["IsActionPlanEffective"], "entity_type": "Verification"}
            }
        }

        transformer = SimplifiedTransformer(config, use_config=False)
        result = transformer.transform_facility_data(operational_data)

        # Verify complete workflow for operational intelligence
        assert len(result["entities"]["ActionRequest"]) == 1
        assert len(result["entities"]["Problem"]) == 1
        assert len(result["entities"]["RootCause"]) == 1
        assert len(result["entities"]["ActionPlan"]) == 1
        assert len(result["entities"]["Verification"]) == 1

        # Verify causal intelligence for analytics
        root_cause = result["entities"]["RootCause"][0]
        action_plan = result["entities"]["ActionPlan"][0]
        verification = result["entities"]["Verification"][0]

        assert root_cause["root_cause_tail"] == "Inadequate preventive maintenance"
        assert action_plan["complete"] == "true"
        assert verification["is_action_plan_effective"] == "true"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

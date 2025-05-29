#!/usr/bin/env python3
"""
Tests for ETL pipeline components
Tests extractor, transformer, and loader integration.
"""

import os
import json
import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from mine_core.pipelines.extractor import FacilityDataExtractor, extract_all_facilities
from mine_core.pipelines.transformer import DataTransformer
from mine_core.pipelines.loader import Neo4jLoader

class TestExtractor(unittest.TestCase):
    """Tests for FacilityDataExtractor class"""

    @patch('pathlib.Path.glob')
    @patch('pathlib.Path.exists')
    def test_get_available_facilities(self, mock_exists, mock_glob):
        """Test get_available_facilities method"""
        # Setup mocks
        mock_exists.return_value = True

        # Create Path objects for mock files
        mock_paths = [
            Path('/fake/path/facility1.json'),
            Path('/fake/path/facility2.json'),
            Path('/fake/path/sample.json')
        ]
        mock_glob.return_value = mock_paths

        # Create extractor and get facilities
        extractor = FacilityDataExtractor('/fake/path')
        facilities = extractor.get_available_facilities()

        # Check results
        self.assertEqual(len(facilities), 3)
        self.assertIn('facility1', facilities)
        self.assertIn('facility2', facilities)
        self.assertIn('sample', facilities)

    @patch('pathlib.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_extract_facility_data(self, mock_json_load, mock_file_open, mock_exists):
        """Test extract_facility_data method"""
        # Setup mocks
        mock_exists.return_value = True

        # Mock JSON data
        mock_data = {
            'sheets': {
                'Sheet1': {
                    'records': [
                        {'id': 1, 'name': 'Record 1'},
                        {'id': 2, 'name': 'Record 2'}
                    ]
                }
            }
        }
        mock_json_load.return_value = mock_data

        # Create extractor and extract data
        extractor = FacilityDataExtractor('/fake/path')
        result = extractor.extract_facility_data('facility1')

        # Check results
        self.assertEqual(result['facility_id'], 'facility1')
        self.assertEqual(len(result['records']), 2)
        self.assertEqual(result['records'][0]['id'], 1)
        self.assertEqual(result['records'][1]['name'], 'Record 2')

class TestTransformer(unittest.TestCase):
    """Tests for DataTransformer class"""

    def setUp(self):
        """Set up test cases"""
        self.transformer = DataTransformer()

        # Sample facility data
        self.facility_data = {
            'facility_id': 'test_facility',
            'records': [
                {
                    'Action Request Number:': 'AR-001',
                    'Title': 'Test Request',
                    'Initiation Date': '2023-01-01',
                    'Action Types': 'Corrective',
                    'What happened?': 'Test incident occurred',
                    'Root Cause': ['Initial cause', 'Underlying cause'],
                    'Obj. Evidence': ['Evidence item']
                }
            ]
        }

    def test_transform_facility_data(self):
        """Test transform_facility_data method"""
        # Transform data
        transformed = self.transformer.transform_facility_data(self.facility_data)

        # Check facility data
        self.assertEqual(transformed['facility']['facility_id'], 'test_facility')

        # Check ActionRequest
        action_requests = transformed['entities']['ActionRequest']
        self.assertEqual(len(action_requests), 1)
        self.assertEqual(action_requests[0]['action_request_number'], 'AR-001')
        self.assertEqual(action_requests[0]['title'], 'Test Request')

        # Check Problem
        problems = transformed['entities']['Problem']
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0]['what_happened'], 'Test incident occurred')

        # Check RootCause with list extraction
        root_causes = transformed['entities']['RootCause']
        self.assertEqual(len(root_causes), 1)
        self.assertEqual(root_causes[0]['root_cause'], 'Underlying cause')  # Second item
        self.assertEqual(root_causes[0]['objective_evidence'], 'Evidence item')  # First item

class TestLoader(unittest.TestCase):
    """Tests for Neo4jLoader class"""

    def test_load_data(self):
        """Test load_data method"""
        # Create loader
        loader = Neo4jLoader()

        # Mock the database instance directly
        mock_db = MagicMock()
        mock_db.create_entity.return_value = True
        mock_db.batch_create_entities.return_value = True
        mock_db.create_relationship.return_value = True
        loader.db = mock_db

        # Sample transformed data
        transformed_data = {
            'facility': {
                'facility_id': 'test_facility',
                'facility_name': 'Test Facility',
                'active': True
            },
            'entities': {
                'ActionRequest': [
                    {
                        'actionrequest_id': 'ar-001',
                        'facility_id': 'test_facility',
                        'action_request_number': 'AR-001',
                        'title': 'Test Request'
                    }
                ],
                'Problem': [],
                'RootCause': [],
                'ActionPlan': [],
                'Verification': [],
                'Department': [],
                'Asset': [],
                'RecurringStatus': [],
                'AmountOfLoss': [],
                'Review': [],
                'EquipmentStrategy': []
            }
        }

        # Load data
        result = loader.load_data(transformed_data)

        # Check result
        self.assertTrue(result)

        # Check database method calls
        # Should call create_entity for facility, batch_create_entities for ActionRequest,
        # and create_relationship only for ActionRequest->Facility (1 time, since other entities are empty)
        mock_db.create_entity.assert_called_once()
        mock_db.batch_create_entities.assert_called_once()
        self.assertEqual(mock_db.create_relationship.call_count, 1)

        # Test with entities
        transformed_data['entities']['Problem'] = [
            {
                'problem_id': 'prob-001',
                'actionrequest_id': 'ar-001',
                'what_happened': 'Test incident'
            }
        ]

        mock_db.reset_mock()
        result = loader.load_data(transformed_data)

        # Check result
        self.assertTrue(result)

        # Check database method calls
        # Should call create_entity for facility, batch_create_entities for ActionRequest and Problem,
        # and create_relationship for ActionRequest->Facility and Problem->ActionRequest (2 times)
        mock_db.create_entity.assert_called_once()
        self.assertEqual(mock_db.batch_create_entities.call_count, 2)
        self.assertEqual(mock_db.create_relationship.call_count, 2)

class TestPipelineIntegration(unittest.TestCase):
    """Integration tests for full ETL pipeline"""

    @patch('pathlib.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_extract_transform_load(self, mock_json_load, mock_file_open, mock_exists):
        """Test extract-transform-load pipeline"""
        # Setup mocks
        mock_exists.return_value = True

        # Mock JSON data
        mock_data = {
            'sheets': {
                'Sheet1': {
                    'records': [
                        {
                            'Action Request Number:': 'AR-001',
                            'Title': 'Test Request',
                            'Initiation Date': '2023-01-01',
                            'What happened?': 'Test incident',
                            'Root Cause': ['Initial', 'Underlying'],
                            'Obj. Evidence': ['Evidence']
                        }
                    ]
                }
            }
        }
        mock_json_load.return_value = mock_data

        # Create pipeline components
        extractor = FacilityDataExtractor('/fake/path')
        transformer = DataTransformer()
        loader = Neo4jLoader()

        # Mock the loader's database
        mock_db = MagicMock()
        mock_db.create_entity.return_value = True
        mock_db.batch_create_entities.return_value = True
        mock_db.create_relationship.return_value = True
        loader.db = mock_db

        # Run pipeline
        facility_data = extractor.extract_facility_data('test_facility')
        transformed_data = transformer.transform_facility_data(facility_data)
        result = loader.load_data(transformed_data)

        # Check result
        self.assertTrue(result)

        # Check extraction
        self.assertEqual(facility_data['facility_id'], 'test_facility')
        self.assertEqual(len(facility_data['records']), 1)

        # Check transformation
        self.assertEqual(transformed_data['facility']['facility_id'], 'test_facility')
        self.assertEqual(len(transformed_data['entities']['ActionRequest']), 1)

        # Check loading - should have database method calls
        self.assertTrue(mock_db.create_entity.called)
        self.assertTrue(mock_db.batch_create_entities.called)
        self.assertTrue(mock_db.create_relationship.called)

if __name__ == '__main__':
    unittest.main()

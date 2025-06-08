#!/usr/bin/env python3
"""
Test Complete Stakeholder Journey Implementation
Tests the single input → five automatic outputs workflow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import time
from datetime import datetime
from typing import Dict, Any

def test_data_adapter_journey():
    """Test the data adapter's complete stakeholder journey method"""
    print("🧪 Testing Data Adapter Journey Methods...")

    try:
        from dashboard.adapters.data_adapter import get_data_adapter

        data_adapter = get_data_adapter()
        test_input = "excavator motor contamination"

        print(f"📝 Testing input: '{test_input}'")
        start_time = time.time()

        # Test the complete journey method
        journey_results = data_adapter.execute_complete_stakeholder_journey(test_input)

        execution_time = time.time() - start_time
        print(f"⏱️  Execution time: {execution_time:.2f} seconds")

        # Validate results structure
        if journey_results and journey_results.get("metadata", {}).get("success"):
            metadata = journey_results["metadata"]
            print(f"✅ Journey completed successfully!")
            print(f"   Keywords used: {metadata.get('keywords_used', [])}")
            print(f"   Total results: {metadata.get('total_results', 0)}")

            # Check each question section
            questions = [
                "why_did_this_happen",
                "how_do_i_figure_out_whats_wrong",
                "who_can_help_me",
                "what_should_i_check_first",
                "how_do_i_fix_it"
            ]

            for question in questions:
                section = journey_results.get(question, {})
                count = section.get("count", 0)
                title = section.get("title", question)
                print(f"   📋 {title}: {count} results")

            return True, journey_results
        else:
            error = journey_results.get("metadata", {}).get("error", "Unknown error")
            print(f"❌ Journey failed: {error}")
            return False, journey_results

    except Exception as e:
        print(f"❌ Data adapter test failed: {e}")
        return False, None

def test_individual_queries():
    """Test individual stakeholder essential queries"""
    print("\n🔍 Testing Individual Query Methods...")

    try:
        from dashboard.adapters.data_adapter import get_data_adapter

        data_adapter = get_data_adapter()
        test_input = "excavator motor"

        queries_to_test = [
            "why_did_this_happen",
            "how_do_i_figure_out_whats_wrong",
            "who_can_help_me",
            "what_should_i_check_first",
            "how_do_i_fix_it"
        ]

        results_summary = {}

        for query_type in queries_to_test:
            print(f"   Testing: {query_type}")
            start_time = time.time()

            result = data_adapter.execute_stakeholder_essential_query(query_type, test_input)

            execution_time = time.time() - start_time

            if result.get("success"):
                count = result.get("count", 0)
                print(f"   ✅ {query_type}: {count} results ({execution_time:.2f}s)")
                results_summary[query_type] = count
            else:
                error = result.get("error", "Unknown error")
                print(f"   ❌ {query_type}: Failed - {error}")
                results_summary[query_type] = 0

        total_individual = sum(results_summary.values())
        print(f"\n📊 Individual queries total: {total_individual} results")

        return True, results_summary

    except Exception as e:
        print(f"❌ Individual queries test failed: {e}")
        return False, {}

def test_keyword_extraction():
    """Test keyword extraction functionality"""
    print("\n🔤 Testing Keyword Extraction...")

    try:
        from dashboard.adapters.data_adapter import get_data_adapter

        data_adapter = get_data_adapter()

        test_cases = [
            "excavator motor contamination failure",
            "pump vibration noise issue",
            "conveyor belt wear tear",
            "hydraulic leak swing motor",
            "crusher maintenance overload"
        ]

        for test_input in test_cases:
            keywords = data_adapter._extract_keywords_from_input(test_input)
            filter_clause = data_adapter._build_filter_clause(keywords)

            print(f"   Input: '{test_input}'")
            print(f"   Keywords: {keywords}")
            print(f"   Filter length: {len(filter_clause)} chars")

        return True

    except Exception as e:
        print(f"❌ Keyword extraction test failed: {e}")
        return False

def test_component_functions():
    """Test the UI component functions"""
    print("\n🎨 Testing UI Component Functions...")

    try:
        from dashboard.components.stakeholder_essentials import (
            create_complete_stakeholder_journey,
            create_journey_results_display
        )

        # Test component creation
        journey_component = create_complete_stakeholder_journey()
        print("   ✅ Journey component created successfully")

        # Test results display with mock data
        mock_journey_data = {
            "metadata": {
                "success": True,
                "user_input": "test input",
                "keywords_used": ["test", "keyword"],
                "total_results": 25
            },
            "why_did_this_happen": {
                "title": "Why did this happen?",
                "results": [{"root_cause": "Test cause", "frequency": 5}],
                "count": 1
            },
            "how_do_i_figure_out_whats_wrong": {
                "title": "How do I figure out what's wrong?",
                "results": [],
                "count": 0
            },
            "who_can_help_me": {
                "title": "Who can help me?",
                "results": [{"initiating_department": "Maintenance", "success_rate": 85}],
                "count": 1
            },
            "what_should_i_check_first": {
                "title": "What should I check first?",
                "results": [],
                "count": 0
            },
            "how_do_i_fix_it": {
                "title": "How do I fix it?",
                "results": [{"solution": "Test solution", "effectiveness_rate": 90}],
                "count": 1
            }
        }

        results_display = create_journey_results_display(mock_journey_data)
        print("   ✅ Results display component created successfully")

        return True

    except Exception as e:
        print(f"❌ Component functions test failed: {e}")
        return False

def save_test_results(journey_results: Dict[str, Any]):
    """Save test results for analysis"""
    if not journey_results:
        return

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/stakeholder_results/test_complete_journey_{timestamp}.json"

        os.makedirs("data/stakeholder_results", exist_ok=True)

        with open(filename, 'w') as f:
            json.dump(journey_results, f, indent=2, default=str)

        print(f"📁 Test results saved to: {filename}")

    except Exception as e:
        print(f"⚠️  Could not save test results: {e}")

def main():
    """Run complete stakeholder journey implementation tests"""
    print("=" * 60)
    print("🚀 COMPLETE STAKEHOLDER JOURNEY IMPLEMENTATION TEST")
    print("=" * 60)
    print(f"📅 Test started at: {datetime.now()}")

    total_tests = 0
    passed_tests = 0

    # Test 1: Data Adapter Journey
    total_tests += 1
    success, journey_results = test_data_adapter_journey()
    if success:
        passed_tests += 1
        if journey_results:
            save_test_results(journey_results)

    # Test 2: Individual Queries
    total_tests += 1
    success, _ = test_individual_queries()
    if success:
        passed_tests += 1

    # Test 3: Keyword Extraction
    total_tests += 1
    if test_keyword_extraction():
        passed_tests += 1

    # Test 4: Component Functions
    total_tests += 1
    if test_component_functions():
        passed_tests += 1

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Complete stakeholder journey is ready!")
        print("\n🎯 IMPLEMENTATION STATUS:")
        print("   ✅ Backend data adapter methods")
        print("   ✅ Individual query execution")
        print("   ✅ Keyword extraction and filtering")
        print("   ✅ UI component functions")
        print("   ✅ Single input → five outputs workflow")
        return True
    else:
        print(f"⚠️  {total_tests - passed_tests} tests failed. Review implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

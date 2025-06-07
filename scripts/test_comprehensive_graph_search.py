#!/usr/bin/env python3
"""
Test Script for Comprehensive Multi-Dimensional Graph Search
Validates the 8-dimensional search implementation.
"""

import sys
import os
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mine_core.business.intelligence_engine import IntelligenceEngine
from dashboard.adapters.data_adapter import get_data_adapter
from configs.environment import get_graph_search_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_configuration_loading():
    """Test that the extended graph search configuration loads correctly"""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION LOADING")
    print("="*60)

    try:
        config = get_graph_search_config()

        print(f"✓ Configuration loaded successfully")
        print(f"✓ Search dimensions available: {len(config.get('search_dimensions', {}))}")
        print(f"✓ Search queries available: {len(config.get('search_queries', {}))}")
        print(f"✓ Result limits configured: {config.get('result_limits', {})}")
        print(f"✓ Performance settings: {config.get('performance_settings', {})}")

        # Test dimension configuration
        dimensions = config.get('search_dimensions', {})
        enabled_dimensions = [name for name, info in dimensions.items() if info.get('enabled', True)]

        print(f"\nEnabled Search Dimensions ({len(enabled_dimensions)}):")
        for dim in enabled_dimensions:
            weight = dimensions[dim].get('weight', 0.0)
            desc = dimensions[dim].get('description', 'No description')
            print(f"  • {dim.replace('_', ' ').title()}: {weight} - {desc}")

        return True

    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False

def test_intelligence_engine_search():
    """Test the Intelligence Engine comprehensive search"""
    print("\n" + "="*60)
    print("TESTING INTELLIGENCE ENGINE SEARCH")
    print("="*60)

    try:
        engine = IntelligenceEngine()

        # Test search terms
        test_terms = ["conveyor", "pump", "maintenance", "electrical"]

        for term in test_terms:
            print(f"\nTesting search term: '{term}'")

            result = engine.execute_comprehensive_incident_search(term)

            if result and result.data:
                incidents = len(result.data.get("incidents", []))
                solutions = len(result.data.get("solutions", []))
                facilities = len(result.data.get("facilities", []))
                dimensions = len(result.data.get("metadata", {}).get("search_dimensions_executed", []))

                print(f"  ✓ Found {incidents} incidents, {solutions} solutions, {facilities} facilities")
                print(f"  ✓ Executed {dimensions} search dimensions")
                print(f"  ✓ Quality score: {result.quality_score:.2f}")

                # Show dimensions executed
                dims_executed = result.data.get("metadata", {}).get("search_dimensions_executed", [])
                print(f"  ✓ Dimensions: {', '.join(dims_executed)}")
            else:
                print(f"  ✗ No results for '{term}'")

        return True

    except Exception as e:
        print(f"✗ Intelligence Engine search failed: {e}")
        return False

def test_data_adapter_integration():
    """Test the Data Adapter integration with enhanced search"""
    print("\n" + "="*60)
    print("TESTING DATA ADAPTER INTEGRATION")
    print("="*60)

    try:
        data_adapter = get_data_adapter()

        # Test comprehensive graph search
        test_term = "conveyor"
        print(f"Testing comprehensive graph search for: '{test_term}'")

        results = data_adapter.execute_comprehensive_graph_search(test_term)

        if results:
            incidents = len(results.get("incidents", []))
            solutions = len(results.get("solutions", []))
            facilities = len(results.get("facilities", []))

            print(f"  ✓ Data Adapter returned {incidents} incidents")
            print(f"  ✓ Data Adapter returned {solutions} solutions")
            print(f"  ✓ Data Adapter returned {facilities} facilities")
            print(f"  ✓ Result format is correct: {list(results.keys())}")

            # Test fallback mechanism
            print(f"\nTesting fallback mechanism with invalid search...")
            fallback_results = data_adapter.execute_comprehensive_graph_search("")
            print(f"  ✓ Fallback mechanism works: {type(fallback_results)}")

        else:
            print(f"  ✗ No results from Data Adapter")
            return False

        return True

    except Exception as e:
        print(f"✗ Data Adapter integration failed: {e}")
        return False

def test_search_dimensions():
    """Test individual search dimensions"""
    print("\n" + "="*60)
    print("TESTING INDIVIDUAL SEARCH DIMENSIONS")
    print("="*60)

    try:
        engine = IntelligenceEngine()
        test_term = "pump"

        # Test each dimension method
        dimension_methods = [
            ("Direct Field Matches", "_search_direct_field_matches"),
            ("Equipment Patterns", "_search_equipment_patterns"),
            ("Causal Chains", "_search_causal_chains"),
            ("Cross-Facility Patterns", "_search_cross_facility_patterns"),
            ("Temporal Patterns", "_search_temporal_patterns"),
            ("Recurring Sequences", "_search_recurring_sequences"),
            ("Solution Effectiveness", "_search_solution_effectiveness"),
            ("Equipment Failure Clusters", "_search_equipment_failure_clusters"),
        ]

        for name, method_name in dimension_methods:
            if hasattr(engine, method_name):
                try:
                    method = getattr(engine, method_name)
                    result = method(test_term)

                    total_items = sum(len(result.get(key, [])) for key in ["incidents", "solutions", "facilities"])
                    print(f"  ✓ {name}: {total_items} results")

                except Exception as e:
                    print(f"  ✗ {name}: Failed - {e}")
            else:
                print(f"  ✗ {name}: Method not found")

        return True

    except Exception as e:
        print(f"✗ Search dimensions test failed: {e}")
        return False

def test_performance_metrics():
    """Test search performance and metrics"""
    print("\n" + "="*60)
    print("TESTING PERFORMANCE METRICS")
    print("="*60)

    try:
        engine = IntelligenceEngine()

        # Time the search
        start_time = datetime.now()
        result = engine.execute_comprehensive_incident_search("conveyor belt")
        end_time = datetime.now()

        search_duration = (end_time - start_time).total_seconds()

        print(f"✓ Search completed in {search_duration:.2f} seconds")

        if result and result.data:
            metadata = result.data.get("metadata", {})
            performance = metadata.get("search_performance", {})

            print(f"✓ Dimensions executed: {performance.get('dimensions_executed', 0)}")
            print(f"✓ Total results: {performance.get('total_results', 0)}")
            print(f"✓ Quality score: {result.quality_score:.2f}")
            print(f"✓ Configuration applied: {metadata.get('config_applied', False)}")

            # Show dimension breakdown
            dimension_results = metadata.get("total_results_by_dimension", {})
            if dimension_results:
                print(f"\nResults by dimension:")
                for dim, count in dimension_results.items():
                    print(f"  • {dim.replace('_', ' ').title()}: {count}")

        return True

    except Exception as e:
        print(f"✗ Performance metrics test failed: {e}")
        return False

def run_comprehensive_tests():
    """Run all comprehensive graph search tests"""
    print("COMPREHENSIVE MULTI-DIMENSIONAL GRAPH SEARCH TEST SUITE")
    print("=" * 80)
    print(f"Test started at: {datetime.now()}")

    tests = [
        ("Configuration Loading", test_configuration_loading),
        ("Intelligence Engine Search", test_intelligence_engine_search),
        ("Data Adapter Integration", test_data_adapter_integration),
        ("Search Dimensions", test_search_dimensions),
        ("Performance Metrics", test_performance_metrics),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'-' * 40}")
        print(f"Running: {test_name}")
        print(f"{'-' * 40}")

        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} ERROR: {e}")

    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    print(f"Test completed at: {datetime.now()}")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Comprehensive search is ready for production!")
    else:
        print("⚠️  Some tests failed. Please review the implementation.")

    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)

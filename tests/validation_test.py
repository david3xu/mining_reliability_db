#!/usr/bin/env python3
"""
Quick validation test to confirm the incident root cause investigation feature is working correctly.
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from dashboard.adapters.data_adapter import get_data_adapter

def test_potential_root_causes():
    """Test that potential root causes query returns proper field mappings and no null values."""
    print("Testing potential root causes feature...")

    adapter = get_data_adapter()

    # Test with a common search term
    search_term = "belt"
    results = adapter.get_potential_root_causes(search_term)

    print(f"\n=== Results for search term: '{search_term}' ===")
    print(f"Number of results: {len(results)}")

    if results:
        print("\n=== First result ===")
        first_result = results[0]

        # Check that all expected fields are present
        expected_fields = ['incident_id', 'facility', 'problem_description', 'proven_solution']

        for field in expected_fields:
            if field in first_result:
                value = first_result[field]
                is_null = value is None or value == "None" or value == ""
                print(f"✅ {field}: {'❌ NULL/EMPTY' if is_null else '✅ HAS VALUE'} - {value}")
            else:
                print(f"❌ {field}: MISSING FIELD")

        # Check for any null values in all results
        null_count = 0
        for result in results:
            for field in expected_fields:
                if result.get(field) is None or result.get(field) == "None" or result.get(field) == "":
                    null_count += 1

        print(f"\n=== Summary ===")
        print(f"Total null/empty values found: {null_count}")
        print(f"Status: {'✅ PASSED' if null_count == 0 else '❌ FAILED'}")

    else:
        print("❌ No results returned")

    return len(results) > 0 and null_count == 0

if __name__ == "__main__":
    try:
        success = test_potential_root_causes()
        print(f"\n🎯 Final Status: {'✅ ALL TESTS PASSED' if success else '❌ TESTS FAILED'}")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        sys.exit(1)

#!/usr/bin/env python3
"""
Final comprehensive validation of the incident root cause investigation feature.
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from dashboard.adapters.data_adapter import get_data_adapter

def test_comprehensive_validation():
    """Test multiple search terms to validate the complete fix."""
    print("🔍 Running comprehensive validation of incident root cause investigation feature...")

    adapter = get_data_adapter()

    test_terms = ["belt", "motor", "vibration", "contamination", "pump"]
    all_passed = True

    for search_term in test_terms:
        print(f"\n--- Testing search term: '{search_term}' ---")

        try:
            results = adapter.get_potential_root_causes([search_term])  # Use list format

            if not results:
                print(f"⚠️  No results for '{search_term}' (may be expected)")
                continue

            print(f"✅ Found {len(results)} results")

            # Validate field structure in first result
            first_result = results[0]
            expected_fields = ['incident_id', 'facility', 'problem_description', 'proven_solution']

            field_validation_passed = True
            for field in expected_fields:
                if field in first_result:
                    value = first_result[field]
                    is_null = value is None or value == "None" or value == ""
                    if is_null:
                        print(f"❌ {field}: NULL/EMPTY")
                        field_validation_passed = False
                        all_passed = False
                    else:
                        print(f"✅ {field}: HAS VALUE")
                else:
                    print(f"❌ {field}: MISSING FIELD")
                    field_validation_passed = False
                    all_passed = False

            # Count total null values across all results
            null_count = 0
            for result in results:
                for field in expected_fields:
                    if result.get(field) is None or result.get(field) == "None" or result.get(field) == "":
                        null_count += 1

            if null_count > 0:
                print(f"❌ Found {null_count} null values across all results")
                all_passed = False
            else:
                print(f"✅ No null values found in any result")

        except Exception as e:
            print(f"❌ Error testing '{search_term}': {e}")
            all_passed = False

    print(f"\n🎯 Final Comprehensive Validation: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    return all_passed

if __name__ == "__main__":
    try:
        success = test_comprehensive_validation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Critical error during validation: {e}")
        sys.exit(1)

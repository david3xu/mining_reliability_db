#!/usr/bin/env python3
"""
Test what fields the query actually returns
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from dashboard.adapters.data_adapter import get_data_adapter

def test_query_fields():
    """Test what fields the query actually returns"""
    print("="*80)
    print("TESTING QUERY FIELD MAPPING")
    print("="*80)

    data_adapter = get_data_adapter()

    # Test the root cause investigation query with some keywords
    keywords = ["contamination", "particles"]

    try:
        results = data_adapter.execute_diagnostic_query("what_could_be_causing_this", keywords)

        print(f"\nQuery executed with keywords: {keywords}")
        print(f"Number of results: {len(results)}")

        if results:
            print("\nFirst result fields:")
            first_result = results[0]
            for key, value in first_result.items():
                print(f"  {key}: {value}")

            print("\nExpected UI fields:")
            print("  incident_id: ✓ present" if 'incident_id' in first_result else "  incident_id: ❌ missing")
            print("  facility: ✓ present" if 'facility' in first_result else "  facility: ❌ missing")
            print("  problem_description: ✓ present" if 'problem_description' in first_result else "  problem_description: ❌ missing (available: similar_symptoms)")
            print("  proven_solution: ✓ present" if 'proven_solution' in first_result else "  proven_solution: ❌ missing (available: identified_root_cause)")
            print("  location: ✓ present" if 'location' in first_result else "  location: ❌ missing (available: facility)")

        else:
            print("❌ No results returned - might be a filtering issue")

    except Exception as e:
        print(f"❌ Error executing query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_query_fields()

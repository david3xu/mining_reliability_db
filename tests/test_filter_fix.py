#!/usr/bin/env python3
"""
Test script to verify the filter fix works correctly
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from dashboard.adapters.data_adapter import get_data_adapter

def test_filter_fix():
    """Test that different keywords now produce different filter clauses"""
    print("="*80)
    print("TESTING FILTER FIX - VERIFYING DIFFERENT KEYWORDS PRODUCE DIFFERENT RESULTS")
    print("="*80)

    data_adapter = get_data_adapter()

    # Test cases with different keywords
    test_cases = [
        ["excavator", "motor", "failed"],  # Mix of predefined terms
        ["contamination", "particles"],    # Non-predefined terms (should now work!)
        ["bearing", "overheating"],        # Mix of component + non-predefined
        ["drill", "maintenance"],          # Completely non-predefined terms
        ["pump", "seal", "replacement"],   # Mix of predefined + non-predefined
    ]

    print("\nTesting build_flexible_keyword_filter():")
    print("-" * 50)

    for i, keywords in enumerate(test_cases, 1):
        print(f"\nTest {i}: {keywords}")
        filter_clause = data_adapter.build_flexible_keyword_filter(keywords)
        print(f"Filter: {filter_clause}")

        # Check that the filter contains the keywords
        for keyword in keywords:
            if keyword.lower() in filter_clause.lower():
                print(f"  ✅ '{keyword}' found in filter")
            else:
                print(f"  ❌ '{keyword}' NOT found in filter")

    print("\n" + "="*80)
    print("FILTER FIX TEST COMPLETED")
    print("="*80)

    # Test comparison: check that different keywords produce different filters
    filter1 = data_adapter.build_flexible_keyword_filter(["excavator", "motor"])
    filter2 = data_adapter.build_flexible_keyword_filter(["contamination", "particles"])
    filter3 = data_adapter.build_flexible_keyword_filter(["drill", "maintenance"])

    print(f"\nComparison Test:")
    print(f"Filter 1 (excavator, motor): {filter1}")
    print(f"Filter 2 (contamination, particles): {filter2}")
    print(f"Filter 3 (drill, maintenance): {filter3}")

    if filter1 != filter2 != filter3:
        print("✅ SUCCESS: Different keywords produce different filters!")
    else:
        print("❌ FAILURE: Filters are still the same!")

    return filter1 != filter2 != filter3

if __name__ == "__main__":
    try:
        success = test_filter_fix()
        if success:
            print("\n🎉 FILTER FIX VERIFIED SUCCESSFUL!")
        else:
            print("\n❌ FILTER FIX FAILED!")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)

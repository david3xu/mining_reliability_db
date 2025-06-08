#!/usr/bin/env python3
"""
Final production validation - comprehensive test of the incident root cause investigation feature
"""
import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.database.db import get_database

def validate_production_ready():
    print("🔍 FINAL PRODUCTION VALIDATION")
    print("=" * 50)

    db = get_database()

    # Load the fixed query
    with open('/home/291928k/uwa/alcoa/mining_reliability_db/configs/queries/potential_root_causes.cypher', 'r') as f:
        query_template = f.read()

    test_cases = [
        "belt",
        "motor",
        "vibration",
        "contamination",
        "pump"
    ]

    total_tested = 0
    total_passed = 0

    for test_term in test_cases:
        print(f"\n📋 Testing search term: '{test_term}'")
        print("-" * 30)

        query = query_template.replace('{filter_clause}',
                                     f"toLower(p.what_happened) CONTAINS toLower('{test_term}')")

        results = db.execute_query(query)
        total_tested += 1

        # Validation checks
        has_results = len(results) > 0
        no_nulls = all(
            record.get('incident_id') is not None and
            record.get('facility') is not None and
            record.get('problem_description') is not None and
            record.get('proven_solution') is not None
            for record in results
        )
        correct_fields = all(
            'incident_id' in record and
            'facility' in record and
            'problem_description' in record and
            'proven_solution' in record and
            'frequency' in record
            for record in results
        )

        # Status check
        if has_results and no_nulls and correct_fields:
            status = "✅ PASS"
            total_passed += 1
        else:
            status = "❌ FAIL"

        print(f"  Results found: {len(results)}")
        print(f"  No null values: {no_nulls}")
        print(f"  Correct fields: {correct_fields}")
        print(f"  Status: {status}")

        # Show sample result
        if results:
            sample = results[0]
            print(f"  Sample incident: {sample.get('incident_id')}")
            print(f"  Sample facility: {sample.get('facility')[:30]}...")

    print(f"\n🎯 FINAL RESULTS")
    print("=" * 50)
    print(f"Tests run: {total_tested}")
    print(f"Tests passed: {total_passed}")
    print(f"Success rate: {100 * total_passed / total_tested:.1f}%")

    if total_passed == total_tested:
        print("\n🚀 PRODUCTION READY! 🚀")
        print("The incident root cause investigation feature is:")
        print("  ✅ Returning correct field mappings")
        print("  ✅ Filtering out null records")
        print("  ✅ Working across multiple search terms")
        print("  ✅ Ready for dashboard integration")
    else:
        print("\n❌ NOT READY - Issues detected")

if __name__ == "__main__":
    validate_production_ready()

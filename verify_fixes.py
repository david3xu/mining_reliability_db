#!/usr/bin/env python3
"""
Simple code verification - check if our fixes are in place
"""

def check_workflow_processor_fixes():
    """Check if the workflow processor has our completion calculation fixes"""

    print("VERIFYING WORKFLOW PROCESSOR FIXES")
    print("=" * 50)

    # Read the workflow processor file
    with open('/home/291928k/uwa/alcoa/mining_reliability_db/mine_core/business/workflow_processor.py', 'r') as f:
        content = f.read()

    # Check for key implementation elements
    checks = [
        ("_calculate_stage_field_completion method", "_calculate_stage_field_completion("),
        ("Backend field-level calculation", "completion_rate = self._calculate_stage_field_completion("),
        ("Frontend ActionRequest fix", "# Use the same field-level completion calculation as _process_workflow_stages for consistency"),
        ("Raw field completion usage", "raw_field_completion_rates = self.calculate_raw_field_completion_rates()"),
        ("Business fields mapping", "business_fields = stage_config.get(\"business_fields\", [])"),
    ]

    all_checks_passed = True

    for check_name, search_string in checks:
        if search_string in content:
            print(f"  ✅ {check_name}: FOUND")
        else:
            print(f"  ❌ {check_name}: NOT FOUND")
            all_checks_passed = False

    print(f"\nOverall status: {'✅ ALL FIXES IN PLACE' if all_checks_passed else '❌ SOME FIXES MISSING'}")

    # Count key method occurrences
    stage_field_completion_count = content.count("_calculate_stage_field_completion(")
    print(f"\n_calculate_stage_field_completion method called {stage_field_completion_count} times")

    return all_checks_passed

if __name__ == "__main__":
    check_workflow_processor_fixes()

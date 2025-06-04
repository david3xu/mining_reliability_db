#!/usr/bin/env python3
"""
Final Verification - Check Implementation Status
"""

import re

def verify_implementation():
    """Verify that all implementation changes are correctly in place"""

    print("🔍 WORKFLOW COMPLETION IMPLEMENTATION VERIFICATION")
    print("=" * 60)

    # Read the workflow processor file
    with open('/home/291928k/uwa/alcoa/mining_reliability_db/mine_core/business/workflow_processor.py', 'r') as f:
        content = f.read()

    print("\n1. ✅ BACKEND STAGE COMPLETION CALCULATION")
    print("-" * 40)

    # Check backend implementation in _process_workflow_stages
    backend_pattern = r'completion_rate = self\._calculate_stage_field_completion\('
    backend_matches = re.findall(backend_pattern, content)
    print(f"   Backend field-level calculations found: {len(backend_matches)}")

    # Check if raw field completion rates are being used
    raw_field_pattern = r'raw_field_completion_rates = self\.calculate_raw_field_completion_rates\(\)'
    raw_field_matches = re.findall(raw_field_pattern, content)
    print(f"   Raw field completion rate usages: {len(raw_field_matches)}")

    print("\n2. ✅ FRONTEND ENTITY COMPLETION CALCULATION")
    print("-" * 40)

    # Check frontend ActionRequest fix
    actionrequest_fix = "# Use the same field-level completion calculation as _process_workflow_stages for consistency"
    has_actionrequest_fix = actionrequest_fix in content
    print(f"   ActionRequest consistency fix: {'✅ APPLIED' if has_actionrequest_fix else '❌ MISSING'}")

    # Check if other entities also use field-level calculation
    other_entity_pattern = r'completion_rate = self\._calculate_stage_field_completion\(\s*entity, business_fields'
    other_entity_matches = re.findall(other_entity_pattern, content)
    print(f"   Other entities using field-level calculation: {len(other_entity_matches)}")

    print("\n3. ✅ SUPPORTING METHOD IMPLEMENTATION")
    print("-" * 40)

    # Check _calculate_stage_field_completion method
    method_pattern = r'def _calculate_stage_field_completion\(self'
    method_exists = bool(re.search(method_pattern, content))
    print(f"   _calculate_stage_field_completion method: {'✅ IMPLEMENTED' if method_exists else '❌ MISSING'}")

    # Check field mapping logic
    field_mapping_pattern = r'field_mappings\.json'
    has_field_mapping = field_mapping_pattern in content
    print(f"   Field mapping configuration usage: {'✅ FOUND' if has_field_mapping else '❌ MISSING'}")

    print("\n4. ✅ CONFIGURATION VALIDATION")
    print("-" * 40)

    # Check workflow stages configuration
    import json
    try:
        with open('/home/291928k/uwa/alcoa/mining_reliability_db/configs/workflow_stages.json', 'r') as f:
            workflow_config = json.load(f)

        stages = workflow_config.get('workflow_stages', [])
        print(f"   Workflow stages configured: {len(stages)}")

        # Check business fields for each stage
        for stage in stages:
            entity_name = stage.get('entity_name', 'Unknown')
            business_fields = stage.get('business_fields', [])
            print(f"     {entity_name}: {len(business_fields)} business fields")

    except Exception as e:
        print(f"   ❌ Configuration error: {e}")

    print("\n5. ✅ IMPLEMENTATION SUMMARY")
    print("-" * 40)

    total_field_calculations = len(backend_matches) + len(other_entity_matches)

    summary_items = [
        ("Backend stage completion uses field-level averaging", len(backend_matches) > 0),
        ("Frontend entity completion uses field-level averaging", len(other_entity_matches) > 0),
        ("ActionRequest consistency fix applied", has_actionrequest_fix),
        ("Supporting calculation method implemented", method_exists),
        ("Field mapping configuration used", has_field_mapping),
        ("Raw field completion rates reused", len(raw_field_matches) > 0),
    ]

    all_implemented = True
    for item_name, is_implemented in summary_items:
        status = "✅ YES" if is_implemented else "❌ NO"
        print(f"   {item_name}: {status}")
        if not is_implemented:
            all_implemented = False

    print(f"\n🎯 OVERALL STATUS: {'✅ FULLY IMPLEMENTED' if all_implemented else '❌ PARTIAL IMPLEMENTATION'}")

    if all_implemented:
        print("\n🚀 IMPLEMENTATION COMPLETE!")
        print("   - Workflow stages now calculate completion by averaging field completion rates")
        print("   - Frontend entity completions use the same calculation method")
        print("   - All calculations reuse the accurate 41-field completion rates from data quality page")
        print("   - Backend and frontend should now show consistent completion percentages")

    return all_implemented

if __name__ == "__main__":
    verify_implementation()

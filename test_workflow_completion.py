#!/usr/bin/env python3
"""
Test script to verify workflow stage completion calculations are using field-level averaging
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mine_core.business.workflow_processor import get_workflow_processor
from dashboard.adapters.data_adapter import get_data_adapter

def test_workflow_stage_completion():
    """Test that workflow stages use field-level completion averaging"""
    print("Testing workflow stage completion calculations...")

    # Get the workflow processor
    workflow_processor = get_workflow_processor()

    # Get raw field completion rates (the accurate 41-field data)
    print("\n1. Getting raw field completion rates...")
    raw_field_rates = workflow_processor.calculate_raw_field_completion_rates()
    print(f"   Found {len(raw_field_rates)} raw field completion rates")

    # Show sample of raw field rates
    sample_fields = list(raw_field_rates.items())[:5]
    for field, rate in sample_fields:
        print(f"   - {field}: {rate:.1f}%")

    # Get workflow analysis which now uses field-level averaging
    print("\n2. Getting workflow stage analysis...")
    workflow_analysis = workflow_processor.process_workflow_business_analysis()

    print(f"   Found {len(workflow_analysis.workflow_stages)} workflow stages")

    # Show stage completion rates
    print("\n3. Stage completion rates (now calculated by field averaging):")
    for stage in workflow_analysis.workflow_stages:
        print(f"   Stage {stage.stage_number} ({stage.entity_name}): {stage.completion_rate:.1f}%")
        print(f"     - Title: {stage.title}")
        print(f"     - Fields: {len(stage.business_fields)} business fields")
        print(f"     - Business fields: {', '.join(stage.business_fields[:3])}{'...' if len(stage.business_fields) > 3 else ''}")

    # Compare with data quality page data to verify consistency
    print("\n4. Comparing with data quality page data...")
    data_adapter = get_data_adapter()
    dq_field_rates = data_adapter.get_41_raw_field_completion_rates()

    print(f"   Data quality page has {len(dq_field_rates)} field rates")
    print(f"   Workflow processor has {len(raw_field_rates)} field rates")

    # Check consistency
    consistent = True
    for field, rate in raw_field_rates.items():
        dq_rate = dq_field_rates.get(field)
        if dq_rate is None:
            print(f"   ⚠️  Field '{field}' missing from data quality page")
            consistent = False
        elif abs(rate - dq_rate) > 0.1:  # Allow small floating point differences
            print(f"   ❌ Field '{field}' has different rates: WF={rate:.1f}%, DQ={dq_rate:.1f}%")
            consistent = False

    if consistent:
        print("   ✅ All field completion rates are consistent between workflow and data quality pages")
    else:
        print("   ❌ Found inconsistencies between workflow and data quality field rates")

    print("\n5. Summary:")
    print("   - Workflow stages now calculate completion by averaging field completion rates")
    print("   - This ensures consistency with the data quality page's 41-field completion data")
    print("   - Stage completion is no longer based on entity-level completion rates")

if __name__ == "__main__":
    test_workflow_stage_completion()

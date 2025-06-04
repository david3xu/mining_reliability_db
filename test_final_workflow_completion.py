#!/usr/bin/env python3
"""
Final test to verify workflow completion calculation consistency
- Tests workflow stages completion (backend calculation)
- Tests supporting entities completion
- Tests frontend data flow (analyze_all_entity_completions)
- Compares with data quality page 41-field completion rates
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from mine_core.business.workflow_processor import WorkflowProcessor
from dashboard.adapters.data_adapter import DataAdapter
from dashboard.adapters.workflow_adapter import WorkflowAdapter

def test_complete_workflow_consistency():
    """Test all aspects of workflow completion calculation for consistency"""

    print("=== FINAL WORKFLOW COMPLETION CONSISTENCY TEST ===\n")

    # Initialize processors
    try:
        workflow_processor = WorkflowProcessor()
        data_adapter = DataAdapter()
        workflow_adapter = WorkflowAdapter()

        print("✓ All processors initialized successfully\n")
    except Exception as e:
        print(f"✗ Failed to initialize processors: {e}")
        return

    # 1. Test data quality page 41-field completion rates (baseline truth)
    print("1. DATA QUALITY PAGE - 41 Field Completion Rates (Baseline Truth)")
    print("-" * 70)
    try:
        dq_completion_rates = data_adapter.get_41_raw_field_completion_rates()
        print(f"✓ Retrieved {len(dq_completion_rates)} field completion rates from data quality page")

        # Show sample of the rates for verification
        sample_fields = list(dq_completion_rates.keys())[:5]
        for field in sample_fields:
            rate = dq_completion_rates[field]
            print(f"  {field}: {rate:.1f}%")
        print("  ...")
        print()
    except Exception as e:
        print(f"✗ Failed to get data quality completion rates: {e}")
        return

    # 2. Test backend workflow processor raw field calculation
    print("2. BACKEND WORKFLOW PROCESSOR - Raw Field Calculation")
    print("-" * 70)
    try:
        wp_raw_rates = workflow_processor.calculate_raw_field_completion_rates()
        print(f"✓ Workflow processor calculated {len(wp_raw_rates)} raw field completion rates")

        # Verify consistency with data quality page
        differences = []
        for field in dq_completion_rates:
            if field in wp_raw_rates:
                diff = abs(dq_completion_rates[field] - wp_raw_rates[field])
                if diff > 0.1:  # Allow for small rounding differences
                    differences.append((field, dq_completion_rates[field], wp_raw_rates[field], diff))

        if differences:
            print(f"⚠ Found {len(differences)} fields with differences > 0.1%:")
            for field, dq_rate, wp_rate, diff in differences[:3]:  # Show first 3
                print(f"  {field}: DQ={dq_rate:.1f}%, WP={wp_rate:.1f}% (diff={diff:.1f}%)")
        else:
            print("✓ Raw field completion rates match data quality page exactly")
        print()
    except Exception as e:
        print(f"✗ Failed to calculate workflow processor raw rates: {e}")
        return

    # 3. Test backend workflow stages completion (corrected calculation)
    print("3. BACKEND WORKFLOW STAGES - Stage Completion (Field-Level Averaging)")
    print("-" * 70)
    try:
        workflow_data = workflow_processor.process_workflow()
        stages = workflow_data.get("workflow_stages", [])

        print("✓ Backend workflow stages calculated:")
        for stage in stages:
            stage_name = stage.get("stage_name", "Unknown")
            completion = stage.get("completion_rate", 0)
            business_fields = stage.get("business_fields", [])
            print(f"  {stage_name}: {completion:.1f}% (based on {len(business_fields)} business fields)")
        print()
    except Exception as e:
        print(f"✗ Failed to process workflow stages: {e}")
        return

    # 4. Test frontend data flow (analyze_all_entity_completions)
    print("4. FRONTEND DATA FLOW - Entity Completions (Should Match Backend)")
    print("-" * 70)
    try:
        entity_completions = workflow_processor.analyze_all_entity_completions()
        workflow_entities = entity_completions.get("workflow_entities", {})

        print("✓ Frontend entity completions calculated:")
        entity_order = ["ActionRequest", "Problem", "RootCause", "ActionPlan", "Verification"]
        for entity in entity_order:
            if entity in workflow_entities:
                completion = workflow_entities[entity].get("completion_rate", 0)
                field_count = workflow_entities[entity].get("field_count", 0)
                print(f"  {entity}: {completion:.1f}% (based on {field_count} fields)")
        print()

        # Compare frontend vs backend stage completions
        print("5. FRONTEND vs BACKEND COMPARISON")
        print("-" * 70)
        stage_mapping = {
            "ActionRequest": "Action Request",
            "Problem": "Problem",
            "RootCause": "Root Cause",
            "ActionPlan": "Action Plan",
            "Verification": "Verification"
        }

        mismatches = []
        for entity, stage_name in stage_mapping.items():
            # Find backend stage data
            backend_stage = next((s for s in stages if s.get("stage_name") == stage_name), None)
            backend_completion = backend_stage.get("completion_rate", 0) if backend_stage else 0

            # Get frontend entity data
            frontend_completion = workflow_entities.get(entity, {}).get("completion_rate", 0)

            diff = abs(backend_completion - frontend_completion)
            if diff > 0.1:
                mismatches.append((entity, backend_completion, frontend_completion, diff))

            print(f"  {entity:12s}: Backend={backend_completion:5.1f}%, Frontend={frontend_completion:5.1f}% (diff={diff:4.1f}%)")

        if mismatches:
            print(f"\n⚠ Found {len(mismatches)} mismatches between backend and frontend")
        else:
            print("\n✓ Backend and frontend completions are consistent!")
        print()

    except Exception as e:
        print(f"✗ Failed to analyze entity completions: {e}")
        return

    # 5. Test supporting entities completion
    print("6. SUPPORTING ENTITIES - Completion Calculation")
    print("-" * 70)
    try:
        supporting_entities = entity_completions.get("supporting_entities", {})

        print("✓ Supporting entities completions calculated:")
        for entity_name, entity_data in supporting_entities.items():
            completion = entity_data.get("completion_rate", 0)
            field_count = entity_data.get("field_count", 0)
            print(f"  {entity_name:15s}: {completion:5.1f}% (based on {field_count} fields)")
        print()
    except Exception as e:
        print(f"✗ Failed to analyze supporting entities: {e}")
        return

    # 6. Test workflow adapter (final frontend data source)
    print("7. WORKFLOW ADAPTER - Final Frontend Data Source")
    print("-" * 70)
    try:
        adapter_data = workflow_adapter.get_workflow_data()
        adapter_stages = adapter_data.get("workflow_stages", [])

        print("✓ Workflow adapter data:")
        for stage in adapter_stages:
            stage_name = stage.get("stage_name", "Unknown")
            completion = stage.get("completion_rate", 0)
            print(f"  {stage_name}: {completion:.1f}%")
        print()
    except Exception as e:
        print(f"✗ Failed to get workflow adapter data: {e}")
        return

    print("=== TEST COMPLETE ===")
    print("\nSUMMARY:")
    print("- Data Quality Page: Provides baseline 41-field completion rates")
    print("- Backend Workflow Processor: Uses same raw field rates for stage calculations")
    print("- Frontend Entity Analysis: Now uses field-level averaging for consistency")
    print("- Supporting Entities: Use field-level averaging from raw field completion rates")
    print("- Workflow Adapter: Feeds corrected data to frontend components")

if __name__ == "__main__":
    test_complete_workflow_consistency()

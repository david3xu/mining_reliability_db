#!/usr/bin/env python3
"""
Quick test to verify workflow completion calculations consistency
"""

import logging
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_workflow_completion_consistency():
    """Test that workflow completion calculations are consistent between backend and frontend"""

    print("=" * 80)
    print("WORKFLOW COMPLETION CONSISTENCY TEST")
    print("=" * 80)

    try:
        # Import the required modules
        from dashboard.adapters.data_adapter import get_data_adapter
        from dashboard.adapters.workflow_adapter import get_workflow_adapter
        from mine_core.business.workflow_processor import get_workflow_processor

        print("\n1. TESTING DATA QUALITY 41-FIELD COMPLETION RATES")
        print("-" * 60)

        # Get data adapter instance
        data_adapter = get_data_adapter()

        # Get 41-field completion rates (baseline from data quality page)
        field_completion_rates = data_adapter.get_41_raw_field_completion_rates()
        print(f"Total raw fields with completion data: {len(field_completion_rates)}")

        # Show first few field completion rates
        field_items = list(field_completion_rates.items())[:5]
        for field_name, completion_rate in field_items:
            print(f"  {field_name}: {completion_rate:.1f}%")
        print("  ...")

        print("\n2. TESTING BACKEND WORKFLOW STAGE COMPLETION")
        print("-" * 60)

        # Get workflow processor instance
        workflow_processor = get_workflow_processor()

        # Get workflow stages data (backend calculation)
        workflow_analysis = workflow_processor.analyze_workflow_completeness()
        workflow_stages = workflow_analysis.get('workflow_stages', [])

        print("Backend workflow stage completion rates:")
        for stage in workflow_stages:
            stage_name = stage.get('stage_name', 'Unknown')
            completion_rate = stage.get('completion_rate', 0.0)
            print(f"  {stage_name}: {completion_rate:.1f}%")

        print("\n3. TESTING FRONTEND ENTITY COMPLETION")
        print("-" * 60)

        # Get entity completions (frontend data path)
        entity_completions = workflow_processor.analyze_all_entity_completions()

        print("Frontend entity completion rates:")
        for entity_name, entity_data in entity_completions.items():
            completion_rate = entity_data.get('completion_rate', 0.0)
            print(f"  {entity_name}: {completion_rate:.1f}%")

        print("\n4. CONSISTENCY CHECK")
        print("-" * 60)

        # Map workflow stages to entity names for comparison
        stage_entity_mapping = {
            'ActionRequest': 'ActionRequest',
            'Problem': 'Problem',
            'RootCause': 'RootCause',
            'ActionPlan': 'ActionPlan',
            'Verification': 'Verification'
        }

        inconsistencies = []

        # Create lookup for backend stages
        backend_stages = {stage.get('stage_name'): stage.get('completion_rate', 0.0) for stage in workflow_stages}

        for stage_name, entity_name in stage_entity_mapping.items():
            backend_rate = backend_stages.get(stage_name, 0.0)
            frontend_rate = entity_completions.get(entity_name, {}).get('completion_rate', 0.0)

            if abs(backend_rate - frontend_rate) > 0.1:  # Allow small rounding differences
                inconsistencies.append({
                    'stage': stage_name,
                    'backend': backend_rate,
                    'frontend': frontend_rate,
                    'difference': abs(backend_rate - frontend_rate)
                })
                print(f"  ❌ {stage_name}: Backend {backend_rate:.1f}% vs Frontend {frontend_rate:.1f}% (diff: {abs(backend_rate - frontend_rate):.1f}%)")
            else:
                print(f"  ✅ {stage_name}: Backend {backend_rate:.1f}% vs Frontend {frontend_rate:.1f}% (consistent)")

        print("\n5. SUMMARY")
        print("-" * 60)

        if inconsistencies:
            print(f"❌ Found {len(inconsistencies)} inconsistencies between backend and frontend calculations")
            print("These stages need alignment:")
            for issue in inconsistencies:
                print(f"  - {issue['stage']}: {issue['difference']:.1f}% difference")
        else:
            print("✅ All workflow stage completions are consistent between backend and frontend!")
            print("✅ Implementation successfully unified completion calculations!")

        return len(inconsistencies) == 0

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_workflow_completion_consistency()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)

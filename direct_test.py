#!/usr/bin/env python3
"""
Direct workflow completion verification
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

print("Starting workflow completion verification...")

try:
    # Import core module
    from mine_core.business.workflow_processor import get_workflow_processor
    print("✅ Successfully imported workflow processor")

    # Get workflow processor instance
    workflow_processor = get_workflow_processor()
    print("✅ Successfully got workflow processor instance")

    # Test workflow analysis
    workflow_analysis = workflow_processor.analyze_workflow_completeness()
    print("✅ Successfully called analyze_workflow_completeness()")

    # Display workflow stages
    workflow_stages = workflow_analysis.get('workflow_stages', [])
    print(f"\nFound {len(workflow_stages)} workflow stages:")

    for stage in workflow_stages:
        stage_name = stage.get('stage_name', 'Unknown')
        completion_rate = stage.get('completion_rate', 0.0)
        print(f"  {stage_name}: {completion_rate:.1f}%")

    # Test entity completions
    entity_completions = workflow_processor.analyze_all_entity_completions()
    print(f"\nFound {len(entity_completions)} entity completions:")

    for entity_name, entity_data in entity_completions.items():
        completion_rate = entity_data.get('completion_rate', 0.0)
        print(f"  {entity_name}: {completion_rate:.1f}%")

    print("\n✅ Workflow completion verification completed successfully!")

except Exception as e:
    print(f"❌ Error during verification: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

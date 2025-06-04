#!/usr/bin/env python3
"""
Minimal test for workflow completion consistency
"""

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.abspath('.'))

    try:
        from mine_core.business.workflow_processor import get_workflow_processor

        workflow_processor = get_workflow_processor()

        # Backend workflow stages
        print("BACKEND WORKFLOW STAGES:")
        workflow_analysis = workflow_processor.analyze_workflow_completeness()
        workflow_stages = workflow_analysis.get('workflow_stages', [])
        backend_rates = {}
        for stage in workflow_stages:
            stage_name = stage.get('stage_name', 'Unknown')
            completion_rate = stage.get('completion_rate', 0.0)
            backend_rates[stage_name] = completion_rate
            print(f"  {stage_name}: {completion_rate:.1f}%")

        # Frontend entity completions
        print("\nFRONTEND ENTITY COMPLETIONS:")
        entity_completions = workflow_processor.analyze_all_entity_completions()
        frontend_rates = {}
        workflow_entities = ['ActionRequest', 'Problem', 'RootCause', 'ActionPlan', 'Verification']
        for entity_name in workflow_entities:
            entity_data = entity_completions.get(entity_name, {})
            completion_rate = entity_data.get('completion_rate', 0.0)
            frontend_rates[entity_name] = completion_rate
            print(f"  {entity_name}: {completion_rate:.1f}%")

        # Consistency check
        print("\nCONSISTENCY CHECK:")
        stage_entity_mapping = {
            'ActionRequest': 'ActionRequest',
            'Problem': 'Problem',
            'RootCause': 'RootCause',
            'ActionPlan': 'ActionPlan',
            'Verification': 'Verification'
        }

        all_consistent = True
        for stage_name, entity_name in stage_entity_mapping.items():
            backend_rate = backend_rates.get(stage_name, 0.0)
            frontend_rate = frontend_rates.get(entity_name, 0.0)

            if abs(backend_rate - frontend_rate) > 0.1:
                print(f"  ❌ {stage_name}: Backend {backend_rate:.1f}% vs Frontend {frontend_rate:.1f}%")
                all_consistent = False
            else:
                print(f"  ✅ {stage_name}: {backend_rate:.1f}% (consistent)")

        if all_consistent:
            print("\n✅ ALL COMPLETION RATES ARE CONSISTENT!")
        else:
            print("\n❌ INCONSISTENCIES FOUND")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

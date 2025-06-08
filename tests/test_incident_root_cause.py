#!/usr/bin/env python3
"""
Test script for the new symptom-based filtering and diagnostic methods
Tests the incident root cause investigation functionality
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from dashboard.adapters.data_adapter import get_data_adapter

def test_symptom_classification():
    """Test symptom classification functionality"""
    print("="*60)
    print("TESTING SYMPTOM CLASSIFICATION")
    print("="*60)

    data_adapter = get_data_adapter()

    # Test cases with different symptom descriptions
    test_cases = [
        "excavator motor failed with contamination",
        "pump leak causing vibration in hydraulic system",
        "conveyor belt noise and wear detected",
        "crusher bearing contamination and failure"
    ]

    for test_case in test_cases:
        print(f"\nTesting: '{test_case}'")
        classification = data_adapter.classify_incident_symptoms(test_case)
        print(f"  Equipment matches: {classification['equipment_matches']}")
        print(f"  Symptom matches: {classification['symptom_matches']}")
        print(f"  Component matches: {classification['component_matches']}")
        print(f"  Classification score: {classification['classification_score']}")


def test_symptom_based_filter():
    """Test symptom-based filter building"""
    print("\n" + "="*60)
    print("TESTING SYMPTOM-BASED FILTER BUILDING")
    print("="*60)

    data_adapter = get_data_adapter()

    test_keywords = [
        ["excavator", "motor", "contamination"],
        ["pump", "leak"],
        ["bearing", "failed"],
        ["hydraulic", "vibration"]
    ]

    for keywords in test_keywords:
        print(f"\nTesting keywords: {keywords}")
        filter_clause = data_adapter.build_symptom_based_filter(keywords)
        print(f"  Generated filter: {filter_clause}")


def test_diagnostic_queries():
    """Test diagnostic query execution"""
    print("\n" + "="*60)
    print("TESTING DIAGNOSTIC QUERIES")
    print("="*60)

    data_adapter = get_data_adapter()

    # Test with excavator motor contamination scenario
    test_keywords = ["excavator", "motor", "contamination"]
    print(f"Testing diagnostic queries with keywords: {test_keywords}")

    # Test potential root causes
    print("\n1. Testing potential root causes...")
    try:
        root_causes = data_adapter.get_potential_root_causes(test_keywords)
        print(f"   Found {len(root_causes)} potential root causes")
        if root_causes:
            for i, cause in enumerate(root_causes[:3]):  # Show first 3
                print(f"   {i+1}. {cause.get('identified_root_cause', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test investigation approaches
    print("\n2. Testing investigation approaches...")
    try:
        approaches = data_adapter.get_investigation_approaches(test_keywords)
        print(f"   Found {len(approaches)} investigation approaches")
        if approaches:
            for i, approach in enumerate(approaches[:3]):  # Show first 3
                print(f"   {i+1}. {approach.get('investigation_approach', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test diagnostic experts
    print("\n3. Testing diagnostic experts...")
    try:
        experts = data_adapter.get_diagnostic_experts(test_keywords)
        print(f"   Found {len(experts)} expert departments")
        if experts:
            for i, expert in enumerate(experts[:3]):  # Show first 3
                print(f"   {i+1}. {expert.get('initiating_department', 'N/A')} ({expert.get('diagnostic_success_rate', 'N/A')}% success)")
    except Exception as e:
        print(f"   Error: {e}")

    # Test prioritized steps
    print("\n4. Testing prioritized investigation steps...")
    try:
        steps = data_adapter.get_prioritized_investigation_steps(test_keywords)
        print(f"   Found {len(steps)} prioritized steps")
        if steps:
            for i, step in enumerate(steps[:3]):  # Show first 3
                print(f"   {i+1}. {step.get('investigation_step', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")


def test_comprehensive_investigation():
    """Test comprehensive incident investigation"""
    print("\n" + "="*60)
    print("TESTING COMPREHENSIVE INCIDENT INVESTIGATION")
    print("="*60)

    data_adapter = get_data_adapter()

    # Test comprehensive investigation
    incident_description = "Excavator motor failure with contamination detected in hydraulic system"
    incident_keywords = ["excavator", "motor", "contamination", "hydraulic"]

    print(f"Testing comprehensive investigation:")
    print(f"  Description: {incident_description}")
    print(f"  Keywords: {incident_keywords}")

    try:
        investigation = data_adapter.execute_comprehensive_incident_investigation(
            incident_description, incident_keywords
        )

        summary = investigation.get('investigation_summary', {})
        print(f"\nInvestigation Summary:")
        print(f"  Classification score: {summary.get('classification_score', 0)}")
        print(f"  Root causes found: {summary.get('total_root_causes_found', 0)}")
        print(f"  Approaches found: {summary.get('total_approaches_found', 0)}")
        print(f"  Experts found: {summary.get('total_experts_found', 0)}")
        print(f"  Steps found: {summary.get('total_steps_found', 0)}")

        if 'error' in summary:
            print(f"  Error: {summary['error']}")

    except Exception as e:
        print(f"   Error in comprehensive investigation: {e}")


if __name__ == "__main__":
    print("Testing Incident Root Cause Investigation Functionality")
    print("Current working directory:", os.getcwd())

    try:
        test_symptom_classification()
        test_symptom_based_filter()
        test_diagnostic_queries()
        test_comprehensive_investigation()

        print("\n" + "="*60)
        print("ALL TESTS COMPLETED")
        print("="*60)

    except Exception as e:
        print(f"Test execution failed: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
"""
Test script to verify JSON recording functionality
"""

import sys
import os
sys.path.append('/home/291928k/uwa/alcoa/mining_reliability_db')

from utils.json_recorder import JSONRecorder

def test_json_recording():
    """Test the JSON recording functionality"""

    # Create JSONRecorder instance
    json_recorder = JSONRecorder()

    # Sample search data (simulating what comes from the intelligence engine)
    sample_search_data = {
        "direct_matches": [
            {
                "incident_id": "INC001",
                "facility": "Mine Site A",
                "problem_description": "Excavator motor contamination",
                "root_cause": "Oil seal failure",
                "solution": "Replace oil seals and flush system"
            }
        ],
        "equipment_patterns": [
            {
                "equipment_type": "Excavator",
                "failure_pattern": "Motor contamination",
                "frequency": 5
            }
        ],
        "causal_chains": [],
        "cross_facility_patterns": [],
        "temporal_patterns": [],
        "recurring_sequences": [],
        "solution_effectiveness": [],
        "equipment_clusters": [],
        "search_coverage": 2
    }

    # Save search results
    try:
        filepath = json_recorder.save_search_results(
            search_term="excavator motor contamination",
            search_data=sample_search_data,
            metadata={
                "search_type": "test_search",
                "test_run": True
            }
        )

        print(f"✅ JSON recording successful!")
        print(f"📁 File saved to: {filepath}")

        # Load and verify the saved data
        loaded_data = json_recorder.load_search_results(filepath)
        print(f"🔍 Data verification: {len(loaded_data)} top-level keys found")
        print(f"📊 Search term: {loaded_data['search_metadata']['search_term']}")
        print(f"📈 Total results: {loaded_data['statistics']['total_results']}")

        return True

    except Exception as e:
        print(f"❌ JSON recording failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing JSON Recording System...")
    success = test_json_recording()
    if success:
        print("\n✅ JSON recording system is working correctly!")
    else:
        print("\n❌ JSON recording system test failed!")

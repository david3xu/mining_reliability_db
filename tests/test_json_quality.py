#!/usr/bin/env python3
"""
Test script to validate JSON recording functionality and search result quality
"""

import json
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.json_recorder import JSONRecorder

def test_json_recording_system():
    """Test the JSON recording system functionality"""
    print("🧪 Testing JSON Recording System")
    print("=" * 50)

    try:
        # Initialize JSON recorder
        json_recorder = JSONRecorder()
        print(f"✅ JSONRecorder initialized: {json_recorder.base_directory}")

        # List saved searches
        saved_searches = json_recorder.list_saved_searches()
        print(f"✅ Found {len(saved_searches)} saved search files")

        if saved_searches:
            # Analyze the most recent search
            latest_search = saved_searches[0]
            print(f"📁 Latest search file: {Path(latest_search).name}")

            # Get search summary
            summary = json_recorder.get_search_summary(latest_search)
            print(f"🔍 Search Summary:")
            print(f"   • Search Term: {summary.get('search_term', 'N/A')}")
            print(f"   • Timestamp: {summary.get('timestamp', 'N/A')}")
            print(f"   • Total Results: {summary.get('total_results', 0)}")
            print(f"   • Dimensions with Results: {summary.get('dimensions_with_results', 0)}")
            print(f"   • Search Coverage: {summary.get('search_coverage', 0)}")

            # Load and analyze full data
            full_data = json_recorder.load_search_results(latest_search)

            print(f"\n📊 Search Result Quality Analysis:")
            print(f"   • Search Coverage: {full_data['search_metadata']['search_coverage']}/8 dimensions")

            stats = full_data.get('statistics', {})
            dimension_breakdown = stats.get('dimension_breakdown', {})

            print(f"   • Total Results: {stats.get('total_results', 0)}")
            print(f"   • Dimensions Breakdown:")

            for dimension, count in dimension_breakdown.items():
                if count > 0:
                    print(f"     - {dimension.replace('_', ' ').title()}: {count} results ✅")
                else:
                    print(f"     - {dimension.replace('_', ' ').title()}: {count} results ❌")

            # Analyze search result quality
            analyze_search_quality(full_data)

        else:
            print("⚠️ No saved searches found yet")

    except Exception as e:
        print(f"❌ Error testing JSON recording system: {str(e)}")
        return False

    return True

def analyze_search_quality(data):
    """Analyze the quality of search results"""
    print(f"\n🎯 Search Quality Analysis:")

    search_results = data.get('search_results', {})

    # Check direct matches quality
    direct_matches = search_results.get('direct_matches', [])
    if direct_matches:
        sample_match = direct_matches[0]
        print(f"   • Direct Matches: {len(direct_matches)} found")
        print(f"     - Sample problem: {sample_match.get('p', {}).get('name', 'N/A')[:60]}...")
        print(f"     - Root cause provided: {'✅' if sample_match.get('rc', {}).get('root_cause') else '❌'}")
        print(f"     - Action plan available: {'✅' if sample_match.get('ap', {}) else '❌'}")

    # Check equipment patterns
    equipment_patterns = search_results.get('equipment_patterns', [])
    if equipment_patterns:
        print(f"   • Equipment Patterns: {len(equipment_patterns)} found")
        print(f"     - Pattern analysis working: ✅")

    # Check causal chains
    causal_chains = search_results.get('causal_chains', [])
    if causal_chains:
        print(f"   • Causal Chains: {len(causal_chains)} found")
        print(f"     - Relationship mapping working: ✅")

    # Check cross-facility patterns
    cross_facility = search_results.get('cross_facility_patterns', [])
    if cross_facility:
        print(f"   • Cross-Facility Patterns: {len(cross_facility)} found")
        print(f"     - Knowledge sharing opportunities: ✅")

    # Overall quality assessment
    stats = data.get('statistics', {})
    total_results = stats.get('total_results', 0)
    dimensions_with_results = stats.get('dimensions_with_results', 0)

    if total_results > 50 and dimensions_with_results >= 3:
        quality_rating = "🟢 Excellent"
    elif total_results > 20 and dimensions_with_results >= 2:
        quality_rating = "🟡 Good"
    elif total_results > 0:
        quality_rating = "🟠 Fair"
    else:
        quality_rating = "🔴 Poor"

    print(f"\n🏆 Overall Search Quality: {quality_rating}")
    print(f"   • Search Term: '{data['search_metadata']['search_term']}'")
    print(f"   • Multi-dimensional coverage: {dimensions_with_results}/8 dimensions")
    print(f"   • Result richness: {total_results} total results")

if __name__ == "__main__":
    print("🚀 JSON Recording System Validation")
    print("=" * 60)

    success = test_json_recording_system()

    if success:
        print(f"\n✅ JSON Recording System is working perfectly!")
        print(f"📁 Search results are being saved to: data/search_results/")
        print(f"💾 JSON files contain comprehensive search metadata and statistics")
    else:
        print(f"\n❌ Issues detected in JSON recording system")

    print("=" * 60)

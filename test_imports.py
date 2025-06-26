#!/usr/bin/env python3
"""Test script to validate imports after cleanup"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import(module_path, items):
    """Test importing specific items from a module"""
    try:
        module = __import__(module_path, fromlist=items)
        for item in items:
            getattr(module, item)
        print(f"✓ {module_path}: {', '.join(items)}")
        return True
    except Exception as e:
        print(f"✗ {module_path}: {e}")
        return False

def main():
    """Run all import tests"""
    print("Testing imports after search-algorithms-only cleanup...")
    print("=" * 60)

    success_count = 0
    total_count = 0

    # Test core search components
    total_count += 1
    if test_import('dashboard.components', ['create_graph_search_layout']):
        success_count += 1

    total_count += 1
    if test_import('dashboard.components', ['create_cypher_search_layout']):
        success_count += 1

    total_count += 1
    if test_import('dashboard.components', ['create_standard_layout']):
        success_count += 1

    # Test mine_core modules
    total_count += 1
    if test_import('mine_core.analytics.pattern_discovery', ['PatternDiscoveryEngine']):
        success_count += 1

    total_count += 1
    if test_import('mine_core.analytics.workflow_analyzer', ['WorkflowAnalyzer']):
        success_count += 1

    # Test configs
    total_count += 1
    if test_import('configs.environment', ['Config']):
        success_count += 1

    total_count += 1
    if test_import('configs.system_constants', ['SystemConstants']):
        success_count += 1

    # Test utilities
    total_count += 1
    if test_import('utils.json_recorder', ['JSONRecorder']):
        success_count += 1

    total_count += 1
    if test_import('mine_core.shared.common', ['safe_get_nested_value']):
        success_count += 1

    total_count += 1
    if test_import('mine_core.helpers.log_manager', ['LogManager']):
        success_count += 1

    print("=" * 60)
    print(f"Import test results: {success_count}/{total_count} successful")

    if success_count == total_count:
        print("🎉 All imports working correctly!")
        return 0
    else:
        print("⚠️  Some imports failed - see details above")
        return 1

if __name__ == "__main__":
    sys.exit(main())

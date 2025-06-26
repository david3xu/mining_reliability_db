#!/usr/bin/env python3
"""
Quick validation test for search-algorithms-only branch
"""

import sys
import traceback

def test_import(desc, module_path, items):
    """Test importing items from a module"""
    try:
        module = __import__(module_path, fromlist=items)
        for item in items:
            getattr(module, item)
        print(f"✅ {desc}: OK")
        return True
    except Exception as e:
        print(f"❌ {desc}: {e}")
        return False

def test_function_call(desc, func):
    """Test calling a function"""
    try:
        result = func()
        print(f"✅ {desc}: OK")
        return True
    except Exception as e:
        print(f"❌ {desc}: {e}")
        return False

def main():
    print("🔍 Quick Search Branch Validation")
    print("=" * 50)

    tests_passed = 0
    total_tests = 0

    # Test 1: Core imports
    total_tests += 1
    if test_import("Analytics imports", "mine_core.analytics", ["PatternDiscovery", "WorkflowAnalyzer"]):
        tests_passed += 1

    # Test 2: Data adapter
    total_tests += 1
    if test_import("Data adapter", "dashboard.adapters", ["get_data_adapter"]):
        tests_passed += 1

    # Test 3: Config adapter
    total_tests += 1
    if test_import("Config adapter", "dashboard.adapters", ["get_config_adapter"]):
        tests_passed += 1

    # Test 4: Component imports (without callbacks)
    total_tests += 1
    try:
        # Import module but don't instantiate components (they may have callbacks)
        import dashboard.components.graph_search
        import dashboard.components.cypher_search
        import dashboard.components.layout_template
        print("✅ Component modules: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Component modules: {e}")

    # Test 5: App creation (basic test)
    total_tests += 1
    try:
        from dashboard.app import create_app
        # Don't actually create the app as it may start dash server
        print("✅ App import: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ App import: {e}")

    # Test 6: Essential utilities
    total_tests += 1
    if test_import("Utilities", "utils.json_recorder", ["JSONRecorder"]):
        tests_passed += 1

    # Test 7: Config loading
    total_tests += 1
    def test_config():
        from configs.environment import get_schema, get_graph_search_config
        schema = get_schema()
        config = get_graph_search_config()
        return schema is not None and config is not None

    if test_function_call("Config loading", test_config):
        tests_passed += 1

    print("=" * 50)
    print(f"📊 Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 All tests passed! Search branch is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. See details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

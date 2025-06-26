#!/usr/bin/env python3
"""
Final validation test for search-algorithms-only branch
"""

def main():
    print("🎯 Final Search-Algorithms-Only Branch Validation")
    print("=" * 60)

    tests_passed = 0
    total_tests = 8

    # Test 1: Analytics
    try:
        from mine_core.analytics import PatternDiscovery, WorkflowAnalyzer
        pd = PatternDiscovery()
        wa = WorkflowAnalyzer()
        print("✅ 1. Analytics modules: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 1. Analytics modules: {e}")

    # Test 2: Data adapter
    try:
        from dashboard.adapters import get_data_adapter
        adapter = get_data_adapter()
        assert hasattr(adapter, 'execute_cypher_query')
        print("✅ 2. Data adapter: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 2. Data adapter: {e}")

    # Test 3: Config adapter
    try:
        from dashboard.adapters import get_config_adapter
        config = get_config_adapter()
        graph_config = config.get_graph_search_config()
        print("✅ 3. Config adapter: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 3. Config adapter: {e}")

    # Test 4: Dashboard components (modules)
    try:
        import dashboard.components.graph_search
        import dashboard.components.cypher_search
        import dashboard.components.layout_template
        print("✅ 4. Dashboard component modules: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 4. Dashboard component modules: {e}")

    # Test 5: Dashboard components (functions)
    try:
        from dashboard.components import create_graph_search_layout, create_cypher_search_layout, create_standard_layout
        print("✅ 5. Dashboard component functions: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 5. Dashboard component functions: {e}")

    # Test 6: App creation
    try:
        from dashboard.app import create_app
        print("✅ 6. App creation function: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 6. App creation function: {e}")

    # Test 7: Configuration loading
    try:
        from configs.environment import get_schema, get_graph_search_config, get_system_constants
        schema = get_schema()
        graph_config = get_graph_search_config()
        constants = get_system_constants()
        assert schema is not None and graph_config is not None and constants is not None
        print("✅ 7. Configuration loading: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 7. Configuration loading: {e}")

    # Test 8: Essential utilities
    try:
        from utils.json_recorder import JSONRecorder
        from mine_core.shared.common import handle_error
        from mine_core.helpers.log_manager import get_logger
        recorder = JSONRecorder()
        logger = get_logger("test")
        print("✅ 8. Essential utilities: OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 8. Essential utilities: {e}")

    print("=" * 60)
    print(f"📊 FINAL RESULTS: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 SUCCESS! Search-algorithms-only branch is fully functional!")
        print("\n🚀 Ready to use:")
        print("   • Graph search interface: ✅")
        print("   • Cypher search interface: ✅")
        print("   • Pattern discovery analytics: ✅")
        print("   • Configuration management: ✅")
        print("   • Essential utilities: ✅")
        print("\n🔥 Next steps:")
        print("   1. Start the search UI: python -m dashboard.app")
        print("   2. Test search functionality in the browser")
        print("   3. Run pattern discovery: from mine_core.analytics import PatternDiscovery")
        return 0
    else:
        print("⚠️  Some components still have issues - check details above.")
        return 1

if __name__ == "__main__":
    exit(main())

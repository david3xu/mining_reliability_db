#!/usr/bin/env python3
"""End-to-end validation test for search-algorithms-only branch"""

import sys
import traceback

def test_section(name, test_func):
    """Run a test section with error handling"""
    print(f"\n🧪 Testing {name}...")
    try:
        test_func()
        print(f"✅ {name}: PASSED")
        return True
    except Exception as e:
        print(f"❌ {name}: FAILED - {e}")
        traceback.print_exc()
        return False

def test_dashboard_components():
    """Test dashboard search components"""
    from dashboard.components import create_graph_search_layout, create_cypher_search_layout, create_standard_layout
    # Try to instantiate the layouts
    layout1 = create_graph_search_layout()
    layout2 = create_cypher_search_layout()
    layout3 = create_standard_layout("Test", [])
    print("   - Graph search layout created")
    print("   - Cypher search layout created")
    print("   - Standard layout created")

def test_analytics():
    """Test analytics modules"""
    from mine_core.analytics import PatternDiscovery, WorkflowAnalyzer
    # Try to instantiate the classes
    pd = PatternDiscovery()
    wa = WorkflowAnalyzer()
    print("   - PatternDiscovery instantiated")
    print("   - WorkflowAnalyzer instantiated")

def test_data_adapter():
    """Test data adapter"""
    from dashboard.adapters import get_data_adapter
    adapter = get_data_adapter()
    print("   - DataAdapter instantiated")
    # Check if required methods exist
    assert hasattr(adapter, 'execute_cypher_query'), "Missing execute_cypher_query method"
    print("   - execute_cypher_query method available")

def test_config_adapter():
    """Test config adapter"""
    from dashboard.adapters import get_config_adapter
    config = get_config_adapter()
    print("   - ConfigAdapter instantiated")
    # Try to get some basic config
    graph_config = config.get_graph_search_config()
    system_constants = config.get_system_constants()
    print("   - Graph search config loaded")
    print("   - System constants loaded")

def test_configurations():
    """Test configuration loading"""
    from configs.environment import get_schema, get_graph_search_config, get_system_constants
    schema = get_schema()
    graph_config = get_graph_search_config()
    constants = get_system_constants()
    print("   - Model schema loaded")
    print("   - Graph search config loaded")
    print("   - System constants loaded")

def test_utilities():
    """Test essential utilities"""
    from utils.json_recorder import JSONRecorder
    from mine_core.shared.common import handle_error
    from mine_core.helpers.log_manager import get_logger

    recorder = JSONRecorder()
    logger = get_logger("test")
    print("   - JSONRecorder instantiated")
    print("   - Logger created")
    print("   - Common utilities available")

def main():
    """Run all validation tests"""
    print("🚀 Search-Algorithms-Only Branch - End-to-End Validation")
    print("=" * 60)

    tests = [
        ("Dashboard Components", test_dashboard_components),
        ("Analytics Modules", test_analytics),
        ("Data Adapter", test_data_adapter),
        ("Config Adapter", test_config_adapter),
        ("Configuration Loading", test_configurations),
        ("Essential Utilities", test_utilities),
    ]

    passed = 0
    total = len(tests)

    for name, test_func in tests:
        if test_section(name, test_func):
            passed += 1

    print("\n" + "=" * 60)
    print(f"📊 VALIDATION RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Search-algorithms-only branch is ready to use!")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

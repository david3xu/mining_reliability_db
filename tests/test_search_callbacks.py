#!/usr/bin/env python3
"""
Test script to verify search callback functionality
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


def test_search_functionality():
    """Test the search functionality directly"""
    try:
        from dashboard.adapters import get_data_adapter

        print("🔍 Testing search functionality...")

        # Get adapter
        adapter = get_data_adapter()
        print("✅ Data adapter initialized")

        # Test search
        search_term = "pump"
        results = adapter.search_problems_and_causes(search_term)
        print(f"✅ Search executed for '{search_term}'")
        print(f"📊 Found {len(results)} results")

        if results:
            print("📝 Sample result:")
            sample = results[0]
            for key, value in sample.items():
                print(f"   {key}: {str(value)[:50]}...")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_component_loading():
    """Test component loading"""
    try:
        print("\n🧩 Testing component loading...")

        from dashboard.components.incident_search import create_incident_search_layout

        layout = create_incident_search_layout()
        print("✅ Incident search layout created")

        # Check if layout has the required elements
        if hasattr(layout, "children"):
            print("✅ Layout has children")

        return True

    except Exception as e:
        print(f"❌ Component loading error: {e}")
        return False


def test_callback_imports():
    """Test callback imports"""
    try:
        print("\n🔄 Testing callback imports...")

        # Import the module to register callbacks
        import dashboard.components.incident_search

        print("✅ Incident search module imported (callbacks should be registered)")

        return True

    except Exception as e:
        print(f"❌ Callback import error: {e}")
        return False


if __name__ == "__main__":
    print("🧪 SEARCH FUNCTIONALITY TEST")
    print("=" * 50)

    # Run tests
    test1 = test_search_functionality()
    test2 = test_component_loading()
    test3 = test_callback_imports()

    print("\n📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Search functionality: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Component loading: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Callback imports: {'✅ PASS' if test3 else '❌ FAIL'}")

    if all([test1, test2, test3]):
        print("\n🎉 All tests passed! Search should work in web interface.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

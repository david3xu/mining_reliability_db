#!/usr/bin/env python3
"""
Debug script specifically for the Solutions Table issue.
"""
import sys
sys.path.append("/home/291928k/uwa/alcoa/mining_reliability_db")

from dashboard.adapters.data_adapter import get_data_adapter
from dashboard.components.stakeholder_essentials import create_solutions_table

def debug_solutions_table():
    print("🔧 DEBUGGING SOLUTIONS TABLE")
    print("=" * 50)

    # Initialize adapter
    adapter = get_data_adapter()

    # Execute stakeholder journey to get raw data
    search_input = "emergency shutdown"
    print(f"📝 Running stakeholder journey for: '{search_input}'")

    results = adapter.execute_complete_stakeholder_journey(search_input)
    print(f"🚀 Total results: {len(results)}")

    # Get solutions data specifically
    solutions_section = results.get("how_do_i_fix_it", {})
    solutions_data = solutions_section.get("results", [])
    print(f"🎯 Solutions data records: {len(solutions_data)}")

    # Print the section structure first
    print(f"📊 Solutions section structure: {list(solutions_section.keys())}")

    # Print first few records for analysis
    print("\n📊 Raw Solutions Data Sample:")
    if solutions_data:
        for i, record in enumerate(solutions_data[:3]):
            print(f"Record {i+1}:")
            for key, value in record.items():
                print(f"  {key}: {value}")
            print()
    else:
        print("No solutions data found")

    # Test the create_solutions_table function
    print("🏗️ Testing create_solutions_table function...")
    try:
        table_component = create_solutions_table(solutions_data)
        print("✅ Table component created successfully")

        # Check table structure
        if hasattr(table_component, 'children'):
            print(f"📋 Table has children: {len(table_component.children)}")

            # Check for headers
            thead = table_component.children[0] if table_component.children else None
            if thead and hasattr(thead, 'children'):
                tr = thead.children[0] if thead.children else None
                if tr and hasattr(tr, 'children'):
                    headers = [th.children for th in tr.children if hasattr(th, 'children')]
                    print(f"📋 Headers found: {headers}")
                else:
                    print("❌ No TR found in thead")
            else:
                print("❌ No thead found")
        else:
            print("❌ Table component has no children")

    except Exception as e:
        print(f"❌ Error creating table: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_solutions_table()

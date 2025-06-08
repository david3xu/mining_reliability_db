#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from dashboard.adapters.data_adapter import get_data_adapter
from dashboard.components.stakeholder_essentials import (
    create_why_table,
    create_investigation_table,
    create_experts_table,
    create_checklist_table,
    create_solutions_table
)

def test_stakeholder_tables():
    """Test all stakeholder journey tables with Action Request and Facility columns"""
    print("🔬 Testing Stakeholder Journey Tables with Action Request & Facility Columns")
    print("=" * 80)

    # Get data adapter
    adapter = get_data_adapter()

    # Test user input for journey
    user_input = "conveyor belt failure"
    print(f"📝 Testing with input: '{user_input}'")
    print()

    try:
        # Execute complete stakeholder journey to get all data
        print("🚀 Executing complete stakeholder journey...")
        journey_data = adapter.execute_complete_stakeholder_journey(user_input)

        if not journey_data.get("metadata", {}).get("success", False):
            print(f"❌ Journey execution failed: {journey_data.get('metadata', {}).get('error', 'Unknown error')}")
            return

        print(f"✅ Journey completed with {journey_data.get('metadata', {}).get('total_results', 0)} total results")
        print()

        # Test each table function with corresponding journey data
        tables_to_test = [
            ("Why Table", create_why_table, "why_did_this_happen"),
            ("Investigation Table", create_investigation_table, "how_do_i_figure_out_whats_wrong"),
            ("Experts Table", create_experts_table, "who_can_help_me"),
            ("Checklist Table", create_checklist_table, "what_should_i_check_first"),
            ("Solutions Table", create_solutions_table, "how_do_i_fix_it")
        ]

        for table_name, table_func, journey_key in tables_to_test:
            print(f"🔍 Testing {table_name}")
            print("-" * 50)

            try:
                # Get data from journey results
                section_data = journey_data.get(journey_key, {})
                data = section_data.get("results", [])

                print(f"✅ Data retrieved: {len(data) if data else 0} records")

                if data:
                    print(f"📄 Sample record keys: {list(data[0].keys()) if data else 'No data'}")

                # Create table
                table_html = table_func(data)

                # Extract and show headers
                if 'thead' in table_html:
                    start = table_html.find('<thead')
                    end = table_html.find('</thead>') + 8
                    headers_section = table_html[start:end]
                    print(f"📋 Headers section found")

                    # Check for Action Request and Facility in first two columns
                    if 'Action Request' in headers_section and 'Facility' in headers_section:
                        print("✅ Action Request and Facility columns found!")
                    else:
                        print("❌ Missing Action Request or Facility columns")
                        print(f"Headers content: {headers_section[:200]}...")
                else:
                    print("❌ No headers found in table")

                # Show a sample of the table rows if data exists
                if data and 'tbody' in table_html:
                    tbody_start = table_html.find('<tbody')
                    tbody_end = table_html.find('</tbody>') + 8
                    if tbody_start != -1 and tbody_end != -1:
                        tbody_content = table_html[tbody_start:tbody_end]
                        print(f"📊 Table body preview: {tbody_content[:300]}...")

            except Exception as e:
                print(f"❌ Error testing {table_name}: {e}")
                import traceback
                traceback.print_exc()

            print()

    except Exception as e:
        print(f"❌ Error executing stakeholder journey: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_stakeholder_tables()

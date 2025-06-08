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

def validate_table_headers(table_component):
    """Validate that table has Action Request and Facility as first two columns"""
    try:
        if hasattr(table_component, 'children') and table_component.children:
            # Find thead
            for child in table_component.children:
                if hasattr(child, 'children') and child.children:
                    # Check thead children for headers
                    if hasattr(child.children[0], 'children'):
                        headers = [th.children for th in child.children[0].children if hasattr(th, 'children')]
                        if headers and len(headers) >= 2:
                            if headers[0] == 'Action Request' and headers[1] == 'Facility':
                                return True, headers
                            else:
                                return False, headers
        return False, []
    except Exception as e:
        return False, f"Error: {e}"

def final_validation():
    """Final validation of Action Request and Facility column implementation"""
    print("🏁 FINAL VALIDATION: Action Request & Facility Columns Implementation")
    print("=" * 80)

    # Get data adapter
    adapter = get_data_adapter()

    # Test user input for journey
    user_input = "emergency shutdown"
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

        validation_results = []

        for table_name, table_func, journey_key in tables_to_test:
            print(f"🔍 Validating {table_name}")
            print("-" * 50)

            try:
                # Get data from journey results
                section_data = journey_data.get(journey_key, {})
                data = section_data.get("results", [])

                print(f"📊 Records retrieved: {len(data) if data else 0}")

                if data:
                    # Check for records with actual data
                    non_null_records = [r for r in data if any(v is not None and str(v).strip() != '' for v in r.values())]
                    print(f"📄 Records with data: {len(non_null_records)}")

                    # Create table
                    table_component = table_func(data)

                    # Validate headers
                    is_valid, headers = validate_table_headers(table_component)

                    if is_valid:
                        print("✅ SUCCESS: Action Request and Facility are first two columns!")
                        print(f"📋 Full headers: {headers}")
                        validation_results.append((table_name, True, headers))
                    else:
                        print("❌ FAILED: Action Request and Facility columns missing or incorrect")
                        print(f"📋 Actual headers: {headers}")
                        validation_results.append((table_name, False, headers))
                else:
                    print("⚠️ No records returned - cannot validate table structure")
                    validation_results.append((table_name, None, "No data"))

            except Exception as e:
                print(f"❌ Error validating {table_name}: {e}")
                validation_results.append((table_name, False, f"Error: {e}"))

            print()

        # Final summary
        print("🎯 FINAL VALIDATION SUMMARY")
        print("=" * 80)

        successful_tables = [result for result in validation_results if result[1] is True]
        failed_tables = [result for result in validation_results if result[1] is False]
        no_data_tables = [result for result in validation_results if result[1] is None]

        print(f"✅ Successful tables: {len(successful_tables)}/5")
        for table_name, _, headers in successful_tables:
            print(f"   • {table_name}: {headers[:3]}...")  # Show first 3 headers

        if failed_tables:
            print(f"❌ Failed tables: {len(failed_tables)}")
            for table_name, _, error in failed_tables:
                print(f"   • {table_name}: {error}")

        if no_data_tables:
            print(f"⚠️ Tables with no data: {len(no_data_tables)}")
            for table_name, _, status in no_data_tables:
                print(f"   • {table_name}: {status}")

        if len(successful_tables) == 5:
            print("\n🎉 ALL TABLES SUCCESSFULLY UPDATED!")
            print("✅ Action Request and Facility columns have been added as the first two columns to all 5 stakeholder journey tables")
        elif len(successful_tables) >= 3:
            print(f"\n🎊 MOSTLY SUCCESSFUL! {len(successful_tables)} out of 5 tables are working correctly")
            print("✅ Action Request and Facility columns are being added correctly where data is available")
        else:
            print(f"\n⚠️ PARTIAL SUCCESS: Only {len(successful_tables)} out of 5 tables are working")

    except Exception as e:
        print(f"❌ Error during validation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    final_validation()

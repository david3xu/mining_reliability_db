#!/usr/bin/env python3
"""
Single-Input → Five-Output Stakeholder Journey Demonstration
Demonstrates the complete stakeholder journey from one search input to comprehensive answers.
"""

import json
import datetime
from mine_core.database.query_manager import QueryManager

class StakeholderJourneyDemo:
    """Demonstrates the complete single-input → five-output workflow"""

    def __init__(self):
        self.query_manager = QueryManager()
        self.config_path = "/home/291928k/uwa/alcoa/mining_reliability_db/configs/stakeholder_essential_queries.json"

        # Load configuration
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

    def execute_complete_journey(self, user_input: str):
        """Execute complete stakeholder journey from single input"""
        print("="*80)
        print("🎯 MINING RELIABILITY STAKEHOLDER JOURNEY")
        print("="*80)
        print(f"📝 User Input: \"{user_input}\"")
        print(f"⏰ Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        # Extract keywords from user input
        keywords = self._extract_keywords(user_input)
        print(f"🔍 Extracted Keywords: {', '.join(keywords)}")

        # Create filter clause
        filter_clause = self._create_filter_clause(keywords)
        print(f"🔧 Query Filter: {filter_clause[:100]}...")

        # Execute all five questions
        journey_results = {}

        print(f"\n{'🚀 EXECUTING STAKEHOLDER JOURNEY':^80}")
        print("="*80)

        question_titles = {
            'what_could_be_causing_this': '1️⃣  WHY DID THIS HAPPEN?',
            'what_investigation_steps_worked': '2️⃣  HOW DO I FIGURE OUT WHAT\'S WRONG?',
            'who_has_diagnostic_experience': '3️⃣  WHO CAN HELP ME?',
            'what_should_i_check_first': '4️⃣  WHAT SHOULD I CHECK FIRST?',
            'how_do_i_fix_this': '5️⃣  HOW DO I FIX THIS?'
        }

        total_results = 0

        for question_id, question_config in self.config['essential_queries'].items():
            title = question_titles.get(question_id, question_id.replace('_', ' ').title())
            print(f"\n{title}")
            print("-" * 60)

            try:
                result = self.query_manager.execute_stakeholder_essential_query(
                    question_config['query_file'],
                    filter_clause
                )

                if result.success and result.data:
                    count = len(result.data)
                    total_results += count
                    print(f"✅ Found {count} relevant solutions")

                    # Show top 3 results
                    for i, item in enumerate(result.data[:3], 1):
                        self._display_result_summary(i, item, question_id)

                    journey_results[question_id] = {
                        'success': True,
                        'count': count,
                        'data': result.data
                    }

                else:
                    print("⚠️  No solutions found for this aspect")
                    journey_results[question_id] = {
                        'success': False,
                        'count': 0
                    }

            except Exception as e:
                print(f"❌ Error: {str(e)}")
                journey_results[question_id] = {
                    'success': False,
                    'error': str(e)
                }

        # Journey summary
        self._display_journey_summary(user_input, journey_results, total_results)

        return journey_results

    def _extract_keywords(self, user_input: str) -> list:
        """Extract meaningful keywords from user input"""
        # Simple keyword extraction - could be enhanced with NLP
        words = user_input.lower().replace(',', ' ').split()

        # Filter out common words and short words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were', 'a', 'an'}
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]

        return keywords[:6]  # Limit to 6 most relevant keywords

    def _create_filter_clause(self, keywords: list) -> str:
        """Create Cypher filter clause from keywords"""
        if not keywords:
            return "toLower(p.what_happened) CONTAINS toLower('equipment')"

        # Create OR clause for flexible matching
        keyword_filters = []
        for keyword in keywords:
            keyword_filters.append(f"toLower(p.what_happened) CONTAINS toLower('{keyword}')")

        return " OR ".join(keyword_filters)

    def _display_result_summary(self, index: int, item: dict, question_type: str):
        """Display a concise summary of a single result"""
        if question_type == 'what_could_be_causing_this':
            desc = item.get('problem_description', '')[:80] + "..." if len(item.get('problem_description', '')) > 80 else item.get('problem_description', '')
            solution = item.get('proven_solution', '')[:60] + "..." if len(item.get('proven_solution', '')) > 60 else item.get('proven_solution', '')
            print(f"   {index}. Problem: {desc}")
            print(f"      Solution: {solution}")

        elif question_type == 'who_has_diagnostic_experience':
            dept = item.get('initiating_department', 'Unknown')
            facility = item.get('facility', 'Unknown')
            print(f"   {index}. Department: {dept} (Facility: {facility})")

        elif question_type == 'what_should_i_check_first':
            step = item.get('investigation_step', '')[:70] + "..." if len(item.get('investigation_step', '')) > 70 else item.get('investigation_step', '')
            freq = item.get('step_frequency', 1)
            print(f"   {index}. Step: {step} (Used {freq} times)")

        elif question_type == 'how_do_i_fix_this':
            solution = item.get('proven_solution', '')[:70] + "..." if len(item.get('proven_solution', '')) > 70 else item.get('proven_solution', '')
            status = item.get('success_status', 'Unknown')
            print(f"   {index}. Solution: {solution}")
            print(f"      Status: {status}")

        else:
            # Generic display for other question types
            key_field = list(item.keys())[0] if item.keys() else 'data'
            value = str(item.get(key_field, ''))[:70] + "..." if len(str(item.get(key_field, ''))) > 70 else str(item.get(key_field, ''))
            print(f"   {index}. {key_field}: {value}")

    def _display_journey_summary(self, user_input: str, results: dict, total_results: int):
        """Display comprehensive journey summary"""
        print(f"\n{'📊 STAKEHOLDER JOURNEY SUMMARY':^80}")
        print("="*80)

        successful_questions = sum(1 for r in results.values() if r.get('success', False))
        completeness = (successful_questions / 5) * 100

        print(f"🔍 Original Query: \"{user_input}\"")
        print(f"📈 Total Solutions Found: {total_results}")
        print(f"✅ Questions Answered: {successful_questions}/5")
        print(f"🎯 Journey Completeness: {completeness:.1f}%")

        # Stakeholder readiness assessment
        print(f"\n📋 STAKEHOLDER READINESS ASSESSMENT:")
        if completeness >= 80:
            print("🏆 EXCELLENT: Complete guidance available for all stakeholders")
            print("   → Operations teams can proceed with confidence")
            print("   → Management has full visibility and resource planning")
            print("   → Technical teams have comprehensive solutions")
        elif completeness >= 60:
            print("✅ GOOD: Substantial guidance available")
            print("   → Most stakeholder needs addressed")
            print("   → Some areas may need additional investigation")
        elif completeness >= 40:
            print("⚠️  PARTIAL: Limited guidance available")
            print("   → Basic information available")
            print("   → Additional expertise consultation recommended")
        else:
            print("❌ INSUFFICIENT: Inadequate data for stakeholder support")
            print("   → Escalate to subject matter experts")
            print("   → Consider expanding incident database coverage")

        # Next steps recommendation
        print(f"\n🎯 RECOMMENDED NEXT STEPS:")
        if results.get('who_has_diagnostic_experience', {}).get('success'):
            expert_count = results['who_has_diagnostic_experience'].get('count', 0)
            print(f"   1. Contact expertise departments ({expert_count} options available)")

        if results.get('what_should_i_check_first', {}).get('success'):
            step_count = results['what_should_i_check_first'].get('count', 0)
            print(f"   2. Begin prioritized investigation ({step_count} proven approaches)")

        if results.get('how_do_i_fix_this', {}).get('success'):
            solution_count = results['how_do_i_fix_this'].get('count', 0)
            print(f"   3. Implement proven solutions ({solution_count} verified approaches)")

        print(f"   4. Document findings for knowledge base enhancement")

        print("\n" + "="*80)
        print("🚀 STAKEHOLDER JOURNEY COMPLETE - READY FOR ACTION")
        print("="*80)

def main():
    """Demonstrate the single-input → five-output stakeholder journey"""
    demo = StakeholderJourneyDemo()

    # Test scenarios
    test_scenarios = [
        "Excavator rear swing motor failed causing 3.5 days of downtime",
        "Conveyor belt slipping on the main production line",
        "Hydraulic leak detected in the crusher system",
        "Bearing noise in the primary crusher motor",
        "Dust contamination in the processing equipment filters"
    ]

    print("🎯 SINGLE-INPUT → FIVE-OUTPUT STAKEHOLDER JOURNEY DEMO")
    print("🔧 Mining Reliability Database - Comprehensive Intelligence System")
    print(f"📅 Demonstration Date: {datetime.datetime.now().strftime('%B %d, %Y')}")

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*20} SCENARIO {i} {'='*20}")
        results = demo.execute_complete_journey(scenario)

        if i < len(test_scenarios):
            print(f"\n⏸️  Press Enter to continue to next scenario...")
            input()

if __name__ == "__main__":
    main()

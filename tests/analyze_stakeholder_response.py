#!/usr/bin/env python3
"""
Stakeholder Response Generator
Analyzes JSON search results to generate targeted responses for different stakeholder concerns
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.json_recorder import JSONRecorder

class StakeholderResponseGenerator:
    """Generate stakeholder-specific responses from search results"""

    def __init__(self):
        self.json_recorder = JSONRecorder()

    def analyze_search_for_stakeholders(self, search_file_path: str) -> Dict[str, Any]:
        """Analyze search results and generate stakeholder responses"""

        # Load search data
        search_data = self.json_recorder.load_search_results(search_file_path)

        # Extract key information
        search_term = search_data['search_metadata']['search_term']
        results = search_data['search_results']
        stats = search_data['statistics']

        # Generate responses for each stakeholder type
        responses = {
            'operator': self._generate_operator_response(search_term, results, stats),
            'maintenance_tech': self._generate_maintenance_response(search_term, results, stats),
            'engineer': self._generate_engineer_response(search_term, results, stats),
            'manager': self._generate_manager_response(search_term, results, stats),
            'executive': self._generate_executive_response(search_term, results, stats)
        }

        return {
            'search_summary': {
                'search_term': search_term,
                'total_results': stats.get('total_results', 0),
                'timestamp': search_data['search_metadata']['timestamp_formatted']
            },
            'stakeholder_responses': responses,
            'key_insights': self._extract_key_insights(results, stats)
        }

    def _generate_operator_response(self, search_term: str, results: Dict, stats: Dict) -> Dict[str, Any]:
        """Generate immediate action-focused response for operators"""

        direct_matches = results.get('direct_matches', [])
        immediate_actions = []
        safety_concerns = []

        # Extract immediate actions from direct matches
        for match in direct_matches[:3]:  # Top 3 most relevant
            if 'ap' in match and match['ap']:
                action_plan = match['ap'].get('action_plan', '')
                if action_plan and len(action_plan) > 10:
                    immediate_actions.append({
                        'action': action_plan,
                        'completion_status': match['ap'].get('complete', 'Unknown'),
                        'incident_id': match.get('ar', {}).get('action_request_number', 'N/A')
                    })

            # Check for safety indicators
            problem_desc = match.get('p', {}).get('what_happened', '').lower()
            if any(keyword in problem_desc for keyword in ['leak', 'pressure', 'emergency', 'stop', 'failure']):
                safety_concerns.append(match.get('p', {}).get('what_happened', ''))

        response = {
            'priority_level': 'HIGH' if safety_concerns else 'MEDIUM',
            'immediate_actions': immediate_actions[:3],
            'safety_alert': len(safety_concerns) > 0,
            'safety_concerns': safety_concerns,
            'quick_summary': f"Found {len(direct_matches)} similar incidents. {len(immediate_actions)} proven action plans available.",
            'recommendation': self._get_operator_recommendation(immediate_actions, safety_concerns)
        }

        return response

    def _generate_maintenance_response(self, search_term: str, results: Dict, stats: Dict) -> Dict[str, Any]:
        """Generate technical solution-focused response for maintenance technicians"""

        direct_matches = results.get('direct_matches', [])
        equipment_patterns = results.get('equipment_patterns', [])

        proven_solutions = []
        maintenance_procedures = []
        parts_needed = []

        # Extract proven solutions
        for match in direct_matches:
            if 'ap' in match and match['ap'] and match['ap'].get('complete') == 'Yes':
                solution_info = {
                    'solution': match['ap'].get('action_plan', ''),
                    'root_cause': match.get('rc', {}).get('root_cause', ''),
                    'effectiveness': match.get('v', {}).get('is_action_plan_effective', 'Unknown'),
                    'facility': match.get('f', {}).get('facility_name', 'Unknown'),
                    'completion_date': match['ap'].get('completion_date', 'Unknown')
                }
                proven_solutions.append(solution_info)

        # Analyze equipment patterns for maintenance insights
        equipment_insights = self._analyze_equipment_patterns(equipment_patterns)

        response = {
            'proven_solutions': proven_solutions[:5],
            'equipment_insights': equipment_insights,
            'maintenance_complexity': self._assess_maintenance_complexity(proven_solutions),
            'estimated_timeline': self._estimate_repair_timeline(proven_solutions),
            'technical_summary': f"Analysis of {len(direct_matches)} similar cases shows {len(proven_solutions)} proven repair methods.",
            'recommendation': self._get_maintenance_recommendation(proven_solutions, equipment_insights)
        }

        return response

    def _generate_engineer_response(self, search_term: str, results: Dict, stats: Dict) -> Dict[str, Any]:
        """Generate comprehensive analysis for engineers"""

        direct_matches = results.get('direct_matches', [])
        causal_chains = results.get('causal_chains', [])
        cross_facility = results.get('cross_facility_patterns', [])

        # Root cause analysis
        root_causes = {}
        for match in direct_matches:
            root_cause = match.get('rc', {}).get('root_cause', '')
            if root_cause:
                root_causes[root_cause] = root_causes.get(root_cause, 0) + 1

        # Design implications
        design_insights = self._analyze_design_implications(direct_matches, causal_chains)

        # Cross-facility learnings
        facility_insights = self._analyze_cross_facility_patterns(cross_facility)

        response = {
            'root_cause_analysis': dict(sorted(root_causes.items(), key=lambda x: x[1], reverse=True)[:5]),
            'design_implications': design_insights,
            'cross_facility_insights': facility_insights,
            'pattern_strength': len(causal_chains),
            'engineering_complexity': self._assess_engineering_complexity(direct_matches),
            'preventive_measures': self._suggest_preventive_measures(root_causes),
            'comprehensive_summary': f"Engineering analysis of {stats.get('total_results', 0)} related incidents across {stats.get('dimensions_with_results', 0)} analysis dimensions.",
            'recommendation': self._get_engineering_recommendation(root_causes, design_insights)
        }

        return response

    def _generate_manager_response(self, search_term: str, results: Dict, stats: Dict) -> Dict[str, Any]:
        """Generate business impact analysis for managers"""

        direct_matches = results.get('direct_matches', [])
        cross_facility = results.get('cross_facility_patterns', [])

        # Business impact analysis
        facilities_affected = set()
        past_due_items = 0
        completed_actions = 0
        total_incidents = len(direct_matches)

        for match in direct_matches:
            facility = match.get('f', {}).get('facility_name', '')
            if facility:
                facilities_affected.add(facility)

            if match.get('ar', {}).get('past_due_status') == 'Past Due':
                past_due_items += 1

            if match.get('ap', {}).get('complete') == 'Yes':
                completed_actions += 1

        # Resource allocation insights
        resource_insights = self._analyze_resource_requirements(direct_matches)

        response = {
            'business_impact': {
                'facilities_affected': len(facilities_affected),
                'facility_list': list(facilities_affected),
                'total_incidents': total_incidents,
                'completion_rate': f"{(completed_actions/total_incidents*100):.1f}%" if total_incidents > 0 else "0%",
                'past_due_items': past_due_items
            },
            'resource_insights': resource_insights,
            'strategic_recommendations': self._get_strategic_recommendations(facilities_affected, resource_insights),
            'risk_assessment': self._assess_business_risk(past_due_items, total_incidents),
            'cost_implications': self._analyze_cost_implications(direct_matches),
            'management_summary': f"Business analysis shows {len(facilities_affected)} facilities affected with {past_due_items} overdue items requiring attention.",
            'recommendation': self._get_management_recommendation(facilities_affected, past_due_items, completed_actions)
        }

        return response

    def _generate_executive_response(self, search_term: str, results: Dict, stats: Dict) -> Dict[str, Any]:
        """Generate high-level strategic response for executives"""

        direct_matches = results.get('direct_matches', [])

        # Strategic insights
        facilities_affected = set(match.get('f', {}).get('facility_name', '') for match in direct_matches if match.get('f', {}).get('facility_name'))

        # Risk and opportunity analysis
        risk_level = self._assess_strategic_risk(direct_matches, stats)
        opportunities = self._identify_strategic_opportunities(results)

        response = {
            'strategic_overview': {
                'scope': f"{len(facilities_affected)} facilities, {stats.get('total_results', 0)} related incidents",
                'risk_level': risk_level,
                'pattern_detection': f"{stats.get('dimensions_with_results', 0)}/8 intelligence dimensions active"
            },
            'key_opportunities': opportunities,
            'resource_optimization': self._suggest_resource_optimization(facilities_affected, direct_matches),
            'strategic_recommendations': self._get_executive_recommendations(risk_level, opportunities),
            'success_metrics': self._define_success_metrics(direct_matches),
            'executive_summary': f"Strategic analysis of '{search_term}' reveals patterns across {len(facilities_affected)} facilities with actionable intelligence for operational excellence.",
            'next_steps': self._define_executive_next_steps(risk_level, opportunities)
        }

        return response

    def _extract_key_insights(self, results: Dict, stats: Dict) -> Dict[str, Any]:
        """Extract key insights across all stakeholder perspectives"""

        insights = {
            'data_completeness': f"{stats.get('dimensions_with_results', 0)}/8 analysis dimensions returned results",
            'pattern_strength': 'Strong' if stats.get('total_results', 0) > 50 else 'Moderate' if stats.get('total_results', 0) > 20 else 'Weak',
            'intelligence_coverage': stats.get('total_results', 0),
            'cross_facility_knowledge': len(results.get('cross_facility_patterns', [])) > 0,
            'solution_availability': len(results.get('direct_matches', [])) > 0,
            'causal_understanding': len(results.get('causal_chains', [])) > 0
        }

        return insights

    # Helper methods for analysis
    def _get_operator_recommendation(self, actions: List, safety_concerns: List) -> str:
        if safety_concerns:
            return "IMMEDIATE ACTION REQUIRED: Safety concerns detected. Follow emergency procedures and escalate to supervisor."
        elif actions:
            return f"Implement proven action plan from similar incident. {len(actions)} verified solutions available."
        else:
            return "No immediate actions found. Escalate to maintenance team for investigation."

    def _get_maintenance_recommendation(self, solutions: List, equipment_insights: Dict) -> str:
        if solutions:
            effective_solutions = [s for s in solutions if s.get('effectiveness') != 'No']
            if effective_solutions:
                return f"Apply proven solution from {effective_solutions[0].get('facility', 'similar facility')}. Success rate: High."
            else:
                return "Previous solutions show mixed results. Recommend custom approach based on root cause analysis."
        else:
            return "No proven solutions found. Recommend detailed investigation and consultation with engineering team."

    def _get_engineering_recommendation(self, root_causes: Dict, design_insights: Dict) -> str:
        if root_causes:
            primary_cause = list(root_causes.keys())[0]
            return f"Focus on primary root cause: {primary_cause[:100]}... Recommend systematic design review."
        else:
            return "Insufficient root cause data. Recommend comprehensive failure mode analysis."

    def _get_management_recommendation(self, facilities: set, past_due: int, completed: int) -> str:
        if past_due > 0:
            return f"ATTENTION: {past_due} overdue items require immediate resource allocation across {len(facilities)} facilities."
        elif len(facilities) > 3:
            return f"Multi-facility pattern detected. Recommend standardized response protocol development."
        else:
            return f"Localized issue with {completed} successful resolutions. Continue current approach."

    def _assess_maintenance_complexity(self, solutions: List) -> str:
        if not solutions:
            return "High - No proven solutions available"

        avg_timeline = self._estimate_repair_timeline(solutions)
        if "week" in avg_timeline.lower() or "month" in avg_timeline.lower():
            return "High - Extended timeline required"
        elif "day" in avg_timeline.lower():
            return "Medium - Multi-day repair expected"
        else:
            return "Low - Quick resolution possible"

    def _estimate_repair_timeline(self, solutions: List) -> str:
        if not solutions:
            return "Unknown - No historical data"

        # Simple heuristic based on solution complexity
        complex_indicators = ['design', 'modification', 'replacement', 'overhaul', 'rebuild']
        quick_indicators = ['adjust', 'clean', 'tighten', 'replace filter', 'lubricate']

        for solution in solutions:
            action_plan = solution.get('solution', '').lower()
            if any(indicator in action_plan for indicator in complex_indicators):
                return "1-2 weeks (complex repair)"
            elif any(indicator in action_plan for indicator in quick_indicators):
                return "4-8 hours (routine maintenance)"

        return "1-3 days (standard repair)"

    def _analyze_equipment_patterns(self, patterns: List) -> Dict:
        # Simplified equipment pattern analysis
        return {
            'pattern_count': len(patterns),
            'equipment_reliability': 'Moderate' if len(patterns) > 10 else 'Good',
            'maintenance_frequency': 'High' if len(patterns) > 15 else 'Normal'
        }

    def _analyze_design_implications(self, matches: List, causal_chains: List) -> Dict:
        return {
            'design_review_needed': len(matches) > 10,
            'systemic_issues': len(causal_chains) > 5,
            'modification_priority': 'High' if len(matches) > 15 else 'Medium'
        }

    def _analyze_cross_facility_patterns(self, cross_facility: List) -> Dict:
        return {
            'knowledge_sharing_opportunity': len(cross_facility) > 0,
            'standardization_potential': len(cross_facility) > 10,
            'best_practice_available': len(cross_facility) > 5
        }

    def _assess_engineering_complexity(self, matches: List) -> str:
        if len(matches) > 20:
            return "High - Recurring systemic issue"
        elif len(matches) > 10:
            return "Medium - Pattern requires investigation"
        else:
            return "Low - Isolated incidents"

    def _suggest_preventive_measures(self, root_causes: Dict) -> List[str]:
        measures = []
        for cause in list(root_causes.keys())[:3]:
            if 'temperature' in cause.lower():
                measures.append("Implement temperature monitoring and cooling system upgrades")
            elif 'dust' in cause.lower() or 'contamination' in cause.lower():
                measures.append("Enhance filtration and cleaning procedures")
            elif 'vibration' in cause.lower():
                measures.append("Install vibration monitoring and balancing systems")
            else:
                measures.append("Develop targeted maintenance program for identified failure mode")
        return measures if measures else ["Implement comprehensive condition monitoring"]

    def _analyze_resource_requirements(self, matches: List) -> Dict:
        return {
            'technical_expertise_needed': len(matches) > 10,
            'specialized_parts_required': len(matches) > 5,
            'contractor_support': len(matches) > 15,
            'estimated_resource_level': 'High' if len(matches) > 15 else 'Medium' if len(matches) > 5 else 'Low'
        }

    def _get_strategic_recommendations(self, facilities: set, resource_insights: Dict) -> List[str]:
        recommendations = []
        if len(facilities) > 3:
            recommendations.append("Establish cross-facility knowledge sharing protocol")
        if resource_insights.get('technical_expertise_needed'):
            recommendations.append("Invest in specialized training or contractor partnerships")
        if resource_insights.get('specialized_parts_required'):
            recommendations.append("Review inventory management and supplier relationships")
        return recommendations if recommendations else ["Continue current operational procedures"]

    def _assess_business_risk(self, past_due: int, total: int) -> str:
        if past_due == 0:
            return "Low - All items on schedule"
        elif past_due / total > 0.3:
            return "High - Significant overdue items"
        else:
            return "Medium - Some delays present"

    def _analyze_cost_implications(self, matches: List) -> Dict:
        return {
            'incident_frequency': len(matches),
            'cost_category': 'High' if len(matches) > 15 else 'Medium' if len(matches) > 5 else 'Low',
            'prevention_roi': 'High' if len(matches) > 10 else 'Medium'
        }

    def _assess_strategic_risk(self, matches: List, stats: Dict) -> str:
        total_results = stats.get('total_results', 0)
        if total_results > 50:
            return "High - Significant operational impact"
        elif total_results > 20:
            return "Medium - Moderate operational concern"
        else:
            return "Low - Limited operational impact"

    def _identify_strategic_opportunities(self, results: Dict) -> List[str]:
        opportunities = []
        if len(results.get('cross_facility_patterns', [])) > 10:
            opportunities.append("Standardize best practices across facilities")
        if len(results.get('solution_effectiveness', [])) > 5:
            opportunities.append("Scale proven solutions enterprise-wide")
        if len(results.get('equipment_patterns', [])) > 15:
            opportunities.append("Optimize equipment replacement strategies")
        return opportunities if opportunities else ["Enhance incident tracking and analysis capabilities"]

    def _suggest_resource_optimization(self, facilities: set, matches: List) -> List[str]:
        suggestions = []
        if len(facilities) > 3:
            suggestions.append("Centralize expertise across facilities")
        if len(matches) > 20:
            suggestions.append("Invest in predictive maintenance technology")
        return suggestions if suggestions else ["Maintain current resource allocation"]

    def _get_executive_recommendations(self, risk_level: str, opportunities: List) -> List[str]:
        recommendations = []
        if risk_level == "High":
            recommendations.append("Prioritize immediate resource allocation for risk mitigation")
        if opportunities:
            recommendations.extend(opportunities[:2])
        recommendations.append("Implement systematic knowledge management program")
        return recommendations

    def _define_success_metrics(self, matches: List) -> List[str]:
        return [
            "Reduction in similar incident frequency by 30%",
            "Decrease in resolution time by 20%",
            "Improvement in first-time fix rate to >85%",
            "Cross-facility knowledge sharing adoption >80%"
        ]

    def _define_executive_next_steps(self, risk_level: str, opportunities: List) -> List[str]:
        steps = ["Review detailed stakeholder analysis reports"]
        if risk_level == "High":
            steps.append("Schedule immediate leadership review meeting")
        if opportunities:
            steps.append("Develop implementation roadmap for identified opportunities")
        steps.append("Establish quarterly progress review process")
        return steps


def main():
    """Generate stakeholder responses for the most recent search"""
    print("🎯 STAKEHOLDER RESPONSE GENERATOR")
    print("=" * 60)

    generator = StakeholderResponseGenerator()

    # Get the most recent search
    saved_searches = generator.json_recorder.list_saved_searches(limit=1)

    if not saved_searches:
        print("❌ No saved searches found. Please run a search first.")
        return

    latest_search = saved_searches[0]
    print(f"📁 Analyzing: {Path(latest_search).name}")

    # Generate stakeholder analysis
    analysis = generator.analyze_search_for_stakeholders(latest_search)

    # Display results
    print(f"\n🔍 SEARCH SUMMARY:")
    summary = analysis['search_summary']
    print(f"   Search Term: '{summary['search_term']}'")
    print(f"   Total Results: {summary['total_results']}")
    print(f"   Analysis Time: {summary['timestamp']}")

    print(f"\n📊 KEY INSIGHTS:")
    insights = analysis['key_insights']
    for key, value in insights.items():
        print(f"   • {key.replace('_', ' ').title()}: {value}")

    # Display stakeholder responses
    responses = analysis['stakeholder_responses']

    print(f"\n" + "="*60)
    print(f"🏗️ OPERATOR RESPONSE (Immediate Actions)")
    print(f"="*60)
    operator = responses['operator']
    print(f"Priority Level: {operator['priority_level']}")
    print(f"Safety Alert: {'🚨 YES' if operator['safety_alert'] else '✅ NO'}")
    print(f"Quick Summary: {operator['quick_summary']}")
    print(f"Recommendation: {operator['recommendation']}")
    if operator['immediate_actions']:
        print(f"Immediate Actions Available:")
        for i, action in enumerate(operator['immediate_actions'], 1):
            print(f"  {i}. {action['action'][:100]}...")
            print(f"     Status: {action['completion_status']} | ID: {action['incident_id']}")

    print(f"\n" + "="*60)
    print(f"🔧 MAINTENANCE TECHNICIAN RESPONSE")
    print(f"="*60)
    maintenance = responses['maintenance_tech']
    print(f"Technical Summary: {maintenance['technical_summary']}")
    print(f"Maintenance Complexity: {maintenance['maintenance_complexity']}")
    print(f"Estimated Timeline: {maintenance['estimated_timeline']}")
    print(f"Recommendation: {maintenance['recommendation']}")
    if maintenance['proven_solutions']:
        print(f"Proven Solutions ({len(maintenance['proven_solutions'])}):")
        for i, solution in enumerate(maintenance['proven_solutions'][:3], 1):
            print(f"  {i}. Effectiveness: {solution['effectiveness']}")
            print(f"     Solution: {solution['solution'][:100]}...")
            print(f"     Facility: {solution['facility']}")

    print(f"\n" + "="*60)
    print(f"⚙️ ENGINEER RESPONSE (Root Cause Analysis)")
    print(f"="*60)
    engineer = responses['engineer']
    print(f"Comprehensive Summary: {engineer['comprehensive_summary']}")
    print(f"Engineering Complexity: {engineer['engineering_complexity']}")
    print(f"Pattern Strength: {engineer['pattern_strength']} causal relationships identified")
    print(f"Recommendation: {engineer['recommendation']}")
    if engineer['root_cause_analysis']:
        print(f"Top Root Causes:")
        for cause, count in list(engineer['root_cause_analysis'].items())[:3]:
            print(f"  • {cause[:80]}... (Found in {count} incidents)")

    print(f"\n" + "="*60)
    print(f"📈 MANAGER RESPONSE (Business Impact)")
    print(f"="*60)
    manager = responses['manager']
    print(f"Management Summary: {manager['management_summary']}")
    business_impact = manager['business_impact']
    print(f"Business Impact:")
    print(f"  • Facilities Affected: {business_impact['facilities_affected']}")
    print(f"  • Total Incidents: {business_impact['total_incidents']}")
    print(f"  • Completion Rate: {business_impact['completion_rate']}")
    print(f"  • Past Due Items: {business_impact['past_due_items']}")
    print(f"Risk Assessment: {manager['risk_assessment']}")
    print(f"Recommendation: {manager['recommendation']}")

    print(f"\n" + "="*60)
    print(f"🎯 EXECUTIVE RESPONSE (Strategic Overview)")
    print(f"="*60)
    executive = responses['executive']
    print(f"Executive Summary: {executive['executive_summary']}")
    strategic = executive['strategic_overview']
    print(f"Strategic Overview:")
    print(f"  • Scope: {strategic['scope']}")
    print(f"  • Risk Level: {strategic['risk_level']}")
    print(f"  • Pattern Detection: {strategic['pattern_detection']}")
    print(f"Key Opportunities:")
    for opportunity in executive['key_opportunities']:
        print(f"  • {opportunity}")
    print(f"Next Steps:")
    for step in executive['next_steps']:
        print(f"  • {step}")

    print(f"\n" + "="*60)
    print(f"✅ STAKEHOLDER ANALYSIS COMPLETE")
    print(f"📋 All stakeholder concerns addressed with data-driven insights")
    print(f"🎯 Actionable recommendations provided for each role")
    print(f"="*60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Data Quality Analysis Script - EDA Framework for Manager Reporting
Systematic investigation of data quality patterns for engineer effectiveness
"""

import sys
import os
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, Any

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from mine_core.analytics.quality_analyzer import QualityAnalyzer
from mine_core.analytics.workflow_analyzer import WorkflowAnalyzer
from mine_core.analytics.pattern_discovery import PatternDiscovery
from mine_core.database.db import get_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class DataQualityEDA:
    """
    EDA Framework for Data Quality Analysis
    Systematic investigation methodology for manager reporting
    """

    def __init__(self):
        """Initialize EDA components"""
        self.quality_analyzer = QualityAnalyzer()
        self.workflow_analyzer = WorkflowAnalyzer()
        self.pattern_discovery = PatternDiscovery()
        self.db = get_database()

    def conduct_comprehensive_analysis(self, facility_filter: str = None) -> Dict[str, Any]:
        """
        Primary EDA Investigation: Comprehensive data quality assessment

        Methodology:
        Step 1: Data Quality Profiling (missing values, completeness)
        Step 2: Workflow Integrity Analysis (engineer impact assessment)
        Step 3: Cross-Facility Pattern Discovery (learning opportunities)
        Step 4: Strategic Insights Generation (actionable recommendations)
        """

        logger.info("=== Starting Comprehensive Data Quality EDA ===")

        # Step 1: Traditional + Enhanced Data Quality Analysis
        logger.info("Step 1: Conducting data quality profiling...")
        quality_results = self._investigate_data_quality(facility_filter)

        # Step 2: Workflow Impact Assessment
        logger.info("Step 2: Analyzing workflow integrity impact...")
        workflow_results = self._investigate_workflow_impact(facility_filter)

        # Step 3: Pattern Discovery (if analyzing all facilities)
        pattern_results = {}
        if not facility_filter:
            logger.info("Step 3: Discovering cross-facility patterns...")
            pattern_results = self._investigate_cross_facility_patterns()

        # Step 4: Strategic Insights Synthesis
        logger.info("Step 4: Generating strategic insights...")
        strategic_insights = self._synthesize_strategic_insights(
            quality_results, workflow_results, pattern_results
        )

        comprehensive_analysis = {
            "analysis_metadata": {
                "scope": facility_filter if facility_filter else "All Facilities",
                "analysis_type": "Comprehensive Data Quality EDA",
                "focus": "Engineer Root Cause Analysis Effectiveness"
            },
            "data_quality_analysis": quality_results,
            "workflow_impact_analysis": workflow_results,
            "cross_facility_patterns": pattern_results,
            "strategic_insights": strategic_insights,
            "manager_summary": self._generate_manager_summary(strategic_insights)
        }

        logger.info("=== EDA Analysis Complete ===")
        return comprehensive_analysis

    def _investigate_data_quality(self, facility_filter: str) -> Dict[str, Any]:
        """EDA Step 1: Data quality profiling with engineer impact focus"""

        if facility_filter:
            # Single facility deep-dive analysis
            facility_analysis = self.quality_analyzer.analyze_facility_completeness(facility_filter)
            missing_impact = self.quality_analyzer.get_missing_data_impact()

            return {
                "analysis_type": "Single Facility Deep-Dive",
                "facility_analysis": facility_analysis,
                "missing_data_impact": missing_impact
            }
        else:
            # Multi-facility comparative analysis
            all_facilities = self.quality_analyzer.analyze_facility_completeness()
            missing_impact = self.quality_analyzer.get_missing_data_impact()

            return {
                "analysis_type": "Multi-Facility Comparison",
                "facility_comparison": all_facilities,
                "missing_data_impact": missing_impact
            }

    def _investigate_workflow_impact(self, facility_filter: str) -> Dict[str, Any]:
        """EDA Step 2: Workflow integrity analysis for engineer effectiveness"""

        workflow_analysis = self.workflow_analyzer.analyze_workflow_integrity(facility_filter)

        return {
            "workflow_completeness": workflow_analysis["workflow_patterns"],
            "critical_workflow_gaps": workflow_analysis["critical_gaps"],
            "engineer_effectiveness_impact": workflow_analysis["engineer_impact"],
            "workflow_recommendations": workflow_analysis["recommendations"]
        }

    def _investigate_cross_facility_patterns(self) -> Dict[str, Any]:
        """EDA Step 3: Cross-facility pattern discovery for knowledge sharing"""

        return self.pattern_discovery.investigate_cross_facility_patterns()

    def _synthesize_strategic_insights(self, quality: Dict, workflow: Dict, patterns: Dict) -> Dict[str, Any]:
        """EDA Step 4: Strategic insights synthesis from all analysis dimensions"""

        insights = {
            "critical_findings": [],
            "improvement_priorities": [],
            "knowledge_sharing_opportunities": [],
            "business_impact_assessment": {}
        }

        # Critical findings from data quality analysis
        if quality.get("missing_data_impact"):
            impact_data = quality["missing_data_impact"]
            usable_percentage = impact_data.get("engineer_impact", {}).get("usable_for_analysis", 0)
            if usable_percentage < 50:
                insights["critical_findings"].append(
                    f"Critical: Only {usable_percentage}% of incidents are usable for engineer root cause analysis"
                )

        # Workflow impact insights
        workflow_gaps = workflow.get("critical_workflow_gaps", {}).get("critical_gaps", [])
        for gap in workflow_gaps[:2]:  # Top 2 critical gaps
            insights["improvement_priorities"].append(
                f"Priority: {gap['facility']} - {gap['gap_type'].replace('_', ' ')} affects {gap['percentage']}% of incidents"
            )

        # Cross-facility knowledge sharing opportunities
        if patterns.get("knowledge_transfer_opportunities"):
            transfers = patterns["knowledge_transfer_opportunities"].get("high_value_transfers", [])
            for transfer in transfers[:2]:  # Top 2 opportunities
                insights["knowledge_sharing_opportunities"].append(
                    f"Transfer Opportunity: {transfer['expert_facility']} → {transfer['learning_facility']} "
                    f"({transfer['improvement_potential']}% potential improvement)"
                )

        # Business impact assessment
        insights["business_impact_assessment"] = {
            "engineer_productivity_impact": self._assess_engineer_productivity_impact(quality, workflow),
            "knowledge_sharing_potential": self._assess_knowledge_sharing_potential(patterns),
            "data_quality_roi": self._assess_data_quality_roi(quality, workflow)
        }

        return insights

    def _assess_engineer_productivity_impact(self, quality: Dict, workflow: Dict) -> Dict[str, Any]:
        """Assess impact on engineer productivity"""

        impact_data = quality.get("missing_data_impact", {}).get("engineer_impact", {})
        usable_percentage = impact_data.get("usable_for_analysis", 0)

        return {
            "current_usability": f"{usable_percentage}%",
            "productivity_impact": "High" if usable_percentage < 40 else "Medium" if usable_percentage < 70 else "Low",
            "improvement_potential": f"{100 - usable_percentage}% of incidents could become useful with data quality improvements"
        }

    def _assess_knowledge_sharing_potential(self, patterns: Dict) -> Dict[str, Any]:
        """Assess cross-facility knowledge sharing potential"""

        if not patterns:
            return {"potential": "Not analyzed (single facility focus)"}

        transfers = patterns.get("knowledge_transfer_opportunities", {}).get("high_value_transfers", [])
        expertise_centers = patterns.get("knowledge_transfer_opportunities", {}).get("expertise_centers", {})

        return {
            "high_value_opportunities": len(transfers),
            "expertise_centers": len(expertise_centers),
            "sharing_potential": "High" if len(transfers) > 3 else "Medium" if len(transfers) > 0 else "Low"
        }

    def _assess_data_quality_roi(self, quality: Dict, workflow: Dict) -> Dict[str, Any]:
        """Assess ROI of data quality improvements"""

        workflow_gaps = workflow.get("critical_workflow_gaps", {}).get("critical_gaps", [])
        total_affected = sum(gap.get("affected_incidents", 0) for gap in workflow_gaps)

        return {
            "incidents_affected_by_gaps": total_affected,
            "improvement_focus": "Workflow completion" if total_affected > 100 else "Data quality",
            "expected_roi": "High" if total_affected > 200 else "Medium"
        }

    def _generate_manager_summary(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary for manager presentation"""

        return {
            "key_findings": insights.get("critical_findings", [])[:3],
            "immediate_actions": insights.get("improvement_priorities", [])[:3],
            "business_value": insights.get("knowledge_sharing_opportunities", [])[:2],
            "next_steps": [
                "Implement workflow completion improvements at identified facilities",
                "Establish knowledge sharing protocols between high/low performing facilities",
                "Focus data quality efforts on engineer-critical fields"
            ]
        }

def generate_facility_reports(analyzer: DataQualityEDA, output_dir: Path):
    """Generate individual facility reports for manager presentation"""

    # Get list of facilities
    facilities_query = "MATCH (f:Facility) RETURN f.facility_id as id, f.facility_name as name"
    facilities = analyzer.db.execute_query(facilities_query)

    output_dir.mkdir(exist_ok=True)

    for facility in facilities:
        facility_id = facility['id']
        facility_name = facility['name']

        logger.info(f"Generating report for {facility_name}...")

        # Conduct facility-specific analysis
        analysis = analyzer.conduct_comprehensive_analysis(facility_id)

        # Save to JSON for further processing
        report_file = output_dir / f"{facility_id}_quality_analysis.json"
        with open(report_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)

        logger.info(f"Report saved: {report_file}")

def main():
    """Main EDA execution function"""

    parser = argparse.ArgumentParser(
        description="Comprehensive Data Quality EDA Analysis"
    )
    parser.add_argument("--facility", type=str, help="Analyze specific facility (default: all facilities)")
    parser.add_argument("--output-dir", type=str, default="./analysis_output",
                       help="Output directory for reports")
    parser.add_argument("--generate-individual-reports", action="store_true",
                       help="Generate individual facility reports")

    args = parser.parse_args()

    try:
        # Initialize EDA analyzer
        analyzer = DataQualityEDA()

        if args.generate_individual_reports:
            # Generate individual facility reports
            output_dir = Path(args.output_dir)
            generate_facility_reports(analyzer, output_dir)
            print(f"Individual facility reports generated in: {output_dir}")
        else:
            # Conduct comprehensive analysis
            analysis_results = analyzer.conduct_comprehensive_analysis(args.facility)

            # Display manager summary
            manager_summary = analysis_results["manager_summary"]

            print("\n" + "="*60)
            print("DATA QUALITY EDA - MANAGER SUMMARY")
            print("="*60)

            print("\n🔍 KEY FINDINGS:")
            for finding in manager_summary["key_findings"]:
                print(f"  • {finding}")

            print("\n🎯 IMMEDIATE ACTIONS:")
            for action in manager_summary["immediate_actions"]:
                print(f"  • {action}")

            print("\n💡 BUSINESS VALUE OPPORTUNITIES:")
            for value in manager_summary["business_value"]:
                print(f"  • {value}")

            print("\n📋 NEXT STEPS:")
            for step in manager_summary["next_steps"]:
                print(f"  • {step}")

            # Save detailed results
            output_dir = Path(args.output_dir)
            output_dir.mkdir(exist_ok=True)

            scope = args.facility if args.facility else "all_facilities"
            output_file = output_dir / f"data_quality_analysis_{scope}.json"

            with open(output_file, 'w') as f:
                json.dump(analysis_results, f, indent=2, default=str)

            print(f"\n📊 Detailed analysis saved: {output_file}")

        return 0

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        print(f"❌ Analysis failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())

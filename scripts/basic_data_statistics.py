#!/usr/bin/env python3
"""
Basic Data Statistics Analysis - Manager Report Generator
EDA Framework: Missing values, incorrect values, insights for 4 facility sheets
"""

import sys
import os
import json
import logging
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Tuple

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from mine_core.pipelines.extractor import FacilityDataExtractor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class BasicDataStatistics:
    """
    EDA Framework: Basic statistical analysis for manager reporting
    Focus: Missing values, data quality patterns, actionable insights
    """

    def __init__(self, data_dir: str = None):
        """Initialize with data directory"""
        if data_dir is None:
            # Find project root from script location
            script_dir = Path(__file__).resolve().parent
            project_root = script_dir.parent  # scripts -> project_root
            data_dir = project_root / "data" / "facility_data"

        self.extractor = FacilityDataExtractor(data_dir)
        self.facilities = self.extractor.get_available_facilities()

        # Validation check
        if not self.facilities:
            logger.warning(f"No facility data found in: {data_dir}")
            logger.info(f"Looking for JSON files in: {data_dir}")
            if Path(data_dir).exists():
                files = list(Path(data_dir).glob("*"))
                logger.info(f"Directory contents: {files}")
            else:
                logger.error(f"Data directory does not exist: {data_dir}")

    def analyze_all_facilities(self) -> Dict[str, Any]:
        """
        Primary EDA Investigation: Basic statistics across all facilities
        Step 1: Extract data from all facility files
        Step 2: Calculate basic statistics per column
        Step 3: Generate management insights
        Step 4: Create PPT-ready output
        """

        logger.info("=== Starting Basic Data Statistics Analysis ===")

        analysis_results = {
            "executive_summary": {},
            "facility_analyses": {},
            "cross_facility_insights": {},
            "ppt_slides": {}
        }

        # Step 1: Analyze each facility
        logger.info(f"Analyzing {len(self.facilities)} facilities...")

        for facility_id in self.facilities:
            logger.info(f"Processing facility: {facility_id}")
            facility_analysis = self._analyze_facility_statistics(facility_id)
            analysis_results["facility_analyses"][facility_id] = facility_analysis

        # Step 2: Cross-facility comparison
        logger.info("Generating cross-facility insights...")
        analysis_results["cross_facility_insights"] = self._generate_cross_facility_insights(
            analysis_results["facility_analyses"]
        )

        # Step 3: Executive summary
        analysis_results["executive_summary"] = self._generate_executive_summary(
            analysis_results["facility_analyses"],
            analysis_results["cross_facility_insights"]
        )

        # Step 4: PPT slide content
        analysis_results["ppt_slides"] = self._generate_ppt_slides(
            analysis_results["facility_analyses"],
            analysis_results["cross_facility_insights"]
        )

        logger.info("=== Analysis Complete ===")
        return analysis_results

    def _analyze_facility_statistics(self, facility_id: str) -> Dict[str, Any]:
        """EDA Step 1: Basic statistics for single facility"""

        # Extract raw data
        facility_data = self.extractor.extract_facility_data(facility_id)
        records = facility_data.get("records", [])

        if not records:
            return {"error": f"No data found for facility {facility_id}"}

        # Initialize statistics tracking
        column_stats = {}
        total_records = len(records)

        # Get all unique columns across all records
        all_columns = set()
        for record in records:
            all_columns.update(record.keys())

        # Analyze each column
        for column in all_columns:
            column_stats[column] = self._analyze_column_statistics(column, records)

        # Calculate facility-level metrics
        facility_metrics = self._calculate_facility_metrics(records, column_stats)

        return {
            "facility_id": facility_id,
            "total_records": total_records,
            "total_columns": len(all_columns),
            "column_statistics": column_stats,
            "facility_metrics": facility_metrics,
            "data_quality_score": self._calculate_data_quality_score(column_stats),
            "key_issues": self._identify_key_issues(column_stats, facility_metrics)
        }

    def _analyze_column_statistics(self, column: str, records: List[Dict]) -> Dict[str, Any]:
        """EDA Pattern: Column-level statistical analysis"""

        total_records = len(records)
        values = []
        missing_count = 0
        empty_count = 0
        list_values_count = 0

        # Collect values and identify patterns
        for record in records:
            value = record.get(column)

            if value is None:
                missing_count += 1
            elif isinstance(value, str) and not value.strip():
                empty_count += 1
            elif isinstance(value, list):
                list_values_count += 1
                values.append(value)
            else:
                values.append(value)

        # Calculate basic statistics
        present_count = total_records - missing_count - empty_count
        completeness_rate = round((present_count / total_records) * 100, 1)

        # Data type analysis
        data_types = defaultdict(int)
        unique_values = set()

        for value in values:
            if isinstance(value, list):
                data_types["list"] += 1
                unique_values.add(str(value))  # Convert to string for uniqueness
            elif isinstance(value, bool):
                data_types["boolean"] += 1
                unique_values.add(value)
            elif isinstance(value, int):
                data_types["integer"] += 1
                unique_values.add(value)
            elif isinstance(value, str):
                data_types["string"] += 1
                unique_values.add(value)
            else:
                data_types["other"] += 1
                unique_values.add(str(value))

        return {
            "total_records": total_records,
            "missing_values": missing_count,
            "empty_values": empty_count,
            "present_values": present_count,
            "completeness_rate": completeness_rate,
            "list_values": list_values_count,
            "unique_values_count": len(unique_values),
            "data_types": dict(data_types),
            "primary_data_type": max(data_types.items(), key=lambda x: x[1])[0] if data_types else "unknown",
            "quality_flag": "Good" if completeness_rate >= 80 else "Warning" if completeness_rate >= 50 else "Critical"
        }

    def _calculate_facility_metrics(self, records: List[Dict], column_stats: Dict) -> Dict[str, Any]:
        """EDA Pattern: Facility-level aggregated metrics"""

        total_columns = len(column_stats)
        good_columns = sum(1 for stats in column_stats.values() if stats["quality_flag"] == "Good")
        warning_columns = sum(1 for stats in column_stats.values() if stats["quality_flag"] == "Warning")
        critical_columns = sum(1 for stats in column_stats.values() if stats["quality_flag"] == "Critical")

        # Overall completeness
        total_cells = len(records) * total_columns
        missing_cells = sum(stats["missing_values"] + stats["empty_values"] for stats in column_stats.values())
        overall_completeness = round(((total_cells - missing_cells) / total_cells) * 100, 1)

        # List field analysis
        list_columns = [col for col, stats in column_stats.items() if stats["list_values"] > 0]

        return {
            "overall_completeness": overall_completeness,
            "good_quality_columns": good_columns,
            "warning_columns": warning_columns,
            "critical_columns": critical_columns,
            "columns_with_lists": len(list_columns),
            "list_column_names": list_columns,
            "data_quality_distribution": {
                "good": round((good_columns / total_columns) * 100, 1),
                "warning": round((warning_columns / total_columns) * 100, 1),
                "critical": round((critical_columns / total_columns) * 100, 1)
            }
        }

    def _calculate_data_quality_score(self, column_stats: Dict) -> Dict[str, Any]:
        """EDA Pattern: Overall data quality scoring"""

        if not column_stats:
            return {"score": 0, "grade": "F"}

        # Weight completeness rates
        completeness_rates = [stats["completeness_rate"] for stats in column_stats.values()]
        avg_completeness = sum(completeness_rates) / len(completeness_rates)

        # Grade assignment
        if avg_completeness >= 90:
            grade = "A"
        elif avg_completeness >= 80:
            grade = "B"
        elif avg_completeness >= 70:
            grade = "C"
        elif avg_completeness >= 60:
            grade = "D"
        else:
            grade = "F"

        return {
            "score": round(avg_completeness, 1),
            "grade": grade,
            "interpretation": self._interpret_data_quality_score(avg_completeness)
        }

    def _interpret_data_quality_score(self, score: float) -> str:
        """Interpretation of data quality score"""
        if score >= 90:
            return "Excellent data quality - suitable for advanced analytics"
        elif score >= 80:
            return "Good data quality - minor gaps do not impact analysis"
        elif score >= 70:
            return "Acceptable data quality - some analysis limitations"
        elif score >= 60:
            return "Poor data quality - significant data improvement needed"
        else:
            return "Critical data quality issues - major remediation required"

    def _identify_key_issues(self, column_stats: Dict, facility_metrics: Dict) -> List[str]:
        """EDA Pattern: Key issue identification"""

        issues = []

        # Critical completeness issues
        critical_columns = [(col, stats) for col, stats in column_stats.items()
                          if stats["quality_flag"] == "Critical"]

        if critical_columns:
            worst_column = min(critical_columns, key=lambda x: x[1]["completeness_rate"])
            issues.append(f"Critical: '{worst_column[0]}' only {worst_column[1]['completeness_rate']}% complete")

        # Overall completeness issues
        if facility_metrics["overall_completeness"] < 70:
            issues.append(f"Overall data completeness at {facility_metrics['overall_completeness']}% - below acceptable threshold")

        # List field complexity
        if facility_metrics["columns_with_lists"] > 5:
            issues.append(f"{facility_metrics['columns_with_lists']} columns contain list values - requires special handling")

        # Data type inconsistencies
        mixed_type_columns = [col for col, stats in column_stats.items()
                            if len(stats["data_types"]) > 2]
        if mixed_type_columns:
            issues.append(f"{len(mixed_type_columns)} columns have mixed data types")

        return issues

    def _generate_cross_facility_insights(self, facility_analyses: Dict) -> Dict[str, Any]:
        """EDA Step 2: Cross-facility comparative analysis"""

        insights = {
            "facility_rankings": [],
            "common_issues": [],
            "best_practices": [],
            "improvement_opportunities": []
        }

        # Rank facilities by data quality
        facility_scores = []
        for facility_id, analysis in facility_analyses.items():
            if "error" not in analysis:
                facility_scores.append({
                    "facility": facility_id,
                    "score": analysis["data_quality_score"]["score"],
                    "grade": analysis["data_quality_score"]["grade"],
                    "completeness": analysis["facility_metrics"]["overall_completeness"]
                })

        facility_scores.sort(key=lambda x: x["score"], reverse=True)
        insights["facility_rankings"] = facility_scores

        # Identify common issues across facilities
        all_issues = []
        for analysis in facility_analyses.values():
            if "error" not in analysis:
                all_issues.extend(analysis["key_issues"])

        # Find patterns in issues
        issue_patterns = defaultdict(int)
        for issue in all_issues:
            if "Critical:" in issue:
                issue_patterns["Critical completeness issues"] += 1
            elif "Overall data completeness" in issue:
                issue_patterns["Low overall completeness"] += 1
            elif "list values" in issue:
                issue_patterns["Complex list fields"] += 1
            elif "mixed data types" in issue:
                issue_patterns["Data type inconsistencies"] += 1

        insights["common_issues"] = [
            f"{pattern}: affects {count} facilities"
            for pattern, count in issue_patterns.items() if count > 1
        ]

        # Best practices from top performer
        if facility_scores:
            best_facility = facility_scores[0]
            insights["best_practices"] = [
                f"Best performer: {best_facility['facility']} ({best_facility['score']}% data quality)",
                f"Target benchmark: {best_facility['completeness']}% overall completeness"
            ]

        # Improvement opportunities
        if len(facility_scores) >= 2:
            worst_facility = facility_scores[-1]
            gap = best_facility["score"] - worst_facility["score"]
            insights["improvement_opportunities"] = [
                f"Largest improvement opportunity: {worst_facility['facility']} ({gap:.1f}% gap)",
                f"Average data quality: {sum(f['score'] for f in facility_scores) / len(facility_scores):.1f}%"
            ]

        return insights

    def _generate_executive_summary(self, facility_analyses: Dict, cross_insights: Dict) -> Dict[str, Any]:
        """EDA Step 3: Executive summary for manager presentation"""

        valid_analyses = [a for a in facility_analyses.values() if "error" not in a]
        total_facilities = len(valid_analyses)

        if total_facilities == 0:
            return {
                "error": "No valid facility data found for analysis",
                "total_facilities_analyzed": 0,
                "recommendations": [
                    "Verify data directory path and file availability",
                    "Check data file format and structure",
                    "Ensure facility data files are properly named (*.json)"
                ]
            }

        # Key metrics
        scores = [a["data_quality_score"]["score"] for a in valid_analyses]
        avg_quality = sum(scores) / len(scores)

        completeness_rates = [a["facility_metrics"]["overall_completeness"] for a in valid_analyses]
        avg_completeness = sum(completeness_rates) / len(completeness_rates)

        return {
            "total_facilities_analyzed": total_facilities,
            "average_data_quality": round(avg_quality, 1),
            "average_completeness": round(avg_completeness, 1),
            "overall_grade": self._calculate_data_quality_score({"dummy": {"completeness_rate": avg_quality}})["grade"],
            "top_performer": cross_insights["facility_rankings"][0] if cross_insights.get("facility_rankings") else None,
            "bottom_performer": cross_insights["facility_rankings"][-1] if cross_insights.get("facility_rankings") else None,
            "critical_issues_count": len(cross_insights.get("common_issues", [])),
            "business_impact": self._assess_business_impact(avg_quality, cross_insights)
        }

    def _assess_business_impact(self, avg_quality: float, cross_insights: Dict) -> str:
        """Assess business impact of data quality findings"""

        if avg_quality >= 85:
            return "Low risk - Data supports reliable business decisions"
        elif avg_quality >= 70:
            return "Medium risk - Some analysis limitations, manageable with data cleaning"
        elif avg_quality >= 50:
            return "High risk - Significant data quality issues impact decision-making reliability"
        else:
            return "Critical risk - Data quality too poor for reliable business analysis"

    def _generate_ppt_slides(self, facility_analyses: Dict, cross_insights: Dict) -> Dict[str, Any]:
        """EDA Step 4: Generate PPT-ready slide content"""

        slides = {}

        # Generate 1-2 slides per facility
        for facility_id, analysis in facility_analyses.items():
            if "error" in analysis:
                continue

            facility_slides = self._create_facility_slides(facility_id, analysis)
            slides[facility_id] = facility_slides

        # Add summary slide
        slides["cross_facility_summary"] = self._create_summary_slide(cross_insights)

        return slides

    def _create_facility_slides(self, facility_id: str, analysis: Dict) -> List[Dict]:
        """Create 1-2 slides per facility with stakeholder questions"""

        slides = []

        # Slide 1: Data Quality Overview
        slide1 = {
            "title": f"Data Quality Analysis: {facility_id}",
            "key_metrics": {
                "Overall Data Quality": f"{analysis['data_quality_score']['score']}% (Grade {analysis['data_quality_score']['grade']})",
                "Data Completeness": f"{analysis['facility_metrics']['overall_completeness']}%",
                "Total Records": analysis['total_records'],
                "Critical Issues": len(analysis['key_issues'])
            },
            "quality_distribution": analysis['facility_metrics']['data_quality_distribution'],
            "stakeholder_questions": [
                f"Are we comfortable with {analysis['data_quality_score']['score']}% data quality for business decisions?",
                f"What impact does {100 - analysis['facility_metrics']['overall_completeness']}% missing data have on our analysis capability?",
                "Which business processes are creating these data gaps?"
            ]
        }
        slides.append(slide1)

        # Slide 2: Issues & Actions (if significant issues exist)
        if analysis['key_issues']:
            slide2 = {
                "title": f"Critical Issues & Actions: {facility_id}",
                "top_issues": analysis['key_issues'][:3],
                "business_impact": analysis['data_quality_score']['interpretation'],
                "immediate_actions": [
                    "Investigate root causes of missing data patterns",
                    "Implement data validation at source systems",
                    "Establish data quality monitoring dashboard"
                ],
                "stakeholder_questions": [
                    "What resources are needed to address these data quality issues?",
                    "How quickly can we implement data validation improvements?",
                    "What is the cost of continuing with current data quality levels?"
                ]
            }
            slides.append(slide2)

        return slides

    def _create_summary_slide(self, cross_insights: Dict) -> Dict:
        """Create cross-facility summary slide"""

        return {
            "title": "Cross-Facility Data Quality Summary",
            "facility_rankings": cross_insights['facility_rankings'][:3],  # Top 3
            "common_issues": cross_insights['common_issues'],
            "improvement_opportunities": cross_insights['improvement_opportunities'],
            "stakeholder_questions": [
                "Should we standardize data collection processes across all facilities?",
                "How can our best-performing facility share practices with others?",
                "What is our data quality improvement roadmap and timeline?",
                "What budget is needed for data quality initiatives?"
            ]
        }

def main():
    """Main execution function for manager reporting"""

    parser = argparse.ArgumentParser(
        description="Basic Data Statistics Analysis - Manager Report"
    )
    parser.add_argument("--data-dir", type=str, help="Data directory path")
    parser.add_argument("--output-dir", type=str, default="./manager_reports",
                       help="Output directory for reports")
    parser.add_argument("--format", choices=["json", "summary"], default="summary",
                       help="Output format: full json or summary")

    args = parser.parse_args()

    try:
        # Initialize analyzer
        analyzer = BasicDataStatistics(args.data_dir)

        # Conduct analysis
        results = analyzer.analyze_all_facilities()

        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True)

        if args.format == "json":
            # Save full results
            output_file = output_dir / "basic_data_statistics_full.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Full analysis saved: {output_file}")

        else:
            # Display manager summary
            summary = results["executive_summary"]

            print("\n" + "="*60)
            print("BASIC DATA STATISTICS - MANAGER SUMMARY")
            print("="*60)

            if "error" in summary:
                print(f"\n❌ ANALYSIS ERROR:")
                print(f"  • {summary['error']}")
                print(f"\n📋 RECOMMENDATIONS:")
                for rec in summary.get("recommendations", []):
                    print(f"  • {rec}")
                return 1

            print(f"\n📊 ANALYSIS OVERVIEW:")
            print(f"  • Facilities Analyzed: {summary['total_facilities_analyzed']}")
            print(f"  • Average Data Quality: {summary['average_data_quality']}% (Grade {summary['overall_grade']})")
            print(f"  • Average Completeness: {summary['average_completeness']}%")

            if summary.get('top_performer'):
                print(f"\n🏆 PERFORMANCE:")
                print(f"  • Best: {summary['top_performer']['facility']} ({summary['top_performer']['score']}%)")
                print(f"  • Worst: {summary['bottom_performer']['facility']} ({summary['bottom_performer']['score']}%)")

            print(f"\n⚠️  BUSINESS IMPACT:")
            print(f"  • {summary['business_impact']}")

            # Save summary for PPT
            summary_file = output_dir / "manager_summary.json"
            with open(summary_file, 'w') as f:
                json.dump(results["ppt_slides"], f, indent=2, default=str)
            print(f"\n📋 PPT content saved: {summary_file}")

        return 0

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        print(f"❌ Analysis failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())

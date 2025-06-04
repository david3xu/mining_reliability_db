#!/usr/bin/env python3
"""
Merge Process Demonstration Script

This script demonstrates how to use the comprehensive merge system
with different types of datasets and configurations.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from scripts.data_processing.comprehensive_dataset_analyzer import ComprehensiveDatasetAnalyzer
from scripts.data_processing.merge_records import RecordMerger
from scripts.data_processing.validate_merge import MergeValidator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def demonstrate_analysis_workflow(input_file: str, output_dir: str) -> Dict[str, Any]:
    """
    Demonstrate the complete analysis workflow.
    """
    logger.info("🔍 Starting dataset analysis demonstration...")

    analyzer = ComprehensiveDatasetAnalyzer()

    # Load and analyze data
    logger.info(f"📂 Loading data from: {input_file}")
    data = analyzer.load_data(input_file)

    if not data:
        logger.error("❌ Failed to load data")
        return {}

    logger.info(f"📊 Analyzing {len(data)} records...")
    analysis_results = analyzer.analyze_dataset(data, Path(input_file).stem)

    # Generate report
    output_file = Path(output_dir) / f"demo_analysis_{Path(input_file).stem}.json"
    analyzer.generate_analysis_report(analysis_results, str(output_file))

    # Print summary
    print("\n" + "=" * 60)
    print("DATASET ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Dataset: {Path(input_file).name}")
    print(f"Records: {analysis_results['basic_info']['total_records']}")
    print(f"Fields: {analysis_results['basic_info']['total_fields']}")
    print(f"Duplicates: {analysis_results['duplicate_analysis']['duplicate_groups']}")
    print(f"Merge Feasibility: {analysis_results['merge_recommendations']['feasibility']}")
    print("=" * 60)

    return analysis_results


def demonstrate_merge_workflow(input_file: str, output_dir: str) -> Dict[str, Any]:
    """
    Demonstrate the complete merge workflow.
    """
    logger.info("🔧 Starting merge process demonstration...")

    merger = RecordMerger()

    # Process data
    logger.info(f"📂 Processing data from: {input_file}")
    output_file = Path(output_dir) / f"demo_merged_{Path(input_file).stem}.json"
    report_file = Path(output_dir) / f"demo_merge_report_{Path(input_file).stem}.json"

    merge_results = merger.process_data(input_file, str(output_file), str(report_file))

    # Print summary
    print("\n" + "=" * 60)
    print("MERGE PROCESS SUMMARY")
    print("=" * 60)
    print(f"Original Records: {merge_results['original_records']}")
    print(f"Final Records: {merge_results['final_records']}")
    print(f"Duplicates Merged: {merge_results['duplicates_merged']}")
    print(f"Complexity Distribution: {merge_results['complexity_distribution']}")
    print(f"Strategies Used: {merge_results['merge_strategies_used']}")
    print("=" * 60)

    return merge_results


def demonstrate_validation_workflow(
    original_file: str, merged_file: str, report_file: str, output_dir: str
) -> Dict[str, Any]:
    """
    Demonstrate the validation workflow.
    """
    logger.info("✅ Starting validation demonstration...")

    validator = MergeValidator()

    # Validate merge results
    output_file = Path(output_dir) / f"demo_validation_{Path(original_file).stem}.json"
    validation_results = validator.validate_merge_results(original_file, merged_file, report_file)

    # Generate validation report
    validator.generate_validation_report(validation_results, str(output_file))

    return validation_results


def create_sample_dataset() -> str:
    """
    Create a sample dataset for demonstration purposes.
    """
    sample_data = [
        {
            "ID": "DEMO-001",
            "Title": "Equipment Issue A",
            "Action_Plan": ["Inspect equipment", "Replace parts"],
            "Root_Cause": ["Wear and tear"],
            "Status": "Open",
            "Comments": "Initial inspection needed",
            "Priority": "High",
            "Due_Date": "2024-01-15",
            "Amount": 1500,
            "Complete": "No",
        },
        {
            "ID": "DEMO-001",  # Duplicate
            "Title": "Equipment Issue A",
            "Action_Plan": ["Perform maintenance", "Update documentation"],
            "Root_Cause": ["Poor maintenance", "Old equipment"],
            "Status": "In Progress",
            "Comments": "Maintenance scheduled | Parts ordered",
            "Priority": "High",
            "Due_Date": "2024-01-20",
            "Amount": 2000,
            "Complete": "No",
        },
        {
            "ID": "DEMO-002",
            "Title": "Safety Protocol Update",
            "Action_Plan": ["Review protocols"],
            "Root_Cause": ["Outdated procedures"],
            "Status": "Complete",
            "Comments": "Review completed successfully",
            "Priority": "Medium",
            "Due_Date": "2024-01-10",
            "Amount": 500,
            "Complete": "Yes",
        },
    ]

    # Save sample data
    output_file = Path("data/sample_demo_dataset.json")
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(sample_data, f, indent=2)

    logger.info(f"📝 Created sample dataset: {output_file}")
    return str(output_file)


def main():
    """
    Main demonstration function.
    """
    print("\n" + "=" * 80)
    print("COMPREHENSIVE MERGE PROCESS DEMONSTRATION")
    print("=" * 80)

    # Setup
    output_dir = Path("data/exports")
    output_dir.mkdir(exist_ok=True)

    # Option 1: Use sample dataset
    logger.info("🎯 Creating sample dataset for demonstration...")
    sample_file = create_sample_dataset()

    # Step 1: Analyze dataset
    print("\n🔍 STEP 1: DATASET ANALYSIS")
    analysis_results = demonstrate_analysis_workflow(sample_file, str(output_dir))

    # Step 2: Merge records
    print("\n🔧 STEP 2: RECORD MERGING")
    merge_results = demonstrate_merge_workflow(sample_file, str(output_dir))

    # Step 3: Validate results
    print("\n✅ STEP 3: VALIDATION")
    merged_file = str(output_dir / f"demo_merged_{Path(sample_file).stem}.json")
    report_file = str(output_dir / f"demo_merge_report_{Path(sample_file).stem}.json")
    validation_results = demonstrate_validation_workflow(
        sample_file, merged_file, report_file, str(output_dir)
    )

    # Option 2: Use real mining maintenance data (if available)
    mining_data_file = "data/mining_maintenance_nested.json"
    if Path(mining_data_file).exists():
        print("\n🏭 BONUS: MINING MAINTENANCE DATA ANALYSIS")
        print("Found existing mining maintenance data, running analysis...")
        demonstrate_analysis_workflow(mining_data_file, str(output_dir))

    print("\n" + "=" * 80)
    print("✅ DEMONSTRATION COMPLETE!")
    print("=" * 80)
    print("📁 Output files generated in: data/exports/")
    print("📊 Analysis reports: demo_analysis_*.json")
    print("🔧 Merge results: demo_merged_*.json")
    print("📋 Merge reports: demo_merge_report_*.json")
    print("✅ Validation reports: demo_validation_*.json")
    print("=" * 80)


if __name__ == "__main__":
    main()

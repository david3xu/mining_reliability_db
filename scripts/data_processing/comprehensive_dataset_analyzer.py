#!/usr/bin/env python3
"""
Comprehensive Dataset Analyzer

This script performs thorough analysis of any dataset to understand:
1. Data structure and format
2. Field characteristics and patterns
3. Duplicate detection strategies
4. Data quality assessment
5. Merge complexity estimation
6. Recommended merge strategies

Outputs detailed analysis report to guide merge implementation.
"""

import argparse
import csv
import json
import logging
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ComprehensiveDatasetAnalyzer:
    """
    Analyzes datasets comprehensively to understand structure, patterns, and merge requirements.
    """

    def __init__(self):
        self.analysis_results = {}
        self.field_patterns = {
            "id_patterns": ["id", "number", "key", "identifier", "code", "ref"],
            "date_patterns": [
                "date",
                "time",
                "due",
                "completion",
                "verification",
                "reviewed",
                "created",
                "updated",
            ],
            "status_patterns": [
                "stage",
                "complete",
                "status",
                "satisfactory",
                "effective",
                "state",
            ],
            "list_patterns": ["plan", "cause", "action", "asset", "item", "list"],
            "comment_patterns": [
                "comment",
                "description",
                "happened",
                "requirement",
                "evidence",
                "note",
            ],
            "numeric_patterns": [
                "amount",
                "days",
                "count",
                "quantity",
                "duration",
                "past due",
                "loss",
                "cost",
            ],
            "boolean_patterns": [
                "yes",
                "no",
                "true",
                "false",
                "did",
                "is",
                "are",
                "require",
                "has",
            ],
            "category_patterns": [
                "type",
                "category",
                "class",
                "group",
                "dept",
                "centre",
                "division",
            ],
        }

    def detect_file_format(self, file_path: Path) -> str:
        """Detect the format of the input file."""
        suffix = file_path.suffix.lower()

        if suffix == ".json":
            return "json"
        elif suffix in [".csv", ".tsv"]:
            return "csv"
        elif suffix in [".xlsx", ".xls"]:
            return "excel"
        else:
            # Try to detect by content
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    first_char = f.read(1)
                    if first_char in ["{", "["]:
                        return "json"
                    else:
                        return "csv"
            except:
                return "unknown"

    def load_data(self, file_path: Path) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Load data from various file formats and return normalized records.
        Returns: (records_list, metadata)
        """
        file_format = self.detect_file_format(file_path)
        metadata = {
            "file_path": str(file_path),
            "file_format": file_format,
            "file_size": file_path.stat().st_size,
            "load_timestamp": datetime.now().isoformat(),
        }

        try:
            if file_format == "json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Handle different JSON structures
                if isinstance(data, list):
                    records = data
                    metadata["structure_type"] = "list"
                elif isinstance(data, dict):
                    if "sheets" in data:
                        # Multi-sheet structure
                        metadata["structure_type"] = "multi_sheet"
                        metadata["sheets"] = list(data["sheets"].keys())
                        # For now, take the first sheet with records
                        for sheet_name, sheet_data in data["sheets"].items():
                            if "records" in sheet_data:
                                records = sheet_data["records"]
                                metadata["selected_sheet"] = sheet_name
                                break
                        else:
                            records = []
                    elif "records" in data:
                        records = data["records"]
                        metadata["structure_type"] = "wrapped_records"
                    elif "data" in data:
                        records = data["data"]
                        metadata["structure_type"] = "wrapped_data"
                    else:
                        # Single record or unknown structure
                        records = [data]
                        metadata["structure_type"] = "single_record"
                else:
                    records = []
                    metadata["structure_type"] = "unknown"

            elif file_format == "csv":
                df = pd.read_csv(file_path)
                records = df.to_dict("records")
                metadata["structure_type"] = "csv"
                metadata["columns"] = list(df.columns)

            elif file_format == "excel":
                df = pd.read_excel(file_path)
                records = df.to_dict("records")
                metadata["structure_type"] = "excel"
                metadata["columns"] = list(df.columns)

            else:
                records = []
                metadata["error"] = f"Unsupported file format: {file_format}"

        except Exception as e:
            records = []
            metadata["error"] = f"Failed to load file: {str(e)}"
            logger.error(f"Error loading {file_path}: {e}")

        metadata["record_count"] = len(records)
        return records, metadata

    def analyze_field_characteristics(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze characteristics of each field across all records."""
        if not records:
            return {}

        field_analysis = {}

        # Collect all possible field names
        all_fields = set()
        for record in records:
            all_fields.update(record.keys())

        for field_name in all_fields:
            field_values = [record.get(field_name) for record in records]
            non_null_values = [v for v in field_values if v is not None]

            analysis = {
                "field_name": field_name,
                "total_records": len(field_values),
                "non_null_count": len(non_null_values),
                "null_count": len(field_values) - len(non_null_values),
                "null_percentage": (len(field_values) - len(non_null_values))
                / len(field_values)
                * 100,
                "data_types": {},
                "value_patterns": {},
                "sample_values": [],
                "unique_values_count": 0,
                "is_potential_id": False,
                "is_potential_date": False,
                "is_potential_status": False,
                "is_potential_numeric": False,
                "is_potential_boolean": False,
                "is_potential_list": False,
                "suggested_merge_strategy": "unknown",
            }

            # Analyze data types
            type_counter = Counter()
            for value in non_null_values:
                type_counter[type(value).__name__] += 1
            analysis["data_types"] = dict(type_counter)

            # Analyze unique values
            if non_null_values:
                # Convert to string for uniqueness check
                str_values = [str(v) for v in non_null_values]
                unique_values = set(str_values)
                analysis["unique_values_count"] = len(unique_values)
                analysis["uniqueness_ratio"] = len(unique_values) / len(non_null_values)

                # Sample values (first few unique ones)
                analysis["sample_values"] = list(unique_values)[:10]
            else:
                # Handle case with no non-null values
                analysis["uniqueness_ratio"] = 0.0

            # Detect field patterns
            self._detect_field_patterns(field_name, non_null_values, analysis)

            # Suggest merge strategy
            analysis["suggested_merge_strategy"] = self._suggest_merge_strategy(
                field_name, analysis
            )

            field_analysis[field_name] = analysis

        return field_analysis

    def _detect_field_patterns(
        self, field_name: str, values: List[Any], analysis: Dict[str, Any]
    ) -> None:
        """Detect patterns in field values to classify field types."""
        field_lower = field_name.lower()

        # ID field detection
        if any(pattern in field_lower for pattern in self.field_patterns["id_patterns"]):
            analysis["is_potential_id"] = True
            if analysis.get("uniqueness_ratio", 0) > 0.95:  # High uniqueness suggests ID
                analysis["is_potential_id"] = True

        # Date field detection
        if any(pattern in field_lower for pattern in self.field_patterns["date_patterns"]):
            analysis["is_potential_date"] = True
            # Try to parse some values as dates
            date_count = 0
            for value in values[:10]:  # Sample first 10
                if self._try_parse_date(str(value)):
                    date_count += 1
            if date_count > 5:  # More than half are parseable as dates
                analysis["is_potential_date"] = True

        # Status field detection
        if any(pattern in field_lower for pattern in self.field_patterns["status_patterns"]):
            analysis["is_potential_status"] = True
            # Check if values look like status values
            if analysis["unique_values_count"] < 20 and all(
                isinstance(v, str) for v in values[:10]
            ):
                analysis["is_potential_status"] = True

        # Numeric field detection
        if any(pattern in field_lower for pattern in self.field_patterns["numeric_patterns"]):
            analysis["is_potential_numeric"] = True
        numeric_count = 0
        for value in values[:20]:
            try:
                float(str(value))
                numeric_count += 1
            except:
                pass
        if numeric_count > len(values[:20]) * 0.8:  # 80% numeric
            analysis["is_potential_numeric"] = True

        # Boolean field detection
        if any(pattern in field_lower for pattern in self.field_patterns["boolean_patterns"]):
            analysis["is_potential_boolean"] = True
        bool_values = {"yes", "no", "true", "false", "y", "n", "1", "0"}
        if all(str(v).lower() in bool_values for v in values[:10]):
            analysis["is_potential_boolean"] = True

        # List field detection
        if any(pattern in field_lower for pattern in self.field_patterns["list_patterns"]):
            analysis["is_potential_list"] = True
        if any(isinstance(v, list) for v in values[:10]):
            analysis["is_potential_list"] = True

    def _try_parse_date(self, date_str: str) -> bool:
        """Try to parse a string as a date."""
        date_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%Y%m%d",
            "%d-%m-%Y",
        ]

        for fmt in date_formats:
            try:
                datetime.strptime(str(date_str).strip(), fmt)
                return True
            except:
                continue
        return False

        for fmt in date_formats:
            try:
                datetime.strptime(date_str.strip(), fmt)
                return True
            except:
                continue
        return False

    def _suggest_merge_strategy(self, field_name: str, analysis: Dict[str, Any]) -> str:
        """Suggest appropriate merge strategy based on field analysis."""
        # Priority order of detection
        if analysis["is_potential_id"] and analysis.get("uniqueness_ratio", 0) > 0.95:
            return "primary_key"
        elif analysis["is_potential_list"]:
            return "merge_lists"
        elif analysis["is_potential_date"]:
            return "latest_date"
        elif analysis["is_potential_status"]:
            return "prioritize_status"
        elif analysis["is_potential_numeric"]:
            return "max_numeric"
        elif analysis["is_potential_boolean"]:
            return "prioritize_yes"
        elif "comment" in field_name.lower() or "description" in field_name.lower():
            return "concatenate_strings"
        elif analysis["null_percentage"] < 10:  # Low null rate
            return "first_non_null"
        else:
            return "first_non_null"

    def detect_potential_duplicates(
        self, records: List[Dict[str, Any]], field_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Detect potential duplicate records and analyze duplicate patterns."""
        if not records:
            return {}

        # Find potential ID fields
        id_candidates = []
        for field_name, analysis in field_analysis.items():
            if (
                analysis["is_potential_id"]
                or analysis.get("uniqueness_ratio", 0) > 0.9
                or "id" in field_name.lower()
                or "number" in field_name.lower()
            ):
                id_candidates.append(
                    {
                        "field_name": field_name,
                        "uniqueness_ratio": analysis.get("uniqueness_ratio", 0),
                        "confidence": self._calculate_id_confidence(analysis),
                    }
                )

        # Sort by confidence
        id_candidates.sort(key=lambda x: x["confidence"], reverse=True)

        duplicate_analysis = {"id_candidates": id_candidates, "duplicate_groups": {}, "summary": {}}

        # Analyze duplicates for each ID candidate
        for candidate in id_candidates[:3]:  # Check top 3 candidates
            field_name = candidate["field_name"]
            groups = defaultdict(list)

            for i, record in enumerate(records):
                key_value = record.get(field_name)
                if key_value is not None:
                    groups[str(key_value)].append((i, record))

            # Find groups with multiple records
            duplicates = {k: v for k, v in groups.items() if len(v) > 1}

            if duplicates:
                duplicate_analysis["duplicate_groups"][field_name] = {
                    "total_groups": len(groups),
                    "duplicate_groups": len(duplicates),
                    "total_duplicates": sum(len(v) - 1 for v in duplicates.values()),
                    "examples": self._analyze_duplicate_examples(duplicates, field_analysis),
                    "complexity_assessment": self._assess_duplicate_complexity(
                        duplicates, field_analysis
                    ),
                }

        # Summary statistics
        if duplicate_analysis["duplicate_groups"]:
            # Find the best field with actual duplicates
            best_dup_field = None
            best_dup_data = None

            # First try the highest confidence ID field that has duplicates
            for candidate in id_candidates:
                field_name = candidate["field_name"]
                if field_name in duplicate_analysis["duplicate_groups"]:
                    best_dup_field = field_name
                    best_dup_data = duplicate_analysis["duplicate_groups"][field_name]
                    break

            # If no ID candidate has duplicates, use the field with most duplicates
            if not best_dup_field:
                max_duplicates = 0
                for field_name, dup_data in duplicate_analysis["duplicate_groups"].items():
                    if dup_data["total_duplicates"] > max_duplicates:
                        max_duplicates = dup_data["total_duplicates"]
                        best_dup_field = field_name
                        best_dup_data = dup_data

            if best_dup_field and best_dup_data:
                duplicate_analysis["summary"] = {
                    "recommended_id_field": best_dup_field,
                    "total_records": len(records),
                    "unique_records": best_dup_data["total_groups"],
                    "duplicate_records": best_dup_data["total_duplicates"],
                    "duplicate_groups": best_dup_data["duplicate_groups"],
                    "deduplication_potential": best_dup_data["total_duplicates"],
                    "complexity": best_dup_data["complexity_assessment"]["overall_complexity"],
                }

        return duplicate_analysis

    def _calculate_id_confidence(self, field_analysis: Dict[str, Any]) -> float:
        """Calculate confidence that a field is an ID field."""
        confidence = 0.0

        # High uniqueness suggests ID
        confidence += field_analysis.get("uniqueness_ratio", 0) * 0.4

        # Low null rate suggests ID
        confidence += (1 - field_analysis["null_percentage"] / 100) * 0.3

        # Name pattern match
        if field_analysis["is_potential_id"]:
            confidence += 0.3

        return min(1.0, confidence)

    def _analyze_duplicate_examples(
        self, duplicates: Dict[str, List], field_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze examples of duplicate groups to understand differences."""
        examples = []

        for dup_key, records_list in list(duplicates.items())[:3]:  # First 3 examples
            if len(records_list) < 2:
                continue

            example = {
                "duplicate_key": dup_key,
                "record_count": len(records_list),
                "differing_fields": {},
                "field_differences": [],
            }

            # Compare all fields across records in this duplicate group
            all_fields = set()
            for _, record in records_list:
                all_fields.update(record.keys())

            for field_name in all_fields:
                values = [record.get(field_name) for _, record in records_list]

                # Normalize for comparison
                normalized_values = []
                for value in values:
                    if isinstance(value, list):
                        normalized_values.append(tuple(sorted(str(item) for item in value)))
                    else:
                        normalized_values.append(str(value) if value is not None else None)

                unique_values = list(set(normalized_values))

                if len(unique_values) > 1:
                    example["differing_fields"][field_name] = {
                        "unique_count": len(unique_values),
                        "values": values[:3],  # First 3 values as examples
                        "suggested_strategy": field_analysis.get(field_name, {}).get(
                            "suggested_merge_strategy", "unknown"
                        ),
                    }
                    example["field_differences"].append(field_name)

            examples.append(example)

        return examples

    def _assess_duplicate_complexity(
        self, duplicates: Dict[str, List], field_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess the complexity of merging duplicate records."""
        total_differing_fields = 0
        high_risk_fields = 0
        merge_strategies = Counter()

        # Analyze a sample of duplicate groups
        sample_groups = list(duplicates.items())[:10]

        for _, records_list in sample_groups:
            if len(records_list) < 2:
                continue

            # Count differing fields in this group
            all_fields = set()
            for _, record in records_list:
                all_fields.update(record.keys())

            group_differing_fields = 0
            for field_name in all_fields:
                values = [record.get(field_name) for _, record in records_list]
                if len(set(str(v) for v in values)) > 1:
                    group_differing_fields += 1

                    # Track merge strategies
                    strategy = field_analysis.get(field_name, {}).get(
                        "suggested_merge_strategy", "unknown"
                    )
                    merge_strategies[strategy] += 1

                    # Identify high-risk fields
                    if (
                        strategy in ["unknown", "concatenate_strings"]
                        or field_analysis.get(field_name, {}).get("unique_values_count", 0) > 50
                    ):
                        high_risk_fields += 1

            total_differing_fields += group_differing_fields

        avg_differing_fields = total_differing_fields / len(sample_groups) if sample_groups else 0

        # Determine complexity level
        if avg_differing_fields < 2:
            complexity = "low"
        elif avg_differing_fields < 5:
            complexity = "medium"
        else:
            complexity = "high"

        return {
            "overall_complexity": complexity,
            "avg_differing_fields_per_group": avg_differing_fields,
            "high_risk_fields": high_risk_fields,
            "merge_strategies_needed": dict(merge_strategies),
            "sample_size": len(sample_groups),
        }

    def generate_merge_recommendations(
        self, field_analysis: Dict[str, Any], duplicate_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive merge recommendations."""
        recommendations = {
            "merge_feasibility": "unknown",
            "recommended_approach": {},
            "field_strategies": {},
            "risk_assessment": {},
            "implementation_steps": [],
            "validation_requirements": [],
        }

        if not duplicate_analysis.get("summary"):
            recommendations["merge_feasibility"] = "no_duplicates"
            recommendations["recommended_approach"] = {
                "action": "no_action_needed",
                "reason": "No duplicate records detected",
            }
            return recommendations

        summary = duplicate_analysis["summary"]
        complexity = summary.get("complexity", "unknown")

        # Assess feasibility
        if summary["duplicate_records"] == 0:
            recommendations["merge_feasibility"] = "no_duplicates"
        elif complexity == "low":
            recommendations["merge_feasibility"] = "high"
        elif complexity == "medium":
            recommendations["merge_feasibility"] = "medium"
        else:
            recommendations["merge_feasibility"] = "low"

        # Recommended approach
        if recommendations["merge_feasibility"] in ["high", "medium"]:
            recommendations["recommended_approach"] = {
                "action": "automated_merge",
                "id_field": summary["recommended_id_field"],
                "expected_reduction": summary["duplicate_records"],
                "complexity_level": complexity,
            }
        else:
            recommendations["recommended_approach"] = {
                "action": "manual_review",
                "reason": "High complexity or risk detected",
                "complexity_level": complexity,
            }

        # Field-specific strategies
        for field_name, analysis in field_analysis.items():
            recommendations["field_strategies"][field_name] = {
                "strategy": analysis["suggested_merge_strategy"],
                "confidence": "high" if analysis["null_percentage"] < 20 else "medium",
                "risk_level": self._assess_field_risk(analysis),
            }

        # Risk assessment
        high_risk_count = sum(
            1
            for strategy in recommendations["field_strategies"].values()
            if strategy["risk_level"] == "high"
        )

        recommendations["risk_assessment"] = {
            "overall_risk": "high"
            if high_risk_count > 5
            else "medium"
            if high_risk_count > 2
            else "low",
            "high_risk_fields": high_risk_count,
            "data_loss_potential": "high" if complexity == "high" else "low",
            "validation_complexity": complexity,
        }

        # Implementation steps
        if recommendations["merge_feasibility"] in ["high", "medium"]:
            recommendations["implementation_steps"] = [
                "Create backup of original data",
                "Implement field-specific merge strategies",
                "Test merge logic on sample data",
                "Validate merge results",
                "Apply merge to full dataset",
                "Generate merge report",
            ]

        # Validation requirements
        recommendations["validation_requirements"] = [
            "Verify no data loss in critical fields",
            "Check merge logic for edge cases",
            "Validate business logic preservation",
            "Test with sample duplicate groups",
            "Review merge metadata for accuracy",
        ]

        return recommendations

    def _assess_field_risk(self, field_analysis: Dict[str, Any]) -> str:
        """Assess the risk level of merging a specific field."""
        strategy = field_analysis["suggested_merge_strategy"]
        null_pct = field_analysis["null_percentage"]
        unique_count = field_analysis["unique_values_count"]

        # High risk conditions
        if strategy == "unknown":
            return "high"
        if null_pct > 50:
            return "high"
        if unique_count > 100 and strategy == "concatenate_strings":
            return "high"

        # Medium risk conditions
        if strategy in ["concatenate_strings", "merge_lists"] and unique_count > 20:
            return "medium"
        if null_pct > 20:
            return "medium"

        return "low"

    def analyze_dataset(self, file_path: Path) -> Dict[str, Any]:
        """Perform comprehensive analysis of a dataset."""
        logger.info(f"Starting comprehensive analysis of {file_path}")

        # Load data
        records, metadata = self.load_data(file_path)

        analysis_results = {
            "metadata": metadata,
            "dataset_overview": {},
            "field_analysis": {},
            "duplicate_analysis": {},
            "merge_recommendations": {},
            "analysis_timestamp": datetime.now().isoformat(),
        }

        if not records:
            analysis_results["error"] = "No records could be loaded from the file"
            return analysis_results

        # Dataset overview
        analysis_results["dataset_overview"] = {
            "total_records": len(records),
            "total_fields": len(records[0].keys()) if records else 0,
            "sample_record": records[0] if records else {},
            "field_names": list(records[0].keys()) if records else [],
        }

        # Field analysis
        logger.info("Analyzing field characteristics...")
        analysis_results["field_analysis"] = self.analyze_field_characteristics(records)

        # Duplicate analysis
        logger.info("Detecting potential duplicates...")
        analysis_results["duplicate_analysis"] = self.detect_potential_duplicates(
            records, analysis_results["field_analysis"]
        )

        # Merge recommendations
        logger.info("Generating merge recommendations...")
        analysis_results["merge_recommendations"] = self.generate_merge_recommendations(
            analysis_results["field_analysis"], analysis_results["duplicate_analysis"]
        )

        logger.info("Analysis complete")
        return analysis_results

    def save_analysis_report(self, analysis_results: Dict[str, Any], output_file: Path) -> None:
        """Save analysis results to a comprehensive report file."""
        # Create a human-readable report
        report = {
            "analysis_summary": self._create_summary_report(analysis_results),
            "detailed_results": analysis_results,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Analysis report saved to {output_file}")

    def _create_summary_report(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a human-readable summary of the analysis."""
        summary = {
            "file_info": {},
            "data_overview": {},
            "duplicate_summary": {},
            "merge_assessment": {},
            "recommendations": {},
        }

        # File info
        metadata = analysis_results.get("metadata", {})
        summary["file_info"] = {
            "file_path": metadata.get("file_path", "Unknown"),
            "file_format": metadata.get("file_format", "Unknown"),
            "file_size_mb": round(metadata.get("file_size", 0) / (1024 * 1024), 2),
            "load_status": "success" if "error" not in metadata else f"error: {metadata['error']}",
        }

        # Data overview
        overview = analysis_results.get("dataset_overview", {})
        summary["data_overview"] = {
            "total_records": overview.get("total_records", 0),
            "total_fields": overview.get("total_fields", 0),
            "data_structure": metadata.get("structure_type", "Unknown"),
        }

        # Duplicate summary
        dup_analysis = analysis_results.get("duplicate_analysis", {})
        dup_summary = dup_analysis.get("summary", {})
        summary["duplicate_summary"] = {
            "duplicates_detected": len(dup_summary) > 0,
            "recommended_id_field": dup_summary.get("recommended_id_field", "None"),
            "total_duplicate_records": dup_summary.get("duplicate_records", 0),
            "duplicate_groups": dup_summary.get("duplicate_groups", 0),
            "deduplication_potential": dup_summary.get("deduplication_potential", 0),
        }

        # Merge assessment
        recommendations = analysis_results.get("merge_recommendations", {})
        summary["merge_assessment"] = {
            "feasibility": recommendations.get("merge_feasibility", "unknown"),
            "complexity": recommendations.get("recommended_approach", {}).get(
                "complexity_level", "unknown"
            ),
            "overall_risk": recommendations.get("risk_assessment", {}).get(
                "overall_risk", "unknown"
            ),
            "high_risk_fields": recommendations.get("risk_assessment", {}).get(
                "high_risk_fields", 0
            ),
        }

        # Recommendations
        approach = recommendations.get("recommended_approach", {})
        summary["recommendations"] = {
            "action": approach.get("action", "unknown"),
            "reason": approach.get("reason", ""),
            "next_steps": recommendations.get("implementation_steps", [])[:3],  # First 3 steps
        }

        return summary


def main():
    """Main function to run comprehensive dataset analysis."""
    parser = argparse.ArgumentParser(
        description="Comprehensive dataset analyzer for merge planning"
    )
    parser.add_argument(
        "--input",
        help="Input file path (relative to project root or absolute). If not provided, analyzes all files in data/facility_data/",
    )
    parser.add_argument(
        "--output-dir",
        default="data/exports",
        help="Output directory for analysis reports (relative to project root)",
    )
    parser.add_argument(
        "--analyze-all",
        action="store_true",
        help="Analyze all files in data/facility_data directory",
    )

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent
    analyzer = ComprehensiveDatasetAnalyzer()

    # Determine input files
    if args.analyze_all or not args.input:
        facility_data_dir = project_root / "data" / "facility_data"
        input_files = list(facility_data_dir.glob("*.json")) + list(facility_data_dir.glob("*.csv"))
        if not input_files:
            logger.error("No data files found in data/facility_data directory")
            sys.exit(1)
        logger.info(f"Found {len(input_files)} files to analyze")
    else:
        input_path = Path(args.input)
        if not input_path.is_absolute():
            input_path = project_root / input_path
        input_files = [input_path]

        if not input_path.exists():
            logger.error(f"Input file not found: {input_path}")
            sys.exit(1)

    # Create output directory
    output_dir = project_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Analyze each file
    for input_file in input_files:
        logger.info(f"\n{'='*60}")
        logger.info(f"Analyzing: {input_file.name}")
        logger.info(f"{'='*60}")

        try:
            # Perform analysis
            analysis_results = analyzer.analyze_dataset(input_file)

            # Generate output filename
            output_filename = (
                f"analysis_{input_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            output_file = output_dir / output_filename

            # Save results
            analyzer.save_analysis_report(analysis_results, output_file)

            # Print summary - use the original analysis_results directly
            overview = analysis_results.get("dataset_overview", {})
            dup_summary = analysis_results.get("duplicate_analysis", {}).get("summary", {})
            recommendations = analysis_results.get("merge_recommendations", {})

            print(f"\n📊 Analysis Summary for {input_file.name}:")
            print(f"   Total Records: {overview.get('total_records', 0)}")
            print(f"   Total Fields: {overview.get('total_fields', 0)}")
            print(f"   Duplicates Found: {dup_summary.get('duplicate_records', 0)}")
            print(f"   Merge Feasibility: {recommendations.get('merge_feasibility', 'unknown')}")
            print(
                f"   Recommended Action: {recommendations.get('recommended_approach', {}).get('action', 'unknown')}"
            )
            print(f"   Analysis Report: {output_file}")

        except Exception as e:
            logger.error(f"Error analyzing {input_file}: {e}")
            continue

    print(f"\n✅ Analysis complete. Reports saved in: {output_dir}")
    print("\n📋 Next Steps:")
    print("1. Review the analysis reports to understand data structure and duplicates")
    print("2. Validate the recommended merge strategies")
    print("3. Provide feedback on the analysis before implementing merge logic")
    print("4. Consider any domain-specific requirements for merging")


if __name__ == "__main__":
    main()

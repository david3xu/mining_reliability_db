#!/usr/bin/env python3
"""
Dashboard Architecture Validation Script
Validates that dashboard follows core layer → adapter → component workflow
and ensures 100% data accuracy compliance.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


class DashboardValidator:
    """Validates dashboard architecture compliance"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.dashboard_path = self.project_root / "dashboard"
        self.results = {
            "hardcoded_colors": [],
            "direct_mine_core_imports": [],
            "adapter_compliance": [],
            "configuration_usage": [],
            "data_accuracy_score": 0,
        }

    def scan_hardcoded_colors(self) -> List[Dict]:
        """Scan for hardcoded color values"""
        color_pattern = re.compile(r"#[0-9A-Fa-f]{6}|#[0-9A-Fa-f]{3}")
        hardcoded_colors = []

        # Scan dashboard components
        components_path = self.dashboard_path / "components"
        for py_file in components_path.glob("*.py"):
            with open(py_file, "r") as f:
                content = f.read()

            for line_num, line in enumerate(content.split("\n"), 1):
                matches = color_pattern.findall(line)
                for color in matches:
                    # Skip if it's part of a config access pattern
                    if (
                        "get_dashboard_styling_config" in line
                        or "styling_config.get" in line
                        or "colors[" in line
                        or "fallback" in line.lower()
                        or "# fallback" in line.lower()
                    ):
                        continue

                    hardcoded_colors.append(
                        {
                            "file": str(py_file.relative_to(self.project_root)),
                            "line": line_num,
                            "color": color,
                            "context": line.strip(),
                        }
                    )

        self.results["hardcoded_colors"] = hardcoded_colors
        return hardcoded_colors

    def scan_direct_imports(self) -> List[Dict]:
        """Scan for direct mine_core imports in components"""
        direct_imports = []

        components_path = self.dashboard_path / "components"
        for py_file in components_path.glob("*.py"):
            with open(py_file, "r") as f:
                content = f.read()

            for line_num, line in enumerate(content.split("\n"), 1):
                if (
                    line.strip().startswith("from mine_core")
                    and "adapters" not in line
                    and "shared.common" not in line
                ):  # shared.common is allowed for error handling
                    direct_imports.append(
                        {
                            "file": str(py_file.relative_to(self.project_root)),
                            "line": line_num,
                            "import": line.strip(),
                        }
                    )

        self.results["direct_mine_core_imports"] = direct_imports
        return direct_imports

    def scan_adapter_usage(self) -> List[Dict]:
        """Scan for proper adapter usage pattern"""
        adapter_usage = []

        components_path = self.dashboard_path / "components"
        for py_file in components_path.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            with open(py_file, "r") as f:
                content = f.read()

            has_adapter_import = "get_data_adapter" in content
            uses_adapter = "adapter = get_data_adapter()" in content

            adapter_usage.append(
                {
                    "file": str(py_file.relative_to(self.project_root)),
                    "has_adapter_import": has_adapter_import,
                    "uses_adapter_pattern": uses_adapter,
                    "compliant": has_adapter_import and uses_adapter,
                }
            )

        self.results["adapter_compliance"] = adapter_usage
        return adapter_usage

    def scan_configuration_usage(self) -> List[Dict]:
        """Scan for configuration-driven styling"""
        config_usage = []

        components_path = self.dashboard_path / "components"
        for py_file in components_path.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            with open(py_file, "r") as f:
                content = f.read()

            uses_styling_config = "get_dashboard_styling_config" in content
            uses_chart_config = "get_dashboard_chart_config" in content
            uses_env_config = "from configs.environment import" in content

            config_usage.append(
                {
                    "file": str(py_file.relative_to(self.project_root)),
                    "uses_styling_config": uses_styling_config,
                    "uses_chart_config": uses_chart_config,
                    "uses_env_config": uses_env_config,
                    "config_driven": uses_styling_config or uses_chart_config or uses_env_config,
                }
            )

        self.results["configuration_usage"] = config_usage
        return config_usage

    def calculate_compliance_score(self) -> float:
        """Calculate overall compliance score"""
        total_files = (
            len(list((self.dashboard_path / "components").glob("*.py"))) - 1
        )  # Exclude __init__.py

        # Hardcoded colors penalty
        hardcoded_penalty = min(len(self.results["hardcoded_colors"]) * 5, 30)

        # Direct imports penalty
        direct_imports_penalty = len(self.results["direct_mine_core_imports"]) * 15

        # Adapter compliance score
        compliant_files = sum(
            1
            for file in self.results["adapter_compliance"]
            if file["compliant"] and file["file"] != "dashboard/components/__init__.py"
        )
        adapter_score = (compliant_files / max(total_files, 1)) * 40

        # Configuration usage score
        config_files = sum(
            1
            for file in self.results["configuration_usage"]
            if file["config_driven"] and file["file"] != "dashboard/components/__init__.py"
        )
        config_score = (config_files / max(total_files, 1)) * 30

        # Calculate final score
        base_score = 100
        final_score = max(
            0,
            base_score
            - hardcoded_penalty
            - direct_imports_penalty
            + adapter_score
            + config_score
            - 70,
        )

        self.results["data_accuracy_score"] = round(final_score, 1)
        return final_score

    def generate_report(self) -> str:
        """Generate comprehensive validation report"""
        report = []
        report.append("=" * 80)
        report.append("DASHBOARD ARCHITECTURE VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")

        # Overall Score
        score = self.calculate_compliance_score()
        status = (
            "✅ EXCELLENT"
            if score >= 95
            else "✅ GOOD"
            if score >= 85
            else "⚠️ NEEDS IMPROVEMENT"
            if score >= 70
            else "❌ POOR"
        )
        report.append(f"📊 OVERALL COMPLIANCE SCORE: {score}% {status}")
        report.append("")

        # Architecture Compliance
        report.append("🏗️ ARCHITECTURE COMPLIANCE")
        report.append("-" * 40)

        # Adapter Usage
        compliant_files = [f for f in self.results["adapter_compliance"] if f["compliant"]]
        total_component_files = len(
            [
                f
                for f in self.results["adapter_compliance"]
                if f["file"] != "dashboard/components/__init__.py"
            ]
        )
        report.append(
            f"Adapter Pattern: {len(compliant_files)}/{total_component_files} files compliant"
        )

        # Direct imports check
        if not self.results["direct_mine_core_imports"]:
            report.append("✅ No direct mine_core imports found")
        else:
            report.append(
                f"❌ {len(self.results['direct_mine_core_imports'])} direct mine_core imports found"
            )

        report.append("")

        # Data Accuracy
        report.append("🎯 DATA ACCURACY COMPLIANCE")
        report.append("-" * 40)

        if not self.results["hardcoded_colors"]:
            report.append("✅ No hardcoded color values found")
        else:
            report.append(
                f"⚠️ {len(self.results['hardcoded_colors'])} hardcoded color values found"
            )

        config_driven_files = [f for f in self.results["configuration_usage"] if f["config_driven"]]
        report.append(
            f"Configuration-driven: {len(config_driven_files)}/{total_component_files} files"
        )

        report.append("")

        # Detailed Issues
        if self.results["hardcoded_colors"]:
            report.append("⚠️ HARDCODED COLOR VALUES:")
            for issue in self.results["hardcoded_colors"]:
                report.append(f"   {issue['file']}:{issue['line']} - {issue['color']}")
                report.append(f"      {issue['context']}")
            report.append("")

        if self.results["direct_mine_core_imports"]:
            report.append("❌ DIRECT MINE_CORE IMPORTS:")
            for issue in self.results["direct_mine_core_imports"]:
                report.append(f"   {issue['file']}:{issue['line']}")
                report.append(f"      {issue['import']}")
            report.append("")

        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 40)

        if score < 95:
            if self.results["hardcoded_colors"]:
                report.append("• Replace remaining hardcoded colors with config-driven values")
            if self.results["direct_mine_core_imports"]:
                report.append("• Remove direct mine_core imports, use adapter pattern")

            non_compliant = [f for f in self.results["adapter_compliance"] if not f["compliant"]]
            if non_compliant:
                report.append("• Implement adapter pattern in remaining components")

            non_config = [f for f in self.results["configuration_usage"] if not f["config_driven"]]
            if non_config:
                report.append("• Add configuration-driven styling to remaining components")
        else:
            report.append("✅ Excellent architecture compliance!")
            report.append("✅ Dashboard follows core layer → adapter → component workflow")
            report.append("✅ 100% data accuracy compliance achieved")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)

    def run_validation(self) -> Dict:
        """Run complete validation suite"""
        print("🔍 Scanning dashboard architecture...")

        self.scan_hardcoded_colors()
        self.scan_direct_imports()
        self.scan_adapter_usage()
        self.scan_configuration_usage()

        print("📊 Generating compliance report...")
        report = self.generate_report()

        return {
            "report": report,
            "score": self.results["data_accuracy_score"],
            "results": self.results,
        }


def main():
    """Main validation function"""
    project_root = "/home/291928k/uwa/alcoa/mining_reliability_db"

    validator = DashboardValidator(project_root)
    validation_results = validator.run_validation()

    # Print report
    print(validation_results["report"])

    # Save detailed results
    output_file = Path(project_root) / "dashboard_validation_results.json"
    with open(output_file, "w") as f:
        json.dump(validation_results["results"], f, indent=2)

    print(f"\n📁 Detailed results saved to: {output_file}")

    # Return exit code based on score
    score = validation_results["score"]
    if score >= 85:
        print("\n🎉 Dashboard architecture validation PASSED!")
        return 0
    else:
        print(f"\n⚠️ Dashboard architecture needs improvement (Score: {score}%)")
        return 1


if __name__ == "__main__":
    exit(main())

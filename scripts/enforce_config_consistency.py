#!/usr/bin/env python3
"""
Configuration Consistency Enforcement
Automated validation and enforcement of configuration naming standards.
"""

import ast
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple


@dataclass
class NamingRule:
    """Configuration naming convention rule"""

    pattern: str
    description: str
    enforce_prefix: bool = True
    allowed_suffixes: List[str] = None


@dataclass
class ConsistencyViolation:
    """Detected consistency violation"""

    file_path: str
    method_name: str
    violation_type: str
    suggested_fix: str
    severity: str


class ConfigConsistencyEnforcer:
    """Enforce configuration consistency across adapters and environment"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.violations: List[ConsistencyViolation] = []

        # Define naming conventions
        self.naming_rules = {
            "config_methods": NamingRule(
                pattern="get_.*_config",
                description="Configuration access methods must use get_<subject>_config pattern",
                allowed_suffixes=["_config"],
            ),
            "styling_methods": NamingRule(
                pattern="get_.*_styling",
                description="Styling access methods must use get_<subject>_styling pattern",
                allowed_suffixes=["_styling", "_styling_config"],
            ),
            "chart_methods": NamingRule(
                pattern="get_.*chart.*",
                description="Chart-related methods must include 'chart' in name",
                enforce_prefix=False,
            ),
        }

    def enforce_adapter_environment_consistency(self) -> Dict[str, List[ConsistencyViolation]]:
        """Enforce consistency between adapter methods and environment functions"""

        # Get method mappings
        adapter_file = self.project_root / "dashboard/adapters/config_adapter.py"
        env_file = self.project_root / "configs/environment.py"

        adapter_methods = self._extract_methods_from_file(adapter_file)
        env_functions = self._extract_functions_from_file(env_file)

        # Check for consistency violations
        self._check_method_function_mapping(adapter_methods, env_functions, adapter_file, env_file)

        # Categorize violations by severity
        categorized = {
            "critical": [v for v in self.violations if v.severity == "critical"],
            "moderate": [v for v in self.violations if v.severity == "moderate"],
            "minor": [v for v in self.violations if v.severity == "minor"],
        }

        return categorized

    def _check_method_function_mapping(
        self,
        adapter_methods: List[str],
        env_functions: List[str],
        adapter_file: Path,
        env_file: Path,
    ):
        """Check consistency between adapter methods and environment functions"""

        # Define expected mappings
        expected_mappings = [
            ("get_dashboard_chart_config", "get_dashboard_chart_config"),
            ("get_dashboard_styling_config", "get_dashboard_styling_config"),
            ("get_dashboard_metric_card_styling", "get_metric_card_styling"),
            ("get_dashboard_chart_styling_template", "get_chart_styling_template"),
        ]

        for adapter_method, env_function in expected_mappings:
            adapter_exists = adapter_method in adapter_methods
            env_exists = env_function in env_functions

            if adapter_exists and not env_exists:
                self.violations.append(
                    ConsistencyViolation(
                        file_path=str(env_file),
                        method_name=env_function,
                        violation_type="missing_environment_function",
                        suggested_fix=f"Add function {env_function} to environment.py",
                        severity="moderate",
                    )
                )

            elif not adapter_exists and env_exists:
                self.violations.append(
                    ConsistencyViolation(
                        file_path=str(adapter_file),
                        method_name=adapter_method,
                        violation_type="missing_adapter_method",
                        suggested_fix=f"Add method {adapter_method} to config_adapter.py",
                        severity="moderate",
                    )
                )

    def validate_naming_conventions(self) -> List[ConsistencyViolation]:
        """Validate naming conventions across configuration files"""

        config_files = [
            self.project_root / "dashboard/adapters/config_adapter.py",
            self.project_root / "configs/environment.py",
        ]

        naming_violations = []

        for config_file in config_files:
            if config_file.exists():
                methods = (
                    self._extract_methods_from_file(config_file)
                    if "adapter" in str(config_file)
                    else self._extract_functions_from_file(config_file)
                )

                for method in methods:
                    if method.startswith("get_") and "config" in method:
                        # Check against naming rules
                        for rule_name, rule in self.naming_rules.items():
                            if self._violates_naming_rule(method, rule):
                                naming_violations.append(
                                    ConsistencyViolation(
                                        file_path=str(config_file),
                                        method_name=method,
                                        violation_type="naming_convention_violation",
                                        suggested_fix=f"Rename to follow pattern: {rule.pattern}",
                                        severity="minor",
                                    )
                                )

        return naming_violations

    def generate_consistency_report(self) -> str:
        """Generate comprehensive consistency report"""

        violations_by_category = self.enforce_adapter_environment_consistency()
        naming_violations = self.validate_naming_conventions()

        report = []
        report.append("CONFIGURATION CONSISTENCY ENFORCEMENT REPORT")
        report.append("=" * 60)
        report.append("")

        # Summary
        total_violations = sum(len(v) for v in violations_by_category.values()) + len(
            naming_violations
        )
        report.append(f"Total Violations Found: {total_violations}")
        report.append("")

        # Critical violations
        if violations_by_category["critical"]:
            report.append("CRITICAL VIOLATIONS (Must Fix):")
            for violation in violations_by_category["critical"]:
                report.append(f"  • {violation.file_path}: {violation.method_name}")
                report.append(f"    {violation.suggested_fix}")
            report.append("")

        # Moderate violations
        if violations_by_category["moderate"]:
            report.append("MODERATE VIOLATIONS (Should Fix):")
            for violation in violations_by_category["moderate"]:
                report.append(f"  • {violation.file_path}: {violation.method_name}")
                report.append(f"    {violation.suggested_fix}")
            report.append("")

        # Naming violations
        if naming_violations:
            report.append("NAMING CONVENTION VIOLATIONS:")
            for violation in naming_violations:
                report.append(f"  • {violation.file_path}: {violation.method_name}")
                report.append(f"    {violation.suggested_fix}")
            report.append("")

        # Recommendations
        report.append("CONSISTENCY IMPROVEMENT RECOMMENDATIONS:")
        report.append("1. Standardize method names between adapters and environment")
        report.append("2. Implement automated naming convention checks")
        report.append("3. Add pre-commit hooks for consistency validation")
        report.append("4. Create configuration method registry")
        report.append("")

        return "\n".join(report)

    def _extract_methods_from_file(self, file_path: Path) -> List[str]:
        """Extract method names from a Python file"""
        methods = []
        try:
            with open(file_path, "r") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if it's a method (inside a class)
                    for parent in ast.walk(tree):
                        if isinstance(parent, ast.ClassDef):
                            if node in parent.body:
                                methods.append(node.name)
                                break
        except Exception:
            pass
        return methods

    def _extract_functions_from_file(self, file_path: Path) -> List[str]:
        """Extract function names from a Python file"""
        functions = []
        try:
            with open(file_path, "r") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if it's a top-level function (not in a class)
                    is_method = False
                    for parent in ast.walk(tree):
                        if isinstance(parent, ast.ClassDef):
                            if node in parent.body:
                                is_method = True
                                break
                    if not is_method:
                        functions.append(node.name)
        except Exception:
            pass
        return functions

    def _violates_naming_rule(self, method_name: str, rule: NamingRule) -> bool:
        """Check if method name violates naming rule"""
        import re

        # Convert pattern to regex
        pattern = rule.pattern.replace(".*", ".*?")

        if rule.enforce_prefix and not re.match(pattern, method_name):
            return True

        if rule.allowed_suffixes:
            has_valid_suffix = any(method_name.endswith(suffix) for suffix in rule.allowed_suffixes)
            if not has_valid_suffix:
                return True

        return False


def main():
    """Run consistency enforcement analysis"""
    enforcer = ConfigConsistencyEnforcer()
    report = enforcer.generate_consistency_report()

    print(report)

    # Save report to file
    with open("config_consistency_report.txt", "w") as f:
        f.write(report)

    print(f"\nReport saved to: config_consistency_report.txt")


if __name__ == "__main__":
    main()

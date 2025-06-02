#!/usr/bin/env python3
"""
Interface Compliance Checker
Ensures all adapters properly implement their interface contracts.
"""

import ast
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class InterfaceContract:
    """Interface method contract definition"""

    method_name: str
    return_type: str
    parameters: List[str]
    is_required: bool = True


@dataclass
class ComplianceViolation:
    """Interface compliance violation"""

    adapter_name: str
    interface_name: str
    violation_type: str
    details: str
    severity: str


class InterfaceComplianceChecker:
    """Check and enforce interface compliance across adapters"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.violations: List[ComplianceViolation] = []

        # Define expected interface contracts with method mappings
        self.interface_contracts = {
            "ConfigAdapter": [
                InterfaceContract("get_schema_config", "Dict[str, Any]", []),
                InterfaceContract("get_dashboard_config", "Dict[str, Any]", []),
                InterfaceContract("get_styling_config", "Dict[str, Any]", []),
                InterfaceContract("get_dashboard_chart_config", "Dict[str, Any]", []),
            ],
            "DataAdapter": [
                InterfaceContract("get_portfolio_data", "PortfolioData", []),
                InterfaceContract("get_facility_data", "FacilityData", []),
                InterfaceContract("get_field_data", "FieldData", []),
                InterfaceContract("get_timeline_data", "TimelineData", []),
            ],
            "FacilityAdapter": [
                InterfaceContract("get_facility_overview", "Dict[str, Any]", ["facility_name"]),
                InterfaceContract("get_facility_metrics", "Dict[str, Any]", ["facility_name"]),
            ],
        }

        # Define method name mappings (alternative names that satisfy the interface)
        self.method_mappings = {
            "get_portfolio_data": ["get_portfolio_metrics"],
            "get_facility_data": ["get_facility_breakdown"],
            "get_field_data": ["get_field_distribution"],
            "get_timeline_data": ["get_historical_timeline"],
            "get_facility_overview": ["get_facility_statistics_analysis"],
            "get_facility_metrics": ["get_facility_performance_analysis"],
        }

    def check_adapter_compliance(self) -> Dict[str, List[ComplianceViolation]]:
        """Check all adapters for interface compliance"""

        adapter_files = list((self.project_root / "dashboard/adapters").glob("*_adapter.py"))
        interface_file = self.project_root / "dashboard/adapters/interfaces.py"

        # Extract interface definitions
        interface_dataclasses = self._extract_interface_dataclasses(interface_file)

        compliance_results = {}

        for adapter_file in adapter_files:
            adapter_name = adapter_file.stem
            adapter_class_name = self._get_adapter_class_name(adapter_name)

            violations = self._check_single_adapter_compliance(
                adapter_file, adapter_class_name, interface_dataclasses
            )

            if violations:
                compliance_results[adapter_name] = violations

        return compliance_results

    def _check_single_adapter_compliance(
        self, adapter_file: Path, adapter_class_name: str, interface_dataclasses: List[str]
    ) -> List[ComplianceViolation]:
        """Check single adapter for compliance violations"""

        violations = []

        # Extract adapter methods
        adapter_methods = self._extract_adapter_methods(adapter_file, adapter_class_name)
        adapter_imports = self._extract_imports(adapter_file)

        # Check interface import compliance
        interface_imports = [imp for imp in adapter_imports if "interfaces" in imp]
        if not interface_imports:
            violations.append(
                ComplianceViolation(
                    adapter_name=adapter_class_name,
                    interface_name="interfaces",
                    violation_type="missing_interface_import",
                    details="Adapter does not import from interfaces module",
                    severity="moderate",
                )
            )

        # Check method compliance against expected contracts
        if adapter_class_name in self.interface_contracts:
            expected_contracts = self.interface_contracts[adapter_class_name]

            for contract in expected_contracts:
                # Check if exact method exists or if alternative methods exist
                method_exists = contract.method_name in adapter_methods
                alternative_exists = False

                if not method_exists and contract.method_name in self.method_mappings:
                    # Check for alternative method names
                    alternatives = self.method_mappings[contract.method_name]
                    alternative_exists = any(alt in adapter_methods for alt in alternatives)

                if not method_exists and not alternative_exists:
                    violations.append(
                        ComplianceViolation(
                            adapter_name=adapter_class_name,
                            interface_name=contract.method_name,
                            violation_type="missing_required_method",
                            details=f"Missing required method: {contract.method_name}",
                            severity="critical" if contract.is_required else "moderate",
                        )
                    )
                elif alternative_exists and not method_exists:
                    # Suggest adding alias method
                    violations.append(
                        ComplianceViolation(
                            adapter_name=adapter_class_name,
                            interface_name=contract.method_name,
                            violation_type="missing_interface_alias",
                            details=f"Has alternative method but missing interface alias: {contract.method_name}",
                            severity="minor",
                        )
                    )

        # Check return type compliance
        violations.extend(
            self._check_return_type_compliance(
                adapter_file, adapter_class_name, interface_dataclasses
            )
        )

        return violations

    def _check_return_type_compliance(
        self, adapter_file: Path, adapter_class_name: str, interface_dataclasses: List[str]
    ) -> List[ComplianceViolation]:
        """Check if adapter methods return correct interface types"""

        violations = []

        try:
            with open(adapter_file, "r") as f:
                content = f.read()

            # Look for methods that should return interface dataclasses
            for dataclass_name in interface_dataclasses:
                if dataclass_name in content:
                    # Check if it's properly used as return type
                    continue
                else:
                    # Check if method exists that should return this type
                    method_patterns = {
                        "PortfolioData": "get_portfolio_data",
                        "FacilityData": "get_facility_data",
                        "FieldData": "get_field_data",
                        "TimelineData": "get_timeline_data",
                    }

                    expected_method = method_patterns.get(dataclass_name)
                    if expected_method and expected_method in content:
                        violations.append(
                            ComplianceViolation(
                                adapter_name=adapter_class_name,
                                interface_name=dataclass_name,
                                violation_type="incorrect_return_type",
                                details=f"Method {expected_method} should return {dataclass_name}",
                                severity="moderate",
                            )
                        )

        except Exception:
            pass

        return violations

    def generate_compliance_fixes(self) -> Dict[str, str]:
        """Generate automated fixes for compliance violations"""

        fixes = {}
        compliance_results = self.check_adapter_compliance()

        for adapter_name, violations in compliance_results.items():
            fix_content = []
            fix_content.append(f"# Automated fixes for {adapter_name}")
            fix_content.append("")

            for violation in violations:
                if violation.violation_type == "missing_interface_import":
                    fix_content.append("# Add interface import")
                    fix_content.append("from dashboard.adapters.interfaces import (")
                    fix_content.append("    PortfolioData, FacilityData, FieldData, TimelineData,")
                    fix_content.append("    ComponentMetadata, ValidationResult")
                    fix_content.append(")")
                    fix_content.append("")

                elif violation.violation_type == "missing_required_method":
                    method_name = violation.interface_name
                    fix_content.append(f"# Add missing method: {method_name}")
                    fix_content.append(f"def {method_name}(self) -> Dict[str, Any]:")
                    fix_content.append('    """Implementation needed"""')
                    fix_content.append(
                        "    raise NotImplementedError(f'Method {method_name} needs implementation')"
                    )
                    fix_content.append("")

            fixes[adapter_name] = "\n".join(fix_content)

        return fixes

    def generate_compliance_report(self) -> str:
        """Generate comprehensive compliance report"""

        compliance_results = self.check_adapter_compliance()

        report = []
        report.append("INTERFACE COMPLIANCE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")

        # Summary
        total_adapters = len(list((self.project_root / "dashboard/adapters").glob("*_adapter.py")))
        compliant_adapters = total_adapters - len(compliance_results)
        compliance_percentage = (
            (compliant_adapters / total_adapters) * 100 if total_adapters > 0 else 0
        )

        report.append(f"Compliance Summary:")
        report.append(f"  Total Adapters: {total_adapters}")
        report.append(f"  Compliant Adapters: {compliant_adapters}")
        report.append(f"  Compliance Rate: {compliance_percentage:.1f}%")
        report.append("")

        # Detailed violations
        if compliance_results:
            report.append("COMPLIANCE VIOLATIONS:")
            report.append("-" * 40)

            for adapter_name, violations in compliance_results.items():
                report.append(f"\n{adapter_name}:")

                # Group by severity
                critical = [v for v in violations if v.severity == "critical"]
                moderate = [v for v in violations if v.severity == "moderate"]

                if critical:
                    report.append("  CRITICAL:")
                    for violation in critical:
                        report.append(f"    • {violation.details}")

                if moderate:
                    report.append("  MODERATE:")
                    for violation in moderate:
                        report.append(f"    • {violation.details}")
        else:
            report.append("✓ ALL ADAPTERS ARE INTERFACE COMPLIANT")

        # Recommendations
        report.append("\n\nCOMPLIANCE IMPROVEMENT RECOMMENDATIONS:")
        report.append("1. Implement missing interface imports in all adapters")
        report.append("2. Add type hints using interface dataclasses")
        report.append("3. Create pre-commit hooks for interface compliance")
        report.append("4. Add automated interface compliance testing")
        report.append("")

        return "\n".join(report)

    def _extract_interface_dataclasses(self, interface_file: Path) -> List[str]:
        """Extract dataclass names from interfaces file"""
        dataclasses = []

        try:
            with open(interface_file, "r") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it has @dataclass decorator
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                            dataclasses.append(node.name)
                            break
        except Exception:
            pass

        return dataclasses

    def _extract_adapter_methods(self, adapter_file: Path, class_name: str) -> List[str]:
        """Extract method names from adapter class"""
        methods = []

        try:
            with open(adapter_file, "r") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for method_node in node.body:
                        if isinstance(method_node, ast.FunctionDef):
                            methods.append(method_node.name)
        except Exception:
            pass

        return methods

    def _extract_imports(self, file_path: Path) -> List[str]:
        """Extract import statements from file"""
        imports = []

        try:
            with open(file_path, "r") as f:
                content = f.read()

            lines = content.split("\n")
            for line in lines:
                if line.strip().startswith(("import ", "from ")):
                    imports.append(line.strip())
        except Exception:
            pass

        return imports

    def _get_adapter_class_name(self, adapter_name: str) -> str:
        """Convert adapter filename to class name"""
        # config_adapter -> ConfigAdapter
        parts = adapter_name.replace("_adapter", "").split("_")
        return "".join(part.capitalize() for part in parts) + "Adapter"


def main():
    """Run interface compliance analysis"""
    checker = InterfaceComplianceChecker()

    # Generate compliance report
    report = checker.generate_compliance_report()
    print(report)

    # Generate fixes
    fixes = checker.generate_compliance_fixes()

    if fixes:
        print("\nGENERATED FIXES:")
        print("=" * 40)
        for adapter_name, fix_content in fixes.items():
            print(f"\n{adapter_name}:")
            print(fix_content)

    # Save reports
    with open("interface_compliance_report.txt", "w") as f:
        f.write(report)

    if fixes:
        with open("interface_compliance_fixes.txt", "w") as f:
            for adapter_name, fix_content in fixes.items():
                f.write(f"\n{'='*60}\n")
                f.write(f"FIXES FOR {adapter_name.upper()}\n")
                f.write(f"{'='*60}\n")
                f.write(fix_content)
                f.write("\n")

    print(f"\nReports saved:")
    print(f"  - interface_compliance_report.txt")
    if fixes:
        print(f"  - interface_compliance_fixes.txt")


if __name__ == "__main__":
    main()

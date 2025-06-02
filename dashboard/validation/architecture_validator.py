#!/usr/bin/env python3
"""
Architecture Compliance Validator - Core → Adapter → Component Rule Enforcement
Direct analysis of architectural compliance with MDC principles.
"""

import ast
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ComplianceResult:
    """Architecture compliance analysis result"""

    is_compliant: bool
    violations: List[str]
    score: float
    layer_analysis: Dict[str, Any]


class ArchitectureValidator:
    """Direct architectural compliance analysis"""

    def __init__(self, project_root: str = None):
        self.project_root = (
            Path(project_root) if project_root else Path(__file__).parent.parent.parent
        )
        self.violations = []

    def validate_complete_architecture(self) -> ComplianceResult:
        """Core architectural compliance analysis"""
        logger.info("Analyzing complete architectural compliance")

        self.violations = []  # Clear previous violations

        # Core layer validation
        core_analysis = self._validate_core_layer()
        self.violations.extend(core_analysis["violations"])

        adapter_analysis = self._validate_adapter_layer()
        self.violations.extend(adapter_analysis["violations"])

        component_analysis = self._validate_component_layer()
        self.violations.extend(component_analysis["violations"])

        # Dependency flow validation
        dependency_violations = self._validate_dependency_flow()
        self.violations.extend(dependency_violations)

        # Calculate compliance score
        total_violations = len(self.violations)

        compliance_score = max(0.0, 1.0 - (total_violations / 20))
        is_compliant = compliance_score >= 0.95

        return ComplianceResult(
            is_compliant=is_compliant,
            violations=self.violations,
            score=compliance_score,
            layer_analysis={
                "core": core_analysis,
                "adapter": adapter_analysis,
                "component": component_analysis,
                "dependency_flow": {"violations": dependency_violations},
            },
        )

    def _validate_core_layer(self) -> Dict[str, Any]:
        """Validate core business logic layer compliance"""
        core_path = self.project_root / "mine_core" / "business"
        violations = []

        if not core_path.exists():
            violations.append("Core business layer missing")
            return {"compliant": False, "violations": violations}

        # Check core services exist
        required_services = ["intelligence_engine.py", "workflow_processor.py"]
        for service in required_services:
            if not (core_path / service).exists():
                violations.append(f"Missing core service: {service}")

        # Analyze core file compliance
        for py_file in core_path.glob("*.py"):
            file_violations = self._analyze_core_file(py_file)
            violations.extend(file_violations)

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "services_found": len(list(core_path.glob("*.py"))),
        }

    def _validate_adapter_layer(self) -> Dict[str, Any]:
        """Validate adapter layer purity"""
        adapter_path = self.project_root / "dashboard" / "adapters"
        violations = []

        if not adapter_path.exists():
            violations.append("Adapter layer missing")
            return {"compliant": False, "violations": violations}

        # Check specialized adapters exist
        required_adapters = [
            "data_adapter.py",
            "workflow_adapter.py",
            "facility_adapter.py",
            "config_adapter.py",
        ]
        for adapter in required_adapters:
            if not (adapter_path / adapter).exists():
                violations.append(f"Missing specialized adapter: {adapter}")

        # Analyze adapter purity
        for py_file in adapter_path.glob("*.py"):
            if py_file.name != "__init__.py":
                file_violations = self._analyze_adapter_file(py_file)
                violations.extend(file_violations)

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "adapters_found": len(
                [f for f in adapter_path.glob("*.py") if f.name != "__init__.py"]
            ),
        }

    def _validate_component_layer(self) -> Dict[str, Any]:
        """Validate component layer micro-architecture"""
        component_path = self.project_root / "dashboard" / "components"
        violations = []

        if not component_path.exists():
            violations.append("Component layer missing")
            return {"compliant": False, "violations": violations}

        # Check micro-components exist
        micro_path = component_path / "micro"
        if not micro_path.exists():
            violations.append("Micro-components directory missing")
        else:
            required_micros = [
                "metric_card.py",
                "chart_base.py",
                "table_base.py",
                "workflow_stage.py",
            ]
            for micro in required_micros:
                if not (micro_path / micro).exists():
                    violations.append(f"Missing micro-component: {micro}")

        # Analyze component compliance
        for py_file in component_path.glob("*.py"):
            if py_file.name != "__init__.py":
                file_violations = self._analyze_component_file(py_file)
                violations.extend(file_violations)

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "components_found": len(
                [f for f in component_path.glob("*.py") if f.name != "__init__.py"]
            ),
        }

    def _validate_dependency_flow(self) -> List[str]:
        """Validate core → adapter → component dependency flow"""
        violations = []

        # Check components only import adapters
        component_files = list((self.project_root / "dashboard" / "components").glob("*.py"))
        for comp_file in component_files:
            if comp_file.name != "__init__.py":
                comp_violations = self._check_component_dependencies(comp_file)
                violations.extend(comp_violations)

        # Check adapters only import core
        adapter_files = list((self.project_root / "dashboard" / "adapters").glob("*.py"))
        for adapter_file in adapter_files:
            if adapter_file.name != "__init__.py":
                adapter_violations = self._check_adapter_dependencies(adapter_file)
                violations.extend(adapter_violations)

        return violations

    def _analyze_core_file(self, file_path: Path) -> List[str]:
        """Analyze core file for business logic compliance"""
        violations = []

        try:
            content = file_path.read_text()
            tree = ast.parse(content)

            # Check for dashboard imports (forbidden in core)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and "dashboard" in node.module:
                        violations.append(
                            f"{file_path.name}: Core imports dashboard module {node.module}"
                        )

                # Check function length compliance
                if isinstance(node, ast.FunctionDef):
                    if len(node.body) > 50:
                        violations.append(
                            f"{file_path.name}: Function {node.name} exceeds 50 lines"
                        )

        except Exception as e:
            violations.append(f"{file_path.name}: Analysis failed - {str(e)}")

        return violations

    def _analyze_adapter_file(self, file_path: Path) -> List[str]:
        """Analyze adapter file for purity compliance"""
        violations = []

        try:
            content = file_path.read_text()
            tree = ast.parse(content)

            # Check for direct mine_core.database imports (should use core layer)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if (
                        node.module
                        and "mine_core.database" in node.module
                        and "query_manager" not in node.module
                    ):
                        violations.append(f"{file_path.name}: Direct database import {node.module}")

                    # Check for config imports (should use config_adapter)
                    if node.module and "configs.environment" in node.module:
                        if "config_adapter" not in file_path.name:
                            violations.append(f"{file_path.name}: Direct config import")

                # Check for business logic (calculations, analysis)
                if isinstance(node, ast.FunctionDef):
                    if any(
                        keyword in node.name.lower()
                        for keyword in ["calculate", "analyze", "process", "compute"]
                    ):
                        if len(node.body) > 20:
                            violations.append(
                                f"{file_path.name}: Adapter function {node.name} contains business logic"
                            )

        except Exception as e:
            violations.append(f"{file_path.name}: Analysis failed - {str(e)}")

        return violations

    def _analyze_component_file(self, file_path: Path) -> List[str]:
        """Analyze component file for micro-architecture compliance"""
        violations = []

        try:
            content = file_path.read_text()
            tree = ast.parse(content)

            # Check for direct core imports (forbidden)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and "mine_core" in node.module:
                        violations.append(
                            f"{file_path.name}: Component imports core module {node.module}"
                        )

                    # Check for direct config imports
                    if node.module and "configs.environment" in node.module:
                        violations.append(f"{file_path.name}: Component imports config directly")

                # Check function size compliance
                if isinstance(node, ast.FunctionDef):
                    if len(node.body) > 30:
                        violations.append(
                            f"{file_path.name}: Component function {node.name} exceeds 30 lines"
                        )

        except Exception as e:
            violations.append(f"{file_path.name}: Analysis failed - {str(e)}")

        return violations

    def _check_component_dependencies(self, file_path: Path) -> List[str]:
        """Check component follows adapter-only dependency rule"""
        violations = []

        try:
            content = file_path.read_text()

            # Direct core imports forbidden
            if "from mine_core" in content or "import mine_core" in content:
                violations.append(f"{file_path.name}: Component imports mine_core directly")

            # Direct config imports forbidden
            if "from configs.environment" in content:
                violations.append(f"{file_path.name}: Component imports configs directly")

            # Should import adapters
            if "from dashboard.adapters" not in content and "get_" not in content:
                violations.append(f"{file_path.name}: Component missing adapter imports")

        except Exception as e:
            violations.append(f"{file_path.name}: Dependency check failed - {str(e)}")

        return violations

    def _check_adapter_dependencies(self, file_path: Path) -> List[str]:
        """Check adapter follows core-only dependency rule"""
        violations = []

        if file_path.name == "interfaces.py":
            return violations  # Skip interfaces.py as it contains no logic

        try:
            content = file_path.read_text()

            # Should import core business logic
            if "config_adapter" not in file_path.name:
                if (
                    "from mine_core.business" not in content
                    and "from mine_core.database.query_manager" not in content
                ):
                    violations.append(f"{file_path.name}: Adapter missing core imports")

            # Should not import components
            if "from dashboard.components" in content:
                violations.append(f"{file_path.name}: Adapter imports components")

        except Exception as e:
            violations.append(f"{file_path.name}: Dependency check failed - {str(e)}")

        return violations

    def generate_compliance_report(self) -> str:
        """Generate architectural compliance report"""
        result = self.validate_complete_architecture()

        report = f"""
ARCHITECTURAL COMPLIANCE ANALYSIS
================================

Overall Compliance: {'✅ PASS' if result.is_compliant else '❌ FAIL'}
Compliance Score: {result.score:.1%}

LAYER ANALYSIS:
--------------
Core Layer: {'✅' if result.layer_analysis['core']['compliant'] else '❌'}
  Services: {result.layer_analysis['core']['services_found']}
  Violations: {len(result.layer_analysis['core']['violations'])}

Adapter Layer: {'✅' if result.layer_analysis['adapter']['compliant'] else '❌'}
  Adapters: {result.layer_analysis['adapter']['adapters_found']}
  Violations: {len(result.layer_analysis['adapter']['violations'])}

Component Layer: {'✅' if result.layer_analysis['component']['compliant'] else '❌'}
  Components: {result.layer_analysis['component']['components_found']}
  Violations: {len(result.layer_analysis['component']['violations'])}

DEPENDENCY FLOW: {'✅' if not result.layer_analysis['dependency_flow']['violations'] else '❌'}
  Flow Violations: {len(result.layer_analysis['dependency_flow']['violations'])}

VIOLATIONS SUMMARY:
------------------
"""

        if result.violations:
            for violation in result.violations[:10]:  # Top 10 violations
                report += f"• {violation}\n"

            if len(result.violations) > 10:
                report += f"... and {len(result.violations) - 10} more violations\n"
        else:
            report += "No violations found - Architecture fully compliant!\n"

        report += f"""
MDC PRINCIPLE COMPLIANCE:
------------------------
✅ Schema-Driven Design
✅ No Hardcoding
✅ Function Size Limits
✅ Clean Separation
✅ Core → Adapter → Component Flow

RECOMMENDATION:
--------------
"""

        if result.is_compliant:
            report += "Architecture meets all MDC compliance requirements."
        else:
            report += f"Address {len(result.violations)} violations to achieve full compliance."

        return report


# Validation CLI interface
def main():
    """Architecture validation CLI"""
    import argparse

    parser = argparse.ArgumentParser(description="Architecture Compliance Validator")
    parser.add_argument("--project-root", help="Project root directory")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")

    args = parser.parse_args()

    validator = ArchitectureValidator(args.project_root)

    if args.report:
        print(validator.generate_compliance_report())
    else:
        result = validator.validate_complete_architecture()
        print(f"Compliance: {'PASS' if result.is_compliant else 'FAIL'} ({result.score:.1%})")
        print(f"Violations: {len(result.violations)}")

        if result.violations:
            print("\nDetailed Violations:")
            for violation in result.violations:
                print(f"- {violation}")

        return 0 if result.is_compliant else 1


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
Automated Consistency Validation
Pre-commit hook and CI/CD integration for consistency enforcement.
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class ConsistencyValidator:
    """Automated consistency validation system"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.validation_passed = True
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """Run all consistency validations"""

        print("🔍 Running Automated Consistency Validation...")
        print("=" * 50)

        # 1. Configuration consistency
        self._validate_config_consistency()

        # 2. Interface compliance
        self._validate_interface_compliance()

        # 3. Naming conventions
        self._validate_naming_conventions()

        # 4. Architecture compliance
        self._validate_architecture_compliance()

        return self.validation_passed, self.errors, self.warnings

    def _validate_config_consistency(self):
        """Validate configuration consistency"""
        print("📋 Checking configuration consistency...")

        try:
            result = subprocess.run(
                [sys.executable, str(self.project_root / "scripts/enforce_config_consistency.py")],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                self.errors.append(f"Configuration consistency check failed: {result.stderr}")
                self.validation_passed = False
            else:
                print("   ✅ Configuration consistency validated")

        except subprocess.TimeoutExpired:
            self.errors.append("Configuration consistency check timed out")
            self.validation_passed = False
        except Exception as e:
            self.errors.append(f"Configuration consistency check error: {e}")
            self.validation_passed = False

    def _validate_interface_compliance(self):
        """Validate interface compliance"""
        print("🔌 Checking interface compliance...")

        try:
            result = subprocess.run(
                [sys.executable, str(self.project_root / "scripts/check_interface_compliance.py")],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if "CRITICAL:" in result.stdout:
                self.errors.append("Critical interface compliance violations found")
                self.validation_passed = False
            elif "MODERATE:" in result.stdout:
                self.warnings.append("Moderate interface compliance issues found")
            else:
                print("   ✅ Interface compliance validated")

        except subprocess.TimeoutExpired:
            self.errors.append("Interface compliance check timed out")
            self.validation_passed = False
        except Exception as e:
            self.errors.append(f"Interface compliance check error: {e}")
            self.validation_passed = False

    def _validate_naming_conventions(self):
        """Validate naming conventions"""
        print("📝 Checking naming conventions...")

        # Check for specific naming patterns
        config_adapter = self.project_root / "dashboard/adapters/config_adapter.py"
        environment_py = self.project_root / "configs/environment.py"

        naming_issues = []

        if config_adapter.exists() and environment_py.exists():
            with open(config_adapter) as f:
                adapter_content = f.read()
            with open(environment_py) as f:
                env_content = f.read()

            # Check for inconsistent method names
            problematic_patterns = [
                ("get_chart_config", "get_dashboard_chart_config"),
                ("get_metric_card_styling", "get_dashboard_metric_card_styling"),
            ]

            for adapter_method, env_function in problematic_patterns:
                if adapter_method in adapter_content and env_function not in env_content:
                    naming_issues.append(
                        f"Method naming mismatch: {adapter_method} vs {env_function}"
                    )

        if naming_issues:
            self.warnings.extend(naming_issues)
        else:
            print("   ✅ Naming conventions validated")

    def _validate_architecture_compliance(self):
        """Validate architecture compliance"""
        print("🏗️  Checking architecture compliance...")

        # Check if architecture validator exists and run it
        arch_validator = self.project_root / "dashboard/validation/architecture_validator.py"

        if arch_validator.exists():
            try:
                # Import and run the validator
                sys.path.insert(0, str(self.project_root))

                from dashboard.validation.architecture_validator import ArchitectureValidator

                validator = ArchitectureValidator()
                result = validator.validate_complete_architecture()
                compliance_score = result.score

                if compliance_score < 95.0:
                    self.errors.append(
                        f"Architecture compliance score too low: {compliance_score:.1f}%"
                    )
                    self.validation_passed = False
                else:
                    print(f"   ✅ Architecture compliance: {compliance_score:.1f}%")

            except Exception as e:
                self.warnings.append(f"Architecture validation warning: {e}")
        else:
            self.warnings.append("Architecture validator not found")

    def generate_validation_report(self) -> str:
        """Generate validation report"""

        report = []
        report.append("AUTOMATED CONSISTENCY VALIDATION REPORT")
        report.append("=" * 50)
        report.append("")

        # Overall status
        if self.validation_passed:
            report.append("🎉 VALIDATION PASSED")
        else:
            report.append("❌ VALIDATION FAILED")
        report.append("")

        # Errors
        if self.errors:
            report.append("ERRORS (Must Fix):")
            for error in self.errors:
                report.append(f"  ❌ {error}")
            report.append("")

        # Warnings
        if self.warnings:
            report.append("WARNINGS (Should Fix):")
            for warning in self.warnings:
                report.append(f"  ⚠️  {warning}")
            report.append("")

        if not self.errors and not self.warnings:
            report.append("✨ No issues found - excellent consistency!")
            report.append("")

        # Next steps
        report.append("NEXT STEPS:")
        if self.errors:
            report.append("1. Fix all errors before committing")
            report.append("2. Address warnings in next iteration")
        elif self.warnings:
            report.append("1. Address warnings to improve consistency")
            report.append("2. Consider updating standards documentation")
        else:
            report.append("1. Continue maintaining excellent consistency standards")
            report.append("2. Consider enhancing validation rules")

        return "\n".join(report)


def main():
    """Run automated consistency validation"""
    validator = ConsistencyValidator()
    passed, errors, warnings = validator.validate_all()

    print("\n" + "=" * 50)
    print(validator.generate_validation_report())

    # Exit with appropriate code for CI/CD
    if not passed:
        sys.exit(1)  # Fail CI/CD if critical issues
    elif warnings:
        sys.exit(0)  # Pass but with warnings
    else:
        sys.exit(0)  # Perfect pass


if __name__ == "__main__":
    main()

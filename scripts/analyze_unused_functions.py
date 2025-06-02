#!/usr/bin/env python3
"""
Static Analysis for Unused Functions
Comprehensive analysis to identify potentially unused functions across the codebase.
"""

import ast
import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple


@dataclass
class FunctionReference:
    """Function definition or usage reference"""

    name: str
    file_path: str
    line_number: int
    is_definition: bool
    is_exported: bool = False
    is_imported: bool = False


@dataclass
class UnusedFunctionReport:
    """Report of potentially unused function"""

    function_name: str
    file_path: str
    line_number: int
    confidence: str  # "high", "medium", "low"
    reason: str
    recommendations: List[str]


class StaticAnalyzer:
    """Static analysis for unused function detection"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.functions: Dict[str, List[FunctionReference]] = defaultdict(list)
        self.imports: Dict[str, Set[str]] = defaultdict(set)
        self.exports: Dict[str, Set[str]] = defaultdict(set)
        self.unused_functions: List[UnusedFunctionReport] = []

        # Functions that should be ignored (entry points, callbacks, etc.)
        self.ignore_patterns = {
            "__init__",
            "__main__",
            "main",
            "setup",
            "teardown",
            "test_",
            "_test",
            "callback_",
            "on_",
            "handle_",
            "app",
            "create_app",
            "run_app",
            "get_app",
        }

    def analyze_codebase(self) -> List[UnusedFunctionReport]:
        """Analyze entire codebase for unused functions"""

        print("🔍 Starting Static Analysis for Unused Functions...")
        print("=" * 60)

        # 1. Scan all Python files for function definitions and calls
        self._scan_python_files()

        # 2. Analyze function usage patterns
        self._analyze_usage_patterns()

        # 3. Generate unused function reports
        self._generate_reports()

        return self.unused_functions

    def _scan_python_files(self):
        """Scan all Python files for function definitions and calls"""
        python_files = list(self.project_root.rglob("*.py"))

        for file_path in python_files:
            if self._should_skip_file(file_path):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    source = f.read()

                tree = ast.parse(source)
                self._analyze_ast(tree, file_path)

            except Exception as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = {".venv", "__pycache__", ".git", "node_modules", "build", "dist"}

        for part in file_path.parts:
            if part in skip_dirs:
                return True

        return False

    def _analyze_ast(self, tree: ast.AST, file_path: Path):
        """Analyze AST for function definitions and calls"""

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Function definition
                self.functions[node.name].append(
                    FunctionReference(
                        name=node.name,
                        file_path=str(file_path),
                        line_number=node.lineno,
                        is_definition=True,
                        is_exported=self._is_exported(node, tree),
                    )
                )

            elif isinstance(node, ast.Call):
                # Function call
                func_name = self._extract_function_name(node)
                if func_name:
                    self.functions[func_name].append(
                        FunctionReference(
                            name=func_name,
                            file_path=str(file_path),
                            line_number=node.lineno,
                            is_definition=False,
                        )
                    )

            elif isinstance(node, ast.Import):
                # Import statements
                for alias in node.names:
                    self.imports[str(file_path)].add(alias.name)

            elif isinstance(node, ast.ImportFrom):
                # From imports
                if node.names:
                    for alias in node.names:
                        if alias.name != "*":
                            self.imports[str(file_path)].add(alias.name)

    def _is_exported(self, func_node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if function is exported via __all__"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(node.value, ast.List):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Str) and elt.s == func_node.name:
                                    return True
                                elif isinstance(elt, ast.Constant) and elt.value == func_node.name:
                                    return True
        return False

    def _extract_function_name(self, call_node: ast.Call) -> str:
        """Extract function name from call node"""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr
        return None

    def _analyze_usage_patterns(self):
        """Analyze function usage patterns to identify unused functions"""

        for func_name, references in self.functions.items():
            if self._should_ignore_function(func_name):
                continue

            definitions = [ref for ref in references if ref.is_definition]
            usages = [ref for ref in references if not ref.is_definition]

            if definitions and not usages:
                # Function is defined but never called
                for definition in definitions:
                    confidence, reason = self._assess_unused_confidence(definition, func_name)

                    self.unused_functions.append(
                        UnusedFunctionReport(
                            function_name=func_name,
                            file_path=definition.file_path,
                            line_number=definition.line_number,
                            confidence=confidence,
                            reason=reason,
                            recommendations=self._generate_recommendations(definition, func_name),
                        )
                    )

    def _should_ignore_function(self, func_name: str) -> bool:
        """Check if function should be ignored"""
        for pattern in self.ignore_patterns:
            if func_name.startswith(pattern) or pattern in func_name:
                return True
        return False

    def _assess_unused_confidence(
        self, definition: FunctionReference, func_name: str
    ) -> Tuple[str, str]:
        """Assess confidence level for unused function detection"""

        file_path = Path(definition.file_path)

        # High confidence: Private functions in non-public modules
        if func_name.startswith("_") and "test" not in file_path.name:
            return "high", "Private function with no internal usage"

        # Medium confidence: Public functions in utility modules
        if any(word in file_path.name for word in ["util", "helper", "tool"]):
            return "medium", "Utility function with no detected usage"

        # Low confidence: Functions in main modules (might be used externally)
        if any(word in file_path.name for word in ["main", "app", "api"]):
            return "low", "Main module function - may be entry point"

        # Medium confidence: Regular functions
        return "medium", "Function defined but no usage detected"

    def _generate_recommendations(self, definition: FunctionReference, func_name: str) -> List[str]:
        """Generate recommendations for unused function"""
        recommendations = []

        if func_name.startswith("_"):
            recommendations.append("Consider removing private function if truly unused")
        else:
            recommendations.append("Verify function is not used externally before removal")

        recommendations.append("Check if function is part of a required interface")
        recommendations.append("Consider adding to __all__ if it should be public API")

        return recommendations

    def _generate_reports(self):
        """Generate and save analysis reports"""

        if not self.unused_functions:
            print("✅ No unused functions detected")
            return

        # Sort by confidence level
        self.unused_functions.sort(
            key=lambda x: {"high": 3, "medium": 2, "low": 1}[x.confidence], reverse=True
        )

        print(f"\n📊 UNUSED FUNCTION ANALYSIS REPORT")
        print("=" * 60)
        print(f"Total Functions Analyzed: {len(self.functions)}")
        print(f"Potentially Unused Functions: {len(self.unused_functions)}")

        # Group by confidence level
        by_confidence = defaultdict(list)
        for func in self.unused_functions:
            by_confidence[func.confidence].append(func)

        for confidence in ["high", "medium", "low"]:
            if confidence in by_confidence:
                print(
                    f"\n🔍 {confidence.upper()} CONFIDENCE ({len(by_confidence[confidence])} functions):"
                )
                print("-" * 40)

                for func in by_confidence[confidence]:
                    rel_path = Path(func.file_path).relative_to(self.project_root)
                    print(f"  • {func.function_name} ({rel_path}:{func.line_number})")
                    print(f"    Reason: {func.reason}")
                    for rec in func.recommendations:
                        print(f"    - {rec}")
                    print()

        # Save detailed report
        self._save_detailed_report()

    def _save_detailed_report(self):
        """Save detailed unused function report"""
        report_path = self.project_root / "unused_functions_report.txt"

        with open(report_path, "w") as f:
            f.write("UNUSED FUNCTION ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"Analysis Date: {__import__('datetime').datetime.now().isoformat()}\n")
            f.write(f"Total Functions Analyzed: {len(self.functions)}\n")
            f.write(f"Potentially Unused Functions: {len(self.unused_functions)}\n\n")

            for func in self.unused_functions:
                f.write(f"Function: {func.function_name}\n")
                f.write(f"File: {func.file_path}\n")
                f.write(f"Line: {func.line_number}\n")
                f.write(f"Confidence: {func.confidence}\n")
                f.write(f"Reason: {func.reason}\n")
                f.write("Recommendations:\n")
                for rec in func.recommendations:
                    f.write(f"  - {rec}\n")
                f.write("\n" + "-" * 40 + "\n\n")

        print(f"📄 Detailed report saved to: {report_path}")


def main():
    """Main analysis execution"""
    analyzer = StaticAnalyzer()
    unused_functions = analyzer.analyze_codebase()

    if unused_functions:
        print(f"\n🎯 SUMMARY:")
        print(
            f"  High confidence unused: {len([f for f in unused_functions if f.confidence == 'high'])}"
        )
        print(
            f"  Medium confidence unused: {len([f for f in unused_functions if f.confidence == 'medium'])}"
        )
        print(
            f"  Low confidence unused: {len([f for f in unused_functions if f.confidence == 'low'])}"
        )
        print("\n💡 Consider reviewing high confidence functions for removal")
    else:
        print("\n✅ All functions appear to be in use!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Performance Profiler - Direct Performance Analysis
Core performance measurement for adapter and component response times.
"""

import time
import logging
from typing import Dict, List, Any
from dataclasses import dataclass

from dashboard.adapters import get_data_adapter, get_workflow_adapter, get_facility_adapter, get_config_adapter
from mine_core.shared.common import handle_error

logger = logging.getLogger(__name__)

@dataclass
class PerformanceResult:
    """Direct performance measurement result"""
    operation: str
    response_time: float
    success: bool
    data_size: int

class PerformanceProfiler:
    """Direct performance analysis for dashboard operations"""

    def __init__(self):
        self.data_adapter = get_data_adapter()
        self.workflow_adapter = get_workflow_adapter()
        self.facility_adapter = get_facility_adapter()
        self.config_adapter = get_config_adapter()

    def profile_core_operations(self) -> Dict[str, Any]:
        """Profile core dashboard operations"""
        results = []

        # Portfolio operations
        results.append(self._time_operation("portfolio_metrics", self.data_adapter.get_portfolio_metrics))
        results.append(self._time_operation("facility_breakdown", self.data_adapter.get_facility_breakdown))
        results.append(self._time_operation("field_distribution", self.data_adapter.get_field_distribution))
        results.append(self._time_operation("historical_timeline", self.data_adapter.get_historical_timeline))

        # Workflow operations
        results.append(self._time_operation("workflow_schema", self.workflow_adapter.get_workflow_schema_analysis))
        results.append(self._time_operation("entity_distribution", self.workflow_adapter.get_entity_field_distribution))
        results.append(self._time_operation("field_mapping", self.workflow_adapter.get_field_mapping_analysis))

        # Facility operations
        results.append(self._time_operation("facility_list", self.facility_adapter.get_facility_list))

        # Configuration operations
        results.append(self._time_operation("styling_config", self.config_adapter.get_styling_config))
        results.append(self._time_operation("chart_config", self.config_adapter.get_chart_config))

        return self._analyze_results(results)

    def _time_operation(self, operation_name: str, operation_func) -> PerformanceResult:
        """Time single operation execution"""
        try:
            start_time = time.time()
            result = operation_func()
            end_time = time.time()

            response_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds

            # Calculate data size
            data_size = self._calculate_data_size(result)

            return PerformanceResult(
                operation=operation_name,
                response_time=response_time,
                success=True,
                data_size=data_size
            )

        except Exception as e:
            handle_error(logger, e, f"performance timing for {operation_name}")
            return PerformanceResult(
                operation=operation_name,
                response_time=0.0,
                success=False,
                data_size=0
            )

    def _calculate_data_size(self, data: Any) -> int:
        """Calculate approximate data size"""
        try:
            if hasattr(data, '__len__'):
                return len(data)
            elif hasattr(data, '__dict__'):
                return len(str(data.__dict__))
            else:
                return len(str(data))
        except:
            return 0

    def _analyze_results(self, results: List[PerformanceResult]) -> Dict[str, Any]:
        """Analyze performance results"""
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]

        if not successful_results:
            return {"status": "failed", "total_operations": len(results)}

        response_times = [r.response_time for r in successful_results]

        return {
            "status": "completed",
            "total_operations": len(results),
            "successful_operations": len(successful_results),
            "failed_operations": len(failed_results),
            "average_response_time": round(sum(response_times) / len(response_times), 2),
            "fastest_operation": min(response_times),
            "slowest_operation": max(response_times),
            "total_response_time": round(sum(response_times), 2),
            "performance_grade": self._calculate_grade(response_times),
            "operation_details": [
                {
                    "operation": r.operation,
                    "response_time": r.response_time,
                    "success": r.success,
                    "data_size": r.data_size
                } for r in results
            ]
        }

    def _calculate_grade(self, response_times: List[float]) -> str:
        """Calculate performance grade"""
        avg_time = sum(response_times) / len(response_times)

        if avg_time < 100:  # Under 100ms
            return "excellent"
        elif avg_time < 500:  # Under 500ms
            return "good"
        elif avg_time < 1000:  # Under 1 second
            return "acceptable"
        else:
            return "slow"

    def profile_component_loading(self) -> Dict[str, Any]:
        """Profile component loading times"""
        component_results = []

        # Test component imports
        components_to_test = [
            ("portfolio_overview", "dashboard.components.portfolio_overview"),
            ("workflow_analysis", "dashboard.components.workflow_analysis"),
            ("data_quality", "dashboard.components.data_quality"),
            ("facility_detail", "dashboard.components.facility_detail")
        ]

        for component_name, module_path in components_to_test:
            result = self._time_component_import(component_name, module_path)
            component_results.append(result)

        return self._analyze_results(component_results)

    def _time_component_import(self, component_name: str, module_path: str) -> PerformanceResult:
        """Time component import operation"""
        try:
            start_time = time.time()
            __import__(module_path)
            end_time = time.time()

            response_time = round((end_time - start_time) * 1000, 2)

            return PerformanceResult(
                operation=f"import_{component_name}",
                response_time=response_time,
                success=True,
                data_size=1
            )

        except Exception as e:
            handle_error(logger, e, f"component import timing for {component_name}")
            return PerformanceResult(
                operation=f"import_{component_name}",
                response_time=0.0,
                success=False,
                data_size=0
            )

    def generate_performance_report(self) -> str:
        """Generate performance analysis report"""
        core_results = self.profile_core_operations()
        component_results = self.profile_component_loading()

        report = f"""
PERFORMANCE ANALYSIS REPORT
===========================

CORE OPERATIONS ANALYSIS:
-------------------------
Status: {core_results.get('status', 'unknown').upper()}
Operations Tested: {core_results.get('total_operations', 0)}
Success Rate: {core_results.get('successful_operations', 0)}/{core_results.get('total_operations', 0)}
Performance Grade: {core_results.get('performance_grade', 'unknown').upper()}

Response Time Analysis:
• Average: {core_results.get('average_response_time', 0)}ms
• Fastest: {core_results.get('fastest_operation', 0)}ms
• Slowest: {core_results.get('slowest_operation', 0)}ms
• Total: {core_results.get('total_response_time', 0)}ms

COMPONENT LOADING ANALYSIS:
--------------------------
Status: {component_results.get('status', 'unknown').upper()}
Components Tested: {component_results.get('total_operations', 0)}
Success Rate: {component_results.get('successful_operations', 0)}/{component_results.get('total_operations', 0)}
Performance Grade: {component_results.get('performance_grade', 'unknown').upper()}

Import Time Analysis:
• Average: {component_results.get('average_response_time', 0)}ms
• Fastest: {component_results.get('fastest_operation', 0)}ms
• Slowest: {component_results.get('slowest_operation', 0)}ms

DETAILED OPERATION BREAKDOWN:
----------------------------
"""

        # Add operation details
        for operation in core_results.get('operation_details', []):
            status = "✅" if operation['success'] else "❌"
            report += f"{status} {operation['operation']}: {operation['response_time']}ms\n"

        report += f"""
PERFORMANCE RECOMMENDATIONS:
----------------------------
"""

        avg_time = core_results.get('average_response_time', 0)
        if avg_time < 100:
            report += "Performance is excellent - no optimization needed.\n"
        elif avg_time < 500:
            report += "Performance is good - monitor for regression.\n"
        elif avg_time < 1000:
            report += "Performance is acceptable - consider caching optimization.\n"
        else:
            report += "Performance is slow - immediate optimization required.\n"

        return report

def main():
    """Performance profiling CLI"""
    import argparse

    parser = argparse.ArgumentParser(description="Dashboard Performance Profiler")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--operations", action="store_true", help="Profile core operations only")
    parser.add_argument("--components", action="store_true", help="Profile component loading only")

    args = parser.parse_args()

    profiler = PerformanceProfiler()

    if args.report:
        print(profiler.generate_performance_report())
    elif args.operations:
        results = profiler.profile_core_operations()
        print(f"Operations Performance: {results['performance_grade'].upper()}")
        print(f"Average Response: {results['average_response_time']}ms")
    elif args.components:
        results = profiler.profile_component_loading()
        print(f"Component Loading: {results['performance_grade'].upper()}")
        print(f"Average Import: {results['average_response_time']}ms")
    else:
        # Quick performance check
        results = profiler.profile_core_operations()
        print(f"Dashboard Performance: {results['performance_grade'].upper()}")
        print(f"Success Rate: {results['successful_operations']}/{results['total_operations']}")
        print(f"Average Response: {results['average_response_time']}ms")

if __name__ == "__main__":
    main()
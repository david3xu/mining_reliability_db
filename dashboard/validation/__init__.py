#!/usr/bin/env python3
"""
Dashboard Validation Package
Architecture compliance and performance validation tools.
"""

from dashboard.validation.architecture_validator import ArchitectureValidator, ComplianceResult
from dashboard.validation.performance_profiler import PerformanceProfiler, PerformanceResult
from dashboard.validation.integration_tester import IntegrationTester, IntegrationResult

__all__ = [
    'ArchitectureValidator',
    'ComplianceResult',
    'PerformanceProfiler',
    'PerformanceResult',
    'IntegrationTester',
    'IntegrationResult'
]
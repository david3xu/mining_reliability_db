"""
Mining Reliability Search Algorithms Core Package
Focused search algorithms and pattern discovery for mining reliability data.
"""

__version__ = "1.0.0"

# Core Search Analytics
from mine_core.analytics import PatternDiscovery, WorkflowAnalyzer

# Database Layer for Search Operations
from mine_core.database import get_database

# Essential Utilities for Search
from mine_core.helpers import get_logger, setup_logging
from mine_core.shared import handle_error, setup_project_environment

__all__ = [
    # Database Layer
    "get_database",
    # Helper functions
    "setup_logging",
    "get_logger",
    "handle_error",
    "setup_project_environment",
    # Analytics classes
    "WorkflowAnalyzer",
    "PatternDiscovery",
]

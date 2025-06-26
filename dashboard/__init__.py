#!/usr/bin/env python3
"""
Mining Reliability Search Dashboard - Main Package
Search-focused analytics platform with minimal architecture.
"""

__version__ = "2.0.0"
__author__ = "Mining Analytics Team"
__description__ = "Search-focused operational intelligence dashboard"

# Main application entry point
from dashboard.app import SearchDashboardApp, create_app

__all__ = ["SearchDashboardApp", "create_app", "__version__"]

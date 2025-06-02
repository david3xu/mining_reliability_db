#!/usr/bin/env python3
"""
Mining Reliability Dashboard - Main Package
Professional analytics platform with Core → Adapter → Component architecture.
"""

__version__ = "2.0.0"
__author__ = "Mining Analytics Team"
__description__ = "Professional operational intelligence dashboard"

# Main application entry point
from dashboard.app import PurifiedDashboardApp, create_app

__all__ = ["PurifiedDashboardApp", "create_app", "__version__"]

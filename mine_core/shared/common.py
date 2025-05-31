#!/usr/bin/env python3
"""
Shared Utilities for Mining Reliability Database
Common functions used across modules.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

def setup_project_path():
    """Add project root to Python path - used by all scripts"""
    project_root = Path(__file__).resolve().parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    return project_root

def setup_logging(level: str = "INFO", name: str = None) -> logging.Logger:
    """Standardized logging setup for all modules"""
    from mine_core.shared.constants import LOG_FORMAT

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=LOG_FORMAT
    )

    # Return logger for specific module
    return logging.getLogger(name or __name__)

def handle_error(logger: logging.Logger, error: Exception, context: str) -> None:
    """Standardized error handling"""
    logger.error(f"Error in {context}: {error}")

def get_env_with_default(key: str, default: str) -> str:
    """Safe environment variable access"""
    return os.environ.get(key, default)

def validate_required_env(required_vars: list) -> bool:
    """Validate required environment variables exist"""
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")
    return True

def ensure_directory(path: Path) -> Path:
    """Ensure directory exists, create if necessary"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_project_root() -> Path:
    """Get project root directory"""
    return Path(__file__).resolve().parent.parent.parent

def get_data_directory() -> Path:
    """Get default data directory"""
    return get_project_root() / "data" / "facility_data"

#!/usr/bin/env python3
"""
Consolidated Project Utilities - Environment-independent shared functions
Project setup, logging, and error handling utilities.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional
from configs.environment import get_log_level, get_log_file, get_project_root

def setup_project_path():
    """Add project root to Python path - standardized for all scripts"""
    project_root = get_project_root()
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    return project_root

def setup_logging(level: str = None, name: str = None) -> logging.Logger:
    """Unified logging setup using environment configuration"""
    # Get configuration from environment gateway
    log_level = level or get_log_level()
    log_file = get_log_file()

    # Standardized log format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure root logger
    root_logger = logging.getLogger()

    # Avoid duplicate handlers
    if not root_logger.handlers:
        root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(console_handler)

        # File handler if configured
        if log_file:
            try:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(logging.Formatter(log_format))
                root_logger.addHandler(file_handler)
            except Exception as e:
                print(f"Warning: Could not setup file logging: {e}")

    # Return logger for specific module
    return logging.getLogger(name or __name__)

def setup_project_environment(script_name: str = None, log_level: str = None) -> logging.Logger:
    """Standardized initialization for all scripts - single entry point"""
    # Setup project path
    setup_project_path()

    # Setup logging
    logger = setup_logging(level=log_level, name=script_name or __name__)

    # Log initialization
    logger.info(f"Initialized project environment for {script_name or 'script'}")

    return logger

def handle_error(logger: logging.Logger, error: Exception, context: str) -> None:
    """Standardized error handling and logging"""
    logger.error(f"Error in {context}: {error}")

def ensure_directory(path: Path) -> Path:
    """Ensure directory exists, create if necessary"""
    path.mkdir(parents=True, exist_ok=True)
    return path

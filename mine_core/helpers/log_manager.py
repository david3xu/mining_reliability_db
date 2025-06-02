#!/usr/bin/env python3
"""
Logging Manager
Provides consistent logging setup across the application.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Cache for loggers
_loggers: Dict[str, logging.Logger] = {}


def setup_logging(level: str = None, log_file: str = None, log_format: str = None) -> None:
    """
    Set up application-wide logging configuration

    Parameters:
    -----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log_file : str
        Path to log file (if None, logs to console only)
    log_format : str
        Log message format string
    """
    # Use environment variables if parameters not provided
    level = level or os.environ.get("LOG_LEVEL", "INFO")
    log_file = log_file or os.environ.get("LOG_FILE")
    log_format = log_format or os.environ.get(
        "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Convert level string to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Add file handler if log file specified
    if log_file:
        # Create directory if it doesn't exist
        log_path = Path(log_file)
        log_dir = log_path.parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        # Create rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Log configuration
    root_logger.info(f"Logging configured: level={level}, file={log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name

    If a logger with this name already exists, returns the existing logger.
    Otherwise, creates a new logger.

    Parameters:
    -----------
    name : str
        Logger name (typically __name__ of the calling module)

    Returns:
    --------
    logging.Logger
        Logger instance
    """
    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)
    return _loggers[name]

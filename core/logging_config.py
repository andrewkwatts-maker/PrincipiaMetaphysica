"""
Logging Configuration
=====================

Industry-standard logging setup for the Principia Metaphysica framework.

Features:
- Structured logging with timestamps
- Configurable log levels
- File and console output
- Context managers for operation tracking

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from contextlib import contextmanager
import time


# Define custom log format
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Log directory
LOG_DIR = Path(__file__).parent.parent / "logs"


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for log output
        console: Whether to output to console

    Returns:
        Root logger configured for the application
    """
    # Create root logger for PM
    logger = logging.getLogger("PM")
    logger.setLevel(level)

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        LOG_DIR.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(LOG_DIR / log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        name: Module name (will be prefixed with 'PM.')

    Returns:
        Logger instance
    """
    return logging.getLogger(f"PM.{name}")


@contextmanager
def log_operation(logger: logging.Logger, operation: str, **context):
    """
    Context manager for logging operation start/end with timing.

    Usage:
        with log_operation(logger, "calculate_proton_decay", m_gut=2.118e16):
            result = calculate()
    """
    start_time = time.time()
    context_str = ", ".join(f"{k}={v}" for k, v in context.items())

    logger.info(f"Starting: {operation}" + (f" ({context_str})" if context_str else ""))

    try:
        yield
        elapsed = time.time() - start_time
        logger.info(f"Completed: {operation} (elapsed: {elapsed:.3f}s)")
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Failed: {operation} after {elapsed:.3f}s - {type(e).__name__}: {e}")
        raise


class SimulationLogger:
    """
    Specialized logger for simulation operations.

    Provides structured logging for:
    - Input parameters
    - Intermediate calculations
    - Results and validation
    - Performance metrics
    """

    def __init__(self, simulation_name: str):
        self.logger = get_logger(f"simulation.{simulation_name}")
        self.simulation_name = simulation_name
        self._start_time: Optional[float] = None
        self._step_count = 0

    def start(self, **parameters):
        """Log simulation start with parameters"""
        self._start_time = time.time()
        self._step_count = 0
        self.logger.info(f"=== Starting {self.simulation_name} ===")
        for key, value in parameters.items():
            self.logger.debug(f"  Parameter: {key} = {value}")

    def step(self, description: str, **data):
        """Log a simulation step"""
        self._step_count += 1
        self.logger.info(f"Step {self._step_count}: {description}")
        for key, value in data.items():
            if isinstance(value, float):
                self.logger.debug(f"    {key} = {value:.6g}")
            else:
                self.logger.debug(f"    {key} = {value}")

    def result(self, name: str, value, unit: str = "", expected: Optional[float] = None):
        """Log a result with optional validation"""
        if isinstance(value, float):
            msg = f"Result: {name} = {value:.6g}"
        else:
            msg = f"Result: {name} = {value}"

        if unit:
            msg += f" {unit}"

        if expected is not None and isinstance(value, (int, float)):
            deviation = abs(value - expected) / expected * 100 if expected != 0 else 0
            msg += f" (expected: {expected:.6g}, deviation: {deviation:.2f}%)"

        self.logger.info(msg)

    def complete(self, status: str = "SUCCESS"):
        """Log simulation completion"""
        elapsed = time.time() - self._start_time if self._start_time else 0
        self.logger.info(
            f"=== {self.simulation_name} {status} "
            f"({self._step_count} steps, {elapsed:.3f}s) ==="
        )

    def error(self, message: str, exception: Optional[Exception] = None):
        """Log an error"""
        if exception:
            self.logger.error(f"ERROR: {message} - {type(exception).__name__}: {exception}")
        else:
            self.logger.error(f"ERROR: {message}")

"""
Logging utilities for Omni-Scanner.
Provides consistent logging across all modules with configurable levels.
"""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log messages."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m'  # Magenta
    }
    RESET = '\033[0m'  # Reset color
    
    def format(self, record):
        # Get the original formatted message
        original_format = super().format(record)
        
        # Add color if it's a terminal that supports it
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            color = self.COLORS.get(record.levelname, '')
            if color:
                return f"{color}{original_format}{self.RESET}"
        
        return original_format


def setup_logging(
    level: str = "INFO",
    log_to_file: bool = True,
    log_file: Optional[str] = None,
    quiet: bool = False,
    verbose: bool = False
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to log to a file
        log_file: Custom log file path
        quiet: Suppress console output (only errors)
        verbose: Enable verbose output (DEBUG level)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Determine logging level
    if verbose:
        level = "DEBUG"
    elif quiet:
        level = "ERROR"
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger('omni_scanner')
    logger.setLevel(numeric_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Console handler (unless quiet mode and not error/critical)
    if not quiet or numeric_level >= logging.ERROR:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        
        # Use colored formatter for console
        console_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        console_formatter = ColoredFormatter(console_format, datefmt='%H:%M:%S')
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        if not log_file:
            # Create logs directory if it doesn't exist
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # Generate log filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"omni_scanner_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Always log DEBUG to file
        
        # Detailed format for file
        file_format = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        file_formatter = logging.Formatter(file_format)
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)
        
        # Log the log file location
        logger.info(f"Logging to file: {log_file}")
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__ of the calling module)
        
    Returns:
        logging.Logger: Logger instance
    """
    if name:
        return logging.getLogger(f'omni_scanner.{name}')
    else:
        return logging.getLogger('omni_scanner')


def log_command_execution(logger: logging.Logger, command: list, success: bool, output: str = "", error: str = ""):
    """
    Log command execution details.
    
    Args:
        logger: Logger instance
        command: Command that was executed
        success: Whether the command succeeded
        output: Command output (stdout)
        error: Command error (stderr)
    """
    command_str = ' '.join(command)
    
    if success:
        logger.info(f"Command executed successfully: {command_str}")
        if output:
            logger.debug(f"Command output: {output[:500]}...")  # Truncate long output
    else:
        logger.error(f"Command failed: {command_str}")
        if error:
            logger.error(f"Command error: {error}")


def log_scan_start(logger: logging.Logger, scan_type: str, target: str, options: dict = None):
    """
    Log the start of a scan operation.
    
    Args:
        logger: Logger instance
        scan_type: Type of scan (ping, arp, nmap, etc.)
        target: Target IP/network
        options: Scan options/parameters
    """
    options_str = ""
    if options:
        options_str = f" with options: {options}"
    
    logger.info(f"Starting {scan_type} scan on target: {target}{options_str}")


def log_scan_complete(logger: logging.Logger, scan_type: str, target: str, duration: float, results_file: str = ""):
    """
    Log the completion of a scan operation.
    
    Args:
        logger: Logger instance
        scan_type: Type of scan
        target: Target IP/network
        duration: Scan duration in seconds
        results_file: Path to results file
    """
    file_info = f" Results saved to: {results_file}" if results_file else ""
    logger.info(f"Completed {scan_type} scan on {target} in {duration:.2f} seconds.{file_info}")


def log_error_with_context(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Log an error with additional context.
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context about when/where the error occurred
    """
    context_str = f" Context: {context}" if context else ""
    logger.error(f"Error occurred: {str(error)}{context_str}", exc_info=True)


# Pre-configured logger for quick access
_default_logger = None


def get_default_logger() -> logging.Logger:
    """Get the default logger instance."""
    global _default_logger
    if _default_logger is None:
        _default_logger = setup_logging()
    return _default_logger
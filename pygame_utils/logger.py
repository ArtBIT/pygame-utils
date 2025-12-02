"""
Logging utility module.

Provides a simple logging wrapper around Python's standard logging module
with convenient methods for debug, info, warning, and error messages.
Supports both console and file logging.

Example:
    >>> from pygame_utils.logger import Logger
    >>> logger = Logger(debug=True, log_file='app.log')
    >>> logger.info('Application started')
    >>> logger.debug('Debug information')
"""

import sys
import datetime
import logging
import os


class Logger:
    """
    Simple logging wrapper with convenient methods.
    
    Provides a clean interface for logging with automatic formatting
    and optional file logging in debug mode.
    """
    def __init__(self, name='pygame_utils', debug=False, log_file=None):
        """
        Initialize a new Logger instance.
        
        Args:
            name: The logger name (default: 'pygame_utils')
            debug: If True, enables debug level logging (default: False)
            log_file: Optional path to log file. If None and debug=True,
                     creates a timestamped log file in current directory
        """
        logging_level = logging.DEBUG if debug else logging.INFO
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging_level)
        self.logger.propagate = False
        self.logger.handlers = []
        
        # Console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # File handler (if debug mode or log_file specified)
        if debug or log_file:
            if log_file is None:
                # Generate filename using iso time
                filename = datetime.datetime.now().isoformat().replace(':', '-') + '.log'
                log_file = filename
            
            # Ensure directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            handler = logging.FileHandler(log_file)
            handler.setLevel(logging_level)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_level(self):
        """Get the current logging level."""
        return self.logger.getEffectiveLevel()

    def set_level(self, level):
        """
        Set the logging level.
        
        Args:
            level: Logging level (e.g., logging.DEBUG, logging.INFO)
        """
        self.logger.setLevel(level)

    def args_to_string(self, args):
        """Convert arguments to a single string."""
        return ', '.join([str(arg) for arg in args])

    def debug(self, *args):
        """Log a debug message."""
        self.logger.debug(self.args_to_string(args))

    def info(self, *args):
        """Log an info message."""
        self.logger.info(self.args_to_string(args))

    def warning(self, *args):
        """Log a warning message."""
        self.logger.warning(self.args_to_string(args))

    def error(self, *args):
        """Log an error message."""
        self.logger.error(self.args_to_string(args))


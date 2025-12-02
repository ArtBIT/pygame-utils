"""
Stopwatch module for performance timing.

Provides utilities for measuring elapsed time, useful for profiling
and performance monitoring. Integrates with AppStats for automatic
statistics collection.

Example:
    >>> from pygame_utils.stopwatch import Stopwatch
    >>> Stopwatch.start('operation')
    >>> # ... do work ...
    >>> elapsed = Stopwatch.stop('operation')
    >>> print(f"Operation took {elapsed} seconds")
"""

import time
from .appstats import AppStats


class SingleStopwatch:
    """
    A single stopwatch instance for timing operations.
    
    Tracks start time, elapsed time, and running state for a single
    named operation.
    """
    def __init__(self, name):
        """
        Initialize a new stopwatch.
        
        Args:
            name: The name/identifier for this stopwatch
        """
        self.name = name
        self.start_time = 0
        self.stop_time = 0
        self.running = False

    def start(self):
        """Start the stopwatch."""
        self.reset()
        self.start_time = self.now()
        self.running = True

    def stop(self):
        """
        Stop the stopwatch and record the elapsed time.
        
        Automatically samples the elapsed time to AppStats.
        
        Returns:
            The elapsed time in seconds
        """
        elapsed_time = self.time()
        self.stop_time = elapsed_time
        self.running = False
        AppStats.sample(self.name, elapsed_time)
        return elapsed_time

    def reset(self):
        """Reset the stopwatch to initial state."""
        self.start_time = 0
        self.stop_time = 0
        self.running = False

    def now(self):
        """Get the current process time."""
        return time.process_time()

    def time(self):
        """
        Get the elapsed time.
        
        Returns:
            Elapsed time in seconds (current time if running, stop time if stopped)
        """
        if self.running:
            return self.now() - self.start_time
        return self.stop_time

    def is_running(self):
        """Check if the stopwatch is currently running."""
        return self.running

    def is_stopped(self):
        """Check if the stopwatch is stopped."""
        return not self.running


class Stopwatch:
    """
    Static class for managing multiple named stopwatches.
    
    Provides a global registry of stopwatches that can be started,
    stopped, and queried by name. All stopwatches are stored in a
    class-level dictionary.
    """
    items = {}

    @staticmethod
    def start(name):
        """
        Start a stopwatch by name.
        
        Creates a new stopwatch if one doesn't exist, otherwise
        starts the existing one.
        
        Args:
            name: The name of the stopwatch to start
        """
        if name not in Stopwatch.items:
            Stopwatch.items[name] = SingleStopwatch(name)
        Stopwatch.items[name].start()

    @staticmethod
    def stop(name):
        """
        Stop a stopwatch by name and return elapsed time.
        
        Args:
            name: The name of the stopwatch to stop
            
        Returns:
            The elapsed time in seconds, or None if stopwatch doesn't exist
        """
        if name in Stopwatch.items:
            elapsed = Stopwatch.items[name].stop()
            return elapsed
        return None

    @staticmethod
    def reset(name):
        """
        Reset a stopwatch by name.
        
        Args:
            name: The name of the stopwatch to reset
        """
        if name in Stopwatch.items:
            Stopwatch.items[name].reset()

    @staticmethod
    def time(name):
        """
        Get the elapsed time for a stopwatch by name.
        
        Args:
            name: The name of the stopwatch
            
        Returns:
            The elapsed time in seconds, or None if stopwatch doesn't exist
        """
        if name in Stopwatch.items:
            return Stopwatch.items[name].time()
        return None

    @staticmethod
    def is_running(name):
        """
        Check if a stopwatch is running.
        
        Args:
            name: The name of the stopwatch
            
        Returns:
            True if running, False otherwise
        """
        if name in Stopwatch.items:
            return Stopwatch.items[name].is_running()
        return False

    @staticmethod
    def is_stopped(name):
        """
        Check if a stopwatch is stopped.
        
        Args:
            name: The name of the stopwatch
            
        Returns:
            True if stopped, False otherwise
        """
        if name in Stopwatch.items:
            return Stopwatch.items[name].is_stopped()
        return True

    @staticmethod
    def stats(name):
        """
        Get statistics for a stopwatch from AppStats.
        
        Args:
            name: The name of the stopwatch
            
        Returns:
            The AppStat object for this stopwatch, or None if it doesn't exist
        """
        if name not in Stopwatch.items:
            return None
        return AppStats.get(name)


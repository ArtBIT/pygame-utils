"""
Performance statistics tracking module.

This module provides utilities for tracking performance metrics over time,
including minimum, maximum, mean, and current values. Useful for profiling
and monitoring application performance.

Example:
    >>> from pygame_utils.appstats import AppStats
    >>> AppStats.sample('fps', 60)
    >>> AppStats.sample('fps', 58)
    >>> stat = AppStats.get('fps')
    >>> print(stat.mean)  # Average FPS
"""


class AppStat:
    """
    Represents a single performance statistic that tracks values over time.
    
    Tracks the current value, total number of samples, mean (moving average),
    minimum, and maximum values.
    """
    def __init__(self, name, value):
        """
        Initialize a new statistic.
        
        Args:
            name: The name/identifier of this statistic
            value: The initial value
        """
        self.name = name
        self.value = value
        self.total_samples = 1
        self.mean = value
        self.min = value
        self.max = value

    def sample(self, value):
        """
        Add a new sample value to the statistic.
        
        Updates the current value, mean (using moving average), min, and max.
        
        Args:
            value: The new sample value to record
        """
        self.value = value
        self.total_samples += 1
        # mean is the average of a list of numbers
        # but since we don't have a list of numbers, we can't calculate the mean, using the moving average
        self.mean += (value - self.mean) / self.total_samples

        self.min = min(self.min, value)
        self.max = max(self.max, value)

    def reset(self):
        """Reset all statistic values to zero."""
        self.value = 0
        self.total_samples = 0
        self.mean = 0
        self.min = 0
        self.max = 0

    def __str__(self):
        """Return a formatted string representation of the statistic."""
        # round to 2 decimal precision
        precision = 3
        result = "\n-----------------"
        result += f"\nStat({self.name})"
        result += f"\n  value: {self.value}"
        result += f"\n  total_samples: {self.total_samples}"
        result += f"\n  mean: {round(self.mean,precision)}"
        result += f"\n  min: {round(self.min,precision)}"
        result += f"\n  max: {round(self.max,precision)}"
        result += "\n-----------------"
        return result

    def __repr__(self):
        return self.__str__()


class AppStats:
    """
    Static class for managing multiple performance statistics.
    
    Provides a global registry of statistics that can be sampled and retrieved
    by name. All statistics are stored in a class-level dictionary.
    """
    items = {}

    @staticmethod
    def sample(name, value):
        """
        Sample a value for a statistic by name.
        
        Creates a new AppStat if one doesn't exist, otherwise adds the sample
        to the existing statistic.
        
        Args:
            name: The name of the statistic
            value: The value to sample
            
        Returns:
            The AppStat object for this statistic
        """
        if name not in AppStats.items:
            AppStats.items[name] = AppStat(name, value)
        else:
            AppStats.items[name].sample(value)
        return AppStats.items[name]

    @staticmethod
    def get(name=None):
        """
        Get a statistic by name, or all statistics.
        
        Args:
            name: The name of the statistic to retrieve, or None for all statistics
            
        Returns:
            The AppStat object if name is provided, or a dict of all statistics
        """
        if name is not None:
            return AppStats.items[name]
        return AppStats.items

    @staticmethod
    def __str__():
        """Return a formatted string representation of all statistics."""
        result = "\n================="
        for name, stat in AppStats.items.items():
            result += f"{stat}"
        result += "\n================="
        return result

    @staticmethod
    def __repr__():
        return AppStats.__str__()


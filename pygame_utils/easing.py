"""
Easing functions module.

Provides a comprehensive library of easing functions for smooth animations
and transitions. Easing functions control the rate of change over time,
creating natural-feeling motion.

All easing functions follow the signature: (t, b, c, d)
- t: current time (0 to d)
- b: start value
- c: change in value (end - start)
- d: duration

Example:
    >>> from pygame_utils.easing import Easing, EasingFunctions
    >>> easing = Easing(0, 100, 100, EasingFunctions.ease_in_out_quad)
    >>> value = easing.update(50)  # Get value at time 50
"""

import math


class Easing:
    """
    Easing calculator that applies an easing function to a value range.
    
    Takes a start value, end value, duration, and easing function,
    and can calculate the eased value at any point in time.
    """
    def __init__(self, start, end, duration, easing_function):
        """
        Initialize an easing calculation.
        
        Args:
            start: The starting value
            end: The ending value
            duration: The total duration of the easing
            easing_function: The easing function to use (from EasingFunctions)
        """
        self.start = start
        self.end = end
        self.duration = duration
        self.easing_function = easing_function

    def update(self, t):
        """
        Calculate the eased value at time t.
        
        Args:
            t: Current time (should be between 0 and duration)
            
        Returns:
            The eased value at time t
        """
        return self.easing_function(t, self.start, self.end - self.start, self.duration)

    @staticmethod
    def ease(from_value, to_value, duration, easing_function):
        """
        Create a new Easing instance.
        
        Args:
            from_value: The starting value
            to_value: The ending value
            duration: The total duration
            easing_function: The easing function to use
            
        Returns:
            A new Easing instance
        """
        return Easing(from_value, to_value, duration, easing_function)


class EasingFunctions:
    """
    Collection of easing functions for animations.
    
    All functions follow the signature: (t, b, c, d)
    - t: current time (0 to d)
    - b: start value
    - c: change in value (end - start)
    - d: duration
    
    Functions are available in three variants:
    - ease_in: Slow start, fast end
    - ease_out: Fast start, slow end
    - ease_in_out: Slow start and end, fast middle
    """
    
    @staticmethod
    def linear(t, b, c, d):
        """
        Linear easing - constant rate of change.
        
        Args:
            t: current time
            b: start value
            c: change in value, end - start
            d: duration
        """
        return c*t/d + b

    @staticmethod
    def ease_in_quad(t, b, c, d):
        """Quadratic ease-in - slow start, accelerating."""
        t /= d
        return c*t*t + b

    @staticmethod
    def ease_out_quad(t, b, c, d):
        """Quadratic ease-out - fast start, decelerating."""
        t /= d
        return -c * t*(t-2) + b

    @staticmethod
    def ease_in_out_quad(t, b, c, d):
        """Quadratic ease-in-out - slow start and end, fast middle."""
        t /= d/2
        if t < 1:
            return c/2*t*t + b
        t -= 1
        return -c/2 * (t*(t-2) - 1) + b

    @staticmethod
    def ease_in_cubic(t, b, c, d):
        """Cubic ease-in - very slow start."""
        t /= d
        return c*t*t*t + b

    @staticmethod
    def ease_out_cubic(t, b, c, d):
        """Cubic ease-out - very fast start."""
        t /= d
        t -= 1
        return c*(t*t*t + 1) + b

    @staticmethod
    def ease_in_out_cubic(t, b, c, d):
        """Cubic ease-in-out - very slow start and end."""
        t /= d/2
        if t < 1:
            return c/2*t*t*t + b
        t -= 2
        return c/2*(t*t*t + 2) + b

    @staticmethod
    def ease_in_quart(t, b, c, d):
        """Quartic ease-in - extremely slow start."""
        t /= d
        return c*t*t*t*t + b

    @staticmethod
    def ease_out_quart(t, b, c, d):
        """Quartic ease-out - extremely fast start."""
        t /= d
        t -= 1
        return -c * (t*t*t*t - 1) + b

    @staticmethod
    def ease_in_out_quart(t, b, c, d):
        """Quartic ease-in-out - extremely slow start and end."""
        t /= d/2
        if t < 1:
            return c/2*t*t*t*t + b
        t -= 2
        return -c/2 * (t*t*t*t - 2) + b

    @staticmethod
    def ease_in_quint(t, b, c, d):
        """Quintic ease-in - very extreme slow start."""
        t /= d
        return c*t*t*t*t*t + b

    @staticmethod
    def ease_out_quint(t, b, c, d):
        """Quintic ease-out - very extreme fast start."""
        t /= d
        t -= 1
        return c*(t*t*t*t*t + 1) + b

    @staticmethod
    def ease_in_out_quint(t, b, c, d):
        """Quintic ease-in-out - very extreme slow start and end."""
        t /= d/2
        if t < 1:
            return c/2*t*t*t*t*t + b
        t -= 2
        return c/2*(t*t*t*t*t + 2) + b

    @staticmethod
    def ease_in_sine(t, b, c, d):
        """Sine ease-in - smooth slow start."""
        return -c * math.cos(t/d * (math.pi/2)) + c + b

    @staticmethod
    def ease_out_sine(t, b, c, d):
        """Sine ease-out - smooth fast start."""
        return c * math.sin(t/d * (math.pi/2)) + b

    @staticmethod
    def ease_in_out_sine(t, b, c, d):
        """Sine ease-in-out - smooth slow start and end."""
        return -c/2 * (math.cos(math.pi*t/d) - 1) + b

    @staticmethod
    def ease_in_expo(t, b, c, d):
        """Exponential ease-in - very dramatic slow start."""
        return c * math.pow( 2, 10 * (t/d - 1) ) + b

    @staticmethod
    def ease_out_expo(t, b, c, d):
        """Exponential ease-out - very dramatic fast start."""
        return c * ( -math.pow( 2, -10 * t/d ) + 1 ) + b

    @staticmethod
    def ease_in_out_expo(t, b, c, d):
        """Exponential ease-in-out - very dramatic slow start and end."""
        t /= d/2
        if t < 1:
            return c/2 * math.pow( 2, 10 * (t - 1) ) + b
        t -= 1
        return c/2 * ( -math.pow( 2, -10 * t) + 2 ) + b

    @staticmethod
    def ease_in_circ(t, b, c, d):
        """Circular ease-in - accelerating circular motion."""
        t /= d
        return -c * (math.sqrt(1 - t*t) - 1) + b

    @staticmethod
    def ease_out_circ(t, b, c, d):
        """Circular ease-out - decelerating circular motion."""
        t /= d
        t -= 1
        return c * math.sqrt(1 - t*t) + b

    @staticmethod
    def ease_in_out_circ(t, b, c, d):
        """Circular ease-in-out - circular motion with slow start and end."""
        t /= d/2
        if t < 1:
            return -c/2 * (math.sqrt(1 - t*t) - 1) + b
        t -= 2
        return c/2 * (math.sqrt(1 - t*t) + 1) + b

    @staticmethod
    def ease_in_elastic(t, b, c, d, a=None, p=None):
        """
        Elastic ease-in - bouncy effect with slow start.
        
        Args:
            t: current time
            b: start value
            c: change in value
            d: duration
            a: amplitude (optional, defaults to c)
            p: period (optional, defaults to d * 0.3)
        """
        if t == 0:
            return b
        t /= d
        if t == 1:
            return b + c
        if not p:
            p = d * 0.3
        if not a or a < abs(c):
            a = c
            s = p/4
        else:
            s = p/(2*math.pi) * math.asin (c/a)
        t -= 1
        return -(a*math.pow(2,10*t) * math.sin( (t*d-s)*(2*math.pi)/p )) + b

    @staticmethod
    def ease_out_elastic(t, b, c, d, a=None, p=None):
        """
        Elastic ease-out - bouncy effect with fast start.
        
        Args:
            t: current time
            b: start value
            c: change in value
            d: duration
            a: amplitude (optional, defaults to c)
            p: period (optional, defaults to d * 0.3)
        """
        if t == 0:
            return b
        t /= d
        if t == 1:
            return b + c
        if not p:
            p = d * 0.3
        if not a or a < abs(c):
            a = c
            s = p/4
        else:
            s = p/(2*math.pi) * math.asin (c/a)
        return a*math.pow(2,-10*t) * math.sin( (t*d-s)*(2*math.pi)/p ) + c + b

    @staticmethod
    def ease_in_out_elastic(t, b, c, d, a=None, p=None):
        """
        Elastic ease-in-out - bouncy effect with slow start and end.
        
        Args:
            t: current time
            b: start value
            c: change in value
            d: duration
            a: amplitude (optional, defaults to c)
            p: period (optional, defaults to d * 0.3 * 1.5)
        """
        if t == 0:
            return b
        t /= d/2
        if t == 2:
            return b + c
        if not p:
            p = d*(0.3*1.5)
        if not a or a < abs(c):
            a = c
            s = p/4
        else:
            s = p/(2*math.pi) * math.asin (c/a)
        if t < 1:
            t -= 1
            return -0.5*(a*math.pow(2,10*t) * math.sin( (t*d-s)*(2*math.pi)/p )) + b
        t -= 1
        return a*math.pow(2,-10*t) * math.sin( (t*d-s)*(2*math.pi)/p )*0.5 + c + b


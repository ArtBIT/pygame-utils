"""
Tweening/animation module.

Provides smooth value interpolation over time with various easing functions.
Supports pause/resume, repeat, ping-pong, and event callbacks.

Example:
    >>> from pygame_utils.tween import Tween, EasingFunctions
    >>> tween = Tween(0, 100, 2.0, 'easeInOutQuad')
    >>> while not tween.is_completed:
    ...     tween.update()
    ...     print(tween.value)
    ... # or call tween.update() in your game loop
"""

import time
from .events import Events
from .easing import EasingFunctions


def now():
    """Get current time in milliseconds."""
    return round(time.time() * 1000)


def lerp(a, b, value):
    """
    Linear interpolation between two values.
    
    Args:
        a: Start value (can be int, float, list, tuple)
        b: End value (must match type of a)
        value: Interpolation factor (0.0 to 1.0)
        
    Returns:
        Interpolated value
    """
    t = type(a)
    if t is list:
        return [lerp(x, y, value) for x, y in zip(a, b)]
    elif t is tuple:
        return tuple(lerp(x, y, value) for x, y in zip(a, b))
    elif t is int:
        return a + int((b - a) * value)
    elif t is float:
        return a + (b - a) * value
    elif t is str:
        # Simple string interpolation (returns substring)
        alen = len(a)
        blen = len(b)
        diff = blen - alen
        pos = int(diff * value)
        return b[:pos]
    return b


# Map easing function names to EasingFunctions methods
# Normalized to 0-1 range for tween library compatibility
def _normalize_easing(func):
    """Wrap easing function to work with 0-1 normalized time."""
    def wrapper(t):
        # t is 0-1, convert to (t, 0, 1, 1) for easing function
        return func(t, 0, 1, 1)
    return wrapper


tween_functions_lookup = {
    'linear': _normalize_easing(EasingFunctions.linear),
    'easeInQuad': _normalize_easing(EasingFunctions.ease_in_quad),
    'easeOutQuad': _normalize_easing(EasingFunctions.ease_out_quad),
    'easeInOutQuad': _normalize_easing(EasingFunctions.ease_in_out_quad),
    'easeInCubic': _normalize_easing(EasingFunctions.ease_in_cubic),
    'easeOutCubic': _normalize_easing(EasingFunctions.ease_out_cubic),
    'easeInOutCubic': _normalize_easing(EasingFunctions.ease_in_out_cubic),
    'easeInQuart': _normalize_easing(EasingFunctions.ease_in_quart),
    'easeOutQuart': _normalize_easing(EasingFunctions.ease_out_quart),
    'easeInOutQuart': _normalize_easing(EasingFunctions.ease_in_out_quart),
    'easeInQuint': _normalize_easing(EasingFunctions.ease_in_quint),
    'easeOutQuint': _normalize_easing(EasingFunctions.ease_out_quint),
    'easeInOutQuint': _normalize_easing(EasingFunctions.ease_in_out_quint),
    'easeInSine': _normalize_easing(EasingFunctions.ease_in_sine),
    'easeOutSine': _normalize_easing(EasingFunctions.ease_out_sine),
    'easeInOutSine': _normalize_easing(EasingFunctions.ease_in_out_sine),
    'easeInExpo': _normalize_easing(EasingFunctions.ease_in_expo),
    'easeOutExpo': _normalize_easing(EasingFunctions.ease_out_expo),
    'easeInOutExpo': _normalize_easing(EasingFunctions.ease_in_out_expo),
    'easeInCirc': _normalize_easing(EasingFunctions.ease_in_circ),
    'easeOutCirc': _normalize_easing(EasingFunctions.ease_out_circ),
    'easeInOutCirc': _normalize_easing(EasingFunctions.ease_in_out_circ),
    'easeInElastic': _normalize_easing(EasingFunctions.ease_in_elastic),
    'easeOutElastic': _normalize_easing(EasingFunctions.ease_out_elastic),
    'easeInOutElastic': _normalize_easing(EasingFunctions.ease_in_out_elastic),
}


def get_tween(name):
    """
    Get an easing function by name.
    
    Args:
        name: Name of the easing function
        
    Returns:
        Easing function that takes 0-1 normalized time
    """
    if name in tween_functions_lookup:
        return tween_functions_lookup[name]
    # Fallback to linear if not found
    return tween_functions_lookup['linear']


class TweenProps:
    """Properties for a tween animation."""
    def __init__(self, from_value, to_value, duration, easing, repeat=1, pingpong=0):
        """
        Initialize tween properties.
        
        Args:
            from_value: Starting value
            to_value: Ending value
            duration: Duration in seconds
            easing: Easing function name (string)
            repeat: Number of times to repeat (0 = no repeat, -1 = infinite)
            pingpong: Number of times to ping-pong (0 = no ping-pong, -1 = infinite)
        """
        self.from_value = from_value
        self.to_value = to_value
        self.duration = duration
        self.easing = easing
        self.repeat = repeat
        self.pingpong = pingpong


class Tween:
    """
    Tween animation for smooth value interpolation.
    
    Interpolates between two values over time using an easing function.
    Supports pause/resume, repeat, ping-pong, and event callbacks.
    """
    def __init__(self, from_value, to_value, duration, easing, repeat=1,
                 update_callback=None, complete_callback=None, auto_start=True, pingpong=0):
        """
        Initialize a new tween.
        
        Args:
            from_value: Starting value
            to_value: Ending value
            duration: Duration in seconds
            easing: Easing function name (string) or function
            repeat: Number of times to repeat (default: 1)
            update_callback: Function called on each update with current value
            complete_callback: Function called when tween completes
            auto_start: If True, start immediately (default: True)
            pingpong: Number of times to ping-pong (default: 0)
        """
        self.props = TweenProps(from_value, to_value, duration, easing, repeat, pingpong)
        self.value = from_value
        self.events = Events()
        if update_callback:
            self.events.on('update', update_callback)
        if complete_callback:
            self.events.on('complete', complete_callback)
        self.reset()
        self.direction = 1
        self.pingpong = 0
        self.count = 0

        if auto_start:
            self.start()

    def on(self, event_name, callback):
        """Subscribe to a tween event."""
        self.events.on(event_name, callback)

    def off(self, event_name, callback):
        """Unsubscribe from a tween event."""
        self.events.off(event_name, callback)

    def reset(self):
        """Reset the tween to initial state."""
        self.start_time = now()
        self.time = 0
        self.is_paused = False
        self.pause_duration = 0
        self.paused_at = 0
        self.is_running = False
        self.is_completed = False

    def start(self):
        """Start the tween."""
        self.is_running = True
        self.start_time = now()

    def stop(self):
        """Stop the tween."""
        if self.is_running:
            self.is_running = False
        self.events.reset()

    def restart(self):
        """Restart the tween from the beginning."""
        self.reset()
        if self.direction == 1:
            self.value = self.props.from_value
        else:
            self.value = self.props.to_value
        self.start()

    def pause(self):
        """Pause the tween."""
        if not self.is_paused:
            self.is_paused = True
            self.paused_at = now()

    def unpause(self):
        """Resume the paused tween."""
        if self.is_paused:
            self.is_paused = False
            self.pause_duration += now() - self.paused_at
            self.paused_at = 0

    def flip(self):
        """Reverse the tween direction."""
        self.direction *= -1

    def complete(self):
        """Mark the tween as completed and fire events."""
        self.events.trigger('update', self.value)
        self.events.trigger('complete', self.value)
        self.is_completed = True
        self.stop()

    def done(self):
        """Handle tween cycle completion."""
        self.value = self.props.to_value
        
        # Handle ping-pong
        if self.props.pingpong != 0:
            if self.direction == 1:
                self.flip()
                return self.restart()
            else:
                self.pingpong += 1
                if self.pingpong < self.props.pingpong or self.props.pingpong == -1:
                    self.flip()
                    return self.restart()
                self.value = self.props.from_value
                self.flip()
                self.pingpong = 0
        
        # Handle repeat
        self.count += 1
        if self.props.repeat == 0:
            return self.complete()
        if self.props.repeat == -1:
            return self.restart()
        if self.count < self.props.repeat:
            return self.restart()
        return self.complete()

    def update(self):
        """
        Update the tween (call once per frame).
        
        Returns:
            Current interpolated value
        """
        if self.is_paused:
            return self.value

        if self.is_completed:
            return self.value

        if not self.is_running:
            return self.value

        # Calculate elapsed time
        ts = now()
        dt = (ts - self.start_time - self.pause_duration) / 1000.0
        self.time = max(0, min(1, dt / self.props.duration))

        # Apply direction
        if self.direction == 1:
            tween_time = self.time
        else:
            tween_time = 1 - self.time

        # Get easing function and apply
        easing_func = get_tween(self.props.easing)
        tween_value = easing_func(tween_time)
        self.value = lerp(self.props.from_value, self.props.to_value, tween_value)

        self.events.trigger('update', self.value)

        if self.time >= 1:
            self.done()

        return self.value


class Tweens:
    """
    Manager for multiple tweens running in parallel.
    
    Provides a convenient way to update multiple tweens at once.
    """
    def __init__(self):
        """Initialize a new Tweens manager."""
        self.tweens = []

    def update(self):
        """Update all running tweens and remove completed ones."""
        for tween in self.tweens:
            tween.update()
        # Remove completed tweens
        self.tweens = [tween for tween in self.tweens if not tween.is_completed]

    def append(self, from_value, to_value, duration, easing, repeat=1,
               update_callback=None, pingpong=0):
        """
        Create and add a new tween.
        
        Returns:
            The created Tween instance
        """
        tween = Tween(from_value, to_value, duration, easing, repeat,
                     update_callback, pingpong=pingpong)
        self.tweens.append(tween)
        return tween

    def reset(self):
        """Reset all tweens (stops them)."""
        self.stop()

    def stop(self):
        """Stop all running tweens."""
        while len(self.tweens) > 0:
            tween = self.tweens.pop()
            tween.stop()

    def pause(self):
        """Pause all running tweens."""
        for tween in self.tweens:
            tween.pause()

    def unpause(self):
        """Resume all paused tweens."""
        for tween in self.tweens:
            tween.unpause()


class TweenGroup:
    """
    Group of tweens that can be managed together.
    
    Useful for coordinating multiple tweens and waiting for all to complete.
    """
    def __init__(self, tweens):
        """
        Initialize a tween group.
        
        Args:
            tweens: List of Tween instances
        """
        self.tweens = tweens

    def on(self, event_name, callback):
        """
        Subscribe to an event that fires when all tweens fire the event.
        
        Args:
            event_name: Event name to listen for
            callback: Function to call when all tweens have fired
        """
        tweens_fired = set()
        
        def on_tween_fire(*kwargs):
            tweens_fired.add(id(kwargs))
            if len(tweens_fired) == len(self.tweens):
                callback(*kwargs)

        for tween in self.tweens:
            tween.on(event_name, on_tween_fire)

    @property
    def is_complete(self):
        """Check if all tweens in the group are complete."""
        for tween in self.tweens:
            if not tween.is_completed:
                return False
        return True

    def stop(self):
        """Stop all tweens in the group."""
        for tween in self.tweens:
            tween.stop()


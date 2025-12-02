"""
Timer utilities module.

Provides game timer functionality with delta time tracking, FPS monitoring,
and callback scheduling (setTimeout/setInterval). Requires pygame.

Example:
    >>> import pygame
    >>> from pygame_utils.timer import GameTimer
    >>> pygame.init()
    >>> screen = pygame.display.set_mode((800, 600))
    >>> timer = GameTimer(fps=60)
    >>> timer.set_timeout(lambda: print("5 seconds passed"), 5000)
    >>> while running:
    ...     timer.update()
    ...     dt = timer.delta_time()
"""

import logging

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    pygame = None

from .events import Events


timer_ids = 0


class TimedCallbacks:
    """
    Manages scheduled callbacks (timeouts and intervals).
    
    Tracks callbacks that should be executed at specific times
    and executes them when their time arrives.
    """
    def __init__(self, timer):
        """
        Initialize timed callbacks manager.
        
        Args:
            timer: GameTimer instance to get current time from
        """
        self.timer = timer
        self.callbacks = []

    def update(self):
        """Execute all callbacks that are due."""
        if len(self.callbacks) == 0:
            return

        now = self.timer.time()
        callbacks_to_run = []
        
        # Collect callbacks that are due (iterate backwards for safe deletion)
        i = len(self.callbacks)
        while i > 0:
            i -= 1
            timer_id, callback_time, callback = self.callbacks[i]
            if now >= callback_time:
                callbacks_to_run.append(callback)
                del self.callbacks[i]

        # Execute callbacks
        for callback in callbacks_to_run:
            try:
                callback()
            except Exception as e:
                logging.error(f"Error in timed callback: {e}")

    def append(self, callback, delay=None, time=None):
        """
        Schedule a callback to run at a specific time.
        
        Args:
            callback: Function to call
            delay: Delay in seconds before executing (converted to milliseconds)
            time: Absolute time in milliseconds to execute (if delay not provided)
            
        Returns:
            Timer ID that can be used to cancel the callback
        """
        global timer_ids
        timer_ids += 1
        timer_id = timer_ids
        
        if delay is not None:
            callback_time = self.timer.time() + int(delay * 1000)
        else:
            callback_time = time
        
        self.callbacks.append((timer_id, callback_time, callback))
        return timer_id

    def set_timeout(self, callback, delay):
        """
        Schedule a callback to run once after a delay.
        
        Args:
            callback: Function to call
            delay: Delay in seconds
            
        Returns:
            Timer ID that can be used to cancel
        """
        return self.append(callback, delay=delay)

    def run_interval(self, callback, delay=None):
        """
        Run a callback immediately, then schedule it to repeat.
        
        Args:
            callback: Function to call
            delay: Delay in seconds between calls
            
        Returns:
            Timer ID that can be used to cancel
        """
        callback()
        return self.set_interval(callback, delay=delay)

    def set_interval(self, callback, delay=None):
        """
        Schedule a callback to run repeatedly at intervals.
        
        Args:
            callback: Function to call
            delay: Delay in seconds between calls
            
        Returns:
            Timer ID that can be used to cancel
        """
        def interval_wrapper():
            callback()
            self.set_interval(callback, delay=delay)
        
        return self.append(interval_wrapper, delay=delay)

    def cancel(self, timer_id):
        """
        Cancel a scheduled callback by timer ID.
        
        Args:
            timer_id: The timer ID returned by set_timeout or set_interval
        """
        for i, callback_data in enumerate(self.callbacks):
            if callback_data[0] == timer_id:
                del self.callbacks[i]
                return

    def cancel_timeout(self, timer_id):
        """Cancel a timeout by timer ID."""
        self.cancel(timer_id)

    def cancel_interval(self, timer_id):
        """Cancel an interval by timer ID."""
        self.cancel(timer_id)


class GameTimer:
    """
    Game timer with delta time tracking and FPS monitoring.
    
    Provides frame timing, delta time calculation, and callback scheduling.
    Requires pygame for clock functionality.
    """
    def __init__(self, fps=60):
        """
        Initialize a new game timer.
        
        Args:
            fps: Target frames per second (default: 60)
        """
        if not HAS_PYGAME:
            raise ImportError("pygame is required for GameTimer. Install it with: pip install pygame")
        
        self.fps = fps
        self.callbacks = TimedCallbacks(self)
        self.clock = pygame.time.Clock()
        self.ticks = 0
        self.frameCount = 0
        self.dt = 0
        self.update_time()

    def set_timeout(self, callback, delay):
        """
        Schedule a callback to run once after a delay.
        
        Args:
            callback: Function to call
            delay: Delay in seconds
            
        Returns:
            Timer ID that can be used to cancel
        """
        return self.callbacks.set_timeout(callback, delay)

    def set_interval(self, callback, delay):
        """
        Schedule a callback to run repeatedly at intervals.
        
        Args:
            callback: Function to call
            delay: Delay in seconds between calls
            
        Returns:
            Timer ID that can be used to cancel
        """
        return self.callbacks.set_interval(callback, delay)

    def cancel_timeout(self, timer_id):
        """Cancel a timeout by timer ID."""
        self.callbacks.cancel_timeout(timer_id)

    def cancel_interval(self, timer_id):
        """Cancel an interval by timer ID."""
        self.callbacks.cancel_interval(timer_id)

    def update_time(self):
        """Update timing information (called automatically by update())."""
        # Elapsed time in milliseconds since last frame
        dt_ms = self.clock.tick(self.fps)
        # Elapsed time since last frame in seconds
        self.dt = dt_ms / 1000.0
        # Total elapsed time in milliseconds since pygame.init()
        self.ticks = pygame.time.get_ticks()

    def update(self):
        """
        Update the timer (call once per frame).
        
        Updates frame timing and executes scheduled callbacks.
        """
        self.frameCount += 1
        self.update_time()
        self.callbacks.update()

    def time(self):
        """
        Get the current time in milliseconds.
        
        Returns:
            Milliseconds since pygame.init()
        """
        return self.ticks

    def fps(self):
        """
        Get the current frames per second.
        
        Returns:
            Current FPS as a float
        """
        return round(self.clock.get_fps(), 2)

    def delta_time(self):
        """
        Get the time since the last frame in seconds.
        
        Returns:
            Delta time in seconds
        """
        return self.dt

    def frame(self):
        """
        Get the number of frames since the timer started.
        
        Returns:
            Frame count
        """
        return self.frameCount


class Timer(Events):
    """
    Simple countdown timer with pause/resume support.
    
    Fires a 'done' event when the timer completes. Can be set to loop.
    """
    def __init__(self, timer, duration, loop=False):
        """
        Initialize a new timer.
        
        Args:
            timer: GameTimer instance to get time from
            duration: Duration in milliseconds
            loop: If True, timer restarts automatically when done
        """
        super().__init__()
        self.timer = timer
        self.loop = loop
        self.duration = duration
        self.started_at = 0
        self.paused_at = 0
        self.pause_time = 0
        self.is_running = False
        self.is_paused = False

    def stop(self):
        """Stop the timer."""
        if not self.is_running:
            return
        self.is_running = False

    def start(self):
        """Start the timer."""
        if self.is_running:
            return

        self.started_at = self.timer.time()
        self.pause_time = 0
        self.is_running = True

    def pause(self):
        """Pause the timer."""
        if self.is_paused:
            return
        self.is_paused = True
        self.paused_at = self.timer.time()

    def unpause(self):
        """Resume the paused timer."""
        if not self.is_paused:
            return
        self.is_paused = False
        self.pause_time += self.timer.time() - self.paused_at

    def update(self):
        """
        Update the timer (call once per frame or via event system).
        
        Checks if timer has completed and fires 'done' event if so.
        """
        if not self.is_running or self.is_paused:
            return

        now = self.timer.time()
        if now - self.started_at + self.pause_time >= self.duration:
            self.pause_time = 0
            self.emit('done')
            if self.loop:
                self.started_at = now
            else:
                self.stop()


"""
pygame-utils: A collection of utility modules for pygame development.

This package provides various utilities for game development including:
- Performance statistics tracking
- Event system
- Easing functions
- Logging utilities
- Persistent registry
- Object pooling
- Stopwatch/timing
- TexturePacker JSON parser
- Timer utilities
- Tweening/animation

Example:
    >>> from pygame_utils import AppStats, Events, Tween
    >>> stats = AppStats.sample('fps', 60)
    >>> events = Events()
    >>> tween = Tween(0, 100, 2.0, 'easeInOutQuad')
"""

from .appstats import AppStat, AppStats
from .events import Event, CallbackList, Events
from .easing import Easing, EasingFunctions
from .logger import Logger
from .registry import Registry
from .pool import ObjectPool
from .stopwatch import SingleStopwatch, Stopwatch
from .texturepacker import TexturePacker
from .timer import TimedCallbacks, GameTimer, Timer
from .tween import (
    now, lerp, get_tween, TweenProps, Tween, Tweens, TweenGroup
)

__version__ = '0.1.0'
__all__ = [
    # AppStats
    'AppStat',
    'AppStats',
    # Events
    'Event',
    'CallbackList',
    'Events',
    # Easing
    'Easing',
    'EasingFunctions',
    # Logger
    'Logger',
    # Registry
    'Registry',
    # Pool
    'ObjectPool',
    # Stopwatch
    'SingleStopwatch',
    'Stopwatch',
    # TexturePacker
    'TexturePacker',
    # Timer
    'TimedCallbacks',
    'GameTimer',
    'Timer',
    # Tween
    'now',
    'lerp',
    'get_tween',
    'TweenProps',
    'Tween',
    'Tweens',
    'TweenGroup',
]


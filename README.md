# pygame-utils

A collection of utility modules for pygame development, providing essential tools for game development including performance tracking, event systems, animations, input handling, and more.

## Used In

These utilities are used in **[Zen Rage](https://store.steampowered.com/app/2934010/Zen_Rage/)** - a digital stress ball game available on Steam. Digitally demolish any image with chainsaws, hammers, machine guns, and more!

## Features

- **Zero dependencies** for core modules (only standard library)
- **Optional dependencies** for enhanced functionality (pygame, pynput, appdirs)
- **Well-documented** with examples and API reference
- **Modular design** - use only what you need

## Installation

```bash
pip install pygame-utils
```

For optional features:

```bash
# With pygame support
pip install pygame-utils[pygame]

# With all optional dependencies
pip install pygame-utils[all]
```

## Modules

### AppStats - Performance Statistics

Track performance metrics over time with min/max/mean calculations.

```python
from pygame_utils import AppStats

# Sample values
AppStats.sample('fps', 60)
AppStats.sample('fps', 58)
AppStats.sample('fps', 62)

# Get statistics
stat = AppStats.get('fps')
print(f"Mean FPS: {stat.mean}")
print(f"Min FPS: {stat.min}")
print(f"Max FPS: {stat.max}")
```

### Events - Event System

Event emitter/listener pattern for decoupled component communication.

```python
from pygame_utils import Events

events = Events()

# Subscribe to events
def on_click(data):
    print(f"Clicked: {data}")

events.on('click', on_click)

# Trigger events
events.emit('click', 'button1')

# One-time listener
events.once('startup', lambda: print("Game started!"))

# Unsubscribe
events.off('click', on_click)
```

### Easing - Easing Functions

Comprehensive library of easing functions for smooth animations.

```python
from pygame_utils import Easing, EasingFunctions
import math

# Create an easing
easing = Easing(0, 100, 100, EasingFunctions.ease_in_out_quad)

# Get eased value at time t
value = easing.update(50)  # Value at time 50

# Use easing functions directly
t = 0.5  # Normalized time (0 to 1)
value = EasingFunctions.ease_in_out_sine(t, 0, 100, 1)
```

### Logger - Logging Utilities

Simple logging wrapper with convenient methods.

```python
from pygame_utils import Logger

# Create logger
logger = Logger(name='mygame', debug=True, log_file='game.log')

# Log messages
logger.debug('Debug information')
logger.info('Application started')
logger.warning('Low memory')
logger.error('Failed to load resource')
```

### Registry - Persistent Storage

Hierarchical key-value storage with SQLite backend.

```python
from pygame_utils import Registry

# Create registry with persistence (pass database path)
registry = Registry('registry.db')
# Or create in-memory registry (no persistence)
# registry = Registry()

# Write values
registry.write('settings.volume', 75)
registry.write('player.name', 'Player1')
registry.increment('stats.score', 100)

# Read values
volume = registry.read('settings.volume', default=50)
score = registry.read('stats.score', default=0)

# Close when done
registry.close()
```

### Input - Input Handling

Keyboard and mouse input management for pygame.

```python
import pygame
from pygame_utils import Input

pygame.init()
screen = pygame.display.set_mode((800, 600))
input_handler = Input()

# Register actions
input_handler.actions.register('jump', ['space', 'w'])
input_handler.actions.register('shoot', ['mouse_button_1', 'z'])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_handler.handle_event(event)
    
    # Check input
    if input_handler.actions.is_pressed('jump'):
        print("Jump!")
    
    if input_handler.is_down('a'):
        print("Moving left")
    
    # Update input state
    input_handler.update()
```

### Pool - Object Pooling

Efficient object reuse to reduce allocation overhead.

```python
from pygame_utils import ObjectPool

class Particle:
    def __init__(self):
        self.active = False
        self.x = 0
        self.y = 0
    
    def alive(self):
        return self.active
    
    def revive(self):
        self.active = True
    
    def kill(self):
        self.active = False

# Create pool
pool = ObjectPool(Particle, size=100)
pool.init()

# Get object from pool
particle = pool.get()
if particle:
    particle.x = 100
    particle.y = 200
    # Use particle...
    pool.return_object(particle)
```

### Stopwatch - Performance Timing

Measure elapsed time for profiling and performance monitoring.

```python
from pygame_utils import Stopwatch

# Start timing
Stopwatch.start('operation')

# ... do work ...

# Stop and get elapsed time
elapsed = Stopwatch.stop('operation')
print(f"Operation took {elapsed} seconds")

# Check if running
if Stopwatch.is_running('operation'):
    current_time = Stopwatch.time('operation')
    print(f"Still running: {current_time} seconds")

# Get statistics
stats = Stopwatch.stats('operation')
if stats:
    print(f"Average time: {stats.mean} seconds")
```

### TexturePacker - Sprite Atlas Parser

Parse TexturePacker JSON exports and extract sprite frames.

```python
import pygame
from pygame_utils import TexturePacker

pygame.init()

# Load frames (image in same directory as JSON)
frames = TexturePacker.get_frames('sprites.json')

# Or with custom image resolver
def resolve_image(json_dir, image_name):
    return f'assets/images/{image_name}'

frames = TexturePacker.get_frames('sprites.json', image_resolver=resolve_image)

# Use frames
sprite_surface, pivot = frames['player_idle']
screen.blit(sprite_surface, (100, 100))
```

### Timer - Game Timer

Frame timing, delta time, and callback scheduling.

```python
import pygame
from pygame_utils import GameTimer, Timer

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Create game timer
timer = GameTimer(fps=60)

# Schedule callbacks
timer.set_timeout(lambda: print("5 seconds passed"), 5.0)
timer.set_interval(lambda: print("Every second"), 1.0)

running = True
while running:
    # Update timer (call once per frame)
    timer.update()
    
    # Get timing information
    dt = timer.delta_time()  # Time since last frame
    fps = timer.fps()        # Current FPS
    time_ms = timer.time()   # Total time in milliseconds
    
    # Simple countdown timer
    countdown = Timer(timer, duration=5000, loop=False)
    countdown.on('done', lambda: print("Time's up!"))
    countdown.start()
    
    # ... game loop ...
```

### Tween - Animation Tweening

Smooth value interpolation with easing functions.

```python
from pygame_utils import Tween, Tweens

# Create a tween
tween = Tween(
    from_value=0,
    to_value=100,
    duration=2.0,  # 2 seconds
    easing='easeInOutQuad',
    update_callback=lambda value: print(f"Value: {value}"),
    complete_callback=lambda value: print("Animation complete!")
)

# Update tween each frame
while not tween.is_completed:
    tween.update()
    # Use tween.value in your game

# Pause/resume
tween.pause()
tween.unpause()

# Manage multiple tweens
tweens = Tweens()
tweens.append(0, 100, 2.0, 'easeInQuad', repeat=1)
tweens.append(0, 200, 1.5, 'easeOutQuad', repeat=1)

# Update all tweens
tweens.update()
```

## Module Dependencies

| Module | Required | Optional |
|--------|----------|----------|
| appstats | None | - |
| events | None | - |
| easing | None | - |
| logger | None | - |
| registry | None | appdirs |
| input | pygame | pynput (for global hotkeys) |
| pool | None | - |
| stopwatch | None | - |
| texturepacker | pygame | - |
| timer | pygame | - |
| tween | None | - |

## Requirements

- Python 3.7+
- pygame (for input, texturepacker, timer modules)
- pynput (optional, for global hotkeys in input module)
- appdirs (optional, for registry default paths)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Examples

See the `examples/` directory for more detailed usage examples for each module.


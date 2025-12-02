"""
Example: Using Tween for smooth animations
"""

import time
from pygame_utils import Tween, Tweens

print("Example 1: Simple tween")
tween = Tween(
    from_value=0,
    to_value=100,
    duration=2.0,
    easing='easeInOutQuad',
    update_callback=lambda v: print(f"Value: {v:.2f}"),
    complete_callback=lambda v: print(f"Complete! Final value: {v}")
)

# Simulate frame updates
start_time = time.time()
while not tween.is_completed:
    tween.update()
    time.sleep(0.1)  # Simulate ~10 FPS

print("\nExample 2: Multiple tweens")
tweens = Tweens()

# Add multiple tweens
tweens.append(0, 50, 1.0, 'easeInQuad', repeat=2)
tweens.append(0, 100, 1.5, 'easeOutQuad', repeat=1)

# Update all tweens
start_time = time.time()
while len(tweens.tweens) > 0:
    tweens.update()
    for i, tween in enumerate(tweens.tweens):
        print(f"Tween {i}: {tween.value:.2f}")
    time.sleep(0.1)

print("\nExample 3: Ping-pong tween")
pingpong = Tween(
    from_value=0,
    to_value=100,
    duration=1.0,
    easing='easeInOutSine',
    pingpong=-1  # Infinite ping-pong
)

# Run for a few cycles
for _ in range(5):
    pingpong.update()
    print(f"Ping-pong value: {pingpong.value:.2f}")
    time.sleep(0.1)

pingpong.stop()


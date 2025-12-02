"""
Example: Using AppStats for performance tracking
"""

from pygame_utils import AppStats

# Simulate FPS sampling
fps_values = [60, 58, 62, 59, 61, 60, 57, 63, 60, 59]

print("Sampling FPS values...")
for fps in fps_values:
    AppStats.sample('fps', fps)

# Get statistics
stat = AppStats.get('fps')
print(f"\nFPS Statistics:")
print(f"  Current: {stat.value}")
print(f"  Mean: {stat.mean:.2f}")
print(f"  Min: {stat.min}")
print(f"  Max: {stat.max}")
print(f"  Total samples: {stat.total_samples}")

# Sample multiple metrics
AppStats.sample('memory', 150.5)
AppStats.sample('memory', 152.3)
AppStats.sample('memory', 148.9)

AppStats.sample('load_time', 1.2)
AppStats.sample('load_time', 1.1)
AppStats.sample('load_time', 1.3)

# Print all statistics
print("\nAll Statistics:")
print(AppStats)


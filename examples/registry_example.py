"""
Example: Using Registry for persistent storage
"""

from pygame_utils import Registry

# Create registry with persistence
# Pass a database path to enable persistence, or None for in-memory only
registry = Registry('registry.db')

# Store values
registry.write('player.name', 'Player1')
registry.write('player.level', 5)
registry.write('settings.volume', 75)
registry.write('settings.fullscreen', True)

# Read values
name = registry.read('player.name', default='Unknown')
level = registry.read('player.level', default=1)
volume = registry.read('settings.volume', default=50)

print(f"Player: {name}, Level: {level}, Volume: {volume}")

# Increment/decrement
registry.increment('player.score', 100)
registry.increment('player.score', 50)
score = registry.read('player.score', default=0)
print(f"Score: {score}")

# Min/max operations
registry.max('player.high_score', 150)
registry.min('player.high_score', 200)
high_score = registry.read('player.high_score', default=0)
print(f"High Score: {high_score}")

# Iterate over all values
print("\nAll registry values:")
registry.each(lambda path, value: print(f"  {path}: {value}"))

# Close registry
registry.close()
print("\nRegistry closed")


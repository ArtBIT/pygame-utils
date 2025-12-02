"""
Example: Using Events for decoupled communication
"""

from pygame_utils import Events

# Create event system
events = Events()

# Subscribe to events
def on_player_move(data):
    print(f"Player moved to: {data}")

def on_enemy_spawn(data):
    print(f"Enemy spawned: {data}")

events.on('player.move', on_player_move)
events.on('enemy.spawn', on_enemy_spawn)

# Trigger events
print("Triggering events...")
events.emit('player.move', (100, 200))
events.emit('enemy.spawn', 'goblin')

# One-time listener
events.once('game.start', lambda: print("Game started!"))

events.emit('game.start')
events.emit('game.start')  # Won't trigger again

# Remove listener
events.off('player.move', on_player_move)
events.emit('player.move', (150, 250))  # Won't trigger

# Remove all listeners for an event
events.off('enemy.spawn')
events.emit('enemy.spawn', 'orc')  # Won't trigger


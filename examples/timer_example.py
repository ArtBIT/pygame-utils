"""
Example: Using GameTimer for frame timing and callbacks
"""

import pygame
from pygame_utils import GameTimer, Timer

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create game timer
timer = GameTimer(fps=60)

# Schedule some callbacks
timer.set_timeout(lambda: print("5 seconds passed!"), 5.0)
timer.set_interval(lambda: print(f"FPS: {timer.fps()}"), 2.0)

# Create a countdown timer
countdown = Timer(timer, duration=10000, loop=False)  # 10 seconds
countdown.on('done', lambda: print("Countdown finished!"))

print("Starting game loop (press ESC to quit)...")
countdown.start()

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Update timer (important: call this every frame)
    timer.update()
    
    # Get timing information
    dt = timer.delta_time()
    fps = timer.fps()
    frame = timer.frame()
    
    # Display info (every 60 frames)
    if frame % 60 == 0:
        print(f"Frame {frame}: FPS={fps:.2f}, DT={dt:.4f}s")
    
    # Simple rendering
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("Game loop ended")


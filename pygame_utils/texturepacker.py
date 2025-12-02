"""
TexturePacker JSON parser module.

Parses TexturePacker JSON export files and extracts individual sprite frames
as Pygame surfaces. Supports rotated sprites and pivot points.

Requires pygame to be installed.

Example:
    >>> import pygame
    >>> from pygame_utils.texturepacker import TexturePacker
    >>> pygame.init()
    >>> frames = TexturePacker.get_frames('sprites.json', image_resolver=lambda name: f'images/{name}')
    >>> sprite_surface, pivot = frames['player_idle']
"""

import json
import os

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    pygame = None


class TexturePacker:
    """
    Parser for TexturePacker JSON export files.
    
    Loads sprite atlases exported from TexturePacker and extracts
    individual frames as Pygame surfaces.
    """
    cache = {}

    @staticmethod
    def get(filepath, image_resolver=None):
        """
        Get frames from a TexturePacker JSON file (with caching).
        
        Args:
            filepath: Path to the TexturePacker JSON file
            image_resolver: Optional function to resolve image paths.
                          Takes (json_dir, image_name) and returns full path.
                          If None, assumes image is in same directory as JSON.
        
        Returns:
            Dictionary mapping frame names to (surface, pivot) tuples
        """
        if filepath not in TexturePacker.cache:
            TexturePacker.cache[filepath] = TexturePacker.get_frames(filepath, image_resolver)
        return TexturePacker.cache[filepath]

    @staticmethod
    def get_frames(filepath, image_resolver=None):
        """
        Parse a TexturePacker JSON file and extract frames.
        
        Args:
            filepath: Path to the TexturePacker JSON file
            image_resolver: Optional function to resolve image paths.
                          Takes (json_dir, image_name) and returns full path.
                          If None, assumes image is in same directory as JSON.
        
        Returns:
            Dictionary mapping frame names to (surface, pivot) tuples
            where surface is a Pygame Surface and pivot is (x, y) or None
        """
        if not HAS_PYGAME:
            raise ImportError("pygame is required for TexturePacker. Install it with: pip install pygame")
        
        # Load JSON file
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Parse meta information
        meta = data['meta']
        imagename = meta['image']
        
        # Resolve image path
        if image_resolver:
            imagepath = image_resolver(os.path.dirname(filepath), imagename)
        else:
            # Default: assume image is in same directory as JSON
            json_dir = os.path.dirname(filepath)
            imagepath = os.path.join(json_dir, imagename)
        
        # Load the atlas image
        image = pygame.image.load(imagepath).convert_alpha()

        # Parse frames
        frames = {}
        data_frames = data['frames']
        for frame_name in data_frames:
            frame_data = data_frames[frame_name]
            frame_rect = frame_data["frame"]
            sourceSize = frame_data["sourceSize"]
            spriteSourceSize = frame_data["spriteSourceSize"]
            
            if frame_data.get("rotated", False):
                # Handle rotated sprites: invert w and h, then rotate by 90
                surf = pygame.Surface((spriteSourceSize["h"], spriteSourceSize["w"]), pygame.SRCALPHA, 32).convert_alpha()
                rect = pygame.Rect(frame_rect["x"], frame_rect["y"], frame_rect["h"], frame_rect["w"])
                surf.blit(image, (0, 0), rect)
                surf = pygame.transform.rotate(surf, 90)
            else:
                # Normal sprite extraction
                surf = pygame.Surface((sourceSize["w"], sourceSize["h"]), pygame.SRCALPHA, 32).convert_alpha()
                rect = pygame.Rect(frame_rect["x"], frame_rect["y"], frame_rect["w"], frame_rect["h"])
                surf.blit(image, (0, 0), rect)

            # Apply offset
            offset = (spriteSourceSize["x"], spriteSourceSize["y"])
            size = (sourceSize["w"], sourceSize["h"])
            frame_orig = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
            frame_orig.blit(surf, offset)
            
            # Extract pivot point if available
            pivot = None
            if 'pivot' in frame_data:
                pivot = (frame_data["pivot"]["x"], frame_data["pivot"]["y"])

            frames[frame_name] = (frame_orig, pivot)

        return frames


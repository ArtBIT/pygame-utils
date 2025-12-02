"""
Object pooling module for efficient object reuse.

Provides a generic object pool implementation that can be used to
reuse objects instead of creating new ones, reducing memory allocation
and garbage collection overhead.

Example:
    >>> from pygame_utils.pool import ObjectPool
    >>> class Particle:
    ...     def __init__(self):
    ...         self.active = False
    ...     def activate(self):
    ...         self.active = True
    ...     def deactivate(self):
    ...         self.active = False
    >>> pool = ObjectPool(Particle, size=100)
    >>> pool.init()
    >>> particle = pool.get()
    >>> # ... use particle ...
    >>> pool.return_object(particle)
"""


class ObjectPool:
    """
    Generic object pool for reusing objects.
    
    Maintains a pool of pre-allocated objects that can be checked out
    and returned, reducing the overhead of object creation and destruction.
    
    Objects must implement an `alive()` method that returns False when
    the object is available for reuse, and a `revive()` method to reactivate
    the object.
    """
    def __init__(self, object_class, size=100):
        """
        Initialize a new object pool.
        
        Args:
            object_class: The class to instantiate for the pool
            size: The number of objects to pre-allocate (default: 100)
        """
        self.object_class = object_class
        self.pool = []
        self.size = size

    def init(self, *args, **kwargs):
        """
        Initialize the pool with pre-allocated objects.
        
        Creates `size` objects and marks them as inactive (not alive).
        
        Args:
            *args: Positional arguments to pass to object constructor
            **kwargs: Keyword arguments to pass to object constructor
        """
        self.pool = []
        for i in range(self.size):
            obj = self.object_class(*args, **kwargs)
            # Mark object as inactive
            if hasattr(obj, 'kill'):
                obj.kill()
            elif hasattr(obj, 'deactivate'):
                obj.deactivate()
            elif hasattr(obj, 'active'):
                obj.active = False
            self.pool.append(obj)

    def get(self):
        """
        Get an available object from the pool.
        
        Returns:
            An available object from the pool, or None if all objects are in use
        """
        for obj in self.pool:
            if not obj.alive():
                if hasattr(obj, 'revive'):
                    obj.revive()
                elif hasattr(obj, 'activate'):
                    obj.activate()
                elif hasattr(obj, 'active'):
                    obj.active = True
                return obj
        return None

    def return_object(self, obj):
        """
        Return an object to the pool for reuse.
        
        Marks the object as inactive so it can be reused.
        
        Args:
            obj: The object to return to the pool
        """
        if hasattr(obj, 'kill'):
            obj.kill()
        elif hasattr(obj, 'deactivate'):
            obj.deactivate()
        elif hasattr(obj, 'active'):
            obj.active = False


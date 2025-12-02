"""
Registry module for persistent key-value storage.

Provides a hierarchical registry system with SQLite backend for persistent
storage. Supports dot-notation paths (e.g., "settings.audio.volume") and
automatic type conversion.

Example:
    >>> from pygame_utils.registry import Registry
    >>> registry = Registry()
    >>> registry.write('settings.volume', 75)
    >>> volume = registry.read('settings.volume', default=50)
    >>> registry.increment('stats.score', 10)
"""

from os import path, makedirs
import sqlite3


class Registry:
    """
    Hierarchical registry with SQLite persistence.
    
    Provides a nested dictionary-like interface with dot-notation paths
    and automatic persistence to SQLite database.
    """
    
    # Database schema
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS registry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE,
        value TEXT,
        type TEXT
    );
    """
    
    def __init__(self, db_path=None):
        """
        Initialize a new Registry instance.
        
        Args:
            db_path: Path to SQLite database file. If None, skips persistence
                     entirely and operates as an in-memory registry only.
        """
        self._registry = {}
        self.db_queue = {}
        
        # If db_path is None, skip persistence altogether
        if db_path is None:
            self.db = None
            return
        
        # Create database if it doesn't exist
        if not path.exists(db_path):
            makedirs(path.dirname(db_path) if path.dirname(db_path) else '.', exist_ok=True)
            # Create empty database with schema
            temp_db = sqlite3.connect(db_path)
            temp_db.execute(self.SCHEMA)
            temp_db.commit()
            temp_db.close()

        try:
            self.db = sqlite3.connect(db_path)
            # Ensure schema exists
            self.db.execute(self.SCHEMA)
            self.db.commit()
            self.load()
        except Exception as e:
            # Continue without database if connection fails
            self.db = None
            print(f"Warning: Failed to open registry database: {e}")

    def store(self):
        """
        Write the collected registry data to the database.
        
        Flushes all queued writes to the database.
        """
        if self.db is None:
            return
            
        try:
            cursor = self.db.cursor()
            for path_key, value in self.db_queue.items():
                cursor.execute(
                    "INSERT OR REPLACE INTO registry (path, value, type) VALUES (?, ?, ?)",
                    (path_key, str(value), type(value).__name__)
                )
            self.db.commit()
        except Exception as e:
            print(f"Warning: Failed to write to registry: {e}")

        self.db_queue = {}

    def write_local(self, path_key, value):
        """
        Write a value to the local registry, without writing to the database.
        
        Args:
            path_key: Dot-notation path (e.g., "settings.volume")
            value: Value to store
            
        Returns:
            The stored value
        """
        branch = self._registry
        for key in path_key.split("."):
            if key not in branch:
                branch[key] = {}

            branch = branch[key]

        if type(branch) is dict:
            branch['__value'] = value

        return value

    def write_db(self, path_key, value, store=False):
        """
        Queue a value to be written to the database.
        
        It will be written when store() is called.
        
        Args:
            path_key: Dot-notation path
            value: Value to store
            store: If True, immediately write to database
            
        Returns:
            The stored value
        """
        self.db_queue[path_key] = value
        if store:
            self.store()
        return value

    def write(self, path_key, value):
        """
        Write a value to the registry (local only, not to database).
        
        Args:
            path_key: Dot-notation path
            value: Value to store
            
        Returns:
            The stored value
        """
        self.write_local(path_key, value)
        return value

    def set(self, path_key, value):
        """Alias for write()."""
        return self.write(path_key, value)

    def reset(self, path_key, value=0):
        """Reset a path to a default value."""
        return self.write(path_key, value)

    def read(self, path_key, default=None):
        """
        Read a value from the registry.
        
        Args:
            path_key: Dot-notation path
            default: Default value if path doesn't exist
            
        Returns:
            The stored value, or default if not found
        """
        branch = self._registry
        for key in path_key.split("."):
            if key not in branch:
                return default

            branch = branch[key]

        if type(branch) is dict:
            # check if dict has key '__value'
            if '__value' in branch:
                return branch['__value']

        return default

    def read_db(self, path_key, default=None):
        """
        Read a value directly from the database.
        
        Args:
            path_key: Dot-notation path
            default: Default value if path doesn't exist
            
        Returns:
            The stored value, or default if not found
        """
        if self.db is None:
            return default
            
        try: 
            cursor = self.db.cursor()
            cursor.execute("SELECT value FROM registry WHERE path = ?", (path_key,))
            row = cursor.fetchone()
            if row is None:
                return default

            return row[0]
        except Exception as e:
            return default

    def get(self, path_key, default=None):
        """Alias for read()."""
        return self.read(path_key, default)

    def increment(self, path_key, amount=1):
        """Increment a numeric value by the given amount."""
        return self.write(path_key, self.read(path_key, 0) + amount)

    def decrement(self, path_key, amount=1):
        """Decrement a numeric value by the given amount."""
        return self.write(path_key, self.read(path_key, 0) - amount)

    def max(self, path_key, value):
        """Set a value to the maximum of current and new value."""
        return self.write(path_key, max(self.read(path_key, value), value))

    def min(self, path_key, value):
        """Set a value to the minimum of current and new value."""
        return self.write(path_key, min(self.read(path_key, value), value))

    def delete(self, path_key):
        """
        Delete a value from the registry.
        
        Args:
            path_key: Dot-notation path to delete
        """
        branch = self._registry
        keys = path_key.split(".")
        for key in keys[:-1]:
            if key not in branch:
                return

            branch = branch[key]

        if keys[-1] in branch:
            del branch[keys[-1]]

    def __str__(self):
        """Return string representation of the registry."""
        return str(self._registry)

    def each(self, callback):
        """
        Iterate over all values in the registry.
        
        Args:
            callback: Function called with (path, value) for each entry
        """
        max_recursion = 100
        def walk(branch, path_key='', depth=0):
            if depth > max_recursion:
                print("Warning: Max recursion reached in registry.each()")
                return

            for key, value in branch.items():
                if key == "__value":
                    callback(path_key, value)
                    continue
                subpath = path_key + "." + key if path_key else key
                walk(branch[key], subpath, depth + 1)

        walk(self._registry)

    def load(self, filter_persist=True):
        """
        Load values from the database into the registry.
        
        Args:
            filter_persist: If True, only load paths starting with "persist"
        """
        if self.db is None:
            return
            
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM registry")
        for row in cursor.fetchall():
            path_key = row[1]
            
            # Apply filters if enabled
            if filter_persist:
                # Only load cumulative values that start with "persist"
                if not path_key.endswith("cumulative"):
                    self.write(path_key, 0)
                    continue

                if not path_key.startswith("persist"):
                    self.write(path_key, 0)
                    continue

            # Convert value based on stored type
            value_type = row[3]
            if value_type == "int":
                value = int(row[2])
            elif value_type == "float":
                value = float(row[2])
            elif value_type == "bool":
                value = bool(row[2])
            else:
                value = row[2]
            self.write(path_key, value)

    def close(self):
        """Close the database connection."""
        if self.db:
            self.db.close()
            self.db = None

    def quit(self):
        """Alias for close()."""
        self.close()


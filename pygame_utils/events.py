"""
Event system module.

Provides an event emitter/listener pattern for decoupled communication
between components. Supports subscribing to events, one-time listeners,
and event triggering with arguments.

Example:
    >>> from pygame_utils.events import Events
    >>> events = Events()
    >>> events.on('click', lambda event: print(f"Clicked: {event}"))
    >>> events.emit('click', 'button1')
"""


class Event:
    """
    Base event class representing an event that occurred.
    
    Attributes:
        event: The event name/type
        target: The object that triggered the event
    """
    def __init__(self, event, target):
        """
        Initialize a new event.
        
        Args:
            event: The event name/type
            target: The object that triggered the event
        """
        self.event = event
        self.target = target


class CallbackList(list):
    """
    A list of callback functions that can be fired with arguments.
    
    Extends the standard list to add a fire() method that calls all
    callbacks in the list with the provided arguments.
    """
    def fire(self, *args, **kwargs):
        """
        Call all callbacks in the list with the provided arguments.
        
        Args:
            *args: Positional arguments to pass to callbacks
            **kwargs: Keyword arguments to pass to callbacks
        """
        for listener in self:
            listener(*args, **kwargs)


class Events:
    """
    Event emitter/listener system for decoupled component communication.
    
    Allows components to subscribe to events and trigger events that
    notify all subscribers. Supports one-time listeners and event removal.
    
    Example:
        >>> events = Events()
        >>> def handler(data):
        ...     print(f"Received: {data}")
        >>> events.on('message', handler)
        >>> events.emit('message', 'Hello')
        Received: Hello
    """
    def __init__(self):
        """Initialize a new Events instance with an empty listener registry."""
        self.listeners = {}

    def on(self, event_name, callback=None):
        """
        Subscribe to an event.
        
        Args:
            event_name: The name of the event to listen for
            callback: The function to call when the event is triggered
            
        Note:
            If callback is None, this method returns without doing anything.
        """
        if callback is None:
            return
        if event_name not in self.listeners:
            self.listeners[event_name] = CallbackList()
        self.listeners[event_name].append(callback)

    def once(self, event_name, callback=None):
        """
        Subscribe to an event for a single occurrence.
        
        The callback will be automatically removed after being called once.
        
        Args:
            event_name: The name of the event to listen for
            callback: The function to call when the event is triggered
        """
        def once_callback(*args, **kwargs):
            self.off(event_name, once_callback)
            callback(*args, **kwargs)
        self.on(event_name, once_callback)

    def off(self, event_name=None, callback=None):
        """
        Unsubscribe from an event.
        
        Args:
            event_name: The name of the event to unsubscribe from.
                       If None, removes all listeners.
            callback: The specific callback to remove.
                     If None, removes all listeners for the event.
        """
        if event_name is None:
            self.reset()
            return

        if event_name not in self.listeners:
            return

        if callback is None:
            self.listeners.pop(event_name, None)
            return

        try:
            self.listeners[event_name].remove(callback)
        except ValueError:
            pass

        if len(self.listeners[event_name]) == 0:
            self.listeners.pop(event_name, None)

    def trigger(self, event_name, *kwargs):
        """
        Trigger an event, calling all subscribed callbacks.
        
        Args:
            event_name: The name of the event to trigger
            *kwargs: Arguments to pass to the callbacks
        """
        if event_name not in self.listeners:
            return
        self.listeners[event_name].fire(*kwargs)

    def emit(self, event_name, *kwargs):
        """
        Alias for trigger().
        
        Args:
            event_name: The name of the event to trigger
            *kwargs: Arguments to pass to the callbacks
        """
        self.trigger(event_name, *kwargs)

    def reset(self):
        """Remove all event listeners."""
        self.listeners = {}


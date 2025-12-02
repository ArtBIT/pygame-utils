"""
Tests for events module
"""

import unittest
from pygame_utils import Events, Event


class TestEvents(unittest.TestCase):
    def setUp(self):
        self.events = Events()

    def test_on_and_emit(self):
        called = [False]
        
        def handler(data):
            called[0] = True
            self.assertEqual(data, 'test')
        
        self.events.on('test', handler)
        self.events.emit('test', 'test')
        self.assertTrue(called[0])

    def test_off_removes_listener(self):
        called = [False]
        
        def handler():
            called[0] = True
        
        self.events.on('test', handler)
        self.events.off('test', handler)
        self.events.emit('test')
        self.assertFalse(called[0])

    def test_off_removes_all_listeners(self):
        called = [False]
        
        def handler():
            called[0] = True
        
        self.events.on('test', handler)
        self.events.off('test')
        self.events.emit('test')
        self.assertFalse(called[0])

    def test_once_only_fires_once(self):
        count = [0]
        
        def handler():
            count[0] += 1
        
        self.events.once('test', handler)
        self.events.emit('test')
        self.events.emit('test')
        self.assertEqual(count[0], 1)

    def test_reset_clears_all(self):
        called = [False]
        
        def handler():
            called[0] = True
        
        self.events.on('test1', handler)
        self.events.on('test2', handler)
        self.events.reset()
        self.events.emit('test1')
        self.events.emit('test2')
        self.assertFalse(called[0])


class TestEventClasses(unittest.TestCase):
    def test_event(self):
        target = object()
        event = Event('click', target)
        self.assertEqual(event.event, 'click')
        self.assertEqual(event.target, target)


if __name__ == '__main__':
    unittest.main()


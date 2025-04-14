import pygame


class EventManager:
    """Manages game-wide events."""

    def __init__(self):
        self.handlers = {}

    def register_handler(self, event_type, handler):
        """Register an event handler."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def unregister_handler(self, event_type, handler):
        """Unregister an event handler."""
        if event_type in self.handlers:
            if handler in self.handlers[event_type]:
                self.handlers[event_type].remove(handler)

    def handle_event(self, event):
        """Handle an event, dispatching to registered handlers."""
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                handler(event)
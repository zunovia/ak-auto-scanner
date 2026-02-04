"""
Keyboard event handler for emergency stop (ESC key).
"""
from pynput import keyboard
from typing import Callable
import threading


class KeyboardHandler:
    """Handles keyboard events for emergency stop."""

    def __init__(self, on_escape: Callable[[], None]):
        """
        Initialize keyboard handler.

        Args:
            on_escape: Callback function to call when ESC is pressed
        """
        self.on_escape = on_escape
        self.listener = None
        self.is_listening = False

    def _on_press(self, key):
        """Handle key press events."""
        try:
            if key == keyboard.Key.esc:
                self.on_escape()
                return False  # Stop listener
        except AttributeError:
            pass

    def start(self):
        """Start listening for keyboard events."""
        if self.is_listening:
            return

        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
        self.is_listening = True

    def stop(self):
        """Stop listening for keyboard events."""
        if not self.is_listening:
            return

        if self.listener:
            self.listener.stop()
            self.listener = None
        self.is_listening = False

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

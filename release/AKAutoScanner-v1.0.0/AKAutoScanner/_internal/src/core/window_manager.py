"""
Windows window management for Kindle app control.
"""
import win32gui
import win32con
import win32api
from typing import Optional, Tuple
import time

from ..utils.logger import logger


class WindowManager:
    """Manages Windows window operations for Kindle app."""

    KINDLE_WINDOW_TITLES = [
        "Kindle for PC",
        "Kindle Previewer",
    ]

    # Exclude our own application window
    EXCLUDE_TITLES = [
        "AK Auto-Scanner",
        "Auto-Scanner",
    ]

    def __init__(self):
        """Initialize window manager."""
        self.kindle_hwnd: Optional[int] = None
        self.original_rect: Optional[Tuple[int, int, int, int]] = None
        self.was_maximized: bool = False

    def find_kindle_window(self) -> Optional[int]:
        """
        Find the Kindle application window.

        Returns:
            Window handle (HWND) if found, None otherwise
        """
        windows = []

        def enum_handler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)

                # Exclude our own application window
                if any(exclude in title for exclude in self.EXCLUDE_TITLES):
                    return

                # Find Kindle windows
                if any(kindle_title in title for kindle_title in self.KINDLE_WINDOW_TITLES):
                    windows.append((hwnd, title))

        try:
            win32gui.EnumWindows(enum_handler, None)
        except Exception as e:
            logger.error(f"Error enumerating windows: {e}")
            return None

        if not windows:
            logger.error("Kindle window not found. Please ensure Kindle for PC is running and a book is open.")
            return None

        # Return the first matching window
        self.kindle_hwnd = windows[0][0]
        logger.info(f"Found Kindle window: {windows[0][1]} (HWND: {self.kindle_hwnd})")
        return self.kindle_hwnd

    def activate_window(self, hwnd: int = None) -> bool:
        """
        Activate (bring to foreground) the Kindle window.

        Args:
            hwnd: Window handle (uses stored handle if None)

        Returns:
            True if successful, False otherwise
        """
        if hwnd is None:
            hwnd = self.kindle_hwnd

        if hwnd is None:
            logger.error("No window handle provided")
            return False

        try:
            # Check if window is minimized
            placement = win32gui.GetWindowPlacement(hwnd)
            if placement[1] == win32con.SW_SHOWMINIMIZED:
                self.was_maximized = placement[1] == win32con.SW_SHOWMAXIMIZED
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.3)

            # Set as foreground window
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.2)

            logger.debug(f"Activated window HWND: {hwnd}")
            return True

        except Exception as e:
            logger.error(f"Error activating window: {e}")
            return False

    def get_window_rect(self, hwnd: int = None) -> Optional[Tuple[int, int, int, int]]:
        """
        Get window position and size.

        Args:
            hwnd: Window handle (uses stored handle if None)

        Returns:
            Tuple of (left, top, right, bottom) or None if error
        """
        if hwnd is None:
            hwnd = self.kindle_hwnd

        if hwnd is None:
            return None

        try:
            rect = win32gui.GetWindowRect(hwnd)
            return rect
        except Exception as e:
            logger.error(f"Error getting window rect: {e}")
            return None

    def get_client_rect(self, hwnd: int = None, margin_top: int = 0, margin_bottom: int = 0,
                        margin_left: int = 0, margin_right: int = 0) -> Optional[Tuple[int, int, int, int]]:
        """
        Get client area coordinates (excludes title bar and borders) with optional margins.

        Args:
            hwnd: Window handle (uses stored handle if None)
            margin_top: Top margin adjustment (negative to expand upward)
            margin_bottom: Bottom margin adjustment (negative to expand downward)
            margin_left: Left margin adjustment (negative to expand leftward)
            margin_right: Right margin adjustment (negative to expand rightward)

        Returns:
            Tuple of (left, top, right, bottom) in screen coordinates
        """
        if hwnd is None:
            hwnd = self.kindle_hwnd

        if hwnd is None:
            return None

        try:
            # Get client rect (relative to window)
            client_rect = win32gui.GetClientRect(hwnd)

            # Convert to screen coordinates
            left, top = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))
            right, bottom = win32gui.ClientToScreen(hwnd, (client_rect[2], client_rect[3]))

            # Apply margins (negative values expand the region)
            left = left - margin_left
            top = top - margin_top
            right = right + margin_right
            bottom = bottom + margin_bottom

            return (left, top, right, bottom)
        except Exception as e:
            logger.error(f"Error getting client rect: {e}")
            return None

    def maximize_window(self, hwnd: int = None) -> bool:
        """
        Maximize the window.

        Args:
            hwnd: Window handle (uses stored handle if None)

        Returns:
            True if successful, False otherwise
        """
        if hwnd is None:
            hwnd = self.kindle_hwnd

        if hwnd is None:
            return False

        try:
            # Store original rect for restoration
            if self.original_rect is None:
                self.original_rect = self.get_window_rect(hwnd)

            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(0.5)  # Wait for window to maximize

            logger.debug("Window maximized")
            return True

        except Exception as e:
            logger.error(f"Error maximizing window: {e}")
            return False

    def restore_window(self, hwnd: int = None) -> bool:
        """
        Restore window to original size.

        Args:
            hwnd: Window handle (uses stored handle if None)

        Returns:
            True if successful, False otherwise
        """
        if hwnd is None:
            hwnd = self.kindle_hwnd

        if hwnd is None:
            return False

        try:
            if self.was_maximized:
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            else:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

            # Restore original position if we have it
            if self.original_rect is not None:
                left, top, right, bottom = self.original_rect
                width = right - left
                height = bottom - top
                win32gui.MoveWindow(hwnd, left, top, width, height, True)

            logger.debug("Window restored")
            return True

        except Exception as e:
            logger.error(f"Error restoring window: {e}")
            return False

    def is_window_valid(self, hwnd: int = None) -> bool:
        """
        Check if window handle is still valid.

        Args:
            hwnd: Window handle (uses stored handle if None)

        Returns:
            True if window is valid, False otherwise
        """
        if hwnd is None:
            hwnd = self.kindle_hwnd

        if hwnd is None:
            return False

        try:
            return win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd)
        except Exception:
            return False

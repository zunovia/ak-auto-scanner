"""
Page capture and navigation for Kindle books.
"""
import pyautogui
import time
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime
from PIL import Image

from ..models.config import Direction, Resolution
from ..utils.logger import logger


class PageCapturer:
    """Handles page screenshots and navigation."""

    # Key mappings for page turning
    DIRECTION_KEYS = {
        Direction.JAPANESE: 'left',   # ← for next page (和書)
        Direction.WESTERN: 'right',   # → for next page (洋書)
    }

    # Alternative keys (fallback)
    DIRECTION_KEYS_ALT = {
        Direction.JAPANESE: 'pageup',
        Direction.WESTERN: 'pagedown',
    }

    def __init__(self, direction: Direction, resolution: Resolution, capture_speed: float):
        """
        Initialize page capturer.

        Args:
            direction: Page turn direction
            resolution: Screenshot resolution mode
            capture_speed: Delay after page turn (seconds)
        """
        self.direction = direction
        self.resolution = resolution
        self.capture_speed = capture_speed

        # Disable PyAutoGUI failsafe (no abort on mouse corner)
        pyautogui.FAILSAFE = False

        logger.info(f"PageCapturer initialized: direction={direction.value}, "
                   f"resolution={resolution.value}, speed={capture_speed}s")

    def capture_page(self, region: Tuple[int, int, int, int], output_path: Path) -> Optional[Path]:
        """
        Capture a screenshot of the specified region.

        Args:
            region: Tuple of (left, top, right, bottom) coordinates
            output_path: Path to save the screenshot

        Returns:
            Path to saved screenshot, or None if failed
        """
        try:
            # Wait for page to stabilize
            time.sleep(self.capture_speed)

            # Calculate region dimensions
            left, top, right, bottom = region
            width = right - left
            height = bottom - top

            logger.debug(f"Capturing region: ({left}, {top}, {right}, {bottom}) "
                        f"[{width}x{height}]")

            # Take screenshot
            screenshot = pyautogui.screenshot(region=(left, top, width, height))

            # Apply resolution scaling
            screenshot = self._apply_resolution_scaling(screenshot)

            # Save screenshot
            output_path.parent.mkdir(parents=True, exist_ok=True)
            screenshot.save(str(output_path), 'PNG', optimize=False)

            logger.debug(f"Screenshot saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return None

    def _apply_resolution_scaling(self, image: Image.Image) -> Image.Image:
        """
        Apply resolution scaling based on resolution mode.

        Args:
            image: Original screenshot

        Returns:
            Scaled image
        """
        if self.resolution == Resolution.LOW:
            # No scaling
            return image

        elif self.resolution == Resolution.MEDIUM:
            # Scale 1.5x for clarity
            new_width = int(image.width * 1.5)
            new_height = int(image.height * 1.5)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        elif self.resolution == Resolution.HIGH:
            # High resolution - no additional scaling needed as we maximize window
            # Could optionally apply slight upscaling here
            return image

        return image

    def turn_page(self, use_alternative: bool = False) -> bool:
        """
        Turn to the next page.

        Args:
            use_alternative: Whether to use alternative key (PageUp/PageDown)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Select key based on direction
            if use_alternative:
                key = self.DIRECTION_KEYS_ALT[self.direction]
            else:
                key = self.DIRECTION_KEYS[self.direction]

            logger.debug(f"Turning page: {key}")

            # Press key multiple times to ensure it registers
            pyautogui.press(key)
            time.sleep(0.1)

            return True

        except Exception as e:
            logger.error(f"Error turning page: {e}")
            return False

    def generate_screenshot_path(self, temp_dir: Path, page_number: int) -> Path:
        """
        Generate a unique screenshot filename.

        Args:
            temp_dir: Temporary directory for screenshots
            page_number: Page number

        Returns:
            Path for screenshot file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"page_{page_number:04d}_{timestamp}.png"
        return temp_dir / filename

    def wait_for_page_load(self, extra_delay: float = 0.0):
        """
        Wait for page to finish loading/rendering.

        Args:
            extra_delay: Additional delay in seconds
        """
        total_delay = self.capture_speed + extra_delay
        logger.debug(f"Waiting {total_delay}s for page to load")
        time.sleep(total_delay)

    @staticmethod
    def click_window_center(region: Tuple[int, int, int, int]):
        """
        Click the center of a window region to ensure focus.

        Args:
            region: Tuple of (left, top, right, bottom) coordinates
        """
        try:
            left, top, right, bottom = region
            center_x = (left + right) // 2
            center_y = (top + bottom) // 2

            logger.debug(f"Clicking window center: ({center_x}, {center_y})")
            pyautogui.click(center_x, center_y)
            time.sleep(0.2)

        except Exception as e:
            logger.error(f"Error clicking window center: {e}")

    def test_capture(self, region: Tuple[int, int, int, int]) -> bool:
        """
        Test if screenshot capture is working.

        Args:
            region: Region to capture

        Returns:
            True if test successful, False otherwise
        """
        try:
            left, top, width, height = region[0], region[1], region[2] - region[0], region[3] - region[1]
            test_screenshot = pyautogui.screenshot(region=(left, top, width, height))
            return test_screenshot is not None and test_screenshot.size[0] > 0
        except Exception as e:
            logger.error(f"Screenshot test failed: {e}")
            return False

"""
Main scanning orchestrator that coordinates the entire workflow.
"""
import time
import shutil
from pathlib import Path
from typing import Optional, Callable, List
from datetime import datetime
import threading

from ..models.config import ScanConfig, ScanState, Resolution
from ..models.scan_state import ScanSession
from ..utils.logger import logger
from .window_manager import WindowManager
from .page_capturer import PageCapturer
from .image_processor import ImageProcessor
from .pdf_generator import PDFGenerator


class Scanner:
    """Main scanner orchestrator."""

    def __init__(self, config: ScanConfig):
        """
        Initialize scanner.

        Args:
            config: Scan configuration
        """
        self.config = config
        self.session = ScanSession()

        # Initialize components
        self.window_manager = WindowManager()
        self.page_capturer = PageCapturer(
            direction=config.direction,
            resolution=config.resolution,
            capture_speed=config.capture_speed
        )
        self.image_processor = ImageProcessor(
            similarity_threshold=config.similarity_threshold
        )
        self.pdf_generator = PDFGenerator(quality=config.pdf_quality)

        # Threading
        self.scan_thread: Optional[threading.Thread] = None
        self.progress_callback: Optional[Callable] = None

        logger.info("Scanner initialized")

    def start_scan(self, progress_callback: Optional[Callable] = None) -> bool:
        """
        Start scanning in a background thread.

        Args:
            progress_callback: Callback function(message, progress, page_count)

        Returns:
            True if scan started successfully, False otherwise
        """
        if self.session.is_active:
            logger.warning("Scan already in progress")
            return False

        self.progress_callback = progress_callback
        self.session.start()

        # Start scan thread
        self.scan_thread = threading.Thread(target=self._scan_workflow, daemon=True)
        self.scan_thread.start()

        logger.info("Scan started")
        return True

    def stop_scan(self):
        """Request scan to stop."""
        if not self.session.is_active:
            return

        logger.info("Stop requested")
        self.session.stop_requested = True
        self._notify_progress("Stopping scan...", None, self.session.pages_captured)

    def _scan_workflow(self):
        """Main scanning workflow (runs in background thread)."""
        try:
            # Validate configuration
            errors = self.config.validate()
            if errors:
                error_msg = "; ".join(errors)
                logger.error(f"Configuration validation failed: {error_msg}")
                self.session.error(error_msg)
                self._notify_progress(f"Error: {error_msg}", 0.0, 0)
                return

            # Prepare directories
            self._prepare_directories()

            # 5-second countdown before starting
            logger.info("Starting 5-second countdown before scan")
            for countdown in range(5, 0, -1):
                if self.session.stop_requested:
                    logger.info("Scan cancelled during countdown")
                    self.session.cancel()
                    self._notify_progress("Scan cancelled", 0.0, 0)
                    return

                self._notify_progress(
                    f"Starting in {countdown} second{'s' if countdown > 1 else ''}... (Press ESC to cancel)",
                    0.0,
                    0
                )
                time.sleep(1)

            # Find and activate Kindle window
            self._notify_progress("Finding Kindle window...", 0.0, 0)
            kindle_hwnd = self.window_manager.find_kindle_window()

            if kindle_hwnd is None:
                error_msg = "Kindle window not found. Please open Kindle app."
                logger.error(error_msg)
                self.session.error(error_msg)
                self._notify_progress(error_msg, 0.0, 0)
                return

            # Activate window
            self._notify_progress("Activating Kindle window...", 0.05, 0)
            if not self.window_manager.activate_window(kindle_hwnd):
                error_msg = "Failed to activate Kindle window"
                logger.error(error_msg)
                self.session.error(error_msg)
                self._notify_progress(error_msg, 0.0, 0)
                return

            # Handle high resolution mode (maximize window)
            if self.config.resolution == Resolution.HIGH:
                self._notify_progress("Maximizing window for high resolution...", 0.1, 0)
                self.window_manager.maximize_window(kindle_hwnd)

            # Get capture region with margins
            capture_region = self.window_manager.get_client_rect(
                kindle_hwnd,
                margin_top=self.config.margin_top,
                margin_bottom=self.config.margin_bottom,
                margin_left=self.config.margin_left,
                margin_right=self.config.margin_right
            )
            if capture_region is None:
                error_msg = "Failed to get window region"
                logger.error(error_msg)
                self.session.error(error_msg)
                self._notify_progress(error_msg, 0.0, 0)
                return

            logger.info(f"Capture region (with margins): {capture_region}")
            logger.info(f"Margins applied: top={self.config.margin_top}, bottom={self.config.margin_bottom}, left={self.config.margin_left}, right={self.config.margin_right}")

            # Use keyboard input instead of clicking to avoid triggering links
            self._notify_progress("Ensuring Kindle window has focus...", 0.12, 0)
            logger.info("Using Ctrl key press to establish focus (avoids clicking links)")
            import pyautogui
            pyautogui.press('ctrl')  # Press Ctrl key - has no effect but establishes focus
            time.sleep(1.5)  # Wait for focus to be established

            # Test capture
            self._notify_progress("Testing screenshot capture...", 0.15, 0)
            if not self.page_capturer.test_capture(capture_region):
                error_msg = "Screenshot test failed"
                logger.error(error_msg)
                self.session.error(error_msg)
                self._notify_progress(error_msg, 0.0, 0)
                return

            # Main capture loop
            self.session.state = ScanState.CAPTURING
            self._capture_loop(capture_region, kindle_hwnd)

            # Check if cancelled
            if self.session.stop_requested:
                logger.info("Scan cancelled by user")
                self.session.cancel()
                self._notify_progress("Scan cancelled", 0.95, self.session.pages_captured)
                self._cleanup()
                return

            # Generate PDF
            if self.session.pages_captured == 0:
                error_msg = "No pages captured"
                logger.error(error_msg)
                self.session.error(error_msg)
                self._notify_progress(error_msg, 0.0, 0)
                return

            self._generate_pdf()

            # Restore window if maximized
            if self.config.resolution == Resolution.HIGH:
                self.window_manager.restore_window(kindle_hwnd)

            # Complete
            logger.info(f"Scan completed: {self.session.pages_captured} pages")
            self._notify_progress(
                f"Scan complete! PDF saved to {self.session.output_pdf_path}",
                1.0,
                self.session.pages_captured
            )

        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.exception(error_msg)
            self.session.error(error_msg)
            self._notify_progress(error_msg, 0.0, self.session.pages_captured)

    def _capture_loop(self, capture_region, kindle_hwnd):
        """
        Main page capture loop.

        Args:
            capture_region: Window region to capture
            kindle_hwnd: Kindle window handle
        """
        previous_img_path: Optional[Path] = None
        consecutive_duplicates = 0
        max_consecutive_duplicates = 5  # Stop after 5 duplicate pages (more robust)

        # Determine scan mode: exact page count (50/100) or auto-detect (large number)
        use_auto_stop = self.config.max_pages >= 1000
        scan_mode = "auto-detect end" if use_auto_stop else f"exact {self.config.max_pages} pages"
        logger.info(f"Scan mode: {scan_mode}")

        for page_num in range(1, self.config.max_pages + 1):
            # Check for stop request
            if self.session.stop_requested:
                logger.info("Stop requested during capture loop")
                break

            # Check if window is still valid
            if not self.window_manager.is_window_valid(kindle_hwnd):
                logger.error("Kindle window closed during scan")
                self.session.error("Kindle window was closed")
                break

            # Generate screenshot path
            img_path = self.page_capturer.generate_screenshot_path(
                self.config.temp_dir, page_num
            )

            # Capture page
            progress = 0.2 + (0.7 * page_num / self.config.max_pages)
            self._notify_progress(
                f"Capturing page {page_num}...",
                progress,
                page_num - 1
            )

            captured_path = self.page_capturer.capture_page(capture_region, img_path)

            if captured_path is None:
                logger.warning(f"Failed to capture page {page_num}, retrying...")
                time.sleep(1.0)
                # Retry once
                captured_path = self.page_capturer.capture_page(capture_region, img_path)
                if captured_path is None:
                    logger.error(f"Failed to capture page {page_num} after retry")
                    continue

            # Add to session
            self.session.add_page(captured_path)

            # Check for duplicate (end of book detection - only in auto mode)
            if previous_img_path is not None and use_auto_stop:
                is_duplicate, similarity = self.image_processor.compare_images(
                    previous_img_path, captured_path
                )

                logger.debug(f"Page {page_num} similarity: {similarity:.4f}")

                if is_duplicate:
                    consecutive_duplicates += 1
                    logger.info(f"Duplicate detected (#{consecutive_duplicates}): page {page_num}")

                    if consecutive_duplicates >= max_consecutive_duplicates:
                        logger.info(f"Reached end of book (detected {consecutive_duplicates} duplicates)")
                        # Remove duplicate pages
                        for _ in range(consecutive_duplicates):
                            if self.session.captured_images:
                                removed = self.session.captured_images.pop()
                                removed.unlink(missing_ok=True)
                                self.session.pages_captured -= 1
                        break
                else:
                    consecutive_duplicates = 0

            # In exact page count mode, just log similarity without stopping
            elif previous_img_path is not None and not use_auto_stop:
                is_duplicate, similarity = self.image_processor.compare_images(
                    previous_img_path, captured_path
                )
                logger.debug(f"Page {page_num} similarity: {similarity:.4f} (exact mode - continuing)")

            previous_img_path = captured_path

            # Re-activate window every 5 pages to maintain focus
            if page_num % 5 == 0:
                logger.debug(f"Re-activating window at page {page_num} to maintain focus")
                self.window_manager.activate_window(kindle_hwnd)
                time.sleep(0.3)

            # Turn page with retry
            page_turned = self.page_capturer.turn_page()
            if not page_turned:
                logger.warning("Failed to turn page, re-activating window and retrying...")
                # Re-activate window to ensure focus
                self.window_manager.activate_window(kindle_hwnd)
                time.sleep(0.5)
                page_turned = self.page_capturer.turn_page()
                if not page_turned:
                    logger.error("Failed to turn page after retry and window re-activation")

            # Small delay between captures
            time.sleep(0.2)

    def _generate_pdf(self):
        """Generate PDF from captured images."""
        self.session.state = ScanState.PROCESSING
        self._notify_progress(
            "Generating PDF...",
            0.9,
            self.session.pages_captured
        )

        # Remove any remaining duplicates
        logger.info("Removing any remaining duplicates...")
        unique_images = self.image_processor.remove_consecutive_duplicates(
            self.session.captured_images
        )
        self.session.captured_images = unique_images

        # Validate images
        valid_images, invalid_images = self.image_processor.validate_images(
            self.session.captured_images
        )

        if not valid_images:
            error_msg = "No valid images to create PDF"
            logger.error(error_msg)
            self.session.error(error_msg)
            self._notify_progress(error_msg, 0.0, 0)
            return

        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"kindle_scan_{timestamp}.pdf"
        output_path = self.config.output_path / output_filename

        # Create PDF
        pdf_path = self.pdf_generator.create_pdf(
            valid_images,
            output_path,
            title=f"Kindle Scan {timestamp}"
        )

        if pdf_path is None:
            error_msg = "Failed to create PDF"
            logger.error(error_msg)
            self.session.error(error_msg)
            self._notify_progress(error_msg, 0.0, self.session.pages_captured)
            return

        self.session.complete(pdf_path)

        # Cleanup temp files
        self._cleanup()

    def _prepare_directories(self):
        """Prepare output and temp directories."""
        self.config.output_path.mkdir(parents=True, exist_ok=True)
        self.config.temp_dir.mkdir(parents=True, exist_ok=True)

        # Clean temp directory
        for file in self.config.temp_dir.glob("*.png"):
            try:
                file.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete temp file {file}: {e}")

    def _cleanup(self):
        """Clean up temporary files."""
        try:
            if self.config.temp_dir.exists():
                for file in self.config.temp_dir.glob("*.png"):
                    try:
                        file.unlink()
                    except Exception as e:
                        logger.warning(f"Failed to delete temp file {file}: {e}")
                logger.info("Temporary files cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def _notify_progress(self, message: str, progress: Optional[float], page_count: int):
        """
        Notify progress callback.

        Args:
            message: Status message
            progress: Progress value (0.0-1.0) or None
            page_count: Current page count
        """
        if self.progress_callback:
            try:
                self.progress_callback(message, progress, page_count)
            except Exception as e:
                logger.error(f"Error in progress callback: {e}")

    def get_status(self) -> dict:
        """
        Get current scan status.

        Returns:
            Dictionary with status information
        """
        return {
            'state': self.session.state.value,
            'pages_captured': self.session.pages_captured,
            'is_active': self.session.is_active,
            'error_message': self.session.error_message,
            'output_pdf': str(self.session.output_pdf_path) if self.session.output_pdf_path else None,
            'duration': self.session.duration,
        }

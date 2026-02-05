"""
Main application window.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading

from ..models.config import ScanConfig, ScanState
from ..core.scanner import Scanner
from ..utils.keyboard_handler import KeyboardHandler
from ..utils.logger import logger
from .settings_panel import SettingsPanel
from .progress_display import ProgressDisplay


class MainWindow:
    """Main application window."""

    def __init__(self):
        """Initialize main window."""
        self.root = tk.Tk()
        self.root.title("AK Auto-Scanner")
        self.root.geometry("550x800")
        self.root.resizable(False, False)

        # State
        self.scanner: Scanner = None
        self.keyboard_handler: KeyboardHandler = None
        self.is_scanning = False

        self._create_widgets()
        self._setup_keyboard_handler()

        logger.info("Main window initialized")

    def _create_widgets(self):
        """Create main window widgets."""

        # Title
        title_label = ttk.Label(
            self.root,
            text="AK Auto-Scanner PDF Tool",
            font=("Arial", 14, "bold"),
            padding="10"
        )
        title_label.pack()

        # Subtitle
        subtitle_label = ttk.Label(
            self.root,
            text="Automatically scan Kindle pages to PDF",
            font=("Arial", 9),
            foreground="#666666"
        )
        subtitle_label.pack()

        # Separator
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

        # Control buttons frame - MOVED TO TOP
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill="x")

        # Start button
        self.start_button = ttk.Button(
            button_frame,
            text="Start Scanning (スキャン開始)",
            command=self._on_start_scan,
            width=30
        )
        self.start_button.pack(side="left", padx=5)

        # Stop button
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop (停止) - ESC",
            command=self._on_stop_scan,
            width=30,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)

        # Separator
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

        # Settings panel
        self.settings_panel = SettingsPanel(self.root)
        self.settings_panel.pack(fill="both", expand=True, padx=10)

        # Separator
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

        # Progress display
        self.progress_display = ProgressDisplay(self.root)
        self.progress_display.pack(fill="x", padx=10)

        # Footer
        footer_frame = ttk.Frame(self.root, padding="5")
        footer_frame.pack(side="bottom", fill="x")

        footer_label = ttk.Label(
            footer_frame,
            text="Scan starts 5 seconds after pressing Start button | Press ESC to cancel anytime",
            font=("Arial", 8),
            foreground="#999999"
        )
        footer_label.pack()

    def _setup_keyboard_handler(self):
        """Setup keyboard handler for ESC key."""
        self.keyboard_handler = KeyboardHandler(on_escape=self._on_escape_pressed)

    def _on_escape_pressed(self):
        """Handle ESC key press."""
        if self.is_scanning:
            logger.info("ESC key pressed")
            self.root.after(0, self._on_stop_scan)

    def _on_start_scan(self):
        """Handle start scan button click."""
        if self.is_scanning:
            return

        try:
            # Get page count setting
            page_count = self.settings_panel.get_page_count()
            max_pages = page_count if page_count > 0 else 10000  # 0 = all pages (up to 10000)

            # Create configuration
            config = ScanConfig(
                direction=self.settings_panel.get_direction(),
                resolution=self.settings_panel.get_resolution(),
                capture_speed=self.settings_panel.get_speed(),
                max_pages=max_pages,
                output_path=Path("output"),
                temp_dir=Path("temp"),
                margin_top=self.settings_panel.get_margin_top(),
                margin_bottom=self.settings_panel.get_margin_bottom(),
                margin_left=self.settings_panel.get_margin_left(),
                margin_right=self.settings_panel.get_margin_right()
            )

            # Validate configuration
            errors = config.validate()
            if errors:
                messagebox.showerror("Configuration Error", "\n".join(errors))
                return

            # Create scanner
            self.scanner = Scanner(config)

            # Update UI
            self.is_scanning = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.settings_panel.disable()
            self.progress_display.reset()

            # Start keyboard listener
            self.keyboard_handler.start()

            # Start scan
            success = self.scanner.start_scan(progress_callback=self._on_progress_update)

            if not success:
                self._on_scan_complete()
                messagebox.showerror("Error", "Failed to start scan")

        except Exception as e:
            logger.exception("Error starting scan")
            messagebox.showerror("Error", f"Failed to start scan: {e}")
            self._on_scan_complete()

    def _on_stop_scan(self):
        """Handle stop scan button click."""
        if not self.is_scanning or self.scanner is None:
            return

        logger.info("Stop scan requested")
        self.scanner.stop_scan()
        self.stop_button.config(state="disabled")

    def _on_progress_update(self, message: str, progress: float, page_count: int):
        """
        Handle progress update from scanner.

        Args:
            message: Status message
            progress: Progress value (0.0-1.0) or None
            page_count: Current page count
        """
        # Update UI in main thread
        self.root.after(0, self._update_progress_ui, message, progress, page_count)

    def _update_progress_ui(self, message: str, progress: float, page_count: int):
        """
        Update progress UI (must be called from main thread).

        Args:
            message: Status message
            progress: Progress value (0.0-1.0) or None
            page_count: Current page count
        """
        self.progress_display.update_progress(message, progress, page_count)

        # Check if scan is complete
        if self.scanner and self.scanner.session.is_finished:
            self._on_scan_complete()

    def _on_scan_complete(self):
        """Handle scan completion."""
        self.is_scanning = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.settings_panel.enable()

        # Stop keyboard listener
        self.keyboard_handler.stop()

        if self.scanner is None:
            return

        # Show completion message
        if self.scanner.session.state == ScanState.COMPLETE:
            pdf_path = self.scanner.session.output_pdf_path
            page_count = self.scanner.session.pages_captured

            self.progress_display.set_complete(
                f"Scan complete! PDF saved to {pdf_path}",
                page_count
            )

            messagebox.showinfo(
                "Scan Complete",
                f"Successfully scanned {page_count} pages!\n\n"
                f"PDF saved to:\n{pdf_path}"
            )

        elif self.scanner.session.state == ScanState.CANCELLED:
            self.progress_display.reset()
            messagebox.showinfo("Scan Cancelled", "Scan was cancelled by user.")

        elif self.scanner.session.state == ScanState.ERROR:
            error_msg = self.scanner.session.error_message
            self.progress_display.set_error(error_msg)
            messagebox.showerror("Scan Error", f"An error occurred:\n{error_msg}")

    def run(self):
        """Run the application."""
        logger.info("Starting application")
        self.root.mainloop()

    def close(self):
        """Close the application."""
        if self.is_scanning and self.scanner:
            self.scanner.stop_scan()

        if self.keyboard_handler:
            self.keyboard_handler.stop()

        self.root.destroy()
        logger.info("Application closed")

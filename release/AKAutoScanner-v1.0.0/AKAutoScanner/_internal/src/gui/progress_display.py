"""
Progress display for scan status.
"""
import tkinter as tk
from tkinter import ttk


class ProgressDisplay(ttk.Frame):
    """Progress display panel."""

    def __init__(self, parent):
        """
        Initialize progress display.

        Args:
            parent: Parent widget
        """
        super().__init__(parent, padding="10")

        # Variables
        self.status_var = tk.StringVar(value="Ready to scan")
        self.page_count_var = tk.StringVar(value="Pages: 0")

        self._create_widgets()

    def _create_widgets(self):
        """Create progress widgets."""

        # Status label
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            font=("Arial", 10),
            foreground="#333333"
        )
        self.status_label.pack(pady=(0, 5))

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill="x", pady=5)

        # Page count label
        self.page_count_label = ttk.Label(
            self,
            textvariable=self.page_count_var,
            font=("Arial", 9),
            foreground="#666666"
        )
        self.page_count_label.pack(pady=(5, 0))

    def update_progress(self, message: str, progress: float = None, page_count: int = 0):
        """
        Update progress display.

        Args:
            message: Status message
            progress: Progress value (0.0-1.0) or None
            page_count: Current page count
        """
        self.status_var.set(message)
        self.page_count_var.set(f"Pages: {page_count}")

        if progress is not None:
            self.progress_bar['value'] = progress * 100
        else:
            # Indeterminate mode
            self.progress_bar['mode'] = 'indeterminate'
            self.progress_bar.start()

        self.update_idletasks()

    def reset(self):
        """Reset progress display."""
        self.status_var.set("Ready to scan")
        self.page_count_var.set("Pages: 0")
        self.progress_bar['value'] = 0
        self.progress_bar['mode'] = 'determinate'
        self.progress_bar.stop()

    def set_complete(self, message: str, page_count: int):
        """
        Set completion message.

        Args:
            message: Completion message
            page_count: Final page count
        """
        self.status_var.set(message)
        self.page_count_var.set(f"Total pages: {page_count}")
        self.progress_bar['value'] = 100

    def set_error(self, message: str):
        """
        Set error message.

        Args:
            message: Error message
        """
        self.status_var.set(f"Error: {message}")
        self.progress_bar['value'] = 0
        self.progress_bar['mode'] = 'determinate'
        self.progress_bar.stop()

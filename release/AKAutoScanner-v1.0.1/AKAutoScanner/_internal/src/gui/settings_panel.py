"""
Settings panel for scan configuration.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable

from ..models.config import Direction, Resolution


class SettingsPanel(ttk.Frame):
    """Settings panel for configuring scan parameters."""

    def __init__(self, parent, on_change: Callable = None):
        """
        Initialize settings panel.

        Args:
            parent: Parent widget
            on_change: Callback when settings change
        """
        super().__init__(parent, padding="10")
        self.on_change = on_change

        # Variables
        self.direction_var = tk.StringVar(value=Direction.WESTERN.value)
        self.resolution_var = tk.StringVar(value=Resolution.MEDIUM.value)
        self.speed_var = tk.DoubleVar(value=1.0)
        self.page_count_var = tk.IntVar(value=0)  # 0 = all pages

        # Margin variables (negative values expand the capture area)
        self.margin_top_var = tk.IntVar(value=-20)
        self.margin_bottom_var = tk.IntVar(value=-20)
        self.margin_left_var = tk.IntVar(value=0)
        self.margin_right_var = tk.IntVar(value=0)

        self._create_widgets()

    def _create_widgets(self):
        """Create settings widgets."""

        # Direction setting
        direction_frame = ttk.LabelFrame(self, text="Page Direction (ページ方向)", padding="5")
        direction_frame.grid(row=0, column=0, sticky="ew", pady=5)

        ttk.Radiobutton(
            direction_frame,
            text="Western (洋書) - Right arrow →",
            variable=self.direction_var,
            value=Direction.WESTERN.value,
            command=self._on_setting_change
        ).pack(anchor="w")

        ttk.Radiobutton(
            direction_frame,
            text="Japanese (和書) - Left arrow ←",
            variable=self.direction_var,
            value=Direction.JAPANESE.value,
            command=self._on_setting_change
        ).pack(anchor="w")

        # Resolution setting
        resolution_frame = ttk.LabelFrame(self, text="Resolution (解像度)", padding="5")
        resolution_frame.grid(row=1, column=0, sticky="ew", pady=5)

        ttk.Radiobutton(
            resolution_frame,
            text="Low (Standard) - Fastest",
            variable=self.resolution_var,
            value=Resolution.LOW.value,
            command=self._on_setting_change
        ).pack(anchor="w")

        ttk.Radiobutton(
            resolution_frame,
            text="Medium (High) - Recommended ★",
            variable=self.resolution_var,
            value=Resolution.MEDIUM.value,
            command=self._on_setting_change
        ).pack(anchor="w")

        ttk.Radiobutton(
            resolution_frame,
            text="High (Ultra) - Best quality (slower)",
            variable=self.resolution_var,
            value=Resolution.HIGH.value,
            command=self._on_setting_change
        ).pack(anchor="w")

        # Speed setting
        speed_frame = ttk.LabelFrame(self, text="Capture Speed (キャプチャ速度)", padding="5")
        speed_frame.grid(row=2, column=0, sticky="ew", pady=5)

        speed_options = [
            ("Fast (0.5s) - May miss pages", 0.5),
            ("Standard (1.0s) - Recommended ★", 1.0),
            ("Slow (2.0s) - Most stable", 2.0),
        ]

        for text, value in speed_options:
            ttk.Radiobutton(
                speed_frame,
                text=text,
                variable=self.speed_var,
                value=value,
                command=self._on_setting_change
            ).pack(anchor="w")

        # Page count setting
        page_count_frame = ttk.LabelFrame(self, text="Scan Mode (スキャンモード)", padding="5")
        page_count_frame.grid(row=3, column=0, sticky="ew", pady=5)

        page_count_options = [
            ("50 pages (50ページずつ)", 50),
            ("100 pages (100ページずつ)", 100),
            ("All pages (全ページ自動) ★", 0),
        ]

        for text, value in page_count_options:
            ttk.Radiobutton(
                page_count_frame,
                text=text,
                variable=self.page_count_var,
                value=value,
                command=self._on_setting_change
            ).pack(anchor="w")

        # Margin settings
        margin_frame = ttk.LabelFrame(self, text="Capture Margins (キャプチャ余白調整)", padding="5")
        margin_frame.grid(row=4, column=0, sticky="ew", pady=5)

        margin_desc = ttk.Label(
            margin_frame,
            text="Negative values expand the capture area (マイナス値で拡大)",
            font=("Arial", 8),
            foreground="#666666"
        )
        margin_desc.pack(anchor="w", pady=(0, 5))

        # Create a grid for margin inputs
        margin_grid = ttk.Frame(margin_frame)
        margin_grid.pack(fill="x")

        # Top margin
        ttk.Label(margin_grid, text="Top (上):").grid(row=0, column=0, sticky="w", padx=(0, 5))
        top_spinbox = ttk.Spinbox(
            margin_grid,
            from_=-100,
            to=100,
            textvariable=self.margin_top_var,
            width=8,
            command=self._on_setting_change
        )
        top_spinbox.grid(row=0, column=1, sticky="w", padx=5)
        ttk.Label(margin_grid, text="px").grid(row=0, column=2, sticky="w")

        # Bottom margin
        ttk.Label(margin_grid, text="Bottom (下):").grid(row=1, column=0, sticky="w", padx=(0, 5))
        bottom_spinbox = ttk.Spinbox(
            margin_grid,
            from_=-100,
            to=100,
            textvariable=self.margin_bottom_var,
            width=8,
            command=self._on_setting_change
        )
        bottom_spinbox.grid(row=1, column=1, sticky="w", padx=5)
        ttk.Label(margin_grid, text="px").grid(row=1, column=2, sticky="w")

        # Left margin
        ttk.Label(margin_grid, text="Left (左):").grid(row=0, column=3, sticky="w", padx=(20, 5))
        left_spinbox = ttk.Spinbox(
            margin_grid,
            from_=-100,
            to=100,
            textvariable=self.margin_left_var,
            width=8,
            command=self._on_setting_change
        )
        left_spinbox.grid(row=0, column=4, sticky="w", padx=5)
        ttk.Label(margin_grid, text="px").grid(row=0, column=5, sticky="w")

        # Right margin
        ttk.Label(margin_grid, text="Right (右):").grid(row=1, column=3, sticky="w", padx=(20, 5))
        right_spinbox = ttk.Spinbox(
            margin_grid,
            from_=-100,
            to=100,
            textvariable=self.margin_right_var,
            width=8,
            command=self._on_setting_change
        )
        right_spinbox.grid(row=1, column=4, sticky="w", padx=5)
        ttk.Label(margin_grid, text="px").grid(row=1, column=5, sticky="w")

        # Info label
        info_text = (
            "使い方:\n"
            "1. Kindleで本を開き、最初のページへ\n"
            "2. 上記の設定を選択\n"
            "3. 文字が途切れる場合はマージンを調整\n"
            "4. 「Start Scanning」をクリック\n"
            "5. 5秒後に自動でスキャン開始\n"
            "6. ESCキーでいつでも停止可能"
        )
        info_label = ttk.Label(
            self,
            text=info_text,
            background="#f0f0f0",
            padding="10",
            justify="left"
        )
        info_label.grid(row=5, column=0, sticky="ew", pady=10)

    def _on_setting_change(self):
        """Handle setting change."""
        if self.on_change:
            self.on_change()

    def get_direction(self) -> Direction:
        """Get selected direction."""
        return Direction(self.direction_var.get())

    def get_resolution(self) -> Resolution:
        """Get selected resolution."""
        return Resolution(self.resolution_var.get())

    def get_speed(self) -> float:
        """Get selected capture speed."""
        return self.speed_var.get()

    def get_page_count(self) -> int:
        """Get selected page count (0 = all pages)."""
        return self.page_count_var.get()

    def get_margin_top(self) -> int:
        """Get top margin."""
        return self.margin_top_var.get()

    def get_margin_bottom(self) -> int:
        """Get bottom margin."""
        return self.margin_bottom_var.get()

    def get_margin_left(self) -> int:
        """Get left margin."""
        return self.margin_left_var.get()

    def get_margin_right(self) -> int:
        """Get right margin."""
        return self.margin_right_var.get()

    def enable(self):
        """Enable all settings."""
        for child in self.winfo_children():
            self._set_widget_state(child, "normal")

    def disable(self):
        """Disable all settings."""
        for child in self.winfo_children():
            self._set_widget_state(child, "disabled")

    def _set_widget_state(self, widget, state):
        """Recursively set widget state."""
        try:
            widget.configure(state=state)
        except tk.TclError:
            pass

        for child in widget.winfo_children():
            self._set_widget_state(child, state)

"""
Scan state management for tracking progress and state.
"""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import ScanState


@dataclass
class ScanSession:
    """Tracks the state of a scanning session."""

    # State
    state: ScanState = ScanState.IDLE

    # Progress
    pages_captured: int = 0
    current_page_path: Optional[Path] = None

    # Timing
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    # Results
    output_pdf_path: Optional[Path] = None
    captured_images: list[Path] = field(default_factory=list)

    # Error handling
    error_message: Optional[str] = None

    # Control flags
    stop_requested: bool = False

    def start(self):
        """Mark session as started."""
        self.state = ScanState.PREPARING
        self.start_time = datetime.now()
        self.pages_captured = 0
        self.captured_images = []
        self.stop_requested = False
        self.error_message = None

    def complete(self, pdf_path: Path):
        """Mark session as completed."""
        self.state = ScanState.COMPLETE
        self.end_time = datetime.now()
        self.output_pdf_path = pdf_path

    def cancel(self):
        """Mark session as cancelled."""
        self.state = ScanState.CANCELLED
        self.end_time = datetime.now()

    def error(self, message: str):
        """Mark session as errored."""
        self.state = ScanState.ERROR
        self.end_time = datetime.now()
        self.error_message = message

    def add_page(self, image_path: Path):
        """Add a captured page to the session."""
        self.captured_images.append(image_path)
        self.current_page_path = image_path
        self.pages_captured += 1

    @property
    def duration(self) -> Optional[float]:
        """Get session duration in seconds."""
        if self.start_time is None:
            return None
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()

    @property
    def is_active(self) -> bool:
        """Check if session is actively scanning."""
        return self.state in [ScanState.PREPARING, ScanState.CAPTURING, ScanState.PROCESSING]

    @property
    def is_finished(self) -> bool:
        """Check if session has finished (completed, cancelled, or errored)."""
        return self.state in [ScanState.COMPLETE, ScanState.CANCELLED, ScanState.ERROR]

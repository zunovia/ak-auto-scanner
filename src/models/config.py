"""
Configuration models and enums for the AK Auto-Scanner.
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class Direction(Enum):
    """Page turn direction for different book types."""
    JAPANESE = "japanese"  # Left arrow for next page (和書)
    WESTERN = "western"    # Right arrow for next page (洋書)


class Resolution(Enum):
    """Screenshot resolution quality modes."""
    LOW = "low"        # Standard - capture at current window size
    MEDIUM = "medium"  # High - scale 1.5x for clarity
    HIGH = "high"      # Ultra - maximize window + full screen capture


class ScanState(Enum):
    """Scanner state machine states."""
    IDLE = "idle"
    PREPARING = "preparing"
    CAPTURING = "capturing"
    PROCESSING = "processing"
    COMPLETE = "complete"
    CANCELLED = "cancelled"
    ERROR = "error"


@dataclass
class ScanConfig:
    """Configuration for a scanning session."""

    # Page turning
    direction: Direction = Direction.WESTERN

    # Image quality
    resolution: Resolution = Resolution.MEDIUM

    # Timing
    capture_speed: float = 1.0  # Seconds between captures (0.5, 1.0, 2.0)

    # Duplicate detection
    similarity_threshold: float = 0.95  # SSIM threshold for detecting duplicates

    # Limits
    max_pages: int = 10000  # Maximum pages to scan before auto-stop

    # Paths
    output_path: Optional[Path] = None  # PDF output path
    temp_dir: Optional[Path] = None     # Temporary screenshot directory

    # PDF settings
    pdf_quality: int = 95  # JPEG quality for PDF images (1-100)

    # Capture region margins (negative values to expand, positive to shrink)
    margin_top: int = -20     # Top margin adjustment in pixels
    margin_bottom: int = -20  # Bottom margin adjustment in pixels
    margin_left: int = 0      # Left margin adjustment in pixels
    margin_right: int = 0     # Right margin adjustment in pixels

    def __post_init__(self):
        """Set default paths if not provided."""
        if self.output_path is None:
            self.output_path = Path("output")
        if self.temp_dir is None:
            self.temp_dir = Path("temp")

        # Ensure paths are Path objects
        if not isinstance(self.output_path, Path):
            self.output_path = Path(self.output_path)
        if not isinstance(self.temp_dir, Path):
            self.temp_dir = Path(self.temp_dir)

    def validate(self) -> list[str]:
        """
        Validate configuration values.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        if self.capture_speed < 0.1 or self.capture_speed > 10.0:
            errors.append("Capture speed must be between 0.1 and 10.0 seconds")

        if self.similarity_threshold < 0.0 or self.similarity_threshold > 1.0:
            errors.append("Similarity threshold must be between 0.0 and 1.0")

        if self.max_pages < 1:
            errors.append("Max pages must be at least 1")

        if self.pdf_quality < 1 or self.pdf_quality > 100:
            errors.append("PDF quality must be between 1 and 100")

        return errors

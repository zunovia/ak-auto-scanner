"""
Input validation utilities.
"""
from pathlib import Path


def validate_positive_number(value: float, name: str = "Value") -> None:
    """
    Validate that a number is positive.

    Args:
        value: Number to validate
        name: Name of the value for error messages

    Raises:
        ValueError: If value is not positive
    """
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def validate_range(value: float, min_val: float, max_val: float, name: str = "Value") -> None:
    """
    Validate that a number is within a range.

    Args:
        value: Number to validate
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
        name: Name of the value for error messages

    Raises:
        ValueError: If value is outside the range
    """
    if value < min_val or value > max_val:
        raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")


def validate_path_exists(path: Path, name: str = "Path") -> None:
    """
    Validate that a path exists.

    Args:
        path: Path to validate
        name: Name of the path for error messages

    Raises:
        FileNotFoundError: If path does not exist
    """
    if not path.exists():
        raise FileNotFoundError(f"{name} does not exist: {path}")


def validate_directory(path: Path, create: bool = False, name: str = "Directory") -> None:
    """
    Validate that a path is a directory.

    Args:
        path: Path to validate
        create: Whether to create the directory if it doesn't exist
        name: Name of the directory for error messages

    Raises:
        ValueError: If path exists but is not a directory
        FileNotFoundError: If path does not exist and create is False
    """
    if path.exists():
        if not path.is_dir():
            raise ValueError(f"{name} is not a directory: {path}")
    elif create:
        path.mkdir(parents=True, exist_ok=True)
    else:
        raise FileNotFoundError(f"{name} does not exist: {path}")


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize a filename by removing invalid characters.

    Args:
        filename: Original filename
        max_length: Maximum length for the filename

    Returns:
        Sanitized filename
    """
    # Remove invalid characters for Windows filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')

    # Truncate to max length
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        if ext:
            max_name_length = max_length - len(ext) - 1
            filename = f"{name[:max_name_length]}.{ext}"
        else:
            filename = filename[:max_length]

    return filename or "untitled"

"""
AK Auto-Scanner PDF Tool - Main Entry Point
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui.main_window import MainWindow
from src.utils.logger import setup_logger


def main():
    """Main entry point."""
    # Setup logging
    logger = setup_logger()
    logger.info("="*50)
    logger.info("AK Auto-Scanner PDF Tool")
    logger.info("="*50)

    try:
        # Create and run main window
        app = MainWindow()
        app.run()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

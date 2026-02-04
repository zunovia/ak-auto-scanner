# AK Auto-Scanner PDF Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

Automatically capture pages from Kindle for PC app and convert them to a single PDF file for personal backup purposes.

## 📥 Quick Download

- **[Download Latest Release](https://github.com/YOUR_USERNAME/ak-auto-scanner/releases)** - Standalone executable (no Python required)
- **[Installation Guide](INSTALLATION.md)** - Detailed installation instructions

## Features

- **Automated Page Capture**: Automatically screenshots and turns pages
- **Multiple Resolution Modes**: Low (fast), Medium (recommended), High (best quality)
- **Japanese & Western Book Support**: Configurable page turn direction
- **Smart Duplicate Detection**: Auto-stops at end of book using SSIM algorithm
- **Emergency Stop**: Press ESC at any time to stop scanning
- **Progress Tracking**: Real-time progress bar and status updates

## Requirements

- Windows 10 or later
- Python 3.8 or later
- Kindle for PC application

## Installation

1. Clone or download this repository:
```bash
cd C:\temp\kindle-pdf
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

1. **Open Kindle for PC** and navigate to the first page of your book

2. **Run the application**:
```bash
python src/main.py
```

3. **Configure settings**:
   - **Page Direction**:
     - Western (洋書): Right arrow → for next page
     - Japanese (和書): Left arrow ← for next page
   - **Resolution**:
     - Low: Fastest, standard quality
     - Medium: Recommended, 1.5x scaling
     - High: Best quality, maximizes window
   - **Capture Speed**:
     - Fast (0.5s): Quick but may miss pages
     - Standard (1.0s): Recommended
     - Slow (2.0s): Most stable for slow devices

4. **Click "Start Scanning"** - a 5-second countdown will begin

5. **Wait 5 seconds** - gives you time to switch to Kindle window

6. **Press ESC** to stop scanning at any time

7. **Find your PDF** in the `output/` directory

### Example Workflow

```
1. Open book in Kindle → Go to first page
2. Run: python src/main.py
3. Select: Western, Medium, 1.0s
4. Click: Start Scanning
5. Wait 5 seconds (countdown) → Scanning begins automatically
6. Wait for completion or press ESC
7. Output: output/kindle_scan_YYYYMMDD_HHMMSS.pdf
```

## Settings Explained

### Page Direction

- **Western (洋書)**: Uses Right arrow key (→) or PageDown to turn pages
  - For English books, left-to-right reading
- **Japanese (和書)**: Uses Left arrow key (←) or PageUp to turn pages
  - For Japanese books, right-to-left reading

### Resolution Modes

| Mode   | Description                          | Speed    | Quality |
|--------|--------------------------------------|----------|---------|
| Low    | Capture at current window size       | Fastest  | Standard|
| Medium | Scale 1.5x for clarity (recommended) | Normal   | High    |
| High   | Maximize window + full screen        | Slower   | Best    |

### Capture Speed

The delay after each page turn to wait for rendering:

- **0.5s (Fast)**: May capture blurry pages if Kindle is slow
- **1.0s (Standard)**: Recommended for most users
- **2.0s (Slow)**: For older computers or large books

## How It Works

1. **Countdown**: 5-second countdown before starting (allows window switching)
2. **Window Detection**: Finds and activates Kindle window
3. **Screenshot Capture**: Takes screenshot of Kindle window
4. **Page Turn**: Sends arrow key to turn page
5. **Wait for Render**: Delays for page to finish loading
6. **Duplicate Detection**: Compares with previous page using SSIM
7. **Auto-Stop**: Stops when duplicate pages detected (end of book)
8. **PDF Generation**: Converts all images to single PDF
9. **Cleanup**: Removes temporary files

## Duplicate Detection

Uses **Structural Similarity Index (SSIM)** algorithm:
- Compares each page with the previous one
- Threshold: 95% similarity
- Detects when reached end of book (same page appears multiple times)
- Automatically stops scanning

## Keyboard Shortcuts

- **ESC**: Emergency stop (stops scanning immediately)

## Output

- **PDF Location**: `output/kindle_scan_YYYYMMDD_HHMMSS.pdf`
- **Logs**: `output/logs/scanner_YYYYMMDD_HHMMSS.log`
- **Temp Files**: Automatically cleaned up after completion

## Troubleshooting

### "Kindle window not found"
- Ensure Kindle for PC is running
- Make sure a book is open (not library view)

### Pages are blurry
- Increase capture speed to 2.0s
- Use higher resolution mode
- Ensure Kindle window is fully visible

### Scanning doesn't stop at end
- SSIM threshold may need adjustment
- Check logs in `output/logs/`
- Manually press ESC to stop

### Some pages are duplicates
- Normal behavior - algorithm removes consecutive duplicates
- If many duplicates, increase capture speed

### Window not activating
- Disable "always on top" for other windows
- Run as administrator if needed

## Advanced Configuration

Edit `src/models/config.py` to adjust:
- `similarity_threshold`: SSIM threshold (default: 0.95)
- `max_pages`: Maximum pages to scan (default: 500)
- `pdf_quality`: JPEG quality in PDF (default: 95)

## Project Structure

```
kindle-pdf/
├── src/
│   ├── main.py                 # Entry point
│   ├── gui/
│   │   ├── main_window.py      # Main GUI window
│   │   ├── settings_panel.py   # Settings controls
│   │   └── progress_display.py # Progress bar
│   ├── core/
│   │   ├── scanner.py          # Main orchestrator
│   │   ├── window_manager.py   # Window control
│   │   ├── page_capturer.py    # Screenshot & page turn
│   │   ├── image_processor.py  # Duplicate detection
│   │   └── pdf_generator.py    # PDF creation
│   ├── models/
│   │   ├── config.py           # Configuration models
│   │   └── scan_state.py       # State management
│   └── utils/
│       ├── logger.py           # Logging
│       ├── keyboard_handler.py # ESC key listener
│       └── validators.py       # Input validation
├── output/                     # PDF output directory
├── temp/                       # Temporary screenshots
├── venv/                       # Python virtual environment
├── run_scanner.bat             # Quick launch script (Windows)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── QUICKSTART_SCANNER.md       # Quick start guide
└── LICENSE                     # MIT License
```

## Performance

- **Memory Usage**: < 500MB for 100-page book
- **Speed**: ~1 page per second (standard mode)
- **PDF Generation**: < 10 seconds for 100 pages

## Legal & Ethical Use

This tool is for **personal backup purposes only**:
- ✅ Backing up your purchased Kindle books
- ✅ Personal archival of your library
- ❌ Sharing or distributing copied books
- ❌ Circumventing DRM for commercial use
- ❌ Violating copyright laws

**Respect copyright and terms of service.**

## Limitations

- Windows only (uses pywin32)
- Requires Kindle for PC (desktop app)
- Display capture only (respects DRM)
- Cannot extract native text (no OCR in MVP)

## Future Enhancements

Potential features for future versions:
- OCR integration for searchable PDFs
- Bookmark detection
- Table of contents generation
- Batch processing multiple books
- Multi-monitor support
- Executable installer (PyInstaller)

## Dependencies

- `pyautogui`: Screenshot and keyboard automation
- `Pillow`: Image processing and PDF generation
- `opencv-python`: Image comparison (SSIM)
- `pywin32`: Windows window management
- `pynput`: Keyboard event listener
- `scikit-image`: SSIM algorithm

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## Support

For issues or questions:
- Check logs in `output/logs/`
- Review troubleshooting section above
- Open an issue on GitHub

## Acknowledgments

- Uses Structural Similarity Index (SSIM) for duplicate detection
- Built with Python, tkinter, and OpenCV
- Inspired by the need for personal book backups

---

**Version**: 1.0.0
**Author**: AK Auto-Scanner
**Last Updated**: 2025-02-04

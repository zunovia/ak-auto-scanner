# 📝 Release Notes

## Version 1.0.1 (2026-02-05)

### 🐛 Bug Fixes

- **Fixed premature scan termination**: Increased "All pages" mode limit from 500 to 10,000 pages
- **Improved scan reliability**: Changed auto-stop detection threshold from 500 to 1,000 pages
- **More robust end-of-book detection**: Increased duplicate detection threshold from 3 to 5 consecutive duplicates to prevent false positives
- **Better page turning reliability**: Added retry logic when page turning fails

### 🔧 Technical Changes

- Modified `max_pages` default from 500 to 10,000 in config
- Updated scan mode threshold to use 1,000 pages for auto-detect mode
- Enhanced page turning with automatic retry on failure
- More resilient handling of temporary page turn failures

---

## Version 1.0.0 (2026-02-04)

### 🎉 Initial Release

First stable release of AK Auto-Scanner!

### ✨ Features

- **Automated Page Capture**: Automatically screenshots and turns pages in Kindle for PC
- **Multiple Resolution Modes**:
  - Low (fast)
  - Medium (recommended, 1.5x scaling)
  - High (best quality, maximizes window)
- **Smart Duplicate Detection**: Uses SSIM algorithm to detect end of book
- **Japanese & Western Book Support**: Configurable page turn direction
- **5-Second Countdown**: Time to prepare before scanning starts
- **Capture Margin Adjustment**: Fix text cutoff issues with adjustable margins
- **Emergency Stop**: Press ESC at any time to stop scanning
- **Real-time Progress Tracking**: Progress bar and status updates
- **Automatic PDF Generation**: Converts all captured pages to a single PDF
- **Clean Temporary Files**: Automatically removes temporary screenshots

### 🎯 Scan Modes

- **50 Pages**: Scan exactly 50 pages
- **100 Pages**: Scan exactly 100 pages
- **All Pages (Auto)**: Automatically detect end of book using duplicate detection

### 🔧 Technical Details

- Built with Python 3.8+
- GUI framework: tkinter
- Image processing: OpenCV, scikit-image, Pillow
- Window management: pywin32, pyautogui
- Keyboard handling: pynput

### 📦 Installation Options

1. **Standalone Executable** (.exe) - No Python installation required
2. **Python Source Code** - For developers and customization

### 🐛 Known Issues

None at this time.

### 📚 Documentation

- [README.md](README.md) - Full documentation
- [START_HERE.md](START_HERE.md) - Quick start guide
- [INSTALLATION.md](INSTALLATION.md) - Installation instructions
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - GitHub setup guide

### 🙏 Acknowledgments

- Uses Structural Similarity Index (SSIM) for duplicate detection
- Built with Python, tkinter, and OpenCV

---

## Future Roadmap

Potential features for future versions:

- [ ] OCR integration for searchable PDFs
- [ ] Bookmark detection and preservation
- [ ] Table of contents generation
- [ ] Batch processing multiple books
- [ ] Multi-monitor support
- [ ] Customizable keyboard shortcuts
- [ ] Automatic page number detection
- [ ] Image enhancement options
- [ ] Cloud storage integration
- [ ] Linux/Mac support

---

**For the latest updates, visit**: https://github.com/YOUR_USERNAME/ak-auto-scanner/releases

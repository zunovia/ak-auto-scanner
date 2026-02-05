# 📝 Release Notes

## Version 1.0.6 (2026-02-05)

### 🐛 Bug Fixes

- **Link clicking completely eliminated**: Removed all window clicking, now using Ctrl key press for focus
- **Window height increased**: Increased from 920px to 1040px (~6cm taller than original)
- **Auto window reactivation**: Window is re-activated every 5 pages to maintain focus
- **No more page jumps**: Links can no longer be accidentally triggered

### 🔧 Technical Changes

- Replaced mouse click with safe keyboard input (Ctrl key) for focus
- Added periodic window reactivation (every 5 pages)
- Window geometry: 550x1040 pixels

### 📝 How It Works Now

1. Uses `SetForegroundWindow()` to activate Kindle window
2. Presses Ctrl key (harmless) to establish keyboard focus
3. Re-activates window every 5 pages to maintain focus
4. Never clicks anywhere in the window - completely avoids links

---

## Version 1.0.5 (2026-02-05)

### 🐛 Bug Fixes

- **Window height increased**: Increased window height from 800px to 920px (~3cm taller)
- **Settings panel fully visible**: All settings now visible without scrolling or cutoff

### 🔧 Technical Changes

- Window geometry changed from 550x800 to 550x920 pixels

---

## Version 1.0.4 (2026-02-05)

### ✨ New Features

- **Custom page count input**: Added ability to enter any custom page number (e.g., 200, 300, 500 pages)
- **Japanese default**: Changed default direction to Japanese (和書) for better user experience

### 🐛 Bug Fixes

- **Click position optimized**: Moved click from bottom-center to bottom-right corner (95%, 95%)
- **Link avoidance improved**: Corner position ensures links are never clicked accidentally
- **50-page mode link skip fixed**: Pages with links are no longer skipped

### 🎯 How to Use Custom Pages

1. Select "Custom (カスタム)" in Scan Mode
2. Enter desired page count in the input field (e.g., 200)
3. Click "Start Scanning"

---

## Version 1.0.3 (2026-02-05)

### 🐛 Bug Fixes

- **Fixed keyboard focus loss**: Re-enabled window clicking at bottom area (90% down) to maintain keyboard focus
- **Improved page turning reliability**: Window is re-activated automatically when page turn fails
- **Smarter retry logic**: Failed page turns now trigger window re-activation before retry

### 🔧 Technical Changes

- Click position moved to bottom area (90% from top) to avoid links while maintaining focus
- Added automatic window re-activation on page turn failure
- Enhanced focus management throughout scan process

### 📝 Background

Previous version (v1.0.2) removed window clicking to avoid link activation, but this caused keyboard focus loss, resulting in pages not turning properly. This version restores clicking but uses a safe bottom position.

---

## Version 1.0.2 (2026-02-05)

### 🐛 Bug Fixes

- **Fixed accidental link clicks**: Removed window center click that was triggering links in Kindle pages
- **Prevent page jumps**: Scanning no longer stops when encountering linked text (e.g., in table of contents)
- **More reliable scanning**: SetForegroundWindow is now sufficient for window focus without clicking

### 🔧 Technical Changes

- Disabled window click during initial setup to avoid triggering internal links
- Updated click_window_center method to use bottom area (90% down) if needed in future
- This ensures continuous scanning regardless of link presence on pages

---

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

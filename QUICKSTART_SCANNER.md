# AK Auto-Scanner - Quick Start Guide

## 🚀 Installation (5 minutes)

### Step 1: Install Python
1. Download Python 3.8 or later from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install Dependencies
Open Command Prompt and navigate to the project directory:
```bash
cd C:\temp\kindle-pdf
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python verify_installation.py
```

If all checks pass ✓, you're ready!

## 📖 First Scan (3 steps)

### 1. Prepare Your Book
- Open **Kindle for PC**
- Open a book
- Navigate to the **first page** you want to scan

### 2. Run the Scanner
**Option A: Using Batch File (Easiest)**
```bash
run_scanner.bat
```

**Option B: Using Python**
```bash
python src/main.py
```

### 3. Configure & Start
1. Select **Page Direction**:
   - **Western** for English books (→)
   - **Japanese** for Japanese books (←)

2. Select **Resolution**:
   - **Medium** (recommended) ★

3. Select **Capture Speed**:
   - **1.0s** (recommended) ★

4. Click **"Start Scanning"**

5. **Press ESC** anytime to stop

6. Find your PDF in `output/kindle_scan_YYYYMMDD_HHMMSS.pdf`

## ⚙️ Settings Guide

### Page Direction
| Book Type | Direction | Key Used |
|-----------|-----------|----------|
| English, Western | Western | Right arrow → |
| Japanese, Manga | Japanese | Left arrow ← |

### Resolution Quality
| Mode | Speed | Quality | When to Use |
|------|-------|---------|-------------|
| Low | Fast | Standard | Quick scans |
| Medium ★ | Normal | High | Most books (recommended) |
| High | Slow | Best | Important documents |

### Capture Speed
| Speed | Use Case |
|-------|----------|
| 0.5s (Fast) | Fast computer, simple pages |
| 1.0s (Standard) ★ | Most situations (recommended) |
| 2.0s (Slow) | Older computer, complex pages |

## 🎯 Tips for Best Results

1. **Window Position**: Kindle window should be fully visible
2. **Lighting**: Not relevant (screen capture, not camera)
3. **Page Count**: Will auto-stop at end of book
4. **Interruption**: Press ESC to stop safely anytime
5. **Multiple Books**: Close previous scan before starting new one

## 🐛 Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| "Kindle window not found" | Open Kindle app and a book |
| Blurry pages | Increase speed to 2.0s |
| Duplicate pages | Normal - automatically removed |
| Scan won't stop | Press ESC key |
| PDF too large | Use Low resolution mode |

## 📁 File Locations

- **PDF Output**: `output/kindle_scan_YYYYMMDD_HHMMSS.pdf`
- **Logs**: `output/logs/scanner_YYYYMMDD_HHMMSS.log`
- **Temp Files**: Automatically deleted after completion

## 🔍 Example Session

```
1. Open Kindle → Navigate to page 1
2. Run: python src/main.py
3. Settings: Western, Medium, 1.0s
4. Click: "Start Scanning"
5. Wait: ~1-2 minutes for 100 pages
6. Result: output/kindle_scan_20250204_143022.pdf
```

## ⌨️ Keyboard Shortcuts

- **ESC**: Stop scanning immediately

## 📊 Performance

- **Speed**: ~1 page per second
- **Memory**: < 500MB
- **100 pages**: ~2 minutes
- **500 pages**: ~8-10 minutes

## ⚖️ Legal Notice

**For Personal Backup Only**

✅ Your purchased books
❌ Sharing or distribution
❌ Commercial use

You are responsible for complying with copyright laws and Amazon's Terms of Service.

## 🆘 Need Help?

1. Check logs: `output/logs/`
2. Read full documentation: `README_SCANNER.md`
3. Run verification: `python verify_installation.py`

## 📝 Version Info

- **Version**: 1.0.0
- **Date**: 2025-02-04
- **Platform**: Windows 10/11
- **Python**: 3.8+

---

**Ready to start? Run:** `run_scanner.bat`

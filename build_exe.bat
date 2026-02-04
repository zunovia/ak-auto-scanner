@echo off
echo ========================================
echo Building AK Auto-Scanner Installer
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install PyInstaller if not already installed
echo Installing PyInstaller...
pip install pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build executable
echo.
echo Building executable...
pyinstaller build_installer.spec

if errorlevel 1 (
    echo.
    echo ========================================
    echo Build FAILED!
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build SUCCESSFUL!
echo ========================================
echo.
echo Executable location: dist\AKAutoScanner\AKAutoScanner.exe
echo.
echo You can now copy the entire 'dist\AKAutoScanner' folder
echo to another PC and run AKAutoScanner.exe
echo.
pause

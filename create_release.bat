@echo off
echo ========================================
echo AK Auto-Scanner Release Creator
echo ========================================
echo.

set VERSION=1.0.2

REM Check if dist folder exists
if not exist "dist\AKAutoScanner" (
    echo Error: Executable not found!
    echo Please run build_exe.bat first.
    pause
    exit /b 1
)

echo Creating release package...
echo.

REM Create release folder
set RELEASE_DIR=release\AKAutoScanner-v%VERSION%
if exist "release" rmdir /s /q release
mkdir "%RELEASE_DIR%"

echo Copying executable...
xcopy /E /I /Y "dist\AKAutoScanner" "%RELEASE_DIR%\AKAutoScanner"

echo Copying documentation...
copy /Y "README.md" "%RELEASE_DIR%\"
copy /Y "START_HERE.md" "%RELEASE_DIR%\"
copy /Y "INSTALLATION.md" "%RELEASE_DIR%\"
copy /Y "LICENSE" "%RELEASE_DIR%\"
copy /Y "RELEASE_NOTES.md" "%RELEASE_DIR%\"

echo Creating output directory...
mkdir "%RELEASE_DIR%\output"
mkdir "%RELEASE_DIR%\output\logs"

echo Creating README for executable...
(
echo AK Auto-Scanner v%VERSION%
echo ========================================
echo.
echo Quick Start:
echo 1. Run AKAutoScanner\AKAutoScanner.exe
echo 2. Open Kindle for PC and navigate to first page
echo 3. Configure settings in the application
echo 4. Click "Start Scanning"
echo 5. Wait 5 seconds for countdown
echo 6. Scanning will begin automatically
echo.
echo Output: output\kindle_scan_YYYYMMDD_HHMMSS.pdf
echo.
echo For detailed instructions, see START_HERE.md
echo.
echo Press ESC at any time to stop scanning.
) > "%RELEASE_DIR%\README.txt"

echo.
echo Creating ZIP archive...
powershell -Command "Compress-Archive -Path 'release\AKAutoScanner-v%VERSION%' -DestinationPath 'AKAutoScanner-v%VERSION%.zip' -Force"

if errorlevel 1 (
    echo Error: Failed to create ZIP archive
    pause
    exit /b 1
)

echo.
echo ========================================
echo Release package created successfully!
echo ========================================
echo.
echo Location: AKAutoScanner-v%VERSION%.zip
echo Size:
powershell -Command "(Get-Item 'AKAutoScanner-v%VERSION%.zip').Length / 1MB | ForEach-Object { '{0:N2} MB' -f $_ }"
echo.
echo This ZIP file can be uploaded to GitHub Releases
echo.
echo Next steps:
echo 1. Go to: https://github.com/YOUR_USERNAME/ak-auto-scanner/releases/new
echo 2. Create tag: v%VERSION%
echo 3. Upload: AKAutoScanner-v%VERSION%.zip
echo 4. Publish release
echo.
pause

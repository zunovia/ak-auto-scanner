@echo off
echo ========================================
echo GitHub Setup Script
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo Error: Git is not installed.
    echo Please download and install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Git is installed.
echo.

REM Initialize git repository if not already initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    git branch -M main
    echo.
) else (
    echo Git repository already initialized.
    echo.
)

REM Display current status
echo Current Git status:
git status
echo.

REM Prompt for GitHub username
set /p GITHUB_USER="Enter your GitHub username: "
if "%GITHUB_USER%"=="" (
    echo Error: GitHub username is required.
    pause
    exit /b 1
)

REM Prompt for repository name
set /p REPO_NAME="Enter repository name (default: ak-auto-scanner): "
if "%REPO_NAME%"=="" set REPO_NAME=ak-auto-scanner

echo.
echo ========================================
echo Configuration:
echo ========================================
echo GitHub User: %GITHUB_USER%
echo Repository: %REPO_NAME%
echo Remote URL: https://github.com/%GITHUB_USER%/%REPO_NAME%.git
echo.

set /p CONFIRM="Is this correct? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Setup cancelled.
    pause
    exit /b 0
)

echo.
echo ========================================
echo Setting up Git...
echo ========================================

REM Add all files
echo Adding files...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: AK Auto-Scanner v1.0.0" -m "- Python-based Kindle page scanner" -m "- Automatic page capture and PDF generation" -m "- GUI with configurable settings" -m "- Smart duplicate detection using SSIM" -m "- 5-second countdown before scan" -m "- Capture margin adjustment feature"

if errorlevel 1 (
    echo.
    echo Note: Commit may have failed if there are no changes.
    echo This is normal if you've already committed.
    echo.
)

REM Add remote
echo.
echo Adding remote repository...
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git 2>nul

if errorlevel 1 (
    echo Remote 'origin' already exists. Updating URL...
    git remote set-url origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Create a new repository on GitHub:
echo    https://github.com/new
echo    Repository name: %REPO_NAME%
echo    Do NOT initialize with README (we already have one)
echo.
echo 2. Push to GitHub:
echo    git push -u origin main
echo.
echo 3. You may be asked to authenticate:
echo    - Use your GitHub username
echo    - Use a Personal Access Token as password
echo      (Create at: https://github.com/settings/tokens)
echo.
echo Full instructions: See GITHUB_SETUP.md
echo.
pause

@echo off
:: SC Global.ini Extractor - Build Script
:: Clones repo from GitHub and builds the EXE

echo.
echo ======================================================================
echo SC Global.ini Extractor - Build Script
echo ======================================================================
echo.

:: Check for git
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Git not found!
    echo Please install Git from: https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

:: Check for Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Set variables
set REPO_URL=https://github.com/BeltaKoda/SC-GlobalIni-Extractor.git
set BRANCH=main
set BUILD_DIR=C:\SCGlobalINIExtractor_build_temp

echo.
echo Step 1: Getting repository...
echo.

:: Check if build_temp exists
if exist "%BUILD_DIR%\.git" (
    echo Found existing repository - updating...
    cd /d "%BUILD_DIR%"
    git checkout %BRANCH%
    git pull origin %BRANCH%
    if %ERRORLEVEL% neq 0 (
        echo.
        echo Git pull failed, trying fresh clone...
        cd ..
        rmdir /s /q "%BUILD_DIR%"
        git clone --branch %BRANCH% --single-branch %REPO_URL% "%BUILD_DIR%"
    )
) else (
    if exist "%BUILD_DIR%" (
        echo Removing invalid build directory...
        rmdir /s /q "%BUILD_DIR%"
    )
    echo Cloning repository...
    git clone --branch %BRANCH% --single-branch %REPO_URL% "%BUILD_DIR%"
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Git clone/pull failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Setting up Python environment...
echo.

cd /d "%BUILD_DIR%"

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)

:: Activate and install dependencies
echo Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

:: Check for unp4k.exe
if not exist "unp4k.exe" (
    echo.
    echo ERROR: unp4k.exe not found!
    echo.
    echo Please download unp4k from:
    echo https://github.com/dolkensp/unp4k/releases
    echo.
    echo Extract ALL files to:
    echo %BUILD_DIR%\
    echo.
    echo Required files:
    echo   - unp4k.exe
    echo   - ICSharpCode.SharpZipLib.dll
    echo   - Zstd.Net.dll
    echo   - x64\ folder
    echo   - x86\ folder
    echo.
    pause
    exit /b 1
)

echo.
echo Step 3: Building EXE with PyInstaller...
echo.

pyinstaller extract_tool.spec --clean --noconfirm

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: PyInstaller build failed!
    pause
    exit /b 1
)

if not exist "dist\SC_GlobalIni_Extractor.exe" (
    echo.
    echo ERROR: EXE not found after build!
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo BUILD COMPLETE!
echo ======================================================================
echo.
echo EXE Location: %BUILD_DIR%\dist\SC_GlobalIni_Extractor.exe
echo.
echo You can now run the EXE to extract global.ini files from Star Citizen!
echo.

:: Copy EXE to C:\SCGlobalINIExtractor\
set "OUTPUT_DIR=C:\SCGlobalINIExtractor"
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo Copying EXE to: %OUTPUT_DIR%
copy "%BUILD_DIR%\dist\SC_GlobalIni_Extractor.exe" "%OUTPUT_DIR%\" >nul

echo.
echo Cleaning up build files...
cd /d "C:\"
rmdir /s /q "%BUILD_DIR%"

echo.
echo ======================================================================
echo Final EXE Location: %OUTPUT_DIR%\SC_GlobalIni_Extractor.exe
echo ======================================================================
echo.

pause

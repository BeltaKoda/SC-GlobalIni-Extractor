# SC Global.ini Extractor - Build Instructions

This directory contains the source code and build tools for the SC Global.ini Extractor GUI application.

## 🎯 Quick Start (Automated Build)

The easiest way to build the EXE is using the automated build script:

```powershell
.\Build-SCIniTool.ps1
```

This will:
1. ✓ Clone the repository from GitHub (or update existing)
2. ✓ Set up Python virtual environment
3. ✓ Install dependencies
4. ✓ Build the EXE with PyInstaller
5. ✓ Create a release package

## 📋 Prerequisites

### Required
- **Windows 10/11**
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Required Tools (Manual Download)
- **unp4k.exe** - [Download from GitHub](https://github.com/dolkensp/unp4k/releases)
  - Download the latest `unp4k-suite-vX.X.X.zip`
  - Extract these files to the `tools/` directory:
    - `unp4k.exe`
    - `ICSharpCode.SharpZipLib.dll`
    - `Zstd.Net.dll`
    - `x64/` folder with `libzstd.dll`
    - `x86/` folder (if present)

## 🔨 Build Methods

### Method 1: Automated Build with Smart Updates (Recommended)

Run the build script from any directory:

```powershell
.\Build-SCIniTool.ps1
```

**How it works:**
- **First run:** Clones the repository to `build_temp/`
- **Subsequent runs:** Does `git pull` to update existing repo (much faster!)
- The script automatically detects if the repo exists and updates it

**Benefits:**
- ✓ Much faster for iterative testing
- ✓ Preserves build artifacts between runs
- ✓ Automatically gets latest changes from GitHub

### Method 2: Force Fresh Clone

If you want to completely start from scratch:

```powershell
.\Build-SCIniTool.ps1 -FreshClone
```

This will delete `build_temp/` and do a fresh clone. Useful if:
- The repo got corrupted
- You want to ensure a completely clean build
- Git pull is having issues

### Method 3: Build from Existing Clone

If you already have the repository cloned and want to build in-place:

```powershell
cd ScCompLangPackRemix/tools
.\Build-SCIniTool.ps1 -SkipClone
```

**Use this when:**
- You're actively developing and want to test local changes
- You don't want the script to touch git at all

### Method 4: Manual Build

1. **Clone the repository:**
   ```powershell
   git clone -b beta/extraction-tool https://github.com/BeltaKoda/ScCompLangPackRemix.git
   cd ScCompLangPackRemix/tools
   ```

2. **Download unp4k.exe and dependencies** (see Prerequisites above)

3. **Create virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Build with PyInstaller:**
   ```powershell
   pyinstaller extract_tool.spec --clean --noconfirm
   ```

6. **Find the EXE:**
   ```
   dist/SC_GlobalIni_Extractor.exe
   ```

## 📁 Project Structure

```
tools/
├── extract_tool.py          # Main Python GUI application
├── extract_tool.spec        # PyInstaller configuration
├── requirements.txt         # Python dependencies
├── build.ps1                # Automated build script
├── BUILD_README.md          # This file
│
├── unp4k.exe               # (Download separately)
├── *.dll                   # (Download with unp4k)
├── x64/                    # (Download with unp4k)
└── x86/                    # (Download with unp4k)
```

## 🎨 GUI Features

The built application includes:
- ✓ Modern dark theme UI with CustomTkinter
- ✓ Automatic detection of LIVE/PTU/EPTU/HOTFIX installations
- ✓ Interactive dropdown for installation selection
- ✓ Version input with validation
- ✓ Progress bar with status updates
- ✓ Error handling and user feedback
- ✓ Single EXE with no dependencies

## 🐛 Troubleshooting

### "Python not found"
- Install Python 3.8+ from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### "unp4k.exe not found during build"
- Download unp4k-suite from https://github.com/dolkensp/unp4k/releases
- Extract ALL files to the `tools/` directory (not just unp4k.exe)
- Required files: unp4k.exe, *.dll files, x64/ and x86/ folders

### "PyInstaller failed"
- Make sure you're running from an activated virtual environment
- Try deleting `build/` and `dist/` folders and rebuilding
- Check that all unp4k dependencies are present

### "Module not found" error
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

## 📦 Distribution

After building, the `release/` folder will contain:
- `SC_GlobalIni_Extractor.exe` - The application
- `README.txt` - User instructions

You can distribute this folder as a ZIP file to end users.

## 🔄 Updating the Tool

To build a new version:
1. Make changes to `extract_tool.py`
2. Commit and push to GitHub
3. Run `build.ps1` to create a new EXE

## 📝 Notes

- The EXE is a single-file bundle (no installation required)
- unp4k.exe and dependencies are embedded in the EXE
- The tool creates a temporary directory during extraction
- Extracted files are saved to `stock-global-ini/` relative to the EXE location

## 🙏 Credits

- **unp4k** - https://github.com/dolkensp/unp4k
- **CustomTkinter** - https://github.com/TomSchimansky/CustomTkinter
- **PyInstaller** - https://www.pyinstaller.org/

---

**Not affiliated with Cloud Imperium Games**

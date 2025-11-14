# SC Global.ini Extractor

A modern GUI tool for extracting the vanilla `global.ini` localization file from Star Citizen's `Data.p4k` archive.

**⚠️ BETA STATUS:** This tool is currently in beta testing.

---

## 🎯 For End Users

**Looking to just use the tool?** Download the pre-built EXE from the [Releases Page](https://github.com/BeltaKoda/SC-GlobalIni-Extractor/releases).

---

## 🎨 Tool Features

- ✅ Modern dark-themed GUI
- ✅ Auto-detects LIVE, PTU, EPTU, and HOTFIX installations
- ✅ Auto-detects game version from log files
- ✅ Interactive dropdown selection
- ✅ Custom output file picker with dynamic filenames
- ✅ Real-time progress updates
- ✅ Single EXE - no installation required
- ✅ Saves with versioned filenames (e.g., `StockGlobal-4-4-0-PTU.ini`)

---

## 🎮 Using the Tool

1. **Run the EXE:** `SC_GlobalIni_Extractor.exe`
2. **Select Installation:** Choose from detected installations (LIVE, PTU, EPTU, HOTFIX)
3. **Verify Version:** Version is auto-detected and pre-filled
4. **Choose Output Location:** Browse to select where to save the file (filename updates automatically)
5. **Extract:** Click "Extract global.ini" and wait 1-2 minutes
6. **Done!** File saved to your chosen location

### Output Files

Extracted files use this naming format:

```
StockGlobal-{VERSION}-{BRANCH}.ini
```

**Examples:**
- `StockGlobal-4-4-0-PTU.ini`
- `StockGlobal-4-3-2-LIVE.ini`
- `StockGlobal-4-4-1-EPTU.ini`

The filename updates automatically as you type the version or change the installation!

---

## 🔨 For Developers

### Building from Source

#### Prerequisites

**Required Software:**
- **Windows 10/11**
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)

**Required Tools:**
- **unp4k.exe** - [Download](https://github.com/dolkensp/unp4k/releases)
  - Download `unp4k-suite-vX.X.X.zip`
  - Extract ALL files to the repo root:
    - `unp4k.exe`
    - `ICSharpCode.SharpZipLib.dll`
    - `Zstd.Net.dll`
    - `x64/` folder
    - `x86/` folder

#### Option 1: Automated Build Script (Recommended)

```batch
Build-SCIniTool.bat
```

This script will:
1. Clone/update the repository from GitHub
2. Set up Python virtual environment
3. Install dependencies
4. Build the EXE with PyInstaller
5. Copy to `C:\SCGlobalINIExtractor\`

**See [BUILD_README.md](BUILD_README.md) for detailed build instructions.**

#### Option 2: Manual Build

```powershell
# Clone the repo
git clone https://github.com/BeltaKoda/SC-GlobalIni-Extractor.git
cd SC-GlobalIni-Extractor

# Download and extract unp4k suite to this directory

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Build EXE
pyinstaller extract_tool.spec --clean --noconfirm
```

The EXE will be in `dist/SC_GlobalIni_Extractor.exe`

---

## 📁 Project Structure

```
SC-GlobalIni-Extractor/
├── extract_tool.py          # Main GUI application source
├── extract_tool.spec        # PyInstaller build configuration
├── requirements.txt         # Python dependencies
├── Build-SCIniTool.bat      # Automated build script
├── BUILD_README.md          # Detailed build instructions
├── README.md                # This file
│
# Required for building (download separately):
├── unp4k.exe
├── ICSharpCode.SharpZipLib.dll
├── Zstd.Net.dll
├── x64/
│   └── libzstd.dll
└── x86/
    └── libzstd.dll
```

---

## 🐛 Troubleshooting

### End User Issues

#### "No Star Citizen installations found"
- Ensure Star Citizen is installed in a standard location
- Check common paths: `C:\Program Files\Roberts Space Industries\StarCitizen\`
- Try reinstalling Star Citizen if Data.p4k is missing

#### "Extraction timed out" or "Extraction failed"
- Close other applications to free up system resources
- Ensure Data.p4k is not corrupted (verify files in RSI Launcher)
- Try extracting from a different branch (LIVE vs PTU)
- Check that you have sufficient disk space

### Build Issues

#### "Python not found"
- Install Python 3.8+ from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

#### "unp4k.exe not found during build"
- Download complete unp4k-suite from https://github.com/dolkensp/unp4k/releases
- Extract ALL files to the repo root (not just unp4k.exe)
- Required: unp4k.exe, *.dll files, x64/ and x86/ folders

#### "PyInstaller failed"
- Ensure virtual environment is activated
- Delete `build/` and `dist/` folders and rebuild
- Verify all dependencies: `pip install -r requirements.txt`

**For detailed troubleshooting, see [BUILD_README.md](BUILD_README.md)**

---

## 💡 Use Cases

- **Language Pack Creators:** Extract vanilla global.ini to modify for custom language packs
- **Modders:** Access localization strings for SC mods
- **Data Miners:** Extract game text for analysis
- **Translators:** Create translations for Star Citizen

### Example Projects Using This Tool

- [ScCompLangPackRemix](https://github.com/BeltaKoda/ScCompLangPackRemix) - Compact component naming language pack

---

## 🙏 Credits

- **unp4k** - https://github.com/dolkensp/unp4k
- **CustomTkinter** - https://github.com/TomSchimansky/CustomTkinter
- **PyInstaller** - https://www.pyinstaller.org/
- **Star Citizen** - Cloud Imperium Games

**Not affiliated with or endorsed by Cloud Imperium Games**

---

## 📄 License

This project is provided as-is for the Star Citizen community. Feel free to fork, modify, and improve!

Star Citizen®, Roberts Space Industries® and Cloud Imperium® are registered trademarks of Cloud Imperium Rights LLC.

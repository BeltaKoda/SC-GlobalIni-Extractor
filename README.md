# SC Global.ini Extractor

A modern GUI tool for extracting the vanilla `global.ini` localization file from Star Citizen's `Data.p4k` archive.

![GitHub Release](https://img.shields.io/github/v/release/BeltaKoda/SC-GlobalIni-Extractor?style=flat-square)
![GitHub Downloads](https://img.shields.io/github/downloads/BeltaKoda/SC-GlobalIni-Extractor/total?style=flat-square)

---

## 📦 Download

**👉 [Download Latest Release](https://github.com/BeltaKoda/SC-GlobalIni-Extractor/releases/latest)**

Download `SC_GlobalIni_Extractor.exe` - No installation required!

### Why Download from GitHub Releases?

- ✅ **Built automatically** by GitHub Actions (not on a local PC)
- ✅ **Transparent build process** - All build logs are public and auditable
- ✅ **Verified source** - Built from the exact tagged commit
- ✅ **Safe and trustworthy** - No need to trust a random EXE from someone's computer

Every release shows which commit it was built from, and you can review the build logs to verify the EXE matches the source code.

---

## 🎨 Features

- ✅ **Modern dark-themed GUI** - Clean and professional interface
- ✅ **Auto-detects installations** - Finds LIVE, PTU, EPTU, and HOTFIX
- ✅ **Auto-detects version** - Reads version from Star Citizen log files
- ✅ **Dynamic filenames** - Filename updates as you type
- ✅ **Custom output location** - Save anywhere with "Save As" dialog
- ✅ **Real-time progress** - See extraction progress with status updates
- ✅ **Single EXE** - No installation, no dependencies to manage
- ✅ **Versioned output** - Files saved as `StockGlobal-{VERSION}-{BRANCH}.ini`

---

## 🎮 How to Use

1. **Download** `SC_GlobalIni_Extractor.exe` from [Releases](https://github.com/BeltaKoda/SC-GlobalIni-Extractor/releases/latest)
2. **Run the EXE** - Double-click to launch (no installation needed)
3. **Select Installation** - Tool auto-detects your SC installations
4. **Verify Version** - Version is auto-filled from game logs
5. **Choose Output** - Browse to select where to save (filename updates automatically)
6. **Extract** - Click "Extract global.ini" and wait 1-2 minutes
7. **Done!** - File saved to your chosen location

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

## 💡 Use Cases

- **Language Pack Creators** - Extract vanilla global.ini to create custom language packs
- **Modders** - Access localization strings for Star Citizen mods
- **Data Miners** - Extract game text for analysis and documentation
- **Translators** - Create translations for the Star Citizen community

### Example Projects

- [ScCompLangPackRemix](https://github.com/BeltaKoda/ScCompLangPackRemix) - Compact component naming language pack created with this tool

---

## 🐛 Troubleshooting

### "No Star Citizen installations found"
- Ensure Star Citizen is installed in a standard location
- Check common paths: `C:\Program Files\Roberts Space Industries\StarCitizen\`
- Verify `Data.p4k` exists in your installation's LIVE/PTU/EPTU folder

### "Extraction timed out" or "Extraction failed"
- Close other applications to free up system resources
- Verify files in RSI Launcher (ensures Data.p4k isn't corrupted)
- Try extracting from a different branch (LIVE vs PTU)
- Ensure you have sufficient disk space (extraction needs ~2GB temp space)

### Windows SmartScreen Warning
- This is normal for unsigned applications
- Click "More info" → "Run anyway"
- The EXE is built by GitHub Actions - you can verify the build logs are clean

---

## 🔨 For Developers

Want to build from source or contribute? See below!

### Building Locally

#### Prerequisites

**Required Software:**
- **Windows 10/11**
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)

**Required Dependencies:**
- **unp4k.exe** - [Download](https://github.com/dolkensp/unp4k/releases)
  - Download `unp4k-suite-vX.X.X.zip`
  - Extract ALL files to the repo root:
    - `unp4k.exe`
    - `ICSharpCode.SharpZipLib.dll`
    - `Zstd.Net.dll`
    - `x64/` folder
    - `x86/` folder

#### Option 1: Automated Local Build (Quick)

```batch
Build-Local.bat
```

This script will:
1. Clone/update the repository from GitHub
2. Set up Python virtual environment
3. Install dependencies
4. Build the EXE with PyInstaller
5. Copy to `C:\SCGlobalINIExtractor\`

**Note:** This is for local development only. End users should download from GitHub Releases.

#### Option 2: Manual Build (Full Control)

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

**See [BUILD_README.md](BUILD_README.md) for detailed build instructions.**

### GitHub Actions Workflow

This project uses GitHub Actions to automatically build and release the EXE:

- **Trigger:** Push a tag like `v1.0.0`
- **Build:** GitHub Actions builds the EXE on Windows Server
- **Release:** Automatically creates a GitHub Release with the EXE attached
- **Transparency:** All build logs are public and auditable

**Workflow file:** [`.github/workflows/build-release.yml`](.github/workflows/build-release.yml)

This ensures users get a trusted build from a transparent, auditable process instead of downloading an EXE built on someone's local machine.

---

## 📁 Project Structure

```
SC-GlobalIni-Extractor/
├── .github/
│   └── workflows/
│       └── build-release.yml     # GitHub Actions workflow for releases
├── extract_tool.py               # Main GUI application source
├── extract_tool.spec             # PyInstaller build configuration
├── requirements.txt              # Python dependencies
├── Build-Local.bat               # Local build script (for developers)
├── BUILD_README.md               # Detailed build documentation
├── README.md                     # This file
└── .gitignore                    # Git ignore rules

# Not tracked in git (download separately for local builds):
├── unp4k.exe
├── ICSharpCode.SharpZipLib.dll
├── Zstd.Net.dll
├── x64/
│   └── libzstd.dll
└── x86/
    └── libzstd.dll
```

---

## 🙏 Credits

- **unp4k** - https://github.com/dolkensp/unp4k - Tool for extracting Star Citizen .p4k archives
- **CustomTkinter** - https://github.com/TomSchimansky/CustomTkinter - Modern GUI framework
- **PyInstaller** - https://www.pyinstaller.org/ - Python to EXE bundler
- **Star Citizen** - Cloud Imperium Games - The game this tool supports

---

## 📄 License

This project is provided as-is for the Star Citizen community. Feel free to fork, modify, and improve!

Star Citizen®, Roberts Space Industries® and Cloud Imperium® are registered trademarks of Cloud Imperium Rights LLC.

**Not affiliated with or endorsed by Cloud Imperium Games**

---

## ⭐ Support

If this tool helped you, consider:
- ⭐ Starring the repo
- 🐛 Reporting bugs in [Issues](https://github.com/BeltaKoda/SC-GlobalIni-Extractor/issues)
- 🔀 Contributing improvements via Pull Requests
- 📢 Sharing with other language pack creators!

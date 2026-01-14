# SC Global.ini Extractor

A modern GUI tool for extracting the vanilla `global.ini` localization file from Star Citizen's `Data.p4k` archive.

![GitHub Release](https://img.shields.io/github/v/release/BeltaKoda/SC-GlobalIni-Extractor?style=flat-square)
![GitHub Downloads](https://img.shields.io/github/downloads/BeltaKoda/SC-GlobalIni-Extractor/total?style=flat-square)

---

## 📦 Download

**👉 [Download Latest Release](https://github.com/BeltaKoda/SC-GlobalIni-Extractor/releases/latest)**

Download `SC_GlobalIni_Extractor.exe` - No installation required!

*Built automatically by GitHub Actions from source code. All build logs are public and auditable.*

---

## 🎨 Features

- Modern dark-themed GUI
- Auto-detects LIVE, PTU, EPTU, and HOTFIX installations
- Supports custom installation paths
- Auto-detects game version from log files
- Dynamic filename generation
- Custom output file picker
- Real-time progress updates
- Single EXE - no installation required

---

## 🎮 How to Use

1. Download `SC_GlobalIni_Extractor.exe` from [Releases](https://github.com/BeltaKoda/SC-GlobalIni-Extractor/releases/latest)
2. Run the EXE
3. Select your Star Citizen installation
   - *Note: If your installation isn't detected, check "Use custom installation path" and browse to your StarCitizen folder.*
4. Verify the auto-detected version
5. Choose where to save the file
6. Click "Extract global.ini"

### Download via PowerShell (Windows)

You can also download the latest release directly using PowerShell:

```powershell
Invoke-WebRequest -Uri "https://github.com/BeltaKoda/SC-GlobalIni-Extractor/releases/latest/download/SC_GlobalIni_Extractor.exe" -OutFile "SC_GlobalIni_Extractor.exe"
```

This downloads the latest release EXE to your current directory.

### Output Files

Extracted files use this naming format: `StockGlobal-{VERSION}-{BRANCH}.ini`

**Examples:**
- `StockGlobal-4-4-0-PTU.ini`
- `StockGlobal-4-3-2-LIVE.ini`
- `StockGlobal-4-4-1-EPTU.ini`

---

## 💡 Use Cases

- **Language Pack Creators** - Extract vanilla global.ini to create custom language packs

### Example Project

- [ScCompLangPackRemix](https://github.com/BeltaKoda/ScCompLangPackRemix) - Compact component naming language pack created with this tool

---

## 🐛 Troubleshooting

This EXE is compiled automatically by GitHub Actions. If you have concerns about the file:

1. **View the build logs** - Click on the [workflow run](https://github.com/BeltaKoda/SC-GlobalIni-Extractor/actions) for your downloaded release to see exactly how it was built
2. **Verify the checksum** - Download the EXE and compare its SHA256 hash against what GitHub reports

**Windows SmartScreen warning?** This is normal for unsigned applications. Click "More info" → "Run anyway"

---

## 🔨 For Developers

### Building Locally

#### Prerequisites

**Required Software:**
- Windows 10/11
- Python 3.8+ - [Download](https://www.python.org/downloads/)
- Git - [Download](https://git-scm.com/downloads)

**Required Dependencies:**
- unp4k.exe - [Download](https://github.com/dolkensp/unp4k/releases)
  - Download `unp4k-suite-vX.X.X.zip`
  - Extract ALL files to the repo root

#### Quick Build

```batch
Build-Local.bat
```

Or manually:

```powershell
git clone https://github.com/BeltaKoda/SC-GlobalIni-Extractor.git
cd SC-GlobalIni-Extractor

# Download and extract unp4k suite to this directory

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pyinstaller extract_tool.spec --clean --noconfirm
```

The EXE will be in `dist/SC_GlobalIni_Extractor.exe`

### GitHub Actions Workflow

This project uses GitHub Actions to automatically build and release the EXE when you push a version tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will:
- Build the EXE on Windows Server
- Create a GitHub Release
- Attach the EXE as a download

All build logs are public: [View Workflow Runs](https://github.com/BeltaKoda/SC-GlobalIni-Extractor/actions)

---

## 🙏 Credits

- **unp4k** - https://github.com/dolkensp/unp4k
- **CustomTkinter** - https://github.com/TomSchimansky/CustomTkinter
- **PyInstaller** - https://www.pyinstaller.org/

---

## 📄 License

This project is provided as-is for the Star Citizen community. Feel free to fork, modify, and improve!

Star Citizen®, Roberts Space Industries® and Cloud Imperium® are registered trademarks of Cloud Imperium Rights LLC.

**Not affiliated with or endorsed by Cloud Imperium Games**

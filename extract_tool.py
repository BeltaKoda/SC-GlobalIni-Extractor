"""
Star Citizen Global.ini Extractor
Modern GUI tool for extracting global.ini from Star Citizen installations
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import shutil
import threading
from pathlib import Path
import sys
import os
import re

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SCExtractorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("SC Global.ini Extractor")
        self.geometry("900x600")
        self.resizable(True, True)

        # Get resource directory (for bundled files like unp4k.exe)
        if getattr(sys, 'frozen', False):
            # Running as compiled EXE - use PyInstaller's temp folder for resources
            self.resource_dir = Path(sys._MEIPASS)
            # EXE location for output files
            self.exe_dir = Path(sys.executable).parent
        else:
            # Running as .py script
            self.resource_dir = Path(__file__).parent
            self.exe_dir = Path(__file__).parent

        # Initialize variables
        self.installations = []
        self.selected_installation = None
        self.extracting = False
        self.output_file = None

        # Configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Build UI
        self.create_sidebar()
        self.create_main_area()

        # Auto-scan for installations
        self.after(100, self.scan_installations)

    def create_sidebar(self):
        """Create the sidebar with logo and info"""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Title / Logo area
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="SC Global.ini\nExtractor", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Description
        self.desc_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Extract the vanilla\nglobal.ini file from\nStar Citizen for\ntranslation or modding.",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        )
        self.desc_label.grid(row=1, column=0, padx=20, pady=10)

        # Theme switch (optional, keeping it simple for now)
        # appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        # appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        # appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
        #                                                 command=self.change_appearance_mode_event)
        # appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Footer
        self.footer_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="v1.1.0\n© BeltaKoda",
            font=ctk.CTkFont(size=10),
            text_color="gray50"
        )
        self.footer_label.grid(row=5, column=0, padx=20, pady=20, sticky="s")

    def create_main_area(self):
        """Create the main content area"""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # --- Installation Section ---
        self.inst_frame = ctk.CTkFrame(self.main_frame)
        self.inst_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            self.inst_frame, 
            text="1. Select Installation", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.installation_dropdown = ctk.CTkComboBox(
            self.inst_frame,
            width=400,
            height=35,
            state="disabled",
            command=self._on_installation_changed
        )
        self.installation_dropdown.pack(padx=15, pady=(0, 15), fill="x")

        # --- Version Section ---
        self.ver_frame = ctk.CTkFrame(self.main_frame)
        self.ver_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            self.ver_frame, 
            text="2. Verify Version", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.version_entry = ctk.CTkEntry(
            self.ver_frame,
            placeholder_text="e.g., 3.24.0",
            height=35
        )
        self.version_entry.pack(padx=15, pady=(0, 15), fill="x")
        self.version_entry.bind("<KeyRelease>", lambda e: self.update_output_filename())

        # --- Output Section ---
        self.out_frame = ctk.CTkFrame(self.main_frame)
        self.out_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            self.out_frame, 
            text="3. Output Location", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        out_inner = ctk.CTkFrame(self.out_frame, fg_color="transparent")
        out_inner.pack(fill="x", padx=15, pady=(0, 15))

        self.output_entry = ctk.CTkEntry(out_inner, height=35)
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            out_inner, 
            text="Browse", 
            width=100, 
            height=35,
            command=self.browse_output_file
        )
        self.browse_btn.pack(side="right")

        # --- Action Section ---
        self.action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.action_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.status_label = ctk.CTkLabel(
            self.action_frame, 
            text="Initializing...", 
            text_color="gray"
        )
        self.status_label.pack(pady=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(self.action_frame)
        self.progress_bar.pack(fill="x", pady=(0, 20))
        self.progress_bar.set(0)

        self.extract_button = ctk.CTkButton(
            self.action_frame,
            text="EXTRACT GLOBAL.INI",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color="#2CC985",
            text_color="white",
            hover_color="#229e68",
            state="disabled",
            command=self.start_extraction
        )
        self.extract_button.pack(fill="x", side="bottom")

    def scan_installations(self):
        """Scan for Star Citizen installations"""
        self.status_label.configure(text="Scanning for Star Citizen installations...")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
        # Run scan in background thread
        thread = threading.Thread(target=self._scan_thread, daemon=True)
        thread.start()

    def _scan_thread(self):
        """Background thread for scanning"""
        installations = self.find_installations()
        # Update UI on main thread
        self.after(0, lambda: self._scan_complete(installations))

    def detect_version(self, installation_path):
        """Detect Star Citizen version from log files"""
        try:
            branch_folder = Path(installation_path).parent
            # Try Game.log first
            game_log = branch_folder / "Game.log"
            if game_log.exists():
                version = self._extract_version_from_log(game_log)
                if version: return version

            # Try logbackups folder
            logbackups = branch_folder / "logbackups"
            if logbackups.exists():
                log_files = list(logbackups.glob("Game*.log"))
                if log_files:
                    latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
                    version = self._extract_version_from_log(latest_log)
                    if version: return version
        except Exception:
            pass
        return None

    def _extract_version_from_log(self, log_path):
        """Extract version number from log file"""
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                for _ in range(200):
                    line = f.readline()
                    if not line: break
                    
                    # Pattern 1: "GameVersion: 4.4.0-PTU.12345"
                    match = re.search(r'GameVersion[:\s]+(\d+\.\d+\.?\d*)', line, re.IGNORECASE)
                    if match: return match.group(1)

                    # Pattern 2: "Version 4.4.0" or "v4.4.0"
                    match = re.search(r'Version\s+v?(\d+\.\d+\.?\d*)', line, re.IGNORECASE)
                    if match:
                        version = match.group(1)
                        if version.startswith(('3.', '4.')): return version

                    # Pattern 3: "Star Citizen Alpha 4.4.0"
                    match = re.search(r'Star Citizen Alpha\s+(\d+\.\d+\.?\d*)', line, re.IGNORECASE)
                    if match: return match.group(1)
        except Exception:
            pass
        return None

    def find_installations(self):
        """Find all Star Citizen installations"""
        installations = []
        common_roots = [
            r"C:\Program Files\Roberts Space Industries\StarCitizen",
            r"D:\Program Files\Roberts Space Industries\StarCitizen",
            r"E:\Program Files\Roberts Space Industries\StarCitizen",
            r"F:\Program Files\Roberts Space Industries\StarCitizen",
            r"C:\Games\Roberts Space Industries\StarCitizen",
            r"D:\Games\Roberts Space Industries\StarCitizen",
            r"E:\Games\Roberts Space Industries\StarCitizen",
            r"F:\Games\Roberts Space Industries\StarCitizen",
            r"C:\RSI\StarCitizen",
            r"D:\RSI\StarCitizen",
            r"E:\RSI\StarCitizen",
            r"F:\RSI\StarCitizen"
        ]
        branches = ["LIVE", "PTU", "EPTU", "HOTFIX", "TECH-PREVIEW"]

        for root in common_roots:
            root_path = Path(root)
            if root_path.exists():
                for branch in branches:
                    data_p4k = root_path / branch / "Data.p4k"
                    if data_p4k.exists():
                        detected_version = self.detect_version(str(data_p4k))
                        # Show version if detected, otherwise just show branch name
                        display_text = f"{branch} ({detected_version})" if detected_version else branch
                        installations.append({
                            "branch": branch,
                            "path": str(data_p4k),
                            "display": display_text,
                            "version": detected_version
                        })
        return installations

    def _on_installation_changed(self, selection):
        """Called when installation dropdown selection changes"""
        # Find the selected installation
        # Note: This assumes unique display strings, which is mostly true but could be better
        for inst in self.installations:
            if inst["display"] == selection:
                self.selected_installation = inst
                if inst.get("version"):
                    self.version_entry.delete(0, "end")
                    self.version_entry.insert(0, inst["version"])
                break
        
        self.update_output_filename()

    def generate_filename(self):
        """Generate filename based on version and branch"""
        version = self.version_entry.get().strip()
        branch = "LIVE"
        if self.selected_installation:
            branch = self.selected_installation["branch"]
            
        version_formatted = version.replace(".", "-") if version else "0-0-0"
        return f"StockGlobal-{version_formatted}-{branch}.ini"

    def update_output_filename(self):
        """Update the output entry with new filename based on current inputs"""
        current_path = self.output_entry.get().strip()
        if current_path and Path(current_path).parent.exists():
            output_dir = Path(current_path).parent
        else:
            output_dir = self.exe_dir

        filename = self.generate_filename()
        new_path = output_dir / filename
        
        self.output_entry.delete(0, "end")
        self.output_entry.insert(0, str(new_path))
        self.output_file = new_path

    def browse_output_file(self):
        """Open file save dialog for output location"""
        filename = self.generate_filename()
        current_path = self.output_entry.get()
        initial_dir = str(Path(current_path).parent) if current_path else str(self.exe_dir)

        selected_file = filedialog.asksaveasfilename(
            title="Save extracted global.ini as",
            initialdir=initial_dir,
            initialfile=filename,
            defaultextension=".ini",
            filetypes=[("INI Files", "*.ini"), ("All Files", "*.*")]
        )

        if selected_file:
            self.output_file = Path(selected_file)
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, selected_file)

    def _scan_complete(self, installations):
        """Called when scan is complete"""
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        
        self.installations = installations

        if not installations:
            self.status_label.configure(text="No Star Citizen installations found", text_color="#FF5555")
            messagebox.showerror("No Installations", "Could not find any Star Citizen installations.")
            return

        self.status_label.configure(text=f"Found {len(installations)} installation(s)", text_color="gray")
        
        display_values = [inst["display"] for inst in installations]
        self.installation_dropdown.configure(values=display_values, state="readonly")
        self.installation_dropdown.set(display_values[0])
        
        # Trigger selection logic for the first item
        self._on_installation_changed(display_values[0])
        
        self.extract_button.configure(state="normal")

    def start_extraction(self):
        """Start the extraction process"""
        if self.extracting: return

        # Validate inputs
        if not self.selected_installation:
            messagebox.showerror("Error", "Please select an installation.")
            return

        version = self.version_entry.get().strip()
        if not version:
            messagebox.showerror("Error", "Please enter a version number.")
            return

        output_path = self.output_entry.get().strip()
        if not output_path:
            messagebox.showerror("Error", "Please select an output location.")
            return

        # Check for unp4k.exe
        unp4k_path = self.resource_dir / "unp4k.exe"
        if not unp4k_path.exists():
            messagebox.showerror("Error", f"unp4k.exe not found in {self.resource_dir}")
            return

        # UI State Update
        self.extracting = True
        self.extract_button.configure(state="disabled", text="EXTRACTING...")
        self.installation_dropdown.configure(state="disabled")
        self.version_entry.configure(state="disabled")
        self.output_entry.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Preparing extraction...", text_color="#3B8ED0")

        # Run in background
        thread = threading.Thread(target=self._extract_thread, args=(version,), daemon=True)
        thread.start()

    def _extract_thread(self, version):
        """Background thread for extraction"""
        try:
            self.after(0, lambda: self.progress_bar.set(0.1))
            
            # Create temp directory
            temp_dir = Path(os.environ['TEMP']) / "sc_extract_temp"
            if temp_dir.exists(): shutil.rmtree(temp_dir, ignore_errors=True)
            temp_dir.mkdir(parents=True, exist_ok=True)

            # Copy tools
            self.after(0, lambda: self.status_label.configure(text="Setting up tools..."))
            shutil.copy2(self.resource_dir / "unp4k.exe", temp_dir / "unp4k.exe")
            for dll in self.resource_dir.glob("*.dll"):
                shutil.copy2(dll, temp_dir / dll.name)
            
            # Copy arch dirs
            for arch in ["x64", "x86"]:
                src = self.resource_dir / arch
                if src.exists():
                    dst = temp_dir / arch
                    if dst.exists(): shutil.rmtree(dst)
                    shutil.copytree(src, dst)

            self.after(0, lambda: self.progress_bar.set(0.3))
            self.after(0, lambda: self.status_label.configure(text="Extracting (this may take a minute)..."))

            # Run unp4k
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            result = subprocess.run(
                [str(temp_dir / "unp4k.exe"), self.selected_installation["path"], "Data/Localization/english/global.ini"],
                cwd=temp_dir,
                capture_output=True,
                timeout=300,
                startupinfo=startupinfo
            )

            if result.returncode != 0:
                raise Exception(f"Extraction failed: {result.stderr.decode()}")

            self.after(0, lambda: self.progress_bar.set(0.8))
            
            # Find and save file
            extracted = list(temp_dir.rglob("global.ini"))
            if not extracted: raise Exception("global.ini not found in extracted files")
            
            self.after(0, lambda: self.status_label.configure(text="Saving file..."))
            shutil.copy2(extracted[0], self.output_file)
            
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            self.after(0, lambda: self._extraction_complete(True))

        except Exception as e:
            self.after(0, lambda: self._extraction_complete(False, str(e)))

    def _extraction_complete(self, success, error_msg=None):
        """Called when extraction finishes"""
        self.extracting = False
        self.extract_button.configure(state="normal", text="EXTRACT GLOBAL.INI")
        self.installation_dropdown.configure(state="readonly")
        self.version_entry.configure(state="normal")
        self.output_entry.configure(state="normal")

        if success:
            self.progress_bar.set(1.0)
            self.status_label.configure(text="Extraction Complete!", text_color="#2CC985")
            messagebox.showinfo("Success", f"File saved to:\n{self.output_file}")
        else:
            self.progress_bar.set(0)
            self.status_label.configure(text="Extraction Failed", text_color="#FF5555")
            messagebox.showerror("Error", f"Failed:\n{error_msg}")

def main():
    app = SCExtractorApp()
    app.mainloop()

if __name__ == "__main__":
    main()

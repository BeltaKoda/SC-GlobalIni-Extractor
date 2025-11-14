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
        self.geometry("700x750")
        self.resizable(False, False)

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
        self.output_file = None  # Will be set after UI is built

        # Build UI
        self.create_widgets()

        # Auto-scan for installations
        self.after(100, self.scan_installations)

    def create_widgets(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Star Citizen Global.ini Extractor",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 5))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Extract vanilla global.ini from your Star Citizen installation",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 20))

        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Status section
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Scanning for installations...",
            font=ctk.CTkFont(size=13)
        )
        self.status_label.pack(pady=(20, 10))

        # Installation selection
        installation_frame = ctk.CTkFrame(main_frame)
        installation_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            installation_frame,
            text="Installation:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.installation_dropdown = ctk.CTkComboBox(
            installation_frame,
            width=600,
            height=35,
            font=ctk.CTkFont(size=12),
            state="disabled",
            command=self._on_installation_changed
        )
        self.installation_dropdown.pack(padx=10, pady=(0, 10))

        # Version input
        version_frame = ctk.CTkFrame(main_frame)
        version_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            version_frame,
            text="Version:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            version_frame,
            text="Enter the Star Citizen version (e.g., 4.3.2)",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w", padx=10)

        self.version_entry = ctk.CTkEntry(
            version_frame,
            width=600,
            height=35,
            font=ctk.CTkFont(size=12),
            placeholder_text="e.g., 4.3.2"
        )
        self.version_entry.pack(padx=10, pady=(5, 10))
        # Bind version entry changes to update filename
        self.version_entry.bind("<KeyRelease>", lambda e: self.update_output_filename())

        # Output file selection
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            output_frame,
            text="Output File:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            output_frame,
            text="Full path and filename for the extracted global.ini",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w", padx=10)

        # Output path container (entry + button)
        output_path_container = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_path_container.pack(padx=10, pady=(5, 10), fill="x")

        self.output_entry = ctk.CTkEntry(
            output_path_container,
            width=480,
            height=35,
            font=ctk.CTkFont(size=11),
        )
        self.output_entry.pack(side="left", padx=(0, 10))
        # Initial value will be set after building default filename

        browse_button = ctk.CTkButton(
            output_path_container,
            text="Browse...",
            width=100,
            height=35,
            command=self.browse_output_file,
            font=ctk.CTkFont(size=12)
        )
        browse_button.pack(side="left")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=600)
        self.progress_bar.pack(pady=20, padx=20)
        self.progress_bar.set(0)

        # Progress label
        self.progress_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.progress_label.pack()

        # Extract button
        self.extract_button = ctk.CTkButton(
            main_frame,
            text="Extract global.ini",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=300,
            height=50,
            command=self.start_extraction,
            state="disabled",
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        self.extract_button.pack(pady=30)

        # Footer
        footer_label = ctk.CTkLabel(
            self,
            text="© BeltaKoda | Not affiliated with Cloud Imperium Games",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        footer_label.pack(side="bottom", pady=10)

    def scan_installations(self):
        """Scan for Star Citizen installations"""
        self.status_label.configure(text="Scanning for installations...")
        self.progress_bar.set(0)

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
            # Get the branch folder (parent of Data.p4k)
            branch_folder = Path(installation_path).parent

            # Try Game.log first
            game_log = branch_folder / "Game.log"
            if game_log.exists():
                version = self._extract_version_from_log(game_log)
                if version:
                    return version

            # Try logbackups folder
            logbackups = branch_folder / "logbackups"
            if logbackups.exists():
                # Get most recent log file
                log_files = list(logbackups.glob("Game*.log"))
                if log_files:
                    # Sort by modification time, get most recent
                    latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
                    version = self._extract_version_from_log(latest_log)
                    if version:
                        return version

        except Exception:
            pass

        return None

    def _extract_version_from_log(self, log_path):
        """Extract version number from log file"""
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Read first 200 lines (version info is usually at the start)
                for _ in range(200):
                    line = f.readline()
                    if not line:
                        break

                    # Look for specific Star Citizen version patterns
                    # Pattern 1: "GameVersion: 4.4.0-PTU.12345"
                    match = re.search(r'GameVersion[:\s]+(\d+\.\d+\.?\d*)', line, re.IGNORECASE)
                    if match:
                        return match.group(1)

                    # Pattern 2: "Version 4.4.0" or "v4.4.0"
                    match = re.search(r'Version\s+v?(\d+\.\d+\.?\d*)', line, re.IGNORECASE)
                    if match:
                        version = match.group(1)
                        # Must start with 3 or 4 (Star Citizen major versions)
                        if version.startswith(('3.', '4.')):
                            return version

                    # Pattern 3: "Star Citizen Alpha 4.4.0"
                    match = re.search(r'Star Citizen Alpha\s+(\d+\.\d+\.?\d*)', line, re.IGNORECASE)
                    if match:
                        return match.group(1)

        except Exception:
            pass

        return None

    def find_installations(self):
        """Find all Star Citizen installations"""
        installations = []

        # Common root paths
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

        # Branches to check
        branches = ["LIVE", "PTU", "EPTU", "HOTFIX"]

        for root in common_roots:
            root_path = Path(root)
            if root_path.exists():
                for branch in branches:
                    data_p4k = root_path / branch / "Data.p4k"
                    if data_p4k.exists():
                        # Try to detect version
                        detected_version = self.detect_version(str(data_p4k))

                        installations.append({
                            "branch": branch,
                            "path": str(data_p4k),
                            "display": f"{branch} - {data_p4k}",
                            "version": detected_version
                        })

        return installations

    def _on_installation_changed(self, selection):
        """Called when installation dropdown selection changes"""
        # Find the selected installation and auto-fill version if detected
        selected_index = self.installation_dropdown.cget("values").index(selection)
        installation = self.installations[selected_index]

        if installation.get("version"):
            self.version_entry.delete(0, "end")
            self.version_entry.insert(0, installation["version"])

        # Update output filename with new branch
        self.update_output_filename()

    def generate_filename(self):
        """Generate filename based on version and branch"""
        version = self.version_entry.get().strip()

        # Get branch from selected installation
        branch = "LIVE"  # Default
        if self.installation_dropdown.get():
            try:
                selected_index = self.installation_dropdown.cget("values").index(
                    self.installation_dropdown.get()
                )
                branch = self.installations[selected_index]["branch"]
            except (ValueError, IndexError, KeyError):
                pass

        # Convert version dots to dashes (4.4.0 -> 4-4-0)
        version_formatted = version.replace(".", "-") if version else "0-0-0"

        return f"StockGlobal-{version_formatted}-{branch}.ini"

    def update_output_filename(self):
        """Update the output entry with new filename based on current inputs"""
        # Get current path to preserve directory
        current_path = self.output_entry.get().strip()

        if current_path and Path(current_path).parent.exists():
            # Keep existing directory, update filename
            output_dir = Path(current_path).parent
        else:
            # Use default directory
            output_dir = self.exe_dir

        filename = self.generate_filename()
        new_path = output_dir / filename

        self.output_entry.delete(0, "end")
        self.output_entry.insert(0, str(new_path))
        self.output_file = new_path

    def browse_output_file(self):
        """Open file save dialog for output location"""
        # Get suggested filename
        filename = self.generate_filename()

        # Get initial directory from current path
        current_path = self.output_entry.get()
        if current_path and Path(current_path).parent.exists():
            initial_dir = str(Path(current_path).parent)
        else:
            initial_dir = str(self.exe_dir)

        # Open file save dialog
        selected_file = filedialog.asksaveasfilename(
            title="Save extracted global.ini as",
            initialdir=initial_dir,
            initialfile=filename,
            defaultextension=".ini",
            filetypes=[
                ("INI Files", "*.ini"),
                ("All Files", "*.*")
            ]
        )

        # Update entry if user selected a file
        if selected_file:
            self.output_file = Path(selected_file)
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, selected_file)

    def _scan_complete(self, installations):
        """Called when scan is complete"""
        self.installations = installations

        if not installations:
            self.status_label.configure(
                text="❌ No Star Citizen installations found",
                text_color="red"
            )
            messagebox.showerror(
                "No Installations Found",
                "Could not find any Star Citizen installations.\n\n"
                "Please ensure Star Citizen is installed in a standard location."
            )
            return

        # Update dropdown
        self.status_label.configure(
            text=f"✓ Found {len(installations)} installation(s)",
            text_color="green"
        )

        display_values = [inst["display"] for inst in installations]
        self.installation_dropdown.configure(
            values=display_values,
            state="readonly"
        )
        self.installation_dropdown.set(display_values[0])
        self.extract_button.configure(state="normal")

        # Auto-populate version if detected
        if installations[0].get("version"):
            self.version_entry.delete(0, "end")
            self.version_entry.insert(0, installations[0]["version"])

        # Initialize default output filename
        self.update_output_filename()

    def start_extraction(self):
        """Start the extraction process"""
        if self.extracting:
            return

        # Validate inputs
        selected_index = self.installation_dropdown.cget("values").index(
            self.installation_dropdown.get()
        )
        self.selected_installation = self.installations[selected_index]

        version = self.version_entry.get().strip()
        if not version:
            messagebox.showerror("Version Required", "Please enter a version number")
            return

        # Basic version validation
        if not all(c.isdigit() or c == '.' for c in version):
            messagebox.showerror(
                "Invalid Version",
                "Version should be in format X.X.X (e.g., 4.3.2)"
            )
            return

        # Validate output file path
        output_path = self.output_entry.get().strip()
        if not output_path:
            messagebox.showerror(
                "Output File Required",
                "Please select an output file location"
            )
            return

        try:
            self.output_file = Path(output_path)
            # Ensure parent directory exists
            self.output_file.parent.mkdir(parents=True, exist_ok=True)

            # Validate filename
            if not self.output_file.suffix:
                self.output_file = self.output_file.with_suffix(".ini")
        except Exception as e:
            messagebox.showerror(
                "Invalid Output File",
                f"Cannot use output file path:\n{output_path}\n\nError: {str(e)}"
            )
            return

        # Check for unp4k.exe
        unp4k_path = self.resource_dir / "unp4k.exe"
        if not unp4k_path.exists():
            messagebox.showerror(
                "unp4k.exe Not Found",
                f"Could not find unp4k.exe in:\n{self.resource_dir}\n\n"
                "This should be bundled with the EXE.\n"
                "Please rebuild the tool or download unp4k from:\n"
                "https://github.com/dolkensp/unp4k/releases"
            )
            return

        # Disable UI
        self.extracting = True
        self.extract_button.configure(state="disabled")
        self.installation_dropdown.configure(state="disabled")
        self.version_entry.configure(state="disabled")
        self.output_entry.configure(state="disabled")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Preparing extraction...")

        # Run extraction in background
        thread = threading.Thread(
            target=self._extract_thread,
            args=(version,),
            daemon=True
        )
        thread.start()

    def _extract_thread(self, version):
        """Background thread for extraction"""
        try:
            # Update progress
            self.after(0, lambda: self.progress_bar.set(0.2))
            self.after(0, lambda: self.progress_label.configure(
                text="Setting up temporary directory..."
            ))

            # Create temp directory
            temp_dir = Path(os.environ['TEMP']) / "sc_extract_temp"
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
            temp_dir.mkdir(parents=True, exist_ok=True)

            # Copy unp4k and dependencies
            self.after(0, lambda: self.progress_bar.set(0.3))
            self.after(0, lambda: self.progress_label.configure(
                text="Copying extraction tools..."
            ))

            shutil.copy2(self.resource_dir / "unp4k.exe", temp_dir / "unp4k.exe")

            # Copy DLL dependencies
            for dll_file in self.resource_dir.glob("*.dll"):
                shutil.copy2(dll_file, temp_dir / dll_file.name)

            # Copy x64/x86 directories if they exist
            for arch_dir in ["x64", "x86"]:
                arch_source = self.resource_dir / arch_dir
                if arch_source.exists():
                    arch_dest = temp_dir / arch_dir
                    if arch_dest.exists():
                        shutil.rmtree(arch_dest)
                    shutil.copytree(arch_source, arch_dest)

            # Run extraction
            self.after(0, lambda: self.progress_bar.set(0.4))
            self.after(0, lambda: self.progress_label.configure(
                text="Extracting global.ini (this may take 1-2 minutes)..."
            ))

            data_p4k_path = self.selected_installation["path"]
            branch = self.selected_installation["branch"]

            result = subprocess.run(
                [
                    str(temp_dir / "unp4k.exe"),
                    data_p4k_path,
                    "Data/Localization/english/global.ini"
                ],
                cwd=temp_dir,
                capture_output=True,
                timeout=300
            )

            self.after(0, lambda: self.progress_bar.set(0.8))

            if result.returncode != 0:
                raise Exception(f"Extraction failed with exit code {result.returncode}")

            # Find extracted file
            extracted_files = list(temp_dir.rglob("global.ini"))
            if not extracted_files:
                raise Exception("global.ini not found in extracted files")

            extracted_file = extracted_files[0]

            # Save to output file
            self.after(0, lambda: self.progress_label.configure(
                text="Saving file..."
            ))

            # Use user-selected output file path
            output_path = self.output_file

            shutil.copy2(extracted_file, output_path)

            # Get file size
            file_size_mb = output_path.stat().st_size / (1024 * 1024)

            # Success!
            self.after(0, lambda: self.progress_bar.set(1.0))
            self.after(0, lambda: self._extraction_complete(
                output_path, file_size_mb
            ))

        except subprocess.TimeoutExpired:
            self.after(0, lambda: self._extraction_failed(
                "Extraction timed out after 5 minutes"
            ))
        except Exception as e:
            self.after(0, lambda: self._extraction_failed(str(e)))
        finally:
            # Cleanup
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def _extraction_complete(self, output_path, file_size_mb):
        """Called when extraction completes successfully"""
        self.extracting = False
        self.extract_button.configure(state="normal")
        self.installation_dropdown.configure(state="readonly")
        self.version_entry.configure(state="normal")
        self.output_entry.configure(state="normal")
        self.progress_label.configure(
            text=f"✓ Extraction complete! ({file_size_mb:.2f} MB)",
            text_color="green"
        )

        messagebox.showinfo(
            "Extraction Complete",
            f"Successfully extracted global.ini!\n\n"
            f"Saved to:\n{output_path}\n\n"
            f"File size: {file_size_mb:.2f} MB"
        )

    def _extraction_failed(self, error_message):
        """Called when extraction fails"""
        self.extracting = False
        self.extract_button.configure(state="normal")
        self.installation_dropdown.configure(state="readonly")
        self.version_entry.configure(state="normal")
        self.output_entry.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(
            text="❌ Extraction failed",
            text_color="red"
        )

        messagebox.showerror(
            "Extraction Failed",
            f"Failed to extract global.ini:\n\n{error_message}"
        )


def main():
    app = SCExtractorApp()
    app.mainloop()


if __name__ == "__main__":
    main()

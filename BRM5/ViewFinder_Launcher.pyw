# ============================================================================
#                       ViewFinder_Launcher.pyw
# ============================================================================
"""
ViewFinder Launcher - Runs compiled executables in sequence
This launcher expects ViewFinder_Config.exe and ViewFinder_Main.exe
to be in the same directory.
"""

import sys
import subprocess
import os

def show_error_dialog(title, message):
    """Show error using tkinter dialog"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except:
        pass

def main():
    # Get the directory where this executable is located
    if getattr(sys, 'frozen', False):
        launcher_dir = os.path.dirname(sys.executable)
    else:
        launcher_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths to the compiled executables
    config_exe = os.path.join(launcher_dir, "ViewFinder_Config.exe")
    main_exe = os.path.join(launcher_dir, "ViewFinder_Main.exe")
    
    # Check if executables exist
    if not os.path.exists(config_exe):
        show_error_dialog(
            "Config Executable Not Found",
            f"Cannot find ViewFinder_Config.exe\n\n"
            f"Looking in: {launcher_dir}\n\n"
            f"Please ensure ViewFinder_Config.exe is in the same folder as this launcher."
        )
        return
    
    if not os.path.exists(main_exe):
        show_error_dialog(
            "Main Executable Not Found",
            f"Cannot find ViewFinder_Main.exe\n\n"
            f"Looking in: {launcher_dir}\n\n"
            f"Please ensure ViewFinder_Main.exe is in the same folder as this launcher."
        )
        return
    
    # Launch config executable and wait for it to close
    try:
        config_process = subprocess.run(
            [config_exe],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
    except Exception as e:
        show_error_dialog(
            "Failed to Launch Config Menu",
            f"Error launching ViewFinder_Config.exe:\n\n{str(e)}"
        )
        return
    
    # Launch main executable (don't wait - let it run independently)
    try:
        subprocess.Popen(
            [main_exe],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
    except Exception as e:
        show_error_dialog(
            "Failed to Launch Main App",
            f"Error launching ViewFinder_Main.exe:\n\n{str(e)}"
        )
        return

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        show_error_dialog(
            "Launcher Error",
            f"An unexpected error occurred:\n\n{str(e)}"
        )
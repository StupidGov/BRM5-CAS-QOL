"""
Universal Package Installer
Installs packages with pre-built wheels only (Python 3.14 compatible)
Can also generate .bat/.sh files and requirements.txt
"""

import sys
import subprocess
import platform
import os

# Package definitions
PACKAGES = [
    "PyQt5>=5.15.0",
    "mss>=6.1.0",
    "opencv-python>=4.5.0",
    "numpy>=2.0.0",
    "keyboard>=0.13.5",
    "pyinstaller>=5.0.0"
]

#
### the requirements themselves
#

REQUIREMENTS_CONTENT = """# Python Package Requirements
# Install with: python install_packages.py
# Or use: pip install -r requirements.txt --only-binary=:all:

# Core GUI Framework
PyQt5>=5.15.0

# Screen capture and computer vision
mss>=6.1.0
opencv-python>=4.5.0
numpy>=2.0.0

# Keyboard input handling
keyboard>=0.13.5

# Build tool for compilation (optional)
pyinstaller>=5.0.0
"""

#
### .bat file content
#

BAT_CONTENT = """@echo off
echo ================================================
echo Installing Python packages (pre-built wheels only)
echo ================================================
echo.
pip install -r requirements.txt --only-binary=:all:
echo.
echo ================================================
echo Installation complete!
echo ================================================
pause
"""

#
### .sh file content
#

SH_CONTENT = """#!/bin/bash
echo "================================================"
echo "Installing Python packages (pre-built wheels only)"
echo "================================================"
echo ""
pip install -r requirements.txt --only-binary=:all:
echo ""
echo "================================================"
echo "Installation complete!"
echo "================================================"
read -p "Press Enter to continue..."
"""


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def install_packages():
    """Install packages with pre-built wheels only"""
    print_header("Installing Packages")
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()}\n")
    
    print("Packages to install:")
    for pkg in PACKAGES:
        print(f"  - {pkg}")
    print()
    
    # Confirm installation
    response = input("Proceed with installation? (y/n): ").strip().lower()
    if response != 'y':
        print("Installation cancelled.")
        return False
    
    print("\nInstalling packages...\n")
    
    try:
        # Install packages with --only-binary flag
        cmd = [sys.executable, "-m", "pip", "install"] + PACKAGES + ["--only-binary=:all:"]
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print_header("Installation Successful!")
            return True
        else:
            print_header("Installation Failed!")
            print("Some packages may not have been installed.")
            return False
            
    except Exception as e:
        print_header("Installation Error!")
        print(f"Error: {e}")
        return False


def generate_files():
    """Generate requirements.txt, .bat, and .sh files"""
    print_header("Generating Installation Files")
    
    files_created = []
    
    # Generate requirements.txt
    try:
        with open("requirements.txt", "w") as f:
            f.write(REQUIREMENTS_CONTENT)
        print("✓ Created: requirements.txt")
        files_created.append("requirements.txt")
    except Exception as e:
        print(f"✗ Failed to create requirements.txt: {e}")
    
    # Generate install_requirements.bat (Windows)
    try:
        with open("install_requirements.bat", "w") as f:
            f.write(BAT_CONTENT)
        print("✓ Created: install_requirements.bat (Windows)")
        files_created.append("install_requirements.bat")
    except Exception as e:
        print(f"✗ Failed to create install_requirements.bat: {e}")
    
    # Generate install_requirements.sh (Linux/Mac)
    try:
        with open("install_requirements.sh", "w") as f:
            f.write(SH_CONTENT)
        # Make it executable on Unix systems
        if platform.system() != "Windows":
            os.chmod("install_requirements.sh", 0o755)
        print("✓ Created: install_requirements.sh (Linux/Mac)")
        files_created.append("install_requirements.sh")
    except Exception as e:
        print(f"✗ Failed to create install_requirements.sh: {e}")
    
    if files_created:
        print_header("Files Generated Successfully!")
        print("You can now use:")
        print("  - requirements.txt with: pip install -r requirements.txt --only-binary=:all:")
        print("  - install_requirements.bat on Windows")
        print("  - install_requirements.sh on Linux/Mac")
    else:
        print_header("No Files Generated")
    
    return len(files_created) > 0


def show_menu():
    """Display main menu and get user choice"""
    print_header("Universal Package Installer")
    print("1. Install packages now (with pre-built wheels)")
    print("2. Generate installation files (.txt, .bat, .sh)")
    print("3. Do both (install + generate files)")
    print("4. Exit")
    print()
    
    choice = input("Choose an option (1-4): ").strip()
    return choice


def main():
    """Main program loop"""
    while True:
        choice = show_menu()
        
        if choice == "1":
            install_packages()
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            generate_files()
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            success = install_packages()
            if success:
                print("\nNow generating installation files...\n")
                generate_files()
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            print_header("Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please enter 1-4.\n")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
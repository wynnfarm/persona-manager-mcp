#!/usr/bin/env python3
"""
Install Context Manager for any project

This script copies the context_manager directory to your project
and sets up the necessary files for context management.
"""

import shutil
import sys
import os
from pathlib import Path
import subprocess


def install_context_manager(target_project: str = None):
    """Install context manager to a project"""
    
    # Get current directory (where context_manager is located)
    current_dir = Path(__file__).parent
    context_manager_dir = current_dir.parent / "context_manager"
    
    if not context_manager_dir.exists():
        print("❌ context_manager directory not found!")
        print("Make sure context_manager/ exists in the parent directory")
        sys.exit(1)
    
    # Determine target project
    if target_project:
        target_path = Path(target_project)
    else:
        target_path = Path.cwd()
    
    print(f"🎯 Installing Context Manager to: {target_path}")
    
    # Copy context_manager directory
    target_context_manager = target_path / "context_manager"
    if target_context_manager.exists():
        print(f"⚠️  context_manager already exists in {target_path}")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Installation cancelled")
            return
    
    try:
        shutil.copytree(context_manager_dir, target_context_manager, dirs_exist_ok=True)
        print(f"✅ Copied context_manager to {target_context_manager}")
    except Exception as e:
        print(f"❌ Error copying context_manager: {e}")
        return
    
    # Setup context management
    try:
        # Change to target directory
        original_cwd = Path.cwd()
        os.chdir(target_path)
        
        # Run setup
        result = subprocess.run([
            sys.executable, "context_manager/cli.py", "setup"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Context management setup complete!")
            print("\n🎯 Next steps:")
            print("1. Set your current goal:")
            print(f"   python context_manager/cli.py goal \"Your goal here\"")
            print("2. Check status:")
            print(f"   python context_manager/cli.py status")
            print("3. Or use the generated script:")
            print(f"   python context_check.py")
        else:
            print(f"⚠️  Setup completed with warnings: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error during setup: {e}")
    finally:
        # Return to original directory
        os.chdir(original_cwd)


def main():
    """Main installation function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Install Context Manager for any project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install_context_manager.py                    # Install to current directory
  python install_context_manager.py /path/to/project  # Install to specific project
  python install_context_manager.py --help            # Show this help
        """
    )
    
    parser.add_argument(
        "project_path", 
        nargs="?", 
        help="Target project directory (defaults to current directory)"
    )
    
    args = parser.parse_args()
    
    print("🎯 Context Manager Installer")
    print("=" * 30)
    
    install_context_manager(args.project_path)
    
    print("\n🎉 Installation complete!")
    print("Context Manager is now available in your project.")


if __name__ == "__main__":
    import os
    main()

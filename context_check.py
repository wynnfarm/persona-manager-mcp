#!/usr/bin/env python3
"""
Quick context check script
Run with: python context_check.py
"""

import sys
from pathlib import Path

# Import and run path setup
from setup_path import setup_context_manager_path
setup_context_manager_path()

try:
    from context_manager.utils import quick_status_check, get_project_info
    from context_manager.core import ContextManager
    
    print("🎯 Project Context Check")
    print("=" * 30)
    
    # Get project info
    info = get_project_info()
    print(f"📁 Project: {info['name']}")
    print(f"🐍 Python: {info['python_version']}")
    print(f"📄 Files: {info['files_count']}")
    print(f"📁 Directories: {info['directories_count']}")
    print()
    
    # Show status
    status = quick_status_check()
    print(status)
    
    # Show context manager if available
    if info['has_context_cache']:
        print("\n📊 Context Manager: Active")
    else:
        print("\n📊 Context Manager: Not initialized")
        print("   Run: from context_manager.core import ContextManager")
        print("   Then: cm = ContextManager('ProjectName')")
        
except ImportError as e:
    print(f"❌ Context manager not available: {e}")
    print("📁 Make sure context_manager/ directory exists")
except Exception as e:
    print(f"❌ Error: {e}")

if __name__ == "__main__":
    pass

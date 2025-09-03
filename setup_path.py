#!/usr/bin/env python3
"""
Setup script to configure Python path for context_manager
"""

import sys
from pathlib import Path

def setup_context_manager_path():
    """Add context_manager to Python path"""
    # Get the path to context_manager (parent directory)
    current_dir = Path(__file__).parent
    context_manager_path = current_dir.parent / "context_manager"
    
    if context_manager_path.exists():
        # Add both the parent directory and context_manager directory to path
        parent_path = str(context_manager_path.parent)
        context_manager_dir = str(context_manager_path)
        
        if parent_path not in sys.path:
            sys.path.insert(0, parent_path)
        if context_manager_dir not in sys.path:
            sys.path.insert(0, context_manager_dir)
        
        print(f"✅ Added to Python path:")
        print(f"   {parent_path}")
        print(f"   {context_manager_dir}")
        return True
    else:
        print(f"❌ context_manager not found at: {context_manager_path}")
        return False

if __name__ == "__main__":
    setup_context_manager_path()

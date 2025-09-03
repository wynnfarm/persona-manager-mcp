#!/usr/bin/env python3
"""
Context check script using Context Manager Service

This script checks project context by communicating with the Context Manager API
instead of importing the context_manager directly.
"""

import os
import sys
import requests
from pathlib import Path

def get_context_manager_url():
    """Get the context manager URL from environment or default."""
    return os.getenv("CONTEXT_MANAGER_URL", "http://localhost:8001")

def check_context_service():
    """Check if the context manager service is available."""
    try:
        url = get_context_manager_url()
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Service returned status {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Service unavailable: {e}"

def get_project_context(project_name):
    """Get context for a specific project."""
    try:
        url = get_context_manager_url()
        response = requests.get(f"{url}/project/{project_name}", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting project context: {e}")
        return None

def get_project_info():
    """Get basic project information."""
    current_dir = Path.cwd()
    return {
        "name": current_dir.name,
        "path": str(current_dir),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "files_count": len(list(current_dir.rglob("*"))),
        "directories_count": len([d for d in current_dir.iterdir() if d.is_dir()])
    }

def main():
    """Main function to check context."""
    print("🎯 Project Context Check (Service Mode)")
    print("=" * 40)
    
    # Get project info
    info = get_project_info()
    print(f"📁 Project: {info['name']}")
    print(f"🐍 Python: {info['python_version']}")
    print(f"📄 Files: {info['files_count']}")
    print(f"📁 Directories: {info['directories_count']}")
    print()
    
    # Check context manager service
    service_available, service_info = check_context_service()
    
    if service_available:
        print("✅ Context Manager Service: Available")
        print(f"   URL: {get_context_manager_url()}")
        print(f"   Status: {service_info.get('status', 'unknown')}")
        print()
        
        # Get project context
        project_name = os.getenv("CONTEXT_PROJECT_NAME", "persona-manager-mcp")
        context = get_project_context(project_name)
        
        if context:
            print(f"📊 Context for '{project_name}':")
            print(f"   Goal: {context.get('context', {}).get('current_goal', 'Not set')}")
            print(f"   Issue: {context.get('context', {}).get('current_issue', 'None')}")
            print(f"   Next: {context.get('context', {}).get('next_step', 'Not set')}")
            
            anchors = context.get('context', {}).get('anchors', {})
            if anchors:
                print(f"   Anchors: {', '.join(anchors.keys())}")
        else:
            print(f"📊 Context for '{project_name}': Not initialized")
            print("   Run: context-manager init to initialize")
    else:
        print("❌ Context Manager Service: Unavailable")
        print(f"   Error: {service_info}")
        print()
        print("🔧 To start the service:")
        print("   1. Build context-manager: cd ../context_manager && docker build -t context-manager .")
        print("   2. Start service: docker run -d -p 8001:8000 context-manager")
        print("   3. Or use docker-compose: docker compose up context-manager")

if __name__ == "__main__":
    main()

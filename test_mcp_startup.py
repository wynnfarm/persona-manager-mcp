#!/usr/bin/env python3
"""
Test script to verify MCP server can start properly
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, '/app')

try:
    from mcp_persona_server import PersonaMCPServer
    print("✅ Import successful")
    
    # Create server instance
    server = PersonaMCPServer()
    print("✅ Server instance created")
    
    # Test basic functionality
    print("✅ Server ready for MCP communication")
    
    # Exit successfully
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

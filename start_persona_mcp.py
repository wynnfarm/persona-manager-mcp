#!/usr/bin/env python3
"""
Simple wrapper for the persona-manager MCP server
"""

import os
import sys
import asyncio

# Set environment variables
os.environ['PERSONA_STORAGE_PATH'] = os.path.join(os.path.dirname(__file__), 'personas')
os.environ['CONTEXT_MANAGER_URL'] = 'http://localhost:8000'

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the MCP server
try:
    from mcp_persona_server.server import main
    print("✅ MCP server imported successfully")
    asyncio.run(main())
except Exception as e:
    print(f"❌ Error starting MCP server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

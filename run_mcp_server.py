#!/usr/bin/env python3
"""
MCP Server wrapper for Cursor
"""

import os
import sys
import subprocess

# Set environment variables
os.environ['PERSONA_STORAGE_PATH'] = os.path.join(os.path.dirname(__file__), 'personas')
os.environ['CONTEXT_MANAGER_URL'] = 'http://localhost:8000'

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the MCP server
from mcp_persona_server.server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

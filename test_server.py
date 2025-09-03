#!/usr/bin/env python3
"""
Simple test script to isolate the MCP server initialization issue.
"""

import asyncio
import sys
from mcp_persona_server import PersonaMCPServer
from mcp.server import NotificationOptions

async def test_server():
    """Test server initialization."""
    print("Creating PersonaMCPServer...")
    server = PersonaMCPServer()
    print("✅ PersonaMCPServer created successfully")
    
    print("Testing server.get_capabilities...")
    caps = server.server.get_capabilities(
        notification_options=NotificationOptions(),
        experimental_capabilities=None
    )
    print("✅ get_capabilities works")
    
    print("Server test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_server())

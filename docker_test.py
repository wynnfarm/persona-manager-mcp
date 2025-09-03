#!/usr/bin/env python3
"""
Test script to run in Docker container.
"""

import asyncio
from mcp_persona_server import PersonaMCPServer

async def test():
    print("Creating PersonaMCPServer in Docker...")
    server = PersonaMCPServer()
    print("✅ PersonaMCPServer created")
    
    print("Testing get_capabilities...")
    caps = server.server.get_capabilities(
        notification_options=None,
        experimental_capabilities=None
    )
    print("✅ get_capabilities works in Docker!")

if __name__ == "__main__":
    asyncio.run(test())

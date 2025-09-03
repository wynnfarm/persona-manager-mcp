#!/usr/bin/env python3
"""
Minimal MCP server for testing - using direct tool registration
"""

import os
import sys
import asyncio
import json
from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent

# Set environment variables
os.environ['PERSONA_STORAGE_PATH'] = os.path.join(os.path.dirname(__file__), 'personas')
os.environ['CONTEXT_MANAGER_URL'] = 'http://localhost:8000'

# Create server
server = Server("persona-server")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List all available tools."""
    tools = [
        Tool(
            name="list_personas",
            description="List all available personas",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="create_persona",
            description="Create a new persona",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the persona"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the persona"
                    }
                },
                "required": ["name", "description"]
            }
        )
    ]
    return ListToolsResult(tools=tools)

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls."""
    if name == "list_personas":
        return CallToolResult(
            content=[TextContent(type="text", text='{"personas": []}')]
        )
    elif name == "create_persona":
        return CallToolResult(
            content=[TextContent(type="text", text='{"status": "created", "name": "' + arguments.get("name", "Unknown") + '"}')]
        )
    else:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Unknown tool: {name}")],
            isError=True
        )

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="persona-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())

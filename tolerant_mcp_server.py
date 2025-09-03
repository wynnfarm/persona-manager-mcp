#!/usr/bin/env python3
"""
MCP server that's tolerant of missing initialized notification
"""

import asyncio
import json
import sys
from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent

class TolerantMCPServer:
    def __init__(self):
        self.server = Server("tolerant-test")
        self._register_tools()
        self._initialized = False
    
    def _register_tools(self):
        @self.server.list_tools()
        async def handle_list_tools():
            # Don't check for initialization - just return tools
            tools = [
                Tool(
                    name="hello",
                    description="Say hello",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name to greet"
                            }
                        }
                    }
                )
            ]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            if name == "hello":
                name = arguments.get("name", "World")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Hello, {name}!")]
                )
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                    isError=True
                )
    
    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="tolerant-test",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities=None,
                    ),
                ),
            )

async def main():
    server = TolerantMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())

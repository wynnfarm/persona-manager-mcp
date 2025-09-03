#!/usr/bin/env python3
"""
Minimal MCP server test with lifespan
"""

import asyncio
import json
from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent

class MinimalMCPServer:
    def __init__(self):
        self.server = Server("minimal-test")
        self._register_tools()
        self._register_lifespan()
    
    def _register_tools(self):
        @self.server.list_tools()
        async def handle_list_tools():
            tools = [
                Tool(
                    name="test_tool",
                    description="A test tool",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Message to echo"
                            }
                        }
                    }
                )
            ]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            if name == "test_tool":
                message = arguments.get("message", "Hello")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Echo: {message}")]
                )
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                    isError=True
                )
    
    def _register_lifespan(self):
        @self.server.lifespan()
        async def lifespan(_):
            # Send initialized notification
            yield
            # Cleanup on shutdown
            pass
    
    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="minimal-test",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities=None,
                    ),
                ),
            )

async def main():
    server = MinimalMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())

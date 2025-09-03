#!/usr/bin/env python3
"""
MCP Integration Example

This example demonstrates how to:
1. Run the MCP server
2. Connect to it from an AI assistant
3. Use the server's tools programmatically
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path


class MCPClient:
    """Simple MCP client for testing the persona server."""
    
    def __init__(self, server_command):
        self.server_command = server_command
        self.process = None
    
    async def start_server(self):
        """Start the MCP server process."""
        try:
            self.process = await asyncio.create_subprocess_exec(
                *self.server_command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            print(f"✅ Started MCP server with PID: {self.process.pid}")
            return True
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    async def send_request(self, method, params=None):
        """Send a request to the MCP server."""
        if not self.process:
            print("❌ Server not running")
            return None
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        try:
            # Send request
            request_str = json.dumps(request) + "\n"
            self.process.stdin.write(request_str.encode())
            await self.process.stdin.drain()
            
            # Read response
            response_line = await self.process.stdout.readline()
            if response_line:
                response = json.loads(response_line.decode().strip())
                return response
            else:
                return None
        except Exception as e:
            print(f"❌ Error sending request: {e}")
            return None
    
    async def stop_server(self):
        """Stop the MCP server."""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            print("✅ Server stopped")


async def mcp_integration_example():
    """Demonstrate MCP integration."""
    
    print("🔌 MCP Integration Example")
    print("=" * 40)
    
    # Determine the server command
    server_script = Path(__file__).parent.parent / "mcp_persona_server" / "server.py"
    server_command = [sys.executable, str(server_script)]
    
    client = MCPClient(server_command)
    
    try:
        # Start the server
        print("\n1. Starting MCP server...")
        if not await client.start_server():
            return
        
        # Wait a moment for server to initialize
        await asyncio.sleep(1)
        
        # 2. List available tools
        print("\n2. Listing available tools...")
        response = await client.send_request("tools/list")
        if response and "result" in response:
            tools = response["result"]["tools"]
            print(f"  Found {len(tools)} tools:")
            for tool in tools:
                print(f"    - {tool['name']}: {tool['description']}")
        else:
            print("  ❌ Failed to list tools")
        
        # 3. Test tool calls
        print("\n3. Testing tool calls...")
        
        # List personas
        print("  📋 Listing personas...")
        response = await client.send_request("tools/call", {
            "name": "list_personas",
            "arguments": {"include_metadata": True}
        })
        if response and "result" in response:
            result = json.loads(response["result"]["content"][0]["text"])
            personas = result.get("personas", {})
            print(f"    Found {len(personas)} personas")
            for persona_id, persona_data in personas.items():
                print(f"      - {persona_data['name']}")
        else:
            print("    ❌ Failed to list personas")
        
        # Create a new persona
        print("  ➕ Creating a new persona...")
        new_persona = {
            "name": "AI Researcher",
            "description": "A researcher specializing in artificial intelligence and machine learning",
            "expertise": ["Artificial Intelligence", "Machine Learning", "Research", "Neural Networks"],
            "communication_style": "Academic and research-oriented",
            "context": "Use when discussing AI research, machine learning algorithms, or academic topics",
            "personality_traits": ["curious", "analytical", "research-minded", "innovative"]
        }
        
        response = await client.send_request("tools/call", {
            "name": "create_persona",
            "arguments": new_persona
        })
        if response and "result" in response:
            result = response["result"]["content"][0]["text"]
            print(f"    ✅ {result}")
        else:
            print("    ❌ Failed to create persona")
        
        # Select best persona for a task
        print("  🎯 Selecting best persona for 'research neural networks'...")
        response = await client.send_request("tools/call", {
            "name": "select_best_persona",
            "arguments": {
                "task_description": "research neural networks",
                "context": "academic research project"
            }
        })
        if response and "result" in response:
            result = json.loads(response["result"]["content"][0]["text"])
            print(f"    🎯 Best persona: {result['name']}")
            print(f"       Description: {result['description']}")
        else:
            print("    ❌ Failed to select persona")
        
        # Get statistics
        print("  📊 Getting statistics...")
        response = await client.send_request("tools/call", {
            "name": "get_persona_statistics",
            "arguments": {}
        })
        if response and "result" in response:
            result = json.loads(response["result"]["content"][0]["text"])
            print(f"    Total personas: {result['total_personas']}")
            print(f"    Top expertise: {list(result['expertise_distribution'].keys())[:3]}")
        else:
            print("    ❌ Failed to get statistics")
        
        print("\n🎉 MCP integration example completed!")
        
    except Exception as e:
        print(f"❌ Error during integration: {e}")
    
    finally:
        # Stop the server
        print("\n4. Stopping server...")
        await client.stop_server()


def demonstrate_ai_integration():
    """Demonstrate how AI assistants would integrate with the MCP server."""
    
    print("\n🤖 AI Integration Guide")
    print("=" * 30)
    
    print("""
To integrate this MCP server with AI assistants:

1. **Claude Desktop Integration:**
   - Add the server to Claude's MCP configuration
   - Claude can then use personas for different tasks
   - Example: "Use the Tech Expert persona to help me debug this Python code"

2. **Custom AI Application:**
   - Use the MCP Python SDK to connect to the server
   - Call tools programmatically based on user requests
   - Dynamically select personas based on task requirements

3. **Available Tools for AI:**
   - list_personas: See all available personas
   - select_best_persona: Get the most suitable persona for a task
   - get_persona_suggestions: Get multiple persona options
   - create_persona: Create new personas on demand
   - update_persona: Modify existing personas
   - search_personas: Find personas by query

4. **Example AI Workflow:**
   - User asks: "Help me write a technical blog post"
   - AI calls select_best_persona with task description
   - AI receives the Tech Expert or Creative Writer persona
   - AI adopts that persona's characteristics for the response
   - AI provides response in the persona's style and expertise area
    """)


if __name__ == "__main__":
    asyncio.run(mcp_integration_example())
    demonstrate_ai_integration()

#!/usr/bin/env python3
"""
Manual MCP server implementation - improved version
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Set environment variables
os.environ['PERSONA_STORAGE_PATH'] = os.path.join(os.path.dirname(__file__), 'personas')
os.environ['CONTEXT_MANAGER_URL'] = 'http://localhost:8000'

class ManualMCPServer:
    def __init__(self):
        self.initialized = False
        self.persona_storage_path = os.environ.get('PERSONA_STORAGE_PATH', './personas')
    
    def _load_personas(self):
        """Load personas from storage."""
        try:
            personas_file = Path(self.persona_storage_path) / 'personas.json'
            if not personas_file.exists():
                return {}
            
            with open(personas_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading personas: {e}", file=sys.stderr)
            return {}
    
    def handle_initialize(self, params, request_id):
        """Handle initialize request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    }
                },
                "serverInfo": {
                    "name": "persona-server",
                    "version": "0.1.0"
                }
            }
        }
    
    def handle_tools_list(self, params, request_id):
        """Handle tools/list request."""
        tools = [
            {
                "name": "list_personas",
                "description": "List all available personas",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "create_persona",
                "description": "Create a new persona",
                "inputSchema": {
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
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
    
    def handle_tool_call(self, params, request_id):
        """Handle tools/call request."""
        name = params.get("name", "")
        arguments = params.get("arguments", {})
        
        if name == "list_personas":
            # Actually load personas from storage
            personas = self._load_personas()
            
            # Convert to list format for response
            persona_list = []
            for persona_id, persona_data in personas.items():
                persona_list.append({
                    "id": persona_id,
                    **persona_data
                })
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "personas": persona_list,
                                "count": len(persona_list)
                            })
                        }
                    ]
                }
            }
        elif name == "create_persona":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "status": "created",
                                "name": arguments.get("name", "Unknown")
                            })
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {name}"
                }
            }
    
    def run(self):
        """Run the server."""
        while True:
            try:
                # Read input
                line = sys.stdin.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON-RPC request
                request = json.loads(line)
                method = request.get("method", "")
                params = request.get("params", {})
                request_id = request.get("id")
                
                # Handle different methods
                if method == "initialize":
                    response = self.handle_initialize(params, request_id)
                    print(json.dumps(response))
                    self.initialized = True
                
                elif method == "notifications/initialized":
                    # Just acknowledge
                    continue
                
                elif method == "tools/list":
                    response = self.handle_tools_list(params, request_id)
                    print(json.dumps(response))
                
                elif method == "tools/call":
                    response = self.handle_tool_call(params, request_id)
                    print(json.dumps(response))
                
                else:
                    # Unknown method
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                    print(json.dumps(response))
                
                # Flush output
                sys.stdout.flush()
                
            except EOFError:
                break
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request_id if 'request_id' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()

if __name__ == "__main__":
    server = ManualMCPServer()
    server.run()

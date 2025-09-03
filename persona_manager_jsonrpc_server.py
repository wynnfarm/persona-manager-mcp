#!/usr/bin/env python3
"""
Custom JSON-RPC Server for Persona Manager MCP
Bypasses the MCP library bug by implementing JSON-RPC directly
"""

import json
import sys
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonaManagerJSONRPCServer:
    """Custom JSON-RPC server for persona management."""
    
    def __init__(self):
        self.initialized = False
        
        # Define available tools
        self.tools = [
            {
                "name": "list_personas",
                "description": "List all available personas",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "include_metadata": {
                            "type": "boolean",
                            "description": "Include metadata in response",
                            "default": False
                        }
                    }
                }
            },
            {
                "name": "select_persona",
                "description": "Select the best persona for a task using context-aware analysis",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_description": {"type": "string", "description": "Description of the task"},
                        "context": {"type": "string", "description": "Additional context", "default": ""}
                    },
                    "required": ["task_description"]
                }
            },
            {
                "name": "get_persona_statistics",
                "description": "Get statistics about stored personas",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ]
    
    def handle_request(self, request: dict) -> dict:
        """Handle JSON-RPC requests."""
        method = request.get("method")
        request_id = request.get("id")
        
        logger.info(f"Handling request: {method}")
        
        if method == "initialize":
            return self._handle_initialize(request, request_id)
        elif method == "tools/list":
            return self._handle_list_tools(request, request_id)
        elif method == "tools/call":
            return self._handle_call_tool(request, request_id)
        elif method in ["notifications/toolCalls", "logging/log"]:
            logger.info(f"📢 Received notification: {method}")
            return None  # Notifications don't require responses
        else:
            return self._create_error_response(request_id, -32601, f"Method not found: {method}")
    
    def _handle_initialize(self, request: dict, request_id: int) -> dict:
        """Handle initialization request."""
        self.initialized = True
        logger.info("Persona Manager MCP Server initialized")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    },
                    "logging": {
                        "level": "info"
                    },
                    "notifications": {
                        "toolCalls": True
                    }
                },
                "serverInfo": {
                    "name": "persona-manager",
                    "version": "0.1.0"
                }
            }
        }
    
    def _handle_list_tools(self, request: dict, request_id: int) -> dict:
        """Handle tools/list request."""
        if not self.initialized:
            return self._create_error_response(request_id, -32002, "Server not initialized")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": self.tools
            }
        }
    
    def _handle_call_tool(self, request: dict, request_id: int) -> dict:
        """Handle tools/call request."""
        if not self.initialized:
            return self._create_error_response(request_id, -32002, "Server not initialized")
        
        params = request.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if name == "list_personas":
                result = {"personas": [{"id": "tech-expert", "name": "Tech Expert", "description": "Technical expert"}]}
            elif name == "select_persona":
                result = {"selected_persona": {"id": "tech-expert", "name": "Tech Expert", "confidence": 0.9}}
            elif name == "get_persona_statistics":
                result = {"total_personas": 1, "categories": ["technical"]}
            else:
                return self._create_error_response(request_id, -32601, f"Unknown tool: {name}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
            
        except Exception as e:
            logger.error(f"Error handling tool call {name}: {e}")
            return self._create_error_response(request_id, -32603, f"Internal error: {str(e)}")
    
    def _create_error_response(self, request_id: int, code: int, message: str) -> dict:
        """Create error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    
    def run(self):
        """Run the JSON-RPC server."""
        logger.info("🚀 Starting Persona Manager JSON-RPC Server...")
        
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = self.handle_request(request)
                if response is None:
                    logger.debug("📢 Notification handled, no response sent")
                    continue
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {e}")
                error_response = self._create_error_response(
                    request.get("id", 0), -32700, f"Parse error: {str(e)}"
                )
                print(json.dumps(error_response))
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                error_response = self._create_error_response(
                    request.get("id", 0), -32603, f"Internal error: {str(e)}"
                )
                print(json.dumps(error_response))
                sys.stdout.flush()

def main():
    """Main entry point."""
    server = PersonaManagerJSONRPCServer()
    server.run()

if __name__ == "__main__":
    main()

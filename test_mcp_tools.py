#!/usr/bin/env python3
"""
Test script to verify MCP server tools are working
"""

import json
import subprocess
import sys

def test_mcp_server():
    # Initialize the server
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0.0"}
        }
    }
    
    # List tools request
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    # Send both requests
    requests = json.dumps(init_request) + "\n" + json.dumps(list_tools_request) + "\n"
    
    try:
        result = subprocess.run(
            ["python", "/Users/wynnfarm/dev/persona-manager-mcp/run_mcp_server.py"],
            input=requests,
            text=True,
            capture_output=True,
            timeout=10
        )
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        
        # Parse the responses
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.strip():
                try:
                    response = json.loads(line)
                    print(f"\nResponse: {json.dumps(response, indent=2)}")
                except json.JSONDecodeError:
                    print(f"Non-JSON output: {line}")
                    
    except subprocess.TimeoutExpired:
        print("Timeout waiting for response")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_mcp_server()

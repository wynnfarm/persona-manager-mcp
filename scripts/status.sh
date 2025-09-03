#!/bin/bash

# Quick status script for context management

echo "🎯 MCP Persona Server Status"
echo "============================"

# Python environment
echo "🐍 Python: $(python --version 2>&1)"

# Docker status
if docker info >/dev/null 2>&1; then
    echo "🐳 Docker: Running"
    echo "   Images: $(docker images mcp-persona-server --format 'table {{.Repository}}:{{.Tag}}\t{{.Size}}' 2>/dev/null | tail -n +2 | wc -l)"
else
    echo "🐳 Docker: Not running"
fi

# Project state
echo "📁 Personas: $(ls -1 personas/*.json 2>/dev/null | wc -l | tr -d ' ') files"
echo "🤖 Auto-generated: $(python -c "from mcp_persona_server import PersonaMCPServer; s = PersonaMCPServer(); print(len([p for p in s.persona_manager.get_all_personas().values() if p.get('auto_generated', False)]))" 2>/dev/null || echo "N/A")"

# Current issue
echo ""
echo "🔧 Current Issue:"
echo "   Server initialization error - NotificationOptions fix needed"

# Next action
echo ""
echo "📋 Next: Fix server.py → rebuild → test"

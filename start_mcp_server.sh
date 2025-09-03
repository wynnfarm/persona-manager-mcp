#!/bin/bash
# MCP Server wrapper script

cd /app
export PERSONA_STORAGE_PATH=/app/personas
export CONTEXT_MANAGER_URL=http://host.docker.internal:8000

exec python -m mcp_persona_server.server

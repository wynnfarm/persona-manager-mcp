#!/usr/bin/env node
/**
 * Simple Node.js MCP server for persona management
 */

const { Server } = require('@modelcontextprotocol/server-sequential-thinking');

// Create server
const server = new Server({
  name: 'persona-server',
  version: '0.1.0'
});

// Register tools
server.listTools(async () => {
  return [
    {
      name: 'list_personas',
      description: 'List all available personas',
      inputSchema: {
        type: 'object',
        properties: {}
      }
    },
    {
      name: 'create_persona',
      description: 'Create a new persona',
      inputSchema: {
        type: 'object',
        properties: {
          name: {
            type: 'string',
            description: 'Name of the persona'
          },
          description: {
            type: 'string',
            description: 'Description of the persona'
          }
        },
        required: ['name', 'description']
      }
    }
  ];
});

server.callTool(async (name, arguments) => {
  if (name === 'list_personas') {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({ personas: [] })
        }
      ]
    };
  } else if (name === 'create_persona') {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({ 
            status: 'created', 
            name: arguments.name || 'Unknown' 
          })
        }
      ]
    };
  } else {
    return {
      content: [
        {
          type: 'text',
          text: `Unknown tool: ${name}`
        }
      ],
      isError: true
    };
  }
});

// Start server
server.listen();

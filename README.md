# Persona Manager MCP

A Model Context Protocol (MCP) server for building and managing AI personas. This server allows AI assistants to access and utilize different personas based on the task being performed.

## 🎭 Features

- **Persona Management**: Create, read, update, and delete AI personas
- **Smart Selection**: Intelligent persona selection based on task requirements
- **Global Echo**: Automatic persona echo when Persona Manager is being used
- **MCP Integration**: Easy integration with AI assistants that support MCP
- **TypeScript/Node.js**: Built with modern TypeScript and Node.js architecture

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Docker (optional, for containerized deployment)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/persona-manager-mcp.git
cd persona-manager-mcp
```

2. Install dependencies:
```bash
npm install
```

3. Build the project:
```bash
npm run build
```

### Running the MCP Server

#### Local Development
```bash
npm run dev
```

#### Production Build
```bash
npm run build
node dist/index.js --transport stdio
```

#### Docker
```bash
docker build -t mcp-persona-server:latest .
docker run -i --rm mcp-persona-server:latest node dist/index.js --transport stdio
```

## 🔧 Configuration

### Cursor Integration

Add to your `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "persona-manager": {
      "command": "node",
      "args": ["/path/to/persona-manager-mcp/dist/index.js", "--transport", "stdio"],
      "env": {},
      "cwd": "/path/to/persona-manager-mcp"
    }
  }
}
```

### Global Dev Integration

For all projects under `/dev`, add to `~/dev/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "persona-manager": {
      "command": "node",
      "args": ["/Users/wynnfarm/dev/persona-manager-mcp/dist/index.js", "--transport", "stdio"],
      "env": {},
      "cwd": "/Users/wynnfarm/dev/persona-manager-mcp"
    }
  }
}
```

## 🛠️ Available Tools

### `list_personas`
List all available personas with optional metadata.

**Parameters:**
- `include_metadata` (boolean, optional): Include metadata in response

### `select_persona`
Select the best persona for a task using context-aware analysis.

**Parameters:**
- `task_description` (string, required): Description of the task
- `context` (string, optional): Additional context

### `get_persona_statistics`
Get statistics about stored personas.

**Parameters:** None

### `echo_current_persona`
Echo the currently active persona.

**Parameters:** None

### `set_persona`
Manually set a specific persona by ID.

**Parameters:**
- `persona_id` (string, required): ID of the persona to set

### `create_persona` ✨ NEW
Create a new persona with dynamic storage.

**Parameters:**
- `name` (string, required): Name of the persona
- `description` (string, required): Description of the persona
- `expertise` (array of strings, required): Areas of expertise
- `communication_style` (string, required): Communication style
- `context` (string, optional): Context for when to use this persona
- `personality_traits` (array of strings, optional): Personality traits
- `id` (string, optional): Custom ID (auto-generated if not provided)

### `update_persona` ✨ NEW
Update an existing persona.

**Parameters:**
- `persona_id` (string, required): ID of the persona to update
- `name` (string, optional): New name for the persona
- `description` (string, optional): New description for the persona
- `expertise` (array of strings, optional): New areas of expertise
- `communication_style` (string, optional): New communication style
- `context` (string, optional): New context for when to use this persona
- `personality_traits` (array of strings, optional): New personality traits

### `delete_persona` ✨ NEW
Delete a persona.

**Parameters:**
- `persona_id` (string, required): ID of the persona to delete

### `search_personas` ✨ NEW
Search for personas by name, description, or expertise.

**Parameters:**
- `query` (string, required): Search query to find matching personas

### `get_persona` ✨ NEW
Get a specific persona by ID.

**Parameters:**
- `persona_id` (string, required): ID of the persona to retrieve

## 🎭 Global Persona Echo

The Persona Manager includes a global echo feature that automatically displays which persona is currently active. When a persona is selected or used, it will echo:

```
🎭 Currently using persona: Tech Expert (tech-expert)
   Description: Technical expert with deep knowledge of software development
   Expertise: Python, JavaScript, System Architecture
   Communication Style: Technical and precise
```

## 💾 Dynamic Persona Storage ✨ NEW

The Persona Manager now supports dynamic persona storage with file-based persistence:

### **Features:**
- **Persistent Storage**: Personas are saved to `personas/personas.json`
- **Automatic Loading**: Loads existing personas on startup
- **Fallback System**: Falls back to default personas if storage is unavailable
- **Validation**: Ensures persona data integrity with schema validation
- **Real-time Updates**: Changes are immediately saved to disk

### **Storage Structure:**
```
personas/
├── personas.json          # User-created personas (auto-generated)
├── default_personas.json  # Default personas (fallback)
└── metadata.json         # Storage metadata
```

### **Example Usage:**
```bash
# Create a new persona
create_persona --name "Data Scientist" --description "Expert in data analysis and ML" --expertise "Python,Statistics,Machine Learning" --communication_style "Analytical and data-driven"

# Update an existing persona
update_persona --persona_id "data-scientist" --expertise "Python,Statistics,Machine Learning,Deep Learning"

# Search for personas
search_personas --query "machine learning"

# Delete a persona
delete_persona --persona_id "old-persona"
```

## 📁 Project Structure

```
persona-manager-mcp/
├── src/
│   └── index.ts          # Main MCP server implementation
├── dist/                 # Built JavaScript files
├── personas/             # Persona data storage
├── package.json          # Node.js dependencies
├── tsconfig.json         # TypeScript configuration
├── Dockerfile            # Docker configuration
└── README.md            # This file
```

## 🧪 Development

### Building
```bash
npm run build
```

### Testing
```bash
npm test
```

### Linting
```bash
npm run lint
```

### Formatting
```bash
npm run format
```

## 🔒 Security

This project has been reviewed for sensitive information and is safe for public GitHub repositories. A comprehensive `.gitignore` file is included to prevent accidental commits of sensitive data.

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions, please open an issue on GitHub.

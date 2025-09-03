# Quick Start Guide

Get up and running with the MCP Persona Server in minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd mcp-experiments
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python cli.py --help
   ```

## Quick Test

1. **List available personas:**

   ```bash
   python cli.py list
   ```

2. **Run the demo:**

   ```bash
   python cli.py demo
   ```

3. **Create a new persona:**

   ```bash
   python cli.py create \
     --name "Data Scientist" \
     --description "Expert in data analysis and machine learning" \
     --expertise "Python,Machine Learning,Statistics,Data Analysis"
   ```

4. **Select the best persona for a task:**
   ```bash
   python cli.py select "analyze customer data"
   ```

## Using the MCP Server

### Start the MCP Server

```bash
python -m mcp_persona_server.server
```

The server will start and listen for MCP connections via stdio.

### Integration with AI Assistants

#### Claude Desktop

1. Add the server to Claude's MCP configuration:

   ```json
   {
     "mcpServers": {
       "persona-server": {
         "command": "python",
         "args": ["-m", "mcp_persona_server.server"],
         "env": {}
       }
     }
   }
   ```

2. Restart Claude Desktop

3. Ask Claude to use personas:
   - "Use the Tech Expert persona to help me debug this Python code"
   - "Create a new persona for a marketing specialist"
   - "Which persona would be best for writing a technical blog post?"

#### Custom AI Application

```python
from mcp_persona_server import PersonaMCPServer

# Initialize the server
server = PersonaMCPServer()

# Select best persona for a task
best_persona = server.persona_manager.select_best_persona(
    "write a technical blog post about machine learning"
)

if best_persona:
    print(f"Using persona: {best_persona['name']}")
    print(f"Expertise: {', '.join(best_persona['expertise'])}")
    print(f"Style: {best_persona['communication_style']}")
```

## Available Commands

### CLI Commands

- `list` - List all personas
- `create` - Create a new persona
- `get <id>` - Get a specific persona
- `search <query>` - Search personas
- `select <task>` - Select best persona for a task
- `suggestions <task>` - Get persona suggestions
- `update <id>` - Update a persona
- `delete <id>` - Delete a persona
- `stats` - Show statistics
- `demo` - Run demonstration

### MCP Tools

- `list_personas` - List all personas
- `get_persona` - Get a specific persona
- `create_persona` - Create a new persona
- `update_persona` - Update an existing persona
- `delete_persona` - Delete a persona
- `search_personas` - Search personas by query
- `select_best_persona` - Select the best persona for a task
- `get_persona_suggestions` - Get multiple persona suggestions
- `get_persona_statistics` - Get statistics about personas
- `backup_personas` - Create a backup of all personas

## Example Workflows

### 1. Creating a Specialized Persona

```bash
# Create a persona for a specific domain
python cli.py create \
  --name "Cybersecurity Expert" \
  --description "Specialist in cybersecurity and network security" \
  --expertise "Cybersecurity,Network Security,Penetration Testing,Security Analysis" \
  --style "Technical and security-focused" \
  --context "Use when discussing security vulnerabilities, network threats, or security best practices" \
  --traits "vigilant,analytical,security-minded"
```

### 2. AI-Assisted Persona Selection

```python
# In your AI application
task = "Help me write a security policy for my company"
best_persona = server.persona_manager.select_best_persona(task)

if best_persona:
    # Use the persona's characteristics in your AI response
    response = f"""
    As {best_persona['name']}, I'll help you create a comprehensive security policy.

    Based on my expertise in {', '.join(best_persona['expertise'])}, here are the key areas to consider:
    ...
    """
```

### 3. Dynamic Persona Creation

```python
# Create personas on-demand based on user needs
def create_task_specific_persona(task_description):
    # Analyze the task and create a specialized persona
    persona_data = {
        "name": f"Task Specialist - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "description": f"Specialist for: {task_description}",
        "expertise": extract_keywords_from_task(task_description),
        "communication_style": "Task-focused and efficient",
        "context": f"Created specifically for: {task_description}",
        "personality_traits": ["focused", "efficient", "task-oriented"]
    }

    success, persona_id = server.persona_manager.create_persona(persona_data)
    return persona_id if success else None
```

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'mcp'**

   - Solution: Install the MCP Python SDK: `pip install mcp`

2. **Permission Denied on CLI**

   - Solution: Make the CLI executable: `chmod +x cli.py`

3. **No personas found**

   - Solution: The server creates default personas on first run. Check the `personas/` directory.

4. **MCP connection failed**
   - Solution: Ensure the server is running and the MCP configuration is correct.

### Getting Help

- Check the logs in the `personas/` directory
- Run `python cli.py demo` to test functionality
- Review the full documentation in `README.md`

## Next Steps

1. **Explore the examples** in the `examples/` directory
2. **Run the tests** with `python -m pytest tests/`
3. **Customize personas** for your specific use case
4. **Integrate with your AI application** using the MCP protocol

Happy persona management! 🎭

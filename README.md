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

### `get_task_template` ✨ NEW
Get a specific task template for a persona.

**Parameters:**
- `persona_id` (string, required): ID of the persona
- `task_type` (string, required): Type of task template (e.g., "code_review", "system_design", "story_creation")

### `get_communication_guidelines` ✨ NEW
Get detailed communication guidelines for a persona.

**Parameters:**
- `persona_id` (string, required): ID of the persona

### `get_expertise_details` ✨ NEW
Get detailed expertise breakdown for a persona.

**Parameters:**
- `persona_id` (string, required): ID of the persona

### `get_persona_instructions` ✨ NEW
Get comprehensive instructions and behavior patterns for a persona.

**Parameters:**
- `persona_id` (string, required): ID of the persona

### `recommend_persona_for_task` ✨ NEW
Analyze task descriptions and recommend the best persona based on expertise matching.

**Parameters:**
- `task_description` (string, required): Detailed description of the task to be performed
- `task_type` (string, optional): Task type category (e.g., "coding", "writing", "analysis")
- `complexity_level` (string, optional): Task complexity level ("simple", "moderate", "complex", "expert")
- `domain` (string, optional): Domain or industry context

## 🎯 AI-Powered Task Matching

The Persona Manager now includes intelligent task-to-persona matching that analyzes task descriptions and recommends the best persona based on:

### **Smart Matching Algorithm**
- **Expertise Matching**: Direct and partial word matching with persona expertise areas
- **Task Template Analysis**: Checks for relevant task templates in persona definitions
- **Domain Context**: Considers industry and domain-specific requirements
- **Complexity Assessment**: Matches task complexity with persona proficiency levels
- **Keyword Analysis**: Identifies task-specific keywords in detailed instructions

### **Recommendation Features**
- **Confidence Scoring**: Each recommendation includes a confidence score (0-100%)
- **Multiple Options**: Provides top 3 recommendations with reasoning
- **Detailed Analysis**: Explains why each persona is recommended
- **Alternative Suggestions**: Offers backup options if primary recommendations don't fit

### **Example Usage**
```json
{
  "task_description": "Debug a complex Python application with performance issues",
  "task_type": "debugging",
  "complexity_level": "complex",
  "domain": "software development"
}
```

**Result**: Recommends Tech Expert with 85% confidence, highlighting Python expertise and debugging templates.

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

## 🚀 Enhanced Persona Capabilities ✨ NEW

The Persona Manager now includes **enhanced personas** with detailed instructions, behavior patterns, and task templates for superior task performance:

### **🎯 Detailed Instructions & Behavior Patterns**
- **Comprehensive Guidelines**: Each persona includes detailed instructions on how to behave and approach tasks
- **Behavior Patterns**: Specific patterns and approaches each persona should follow
- **Conversation Starters**: Example conversation starters for different scenarios
- **Response Templates**: Template responses for common situations
- **Decision Frameworks**: Structured decision-making approaches

### **📋 Task Templates & Best Practices**
- **Pre-defined Templates**: Step-by-step guides for common tasks
- **Best Practices**: Industry-standard approaches and methodologies
- **Common Pitfalls**: What to avoid and potential challenges
- **Success Metrics**: How to measure success and effectiveness

### **🔧 Enhanced Expertise Details**
- **Proficiency Levels**: Beginner to expert ratings for each skill
- **Sub-skills**: Detailed breakdown of expertise areas
- **Tools & Technologies**: Specific tools and technologies to use
- **Methodologies**: Industry-standard approaches and frameworks

### **💬 Communication Guidelines**
- **Tone & Approach**: Specific communication preferences
- **Formality Levels**: Casual to formal communication styles
- **Explanation Styles**: How to explain concepts (detailed, concise, step-by-step)
- **Response Length**: Preferred response length and detail level

### **📊 Example Enhanced Personas**

#### **Tech Expert** 🖥️
- **Task Templates**: Code review, system design, debugging
- **Expertise Details**: Python (expert), Machine Learning (advanced), Software Architecture (expert)
- **Communication**: Professional, systematic, step-by-step explanations
- **Tools**: Django, Flask, TensorFlow, Docker, AWS

#### **Creative Writer** ✍️
- **Task Templates**: Story creation, brand voice development
- **Expertise Details**: Creative Writing (expert), Marketing Copy (advanced)
- **Communication**: Engaging, story-driven, emotional connections
- **Methodologies**: Three-Act Structure, AIDA, Show Don't Tell

#### **Business Analyst** 📊
- **Task Templates**: Business analysis, market research
- **Expertise Details**: Business Analysis (expert), Data Analysis (advanced)
- **Communication**: Strategic, data-driven, comprehensive analysis
- **Frameworks**: SWOT analysis, Cost-benefit analysis, ROI calculation

### **🎯 Usage Examples**

```bash
# Get task template for code review
get_task_template --persona_id "tech_expert" --task_type "code_review"

# Get communication guidelines
get_communication_guidelines --persona_id "creative_writer"

# Get detailed instructions
get_persona_instructions --persona_id "business_analyst"

# Get expertise breakdown
get_expertise_details --persona_id "tech_expert"
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

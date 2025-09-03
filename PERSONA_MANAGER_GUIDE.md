# Persona Manager Guide

## Overview

The **Persona Manager** is an intelligent dispatcher that automatically selects the most appropriate AI persona based on the task being accomplished. It acts as a smart role manager that analyzes task requirements and context to choose the best persona for any given situation.

## How It Works

### 🎯 **Intelligent Task Analysis**

The Persona Manager analyzes tasks using multiple dimensions:

1. **Domain Identification** - Determines the primary domain (technology, business, creative, education, science, etc.)
2. **Task Classification** - Categorizes tasks into 8 categories (technical, creative, business, educational, design, scientific, consulting, mentoring)
3. **Complexity Assessment** - Evaluates task complexity (low, medium, high)
4. **Urgency Detection** - Identifies urgency levels (low, normal, high)
5. **Audience Analysis** - Determines target audience (technical, business, general, expert)
6. **Output Format Recognition** - Identifies expected output (text, code, analysis, creative, documentation)

### 🧠 **Sophisticated Scoring Algorithm**

The system uses a weighted scoring algorithm that considers:

- **Expertise Matching** (40% weight) - How well persona expertise matches the task
- **Communication Style** (20% weight) - How well the persona's style fits the audience
- **Context Alignment** (20% weight) - How well the persona's context matches the task
- **Task Category Matching** (15% weight) - How well the persona fits the task category
- **Personality Traits** (5% weight) - How well persona traits align with task requirements

### 📊 **Confidence Scoring**

Each persona selection includes a confidence score (0.0-1.0):

- **High Confidence** (>0.5): Strong match, persona is well-suited
- **Medium Confidence** (0.3-0.5): Good match, persona can handle the task
- **Low Confidence** (<0.3): Weak match, consider alternatives or create new persona

## Available Tools

### MCP Tools (for AI Assistants)

#### 1. `dispatch_persona`

**Purpose**: Intelligently select the best persona for a task with detailed reasoning

**Parameters**:

- `task_description` (required): Description of the task to be performed
- `context` (optional): Additional context about the task or user

**Returns**:

- Selected persona with full details
- Confidence score and reasoning
- Task category classification
- Alternative persona suggestions

**Example**:

```json
{
  "task_description": "debug Python code with complex algorithms",
  "context": "working on a machine learning project"
}
```

#### 2. `analyze_task`

**Purpose**: Analyze a task to understand its characteristics and requirements

**Parameters**:

- `task_description` (required): Description of the task to analyze
- `context` (optional): Additional context

**Returns**:

- Domain, complexity, urgency, audience analysis
- Task category classification
- Output format identification

#### 3. `get_dispatcher_analytics`

**Purpose**: Get analytics about persona selection patterns and usage

**Parameters**: None

**Returns**:

- Total selections made
- Persona usage statistics
- Category distribution
- Recent selection history

#### 4. `suggest_persona_improvements`

**Purpose**: Get suggestions for improving personas based on task requirements

**Parameters**:

- `task_description` (required): Task description to analyze

**Returns**:

- Suggestions for new personas
- Expertise gaps to fill
- Domain coverage improvements

### CLI Commands (for Developers)

#### 1. `dispatch`

```bash
python cli.py dispatch "debug Python code" --context "machine learning project"
```

#### 2. `analyze`

```bash
python cli.py analyze "write a creative story" --context "for children"
```

#### 3. `analytics`

```bash
python cli.py analytics
```

#### 4. `improve`

```bash
python cli.py improve "analyze medical data"
```

## Task Categories

### 🖥️ **Technical**

- **Keywords**: debug, code, programming, software, technical, implementation, algorithm, system, architecture
- **Best Personas**: Tech Expert
- **Use Cases**: Code debugging, system design, technical implementation

### 🎨 **Creative**

- **Keywords**: write, story, creative, narrative, content, marketing, copy, brand, imaginative
- **Best Personas**: Creative Writer, Designer
- **Use Cases**: Content creation, storytelling, creative writing

### 💼 **Business**

- **Keywords**: business, analysis, strategy, market, process, optimization, data analysis, insights
- **Best Personas**: Business Analyst, Consultant
- **Use Cases**: Business analysis, strategic planning, market research

### 📚 **Educational**

- **Keywords**: teach, explain, educate, learn, training, curriculum, instructional, pedagogy
- **Best Personas**: Educator, Mentor
- **Use Cases**: Teaching concepts, educational content, training materials

### 🎨 **Design**

- **Keywords**: design, ui, ux, visual, graphic, aesthetic, user experience, interface, branding
- **Best Personas**: Designer
- **Use Cases**: UI/UX design, visual design, brand design

### 🔬 **Scientific**

- **Keywords**: research, scientific, methodology, evidence, analysis, experiment, hypothesis, data
- **Best Personas**: Scientist
- **Use Cases**: Research, data analysis, scientific methodology

### 💡 **Consulting**

- **Keywords**: consult, advise, strategy, problem solving, organizational, change management
- **Best Personas**: Consultant
- **Use Cases**: Business consulting, strategic advice, organizational development

### 🤝 **Mentoring**

- **Keywords**: mentor, coach, guide, support, development, career, leadership, personal development
- **Best Personas**: Mentor
- **Use Cases**: Career guidance, personal development, leadership coaching

## Example Workflows

### 1. **Technical Task**

```
User: "Help me debug this Python code with complex algorithms"
AI: [Calls dispatch_persona]
AI: [Receives Tech Expert with high confidence]
AI: "As a Tech Expert, I'll help you debug this code. Let me analyze the algorithms..."
```

### 2. **Creative Task**

```
User: "Write a creative story about time travel for a science fiction magazine"
AI: [Calls dispatch_persona]
AI: [Receives Creative Writer with high confidence]
AI: "As a Creative Writer, I'll craft an engaging narrative about time travel..."
```

### 3. **Business Task**

```
User: "Analyze quarterly sales data and provide strategic recommendations for executives"
AI: [Calls dispatch_persona]
AI: [Receives Business Analyst with high confidence]
AI: "As a Business Analyst, I'll examine your sales data and provide strategic insights..."
```

### 4. **Educational Task**

```
User: "Explain quantum physics to a beginner high school student"
AI: [Calls dispatch_persona]
AI: [Receives Educator with high confidence]
AI: "As an Educator, I'll explain quantum physics in simple terms that you can understand..."
```

## Integration with AI Assistants

### Claude Desktop Integration

1. **Add to MCP Configuration**:

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

2. **Use in Conversations**:
   - "Use the Persona Manager to help me debug this code"
   - "Dispatch the best persona for writing a creative story"
   - "Analyze this task and select the appropriate persona"

### Custom AI Applications

```python
from mcp_persona_server import PersonaMCPServer

server = PersonaMCPServer()

# Dispatch persona for a task
recommendation = server.persona_dispatcher.select_persona(
    "analyze customer data for business insights",
    "presentation to executive team"
)

if recommendation.confidence_score > 0.5:
    # Use the selected persona
    persona = recommendation.persona_data
    response = f"As {persona['name']}, I'll help you analyze the customer data..."
else:
    # Consider alternatives or create new persona
    alternatives = recommendation.alternative_personas
```

## Analytics and Insights

### Usage Statistics

- **Total selections**: Number of persona dispatches made
- **Persona usage**: How often each persona is selected
- **Average confidence**: Average confidence scores per persona
- **Category distribution**: Distribution of task categories

### Improvement Suggestions

The system automatically suggests improvements based on:

- **Missing personas**: Domains without appropriate personas
- **Expertise gaps**: Skills not covered by existing personas
- **Low confidence selections**: Tasks where no persona fits well

## Advanced Features

### 1. **Multi-Context Analysis**

The system considers both task description and additional context:

```python
# Same task, different contexts
dispatch_persona("analyze data", "for technical audience")  # → Tech Expert
dispatch_persona("analyze data", "for business executives")  # → Business Analyst
dispatch_persona("analyze data", "for educational purposes") # → Educator
```

### 2. **Confidence Thresholds**

- **High confidence** (>0.5): Use persona directly
- **Medium confidence** (0.3-0.5): Use with consideration
- **Low confidence** (<0.3): Consider alternatives or create new persona

### 3. **Alternative Suggestions**

Always provides 3 alternative personas with their strengths and reasoning.

### 4. **Learning and Adaptation**

The system tracks usage patterns and can suggest improvements based on historical data.

## Best Practices

### 1. **Task Description**

- Be specific about the task requirements
- Include relevant keywords for better matching
- Mention the target audience when relevant

### 2. **Context Usage**

- Provide additional context when it affects persona selection
- Include urgency, complexity, or audience information
- Mention domain-specific requirements

### 3. **Confidence Interpretation**

- High confidence: Persona is well-suited, proceed with confidence
- Medium confidence: Persona can handle the task, but consider alternatives
- Low confidence: Consider creating a new persona or using alternatives

### 4. **Continuous Improvement**

- Review analytics regularly
- Implement suggested improvements
- Create new personas for uncovered domains
- Refine existing personas based on usage patterns

## Troubleshooting

### Common Issues

1. **Low Confidence Scores**

   - **Cause**: No persona matches the task well
   - **Solution**: Create a new persona for the domain or task type

2. **Incorrect Persona Selection**

   - **Cause**: Task description lacks specific keywords
   - **Solution**: Be more specific in task description or add context

3. **Missing Domains**
   - **Cause**: No personas exist for certain domains
   - **Solution**: Create personas for uncovered domains (science, legal, healthcare, etc.)

### Getting Help

- Check analytics to understand usage patterns
- Review improvement suggestions for gaps
- Test with different task descriptions and contexts
- Examine the reasoning provided for selections

## Conclusion

The Persona Manager provides intelligent, automated persona selection that:

- **Analyzes tasks comprehensively** across multiple dimensions
- **Scores personas intelligently** using sophisticated algorithms
- **Provides detailed reasoning** for transparency
- **Suggests alternatives** when primary choice isn't optimal
- **Tracks usage patterns** for continuous improvement
- **Integrates seamlessly** with AI assistants via MCP

This system enables AI assistants to automatically adopt the most appropriate persona for any task, improving response quality and user experience.

🎯 **Happy persona dispatching!**

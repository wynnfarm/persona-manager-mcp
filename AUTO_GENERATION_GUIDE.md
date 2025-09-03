# Auto-Generation Guide

## Overview

The Persona Manager now includes **dynamic auto-generation** functionality that automatically creates new personas when existing ones don't match a task well enough. This feature ensures that the system can always provide an appropriate persona for any task, even if no suitable persona exists.

## How It Works

### 1. **Confidence-Based Triggering**

- When dispatching a persona, the system calculates a confidence score (0.0-1.0)
- If the best available persona has a confidence score below the threshold (default: 0.3), auto-generation is triggered
- A new persona is created based on the task requirements and domain

### 2. **Template-Based Generation**

The system uses domain-specific templates to generate appropriate personas:

#### **Technology Domain**

- **Software Engineer**: Programming, system design, technical implementation
- **DevOps Engineer**: Infrastructure, deployment, operations
- **Data Engineer**: Data pipelines, ETL, big data

#### **Science Domain**

- **Research Scientist**: Scientific methodology, experimentation, analysis
- **Medical Researcher**: Clinical studies, healthcare, biomedical
- **Environmental Scientist**: Sustainability, climate research, ecology

#### **Business Domain**

- **Business Strategist**: Strategic planning, market analysis, competitive analysis
- **Financial Analyst**: Financial analysis, investment, risk assessment
- **Operations Manager**: Process optimization, efficiency, supply chain

#### **Creative Domain**

- **Content Creator**: Digital content, social media, branding
- **Visual Designer**: Graphic design, visual communication, brand identity
- **Copywriter**: Persuasive writing, brand messaging, marketing copy

#### **Healthcare Domain**

- **Medical Professional**: Clinical expertise, patient care, medical practice
- **Public Health Specialist**: Community health, epidemiology, health policy

#### **Legal Domain**

- **Legal Advisor**: Legal practice, regulatory compliance, contract law
- **Compliance Specialist**: Risk management, regulatory affairs, audit

#### **Finance Domain**

- **Investment Advisor**: Investment strategies, portfolio management, financial planning
- **Cryptocurrency Expert**: Blockchain, DeFi, digital assets

### 3. **Intelligent Customization**

Generated personas are customized based on:

- **Task keywords**: Extracted from the task description
- **Domain context**: Specific to the identified domain
- **Audience requirements**: Technical, business, general, or expert
- **Complexity level**: Low, medium, or high
- **Urgency**: Low, normal, or high

## Configuration

### **Enable/Disable Auto-Generation**

```bash
# Enable auto-generation
python cli.py auto enable

# Disable auto-generation
python cli.py auto disable
```

### **Set Confidence Threshold**

```bash
# Set threshold to 0.5 (more strict - generates personas more easily)
python cli.py auto threshold --threshold 0.5

# Set threshold to 0.2 (less strict - only generates when really needed)
python cli.py auto threshold --threshold 0.2
```

### **Check Status**

```bash
# View current configuration
python cli.py auto status
```

### **List Generated Personas**

```bash
# View all auto-generated personas
python cli.py auto list
```

## MCP Tools

### **enable_auto_generation**

Enable or disable automatic persona generation.

**Parameters:**

- `enabled` (boolean): Whether to enable auto-generation (default: true)

**Example:**

```json
{
  "enabled": true
}
```

### **set_confidence_threshold**

Set the confidence threshold for auto-generation.

**Parameters:**

- `threshold` (number): Confidence threshold (0.0-1.0)

**Example:**

```json
{
  "threshold": 0.4
}
```

### **get_auto_generation_status**

Get the current auto-generation configuration.

**Returns:**

```json
{
  "enabled": true,
  "confidence_threshold": 0.3,
  "total_generated": 5
}
```

### **list_generated_personas**

List all auto-generated personas.

**Returns:**

```json
{
  "generated_personas": [
    {
      "id": "software_engineer_20241230_143022",
      "name": "Software Engineer",
      "created_at": "2024-12-30T14:30:22.123456",
      "generation_reason": "Low confidence (0.25) for task: develop blockchain application",
      "original_task": "develop blockchain application for supply chain tracking",
      "task_category": "technical"
    }
  ],
  "total_generated": 1
}
```

## Example Workflows

### **Scenario 1: Cryptocurrency Analysis**

```bash
# Task that requires specialized knowledge
python cli.py dispatch "analyze cryptocurrency market trends and provide investment advice" --context "for a fintech startup"

# Result: Auto-generates "Cryptocurrency Expert" persona
# - Domain: Finance
# - Expertise: Cryptocurrency, Blockchain, DeFi, Digital Assets
# - Communication Style: Innovative and technical
```

### **Scenario 2: Medical Research**

```bash
# Task requiring medical expertise
python cli.py dispatch "conduct clinical trials for a new pharmaceutical drug" --context "phase 3 study"

# Result: Auto-generates "Medical Professional" persona
# - Domain: Healthcare
# - Expertise: Medical Practice, Patient Care, Clinical Diagnosis, Healthcare
# - Communication Style: Clinical and compassionate
```

### **Scenario 3: Legal Compliance**

```bash
# Task requiring legal expertise
python cli.py dispatch "create compliance documentation for GDPR regulations" --context "for European market entry"

# Result: Auto-generates "Compliance Specialist" persona
# - Domain: Legal
# - Expertise: Compliance, Risk Management, Regulatory Affairs, Audit
# - Communication Style: Compliance-focused and systematic
```

## Advanced Features

### **1. Template Scoring**

The system scores available templates based on:

- **Category matching**: How well the template category matches the task
- **Keyword matching**: How many task keywords appear in the template expertise
- **Name matching**: How well the template name matches task requirements

### **2. Dynamic Customization**

Generated personas are customized with:

- **Domain-specific expertise**: Added based on the identified domain
- **Task-specific keywords**: Extracted from the task description
- **Audience-appropriate communication style**: Adapted for the target audience
- **Context-specific descriptions**: Enhanced with domain and complexity information

### **3. Metadata Tracking**

Auto-generated personas include:

- **Creation timestamp**: When the persona was generated
- **Generation reason**: Why it was created (low confidence score)
- **Original task**: The task that triggered generation
- **Task category**: The category of the original task
- **Auto-generated flag**: Identifies it as automatically created

### **4. Analytics Integration**

The system tracks:

- **Total generated personas**: Count of all auto-generated personas
- **Usage statistics**: How often auto-generated personas are selected
- **Confidence improvements**: Whether generated personas improve confidence scores

## Best Practices

### **1. Threshold Configuration**

- **Low threshold (0.2-0.3)**: Conservative approach, only generates when really needed
- **Medium threshold (0.3-0.5)**: Balanced approach, generates for moderate mismatches
- **High threshold (0.5+)**: Aggressive approach, generates frequently for better coverage

### **2. Task Description**

- **Be specific**: Include relevant keywords for better template matching
- **Include context**: Provide additional context for better customization
- **Mention domain**: Explicitly mention the domain when relevant

### **3. Monitoring**

- **Regular status checks**: Monitor auto-generation status and statistics
- **Review generated personas**: Periodically review and refine auto-generated personas
- **Adjust thresholds**: Fine-tune thresholds based on usage patterns

### **4. Quality Control**

- **Review generated personas**: Check that auto-generated personas are appropriate
- **Refine templates**: Update templates based on generated persona quality
- **Manual adjustments**: Manually improve auto-generated personas when needed

## Troubleshooting

### **Common Issues**

#### **1. Too Many Personas Generated**

**Cause**: Threshold set too low
**Solution**: Increase confidence threshold

```bash
python cli.py auto threshold --threshold 0.5
```

#### **2. Poor Quality Generated Personas**

**Cause**: Task description lacks specific keywords
**Solution**: Be more specific in task descriptions

```
# Instead of: "help with coding"
# Use: "debug Python code with machine learning algorithms"
```

#### **3. Auto-Generation Not Working**

**Cause**: Feature disabled or threshold too high
**Solution**: Check status and enable if needed

```bash
python cli.py auto status
python cli.py auto enable
```

#### **4. Duplicate Personas Generated**

**Cause**: Similar tasks triggering generation multiple times
**Solution**: Review and consolidate similar personas manually

### **Debugging Commands**

```bash
# Check auto-generation status
python cli.py auto status

# List all generated personas
python cli.py auto list

# Test with specific threshold
python cli.py auto threshold --threshold 0.4
python cli.py dispatch "your task here"

# Check analytics
python cli.py analytics
```

## Integration Examples

### **Claude Desktop Integration**

```json
{
  "mcpServers": {
    "persona-server": {
      "command": "python",
      "args": ["-m", "mcp_persona_server"],
      "env": {
        "PERSONA_STORAGE_PATH": "./personas"
      }
    }
  }
}
```

### **Custom AI Application**

```python
from mcp_persona_server import PersonaMCPServer

# Initialize server with auto-generation
server = PersonaMCPServer()

# Configure auto-generation
server.persona_dispatcher.enable_auto_generation(True)
server.persona_dispatcher.set_confidence_threshold(0.3)

# Dispatch persona (may trigger auto-generation)
recommendation = server.persona_dispatcher.select_persona(
    "analyze quantum computing algorithms",
    "for cybersecurity research"
)

# Check if persona was auto-generated
if recommendation.persona_data.get('auto_generated', False):
    print(f"Auto-generated: {recommendation.persona_data['name']}")
```

## Summary

The auto-generation feature provides:

✅ **Automatic persona creation** when confidence is low
✅ **Domain-specific templates** for appropriate persona generation
✅ **Intelligent customization** based on task requirements
✅ **Configurable thresholds** for different use cases
✅ **Comprehensive tracking** of generated personas
✅ **Easy management** through CLI and MCP tools

This ensures that the Persona Manager can always provide an appropriate persona for any task, making it truly dynamic and adaptive to user needs.

🎯 **Happy auto-generating!**

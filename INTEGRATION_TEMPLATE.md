# 🚀 MCP Integration Template - Plug & Play Setup

This template provides a simple, plug-and-play way to integrate any new project with the Context Manager and Persona Manager MCPs for real-time context awareness.

## 📋 Quick Setup Checklist

### 1. **Project Registration** (2 minutes)

```bash
# Create your project in Context Manager
curl -X POST "http://localhost:8000/project/YOUR_PROJECT_NAME/update" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Your project goal here"
  }'
```

### 2. **Environment Configuration** (1 minute)

Add these environment variables to your project:

```bash
# Context Manager Integration
export CONTEXT_MANAGER_URL="http://localhost:8000"
export CONTEXT_PROJECT_NAME="YOUR_PROJECT_NAME"

# Persona Manager Integration
export PERSONA_MANAGER_URL="http://localhost:8002"
```

### 3. **Integration Code** (5 minutes)

Copy this integration class to your project:

```python
#!/usr/bin/env python3
"""
MCP Integration Template - Plug & Play Context Awareness
Copy this file to your project and customize as needed.
"""

import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class MCPIntegration:
    """
    Plug-and-play integration with Context Manager and Persona Manager MCPs.
    Provides real-time context awareness for any project.
    """

    def __init__(self, project_name: str, context_manager_url: str = None, persona_manager_url: str = None):
        self.project_name = project_name
        self.context_manager_url = context_manager_url or "http://localhost:8000"
        self.persona_manager_url = persona_manager_url or "http://localhost:8002"

    def get_project_context(self) -> Optional[Dict[str, Any]]:
        """Get current project context from Context Manager."""
        try:
            response = requests.get(f"{self.context_manager_url}/project/{self.project_name}")
            if response.status_code == 200:
                return response.json().get("data", {}).get("context", {})
            return None
        except Exception as e:
            logger.error(f"Error getting project context: {e}")
            return None

    def select_persona_for_task(self, task_description: str, domain: str = None) -> Optional[Dict[str, Any]]:
        """Select the best persona for a task with real-time context awareness."""
        try:
            payload = {
                "task_description": task_description,
                "domain": domain or self.project_name,
                "project_name": self.project_name
            }

            response = requests.post(
                f"{self.persona_manager_url}/select",
                json=payload
            )

            if response.status_code == 200:
                return response.json().get("data", {})
            return None
        except Exception as e:
            logger.error(f"Error selecting persona: {e}")
            return None

    def complete_task(self, task_description: str, result: str, persona_id: str) -> bool:
        """Complete a task and update context in both MCPs."""
        try:
            # Update Context Manager
            self.update_context_feature(task_description)

            # Update Persona Manager
            payload = {
                "project": self.project_name,
                "task_description": task_description,
                "result": result,
                "persona_id": persona_id
            }

            response = requests.post(
                f"{self.persona_manager_url}/complete-task",
                json=payload
            )

            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return False

    def update_context_feature(self, feature: str) -> bool:
        """Add a completed feature to project context."""
        try:
            response = requests.post(
                f"{self.context_manager_url}/project/{self.project_name}/complete-feature",
                json={"feature": feature}
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error updating context feature: {e}")
            return False

    def add_context_issue(self, issue: str) -> bool:
        """Add an issue to project context."""
        try:
            response = requests.post(
                f"{self.context_manager_url}/project/{self.project_name}/update",
                json={"issue": issue}
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error adding context issue: {e}")
            return False

    def add_context_step(self, step: str) -> bool:
        """Add a next step to project context."""
        try:
            response = requests.post(
                f"{self.context_manager_url}/project/{self.project_name}/update",
                json={"next_step": step}
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error adding context step: {e}")
            return False

    def get_task_suggestions(self) -> List[str]:
        """Get task suggestions based on project context."""
        try:
            response = requests.get(f"{self.persona_manager_url}/context/{self.project_name}/suggestions")
            if response.status_code == 200:
                return response.json().get("data", {}).get("suggestions", [])
            return []
        except Exception as e:
            logger.error(f"Error getting task suggestions: {e}")
            return []

    def get_project_analytics(self) -> Optional[Dict[str, Any]]:
        """Get project analytics from Context Manager."""
        try:
            response = requests.get(f"{self.context_manager_url}/analytics/overview")
            if response.status_code == 200:
                data = response.json().get("data", {})
                # Find our project in the summaries
                for project in data.get("project_summaries", []):
                    if project.get("name") == self.project_name:
                        return project
            return None
        except Exception as e:
            logger.error(f"Error getting project analytics: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    # Initialize integration for your project
    integration = MCPIntegration("your-project-name")

    # Get current context
    context = integration.get_project_context()
    print(f"Project context: {context}")

    # Select persona for a task
    persona = integration.select_persona_for_task("Implement user authentication")
    print(f"Selected persona: {persona}")

    # Complete a task
    success = integration.complete_task(
        "Implement user authentication",
        "Created JWT-based auth system with role-based access",
        persona.get("selected_persona", "tech_expert")
    )
    print(f"Task completion: {success}")

    # Get task suggestions
    suggestions = integration.get_task_suggestions()
    print(f"Task suggestions: {suggestions}")
```

## 🎯 Usage Examples

### Basic Integration

```python
from mcp_integration import MCPIntegration

# Initialize for your project
mcp = MCPIntegration("my-awesome-project")

# Get context-aware persona selection
persona = mcp.select_persona_for_task("Design database schema")
print(f"Best persona: {persona['selected_persona']}")

# Complete tasks with automatic context updates
mcp.complete_task(
    "Design database schema",
    "Created normalized schema with proper relationships",
    persona['selected_persona']
)
```

### Advanced Integration

```python
# Get project insights
analytics = mcp.get_project_analytics()
print(f"Project completion: {analytics['completion']}%")

# Get context-driven task suggestions
suggestions = mcp.get_task_suggestions()
for suggestion in suggestions:
    print(f"Suggested task: {suggestion}")

# Add project issues and next steps
mcp.add_context_issue("Need to optimize database queries")
mcp.add_context_step("Implement caching layer")
```

## 🔧 Customization Options

### Custom Context Analysis

```python
class CustomMCPIntegration(MCPIntegration):
    def analyze_task_with_context(self, task: str) -> Dict[str, Any]:
        """Custom task analysis using project context."""
        context = self.get_project_context()

        # Your custom analysis logic here
        analysis = {
            "priority": "high" if "urgent" in task.lower() else "medium",
            "domain": context.get("domain", "general"),
            "estimated_effort": self._estimate_effort(task, context)
        }

        return analysis

    def _estimate_effort(self, task: str, context: Dict[str, Any]) -> str:
        """Estimate task effort based on context."""
        # Your custom effort estimation logic
        return "medium"
```

### Custom Persona Selection

```python
def select_custom_persona(self, task: str, requirements: List[str]) -> str:
    """Custom persona selection with specific requirements."""
    # Get context-aware persona
    persona = self.select_persona_for_task(task)

    # Apply custom filtering based on requirements
    if "security" in requirements and "security_expert" in persona.get("expertise", []):
        return "security_expert"

    return persona.get("selected_persona")
```

## 📊 Integration Benefits

### ✅ **Real-time Context Awareness**

- Persona selection considers current project state
- Task suggestions based on project goals and issues
- Automatic context updates when tasks are completed

### ✅ **Seamless Integration**

- No complex setup required
- Works with any project type
- Minimal code changes needed

### ✅ **Advanced Analytics**

- Project progress tracking
- Persona performance metrics
- Context change frequency analysis

### ✅ **Scalable Architecture**

- Works with multiple projects
- Handles concurrent requests
- Easy to extend and customize

## 🚀 Getting Started

1. **Copy the integration template** to your project
2. **Set environment variables** for MCP URLs
3. **Initialize the integration** with your project name
4. **Start using context-aware features** immediately

## 📝 API Reference

### Core Methods

- `get_project_context()` - Get current project context
- `select_persona_for_task(task, domain)` - Get context-aware persona selection
- `complete_task(task, result, persona)` - Complete task with context updates
- `get_task_suggestions()` - Get context-driven task suggestions
- `get_project_analytics()` - Get project analytics and metrics

### Context Management

- `update_context_feature(feature)` - Add completed feature
- `add_context_issue(issue)` - Add project issue
- `add_context_step(step)` - Add next step

## 🔍 Troubleshooting

### Common Issues

1. **Connection refused**: Check if MCP services are running
2. **Project not found**: Ensure project is registered in Context Manager
3. **Persona selection fails**: Check Persona Manager service status

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed logs of MCP communication
mcp = MCPIntegration("your-project")
```

## 📈 Next Steps

1. **Customize the integration** for your specific needs
2. **Add custom analysis methods** for your domain
3. **Integrate with your existing workflow**
4. **Monitor and optimize** persona selection performance

---

**🎉 That's it! You now have real-time context awareness for your project.**

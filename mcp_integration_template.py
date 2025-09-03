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

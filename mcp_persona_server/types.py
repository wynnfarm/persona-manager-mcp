"""
Shared types and data structures for the MCP Persona Server.

This module contains common data structures used across multiple modules
to avoid circular import issues.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


class TaskCategory(Enum):
    """Categories for different types of tasks."""
    TECHNICAL = "technical"
    CREATIVE = "creative"
    BUSINESS = "business"
    EDUCATIONAL = "educational"
    DESIGN = "design"
    SCIENTIFIC = "scientific"
    CONSULTING = "consulting"
    MENTORING = "mentoring"
    GENERAL = "general"


@dataclass
class TaskContext:
    """Context information about a task."""
    task_description: str
    user_context: str
    domain: str
    complexity: str
    urgency: str
    audience: str
    output_format: str


@dataclass
class PersonaRecommendation:
    """Recommendation result from persona selection."""
    persona_id: str
    persona_data: Dict[str, Any]
    confidence_score: float
    reasoning: str
    alternative_personas: List[Dict[str, Any]]
    task_category: TaskCategory

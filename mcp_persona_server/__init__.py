"""
MCP Persona Server

A Model Context Protocol server for managing AI personas.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .server import PersonaMCPServer
from .persona_manager import PersonaManager
from .storage import PersonaStorage
from .persona_dispatcher import PersonaDispatcher
from .persona_generator import PersonaGenerator
from .types import TaskContext, TaskCategory, PersonaRecommendation

__all__ = ["PersonaMCPServer", "PersonaManager", "PersonaStorage", "PersonaDispatcher", "PersonaGenerator", "TaskContext", "TaskCategory", "PersonaRecommendation"]

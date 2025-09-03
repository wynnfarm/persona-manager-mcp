"""
Main MCP server implementation for persona management.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence
from datetime import datetime

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    LoggingLevel,
)

from .persona_manager import PersonaManager
from .storage import PersonaStorage
from .persona_dispatcher import PersonaDispatcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersonaMCPServer:
    """MCP server for persona management."""
    
    def __init__(self, storage_path: str = "./personas"):
        self.storage = PersonaStorage(storage_path)
        self.persona_manager = PersonaManager(self.storage)
        self.persona_dispatcher = PersonaDispatcher(self.persona_manager)
        self.server = Server("persona-server")
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register all available tools with the MCP server."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List all available tools."""
            tools = [
                Tool(
                    name="list_personas",
                    description="List all available personas",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_metadata": {
                                "type": "boolean",
                                "description": "Include metadata in response",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="get_persona",
                    description="Get a specific persona by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "persona_id": {
                                "type": "string",
                                "description": "The ID of the persona to retrieve"
                            }
                        },
                        "required": ["persona_id"]
                    }
                ),
                Tool(
                    name="create_persona",
                    description="Create a new persona",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the persona"
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the persona"
                            },
                            "expertise": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Areas of expertise"
                            },
                            "communication_style": {
                                "type": "string",
                                "description": "Communication style of the persona"
                            },
                            "context": {
                                "type": "string",
                                "description": "When to use this persona"
                            },
                            "personality_traits": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Personality traits"
                            }
                        },
                        "required": ["name", "description", "expertise"]
                    }
                ),
                Tool(
                    name="update_persona",
                    description="Update an existing persona",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "persona_id": {
                                "type": "string",
                                "description": "The ID of the persona to update"
                            },
                            "updates": {
                                "type": "object",
                                "description": "Fields to update"
                            }
                        },
                        "required": ["persona_id", "updates"]
                    }
                ),
                Tool(
                    name="delete_persona",
                    description="Delete a persona",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "persona_id": {
                                "type": "string",
                                "description": "The ID of the persona to delete"
                            }
                        },
                        "required": ["persona_id"]
                    }
                ),
                Tool(
                    name="search_personas",
                    description="Search personas by criteria",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "expertise": {
                                "type": "string",
                                "description": "Filter by expertise area"
                            },
                            "style": {
                                "type": "string",
                                "description": "Filter by communication style"
                            }
                        }
                    }
                ),
                Tool(
                    name="select_persona",
                    description="Select the best persona for a task using context-aware analysis",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Description of the task"
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context for the task",
                                "default": ""
                            }
                        },
                        "required": ["task_description"]
                    }
                ),
                Tool(
                    name="complete_task",
                    description="Complete a task and update project context",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Description of the completed task"
                            },
                            "result": {
                                "type": "string",
                                "description": "Result or outcome of the task"
                            },
                            "persona_id": {
                                "type": "string",
                                "description": "ID of the persona that completed the task"
                            }
                        },
                        "required": ["task_description", "result", "persona_id"]
                    }
                ),
                Tool(
                    name="get_context_summary",
                    description="Get a summary of current project context",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="suggest_task_priorities",
                    description="Get task priority suggestions based on project context",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="select_best_persona",
                    description="Intelligently select the best persona for a task",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Description of the task"
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context",
                                "default": ""
                            }
                        },
                        "required": ["task_description"]
                    }
                ),
                Tool(
                    name="get_persona_suggestions",
                    description="Get multiple persona suggestions for a task",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Description of the task"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of suggestions",
                                "default": 3
                            }
                        },
                        "required": ["task_description"]
                    }
                ),
                Tool(
                    name="get_persona_statistics",
                    description="Get statistics about stored personas",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="backup_personas",
                    description="Create a backup of all personas",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "backup_path": {
                                "type": "string",
                                "description": "Path for the backup file",
                                "default": "./personas_backup.json"
                            }
                        }
                    }
                ),
                Tool(
                    name="dispatch_persona",
                    description="Intelligently dispatch the best persona for a task with detailed reasoning",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Description of the task to be performed"
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context about the task or user",
                                "default": ""
                            }
                        },
                        "required": ["task_description"]
                    }
                ),
                Tool(
                    name="analyze_task",
                    description="Analyze a task to understand its characteristics and requirements",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Description of the task to analyze"
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context",
                                "default": ""
                            }
                        },
                        "required": ["task_description"]
                    }
                ),
                Tool(
                    name="get_dispatcher_analytics",
                    description="Get analytics about persona selection patterns and usage",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="suggest_persona_improvements",
                    description="Get suggestions for improving personas based on task requirements",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Task description to analyze for improvement suggestions"
                            }
                        },
                        "required": ["task_description"]
                    }
                ),
                Tool(
                    name="enable_auto_generation",
                    description="Enable or disable automatic persona generation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "enabled": {
                                "type": "boolean",
                                "description": "Whether to enable auto-generation",
                                "default": True
                            }
                        }
                    }
                ),
                Tool(
                    name="set_confidence_threshold",
                    description="Set the confidence threshold for auto-generation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "threshold": {
                                "type": "number",
                                "description": "Confidence threshold (0.0-1.0)",
                                "minimum": 0.0,
                                "maximum": 1.0
                            }
                        },
                        "required": ["threshold"]
                    }
                ),
                Tool(
                    name="get_auto_generation_status",
                    description="Get the current auto-generation configuration",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="list_generated_personas",
                    description="List all auto-generated personas",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls."""
            try:
                if name == "list_personas":
                    return await self._handle_list_personas(arguments)
                elif name == "get_persona":
                    return await self._handle_get_persona(arguments)
                elif name == "create_persona":
                    return await self._handle_create_persona(arguments)
                elif name == "update_persona":
                    return await self._handle_update_persona(arguments)
                elif name == "delete_persona":
                    return await self._handle_delete_persona(arguments)
                elif name == "search_personas":
                    return await self._handle_search_personas(arguments)
                elif name == "select_best_persona":
                    return await self._handle_select_best_persona(arguments)
                elif name == "get_persona_suggestions":
                    return await self._handle_get_persona_suggestions(arguments)
                elif name == "get_persona_statistics":
                    return await self._handle_get_persona_statistics(arguments)
                elif name == "backup_personas":
                    return await self._handle_backup_personas(arguments)
                elif name == "dispatch_persona":
                    return await self._handle_dispatch_persona(arguments)
                elif name == "analyze_task":
                    return await self._handle_analyze_task(arguments)
                elif name == "get_dispatcher_analytics":
                    return await self._handle_get_dispatcher_analytics(arguments)
                elif name == "suggest_persona_improvements":
                    return await self._handle_suggest_persona_improvements(arguments)
                elif name == "enable_auto_generation":
                    return await self._handle_enable_auto_generation(arguments)
                elif name == "set_confidence_threshold":
                    return await self._handle_set_confidence_threshold(arguments)
                elif name == "get_auto_generation_status":
                    return await self._handle_get_auto_generation_status(arguments)
                elif name == "list_generated_personas":
                    return await self._handle_list_generated_personas(arguments)
                elif name == "select_persona":
                    return await self._handle_select_persona(arguments)
                elif name == "complete_task":
                    return await self._handle_complete_task(arguments)
                elif name == "get_context_summary":
                    return await self._handle_get_context_summary(arguments)
                elif name == "suggest_task_priorities":
                    return await self._handle_suggest_task_priorities(arguments)
                else:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                        isError=True
                    )
            except Exception as e:
                logger.error(f"Error handling tool call {name}: {e}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
    
    async def _handle_list_personas(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle list_personas tool call."""
        include_metadata = arguments.get("include_metadata", False)
        personas = self.persona_manager.get_all_personas()
        
        if include_metadata:
            metadata = self.storage.get_metadata()
            result = {
                "personas": personas,
                "metadata": metadata
            }
        else:
            result = {"personas": personas}
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))]
        )
    
    async def _handle_get_persona(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get_persona tool call."""
        persona_id = arguments["persona_id"]
        persona = self.persona_manager.get_persona(persona_id)
        
        if persona:
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(persona, indent=2))]
            )
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Persona '{persona_id}' not found")],
                isError=True
            )
    
    async def _handle_create_persona(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle create_persona tool call."""
        success, result = self.persona_manager.create_persona(arguments)
        
        if success:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Persona created successfully with ID: {result}")]
            )
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Failed to create persona: {result}")],
                isError=True
            )
    
    async def _handle_update_persona(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle update_persona tool call."""
        persona_id = arguments["persona_id"]
        updates = arguments["updates"]
        
        success, message = self.persona_manager.update_persona(persona_id, updates)
        
        if success:
            return CallToolResult(
                content=[TextContent(type="text", text=message)]
            )
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=message)],
                isError=True
            )
    
    async def _handle_delete_persona(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle delete_persona tool call."""
        persona_id = arguments["persona_id"]
        success, message = self.persona_manager.delete_persona(persona_id)
        
        if success:
            return CallToolResult(
                content=[TextContent(type="text", text=message)]
            )
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=message)],
                isError=True
            )
    
    async def _handle_search_personas(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle search_personas tool call."""
        query = arguments["query"]
        results = self.persona_manager.search_personas(query)
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(results, indent=2))]
        )
    
    async def _handle_select_best_persona(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle select_best_persona tool call."""
        task_description = arguments["task_description"]
        context = arguments.get("context", "")
        
        best_persona = self.persona_manager.select_best_persona(task_description, context)
        
        if best_persona:
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(best_persona, indent=2))]
            )
        else:
            return CallToolResult(
                content=[TextContent(type="text", text="No suitable persona found for the given task")],
                isError=True
            )
    
    async def _handle_get_persona_suggestions(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get_persona_suggestions tool call."""
        task_description = arguments["task_description"]
        limit = arguments.get("limit", 3)
        
        suggestions = self.persona_manager.get_persona_suggestions(task_description, limit)
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(suggestions, indent=2))]
        )
    
    async def _handle_get_persona_statistics(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get_persona_statistics tool call."""
        stats = self.persona_manager.get_persona_statistics()
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(stats, indent=2))]
        )
    
    async def _handle_backup_personas(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle backup_personas tool call."""
        backup_path = arguments.get("backup_path", "./personas_backup.json")
        success = self.storage.backup_personas(backup_path)
        
        if success:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Backup created successfully at: {backup_path}")]
            )
        else:
            return CallToolResult(
                content=[TextContent(type="text", text="Failed to create backup")],
                isError=True
            )
    
    async def _handle_dispatch_persona(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle dispatch_persona tool call."""
        task_description = arguments["task_description"]
        context = arguments.get("context", "")
        
        try:
            recommendation = self.persona_dispatcher.select_persona(task_description, context)
            
            result = {
                "selected_persona": {
                    "id": recommendation.persona_id,
                    "name": recommendation.persona_data["name"],
                    "description": recommendation.persona_data["description"],
                    "expertise": recommendation.persona_data.get("expertise", []),
                    "communication_style": recommendation.persona_data.get("communication_style", ""),
                    "context": recommendation.persona_data.get("context", "")
                },
                "confidence_score": recommendation.confidence_score,
                "reasoning": recommendation.reasoning,
                "task_category": recommendation.task_category.value,
                "context_insights": recommendation.persona_data.get("context_insights", []),
                "alternative_personas": [
                    {
                        "name": p["name"],
                        "description": p["description"],
                        "expertise": p.get("expertise", [])
                    }
                    for p in recommendation.alternative_personas
                ]
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
        except Exception as e:
            logger.error(f"Error dispatching persona: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error dispatching persona: {str(e)}")],
                isError=True
            )
    
    async def _handle_select_persona(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle select_persona tool call with context-aware analysis."""
        task_description = arguments["task_description"]
        context = arguments.get("context", "")
        
        try:
            recommendation = self.persona_dispatcher.select_persona(task_description, context)
            
            result = {
                "selected_persona": {
                    "id": recommendation.persona_id,
                    "name": recommendation.persona_data["name"],
                    "description": recommendation.persona_data["description"],
                    "expertise": recommendation.persona_data.get("expertise", []),
                    "communication_style": recommendation.persona_data.get("communication_style", ""),
                    "context": recommendation.persona_data.get("context", "")
                },
                "confidence_score": recommendation.confidence_score,
                "reasoning": recommendation.reasoning,
                "task_category": recommendation.task_category.value,
                "context_insights": recommendation.persona_data.get("context_insights", []),
                "alternative_personas": [
                    {
                        "id": alt["id"],
                        "name": alt["name"],
                        "description": alt["description"],
                        "expertise": alt.get("expertise", []),
                        "communication_style": alt.get("communication_style", ""),
                        "context": alt.get("context", "")
                    }
                    for alt in recommendation.alternative_personas
                ]
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error selecting persona: {str(e)}")],
                isError=True
            )
    
    async def _handle_complete_task(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle complete_task tool call."""
        task_description = arguments["task_description"]
        result = arguments["result"]
        persona_id = arguments["persona_id"]
        
        try:
            success = self.persona_dispatcher.complete_task_with_context_update(
                task_description, result, persona_id
            )
            
            if success:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Task completed and context updated successfully")]
                )
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text="Task completed but context update failed")],
                    isError=True
                )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error completing task: {str(e)}")],
                isError=True
            )
    
    async def _handle_get_context_summary(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get_context_summary tool call."""
        try:
            summary = self.persona_dispatcher.get_context_summary()
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(summary, indent=2))]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error getting context summary: {str(e)}")],
                isError=True
            )
    
    async def _handle_suggest_task_priorities(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle suggest_task_priorities tool call."""
        try:
            suggestions = self.persona_dispatcher.suggest_task_priorities()
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(suggestions, indent=2))]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error getting task priorities: {str(e)}")],
                isError=True
            )
    
    async def _handle_analyze_task(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle analyze_task tool call."""
        task_description = arguments["task_description"]
        context = arguments.get("context", "")
        
        try:
            task_context = self.persona_dispatcher.analyze_task(task_description, context)
            task_category = self.persona_dispatcher.classify_task(task_context)
            
            result = {
                "task_description": task_context.task_description,
                "user_context": task_context.user_context,
                "domain": task_context.domain,
                "complexity": task_context.complexity,
                "urgency": task_context.urgency,
                "audience": task_context.audience,
                "output_format": task_context.output_format,
                "task_category": task_category.value
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
        except Exception as e:
            logger.error(f"Error analyzing task: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error analyzing task: {str(e)}")],
                isError=True
            )
    
    async def _handle_get_dispatcher_analytics(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get_dispatcher_analytics tool call."""
        try:
            analytics = self.persona_dispatcher.get_selection_analytics()
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(analytics, indent=2))]
            )
        except Exception as e:
            logger.error(f"Error getting dispatcher analytics: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error getting analytics: {str(e)}")],
                isError=True
            )
    
    async def _handle_suggest_persona_improvements(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle suggest_persona_improvements tool call."""
        task_description = arguments["task_description"]
        
        try:
            suggestions = self.persona_dispatcher.suggest_persona_improvements(task_description)
            
            result = {
                "task_description": task_description,
                "suggestions": suggestions,
                "total_suggestions": len(suggestions)
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
        except Exception as e:
            logger.error(f"Error suggesting improvements: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error suggesting improvements: {str(e)}")],
                isError=True
            )
    
    async def _handle_enable_auto_generation(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle enable_auto_generation tool call."""
        enabled = arguments.get("enabled", True)
        
        try:
            self.persona_dispatcher.enable_auto_generation(enabled)
            
            result = {
                "enabled": enabled,
                "message": f"Auto-generation {'enabled' if enabled else 'disabled'}"
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
        except Exception as e:
            logger.error(f"Error enabling auto-generation: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")],
                isError=True
            )
    
    async def _handle_set_confidence_threshold(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle set_confidence_threshold tool call."""
        threshold = arguments["threshold"]
        
        try:
            self.persona_dispatcher.set_confidence_threshold(threshold)
            
            result = {
                "threshold": threshold,
                "message": f"Confidence threshold set to {threshold}"
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
        except Exception as e:
            logger.error(f"Error setting confidence threshold: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")],
                isError=True
            )
    
    async def _handle_get_auto_generation_status(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle get_auto_generation_status tool call."""
        try:
            status = self.persona_dispatcher.get_auto_generation_status()
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(status, indent=2))]
            )
        except Exception as e:
            logger.error(f"Error getting auto-generation status: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")],
                isError=True
            )
    
    async def _handle_list_generated_personas(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle list_generated_personas tool call."""
        try:
            generated_personas = self.persona_dispatcher.list_generated_personas()
            
            result = {
                "generated_personas": generated_personas,
                "total_generated": len(generated_personas)
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
        except Exception as e:
            logger.error(f"Error listing generated personas: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")],
                isError=True
            )
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="persona-server",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities=None,
                    ),
                ),
            )


async def main():
    """Main entry point."""
    server = PersonaMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

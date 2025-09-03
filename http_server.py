#!/usr/bin/env python3
"""
HTTP server for persona-manager analytics and API endpoints.
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from mcp_persona_server.persona_manager import PersonaManager
from mcp_persona_server.storage import PersonaStorage
from mcp_persona_server.persona_dispatcher import PersonaDispatcher
from mcp_persona_server.types import TaskContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Persona Manager HTTP API",
    description="HTTP API for persona management and analytics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")

# Initialize persona components
storage_path = os.getenv("PERSONA_STORAGE_PATH", "./personas")
storage = PersonaStorage(storage_path)
persona_manager = PersonaManager(storage)
persona_dispatcher = PersonaDispatcher(persona_manager)

def create_response(success: bool, message: str, data: Any = None) -> Dict[str, Any]:
    """Create a standardized API response."""
    return {
        "success": success,
        "message": message,
        "data": data,
        "metadata": {
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "service": "persona-manager"
        }
    }

@app.get("/")
async def root():
    """Serve the persona manager dashboard."""
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        return create_response(
            success=False,
            message="Dashboard not available",
            data={"error": str(e)}
        )

@app.get("/health")
async def health():
    """Health check endpoint."""
    return create_response(
        success=True,
        message="Persona Manager is healthy",
        data={
            "status": "healthy",
            "personas_count": len(persona_manager.get_all_personas()),
            "storage_type": "file"
        }
    )

@app.get("/test-context")
async def test_context():
    """Test endpoint to verify route registration."""
    return create_response(
        success=True,
        message="Context test endpoint working",
        data={"test": "success"}
    )

@app.get("/context/{project_name}")
async def get_project_context(project_name: str):
    """Get project context from Context Manager."""
    try:
        logger.info(f"Getting context for project: {project_name}")
        # Test if the method exists
        if not hasattr(persona_dispatcher, 'get_context_summary_for_project'):
            logger.error("Method get_context_summary_for_project not found")
            raise HTTPException(status_code=500, detail="Method not found")
        
        context_summary = persona_dispatcher.get_context_summary_for_project(project_name)
        logger.info(f"Context summary result: {context_summary}")
        if context_summary:
            return create_response(
                success=True,
                message=f"Context retrieved for project '{project_name}'",
                data=context_summary
            )
        else:
            raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found or no context available")
    except Exception as e:
        logger.error(f"Error getting context for project {project_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/context/{project_name}/suggestions")
async def get_task_suggestions(project_name: str):
    """Get task suggestions based on project context."""
    try:
        suggestions = persona_dispatcher.get_task_suggestions_for_project(project_name)
        return create_response(
            success=True,
            message=f"Task suggestions retrieved for project '{project_name}'",
            data={"suggestions": suggestions}
        )
    except Exception as e:
        logger.error(f"Error getting task suggestions for project {project_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personas")
async def list_personas(search: str = None, domain: str = None, expertise: str = None, limit: int = 50):
    """List all available personas."""
    try:
        all_personas = persona_manager.get_all_personas()
        personas = dict(all_personas)
        
        # Apply filters
        if search:
            search_results = persona_manager.search_personas(search)
            search_ids = {p.get('id', '') for p in search_results}
            personas = {k: v for k, v in personas.items() if k in search_ids}
        
        if domain:
            personas = {k: v for k, v in personas.items() 
                       if domain.lower() in (v.get('context', '') + ' ' + v.get('description', '')).lower()}
        
        if expertise:
            personas = {k: v for k, v in personas.items() 
                       if any(expertise.lower() in exp.lower() for exp in v.get('expertise', []))}
        
        # Apply limit
        if limit and limit < len(personas):
            personas = dict(list(personas.items())[:limit])
        
        return create_response(
            success=True,
            message=f"Retrieved {len(personas)} personas",
            data={
                "personas": personas,
                "count": len(personas),
                "total_available": len(all_personas),
                "filters_applied": {
                    "search": search,
                    "domain": domain,
                    "expertise": expertise,
                    "limit": limit
                }
            }
        )
    except Exception as e:
        logger.error(f"Error listing personas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personas/{persona_id}")
async def get_persona(persona_id: str):
    """Get a specific persona by ID."""
    try:
        persona = persona_manager.get_persona(persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        return create_response(
            success=True,
            message="Persona retrieved successfully",
            data=persona
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting persona {persona_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/personas/{persona_id}")
async def update_persona(persona_id: str, persona_data: Dict[str, Any]):
    """Update or create a persona."""
    try:
        # Ensure the persona_id in the URL matches the data
        persona_data["id"] = persona_id
        
        # Save the persona
        success, message = persona_manager.create_persona(persona_data)
        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        return create_response(
            success=True,
            message="Persona saved successfully",
            data=persona_data
        )
    except Exception as e:
        logger.error(f"Error saving persona {persona_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/personas/{persona_id}")
async def delete_persona(persona_id: str):
    """Delete a persona."""
    try:
        success, message = persona_manager.delete_persona(persona_id)
        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        return create_response(
            success=True,
            message="Persona deleted successfully",
            data={"persona_id": persona_id}
        )
    except Exception as e:
        logger.error(f"Error deleting persona {persona_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics():
    """Get persona selection analytics."""
    try:
        analytics = persona_dispatcher.get_selection_analytics()
        return create_response(
            success=True,
            message="Persona analytics retrieved successfully",
            data=analytics
        )
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/analytics/usage")
async def get_usage_analytics():
    """Get detailed persona usage analytics."""
    try:
        analytics = persona_dispatcher.get_selection_analytics()
        
        # Add additional usage insights
        usage_insights = []
        
        if analytics["total_selections"] > 0:
            # Most used persona
            if analytics["persona_usage"]:
                most_used = max(analytics["persona_usage"].items(), key=lambda x: x[1])
                usage_insights.append(f"Most used persona: {most_used[0]} ({most_used[1]} times)")
            
            # Task category distribution
            if analytics["task_categories"]:
                top_category = max(analytics["task_categories"].items(), key=lambda x: x[1])
                usage_insights.append(f"Most common task type: {top_category[0]} ({top_category[1]} times)")
            
            # Domain distribution
            if analytics["domains"]:
                top_domain = max(analytics["domains"].items(), key=lambda x: x[1])
                usage_insights.append(f"Most common domain: {top_domain[0]} ({top_domain[1]} times)")
        
        analytics["usage_insights"] = usage_insights
        
        return create_response(
            success=True,
            message="Usage analytics retrieved successfully",
            data=analytics
        )
    except Exception as e:
        logger.error(f"Error getting usage analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def record_feedback(request: Dict[str, Any]):
    """Record feedback on persona selection performance."""
    try:
        task_description = request.get("task_description")
        selected_persona = request.get("selected_persona")
        feedback_score = request.get("feedback_score")
        feedback_comment = request.get("feedback_comment", "")
        
        if not all([task_description, selected_persona, feedback_score]):
            raise HTTPException(status_code=400, detail="Missing required fields: task_description, selected_persona, feedback_score")
        
        if not isinstance(feedback_score, int) or feedback_score < 1 or feedback_score > 5:
            raise HTTPException(status_code=400, detail="feedback_score must be an integer between 1 and 5")
        
        persona_dispatcher.record_feedback(task_description, selected_persona, feedback_score, feedback_comment)
        
        return create_response(
            success=True,
            message="Feedback recorded successfully",
            data={
                "task_description": task_description,
                "selected_persona": selected_persona,
                "feedback_score": feedback_score,
                "feedback_comment": feedback_comment
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error recording feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/editor")
async def get_persona_editor():
    """Serve the persona editor HTML page."""
    return FileResponse("static/persona-editor.html")

@app.get("/templates")
async def get_persona_templates():
    """Get predefined persona templates for quick creation."""
    templates = {
        "tech_expert": {
            "name": "Tech Expert",
            "description": "A knowledgeable software engineer with expertise in programming and system architecture",
            "expertise": ["Programming", "System Design", "Software Architecture", "API Design"],
            "communication_style": "Professional and technical",
            "context": "Use when discussing technical implementation details, code reviews, or system design",
            "personality_traits": ["analytical", "detail-oriented", "problem-solver"]
        },
        "business_analyst": {
            "name": "Business Analyst",
            "description": "A strategic thinker with expertise in business analysis and process optimization",
            "expertise": ["Business Analysis", "Process Optimization", "Data Analysis", "Strategy"],
            "communication_style": "Strategic and analytical",
            "context": "Use for business strategy, process analysis, and data-driven decision making",
            "personality_traits": ["strategic", "analytical", "results-oriented"]
        },
        "creative_writer": {
            "name": "Creative Writer",
            "description": "A creative professional with expertise in content creation and storytelling",
            "expertise": ["Content Creation", "Storytelling", "Creative Writing", "Marketing"],
            "communication_style": "Engaging and creative",
            "context": "Use for creative content, storytelling, and marketing materials",
            "personality_traits": ["creative", "imaginative", "expressive"]
        },
        "educator": {
            "name": "Educator",
            "description": "A patient teacher with expertise in explaining complex concepts clearly",
            "expertise": ["Teaching", "Curriculum Design", "Instructional Design", "Learning"],
            "communication_style": "Patient and explanatory",
            "context": "Use for educational content, tutorials, and explaining complex topics",
            "personality_traits": ["patient", "explanatory", "supportive"]
        },
        "designer": {
            "name": "Designer",
            "description": "A visual creative with expertise in design and user experience",
            "expertise": ["UI/UX Design", "Visual Design", "User Research", "Prototyping"],
            "communication_style": "Visual and user-focused",
            "context": "Use for design discussions, user experience, and visual concepts",
            "personality_traits": ["creative", "user-focused", "aesthetic"]
        },
        "scientist": {
            "name": "Scientist",
            "description": "A methodical researcher with expertise in scientific methodology",
            "expertise": ["Research", "Data Analysis", "Scientific Method", "Experimentation"],
            "communication_style": "Methodical and evidence-based",
            "context": "Use for scientific research, data analysis, and evidence-based discussions",
            "personality_traits": ["methodical", "evidence-based", "curious"]
        }
    }
    
    return create_response(
        success=True,
        message=f"Retrieved {len(templates)} persona templates",
        data={
            "templates": templates,
            "count": len(templates)
        }
    )

@app.get("/search")
async def search_personas(query: str, limit: int = 10):
    """Search personas by query."""
    try:
        results = persona_manager.search_personas(query)
        
        # Apply limit
        if limit and limit < len(results):
            results = results[:limit]
        
        return create_response(
            success=True,
            message=f"Found {len(results)} personas matching '{query}'",
            data={
                "results": results,
                "count": len(results),
                "query": query,
                "limit": limit
            }
        )
    except Exception as e:
        logger.error(f"Error searching personas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/recent")
async def get_recent_selections():
    """Get recent persona selections."""
    try:
        analytics = persona_dispatcher.get_selection_analytics()
        recent = analytics.get("recent_selections", [])
        
        return create_response(
            success=True,
            message=f"Retrieved {len(recent)} recent selections",
            data={
                "recent_selections": recent,
                "count": len(recent)
            }
        )
    except Exception as e:
        logger.error(f"Error getting recent selections: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/complete-task")
async def complete_task(request: Dict[str, Any]):
    """Complete a task and update context."""
    try:
        task_description = request.get("task_description", "")
        result = request.get("result", "")
        persona_id = request.get("persona_id", "")
        
        if not task_description or not result or not persona_id:
            raise HTTPException(status_code=400, detail="Missing required fields: task_description, result, persona_id")
        
        # Use the context integration to update context
        success = persona_dispatcher.complete_task_with_context_update(
            task_description, result, persona_id
        )
        
        if success:
            return create_response(
                success=True,
                message="Task completed and context updated successfully",
                data={
                    "task": task_description,
                    "persona_used": persona_id,
                    "context_updated": True
                }
            )
        else:
            return create_response(
                success=False,
                message="Task completed but context update failed",
                data={
                    "task": task_description,
                    "persona_used": persona_id,
                    "context_updated": False
                }
            )
            
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/select")
async def select_persona(request: Dict[str, Any]):
    """Simulate persona selection for testing."""
    try:
        # Create a task context
        task_context = TaskContext(
            task_description=request.get("task_description", "Test task"),
            user_context="",
            domain=request.get("domain", "general"),
            complexity=request.get("complexity", "medium"),
            urgency="normal",
            audience=request.get("audience", "developer"),
            output_format="text"
        )
        
        # Debug: Check available personas
        all_personas = persona_manager.get_all_personas()
        logger.info(f"Available personas: {len(all_personas)}")
        
        # Get persona recommendation with project context
        project_name = request.get("project_name")
        try:
            recommendation = persona_dispatcher.select_persona(
                task_context.task_description, 
                task_context.user_context,
                project_name
            )
        except Exception as e:
            logger.error(f"Error in select_persona: {e}")
            raise HTTPException(status_code=500, detail=f"Error selecting persona: {str(e)}")
        
        # Debug: Check if recommendation is valid
        if recommendation is None:
            raise HTTPException(status_code=500, detail="No persona recommendation returned")
        
        if not hasattr(recommendation, 'persona_id') or not hasattr(recommendation, 'confidence_score'):
            raise HTTPException(status_code=500, detail=f"Invalid recommendation structure: {type(recommendation)}")
        
        # Log the selection
        persona_dispatcher._log_persona_selection(task_context, recommendation)
        
        return create_response(
            success=True,
            message="Persona selected successfully",
            data={
                "selected_persona": recommendation.persona_id,
                "confidence_score": recommendation.confidence_score,
                "task_category": recommendation.task_category.value,
                "reasoning": recommendation.reasoning
            }
        )
    except Exception as e:
        logger.error(f"Error selecting persona: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8002"))
    
    logger.info(f"Starting Persona Manager HTTP server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

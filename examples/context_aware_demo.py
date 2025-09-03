#!/usr/bin/env python3
"""
Context-Aware Persona Selection Demo

This demo showcases the new context-aware features of the persona manager,
including intelligent persona selection based on project context.
"""

import os
import sys
import json
import requests
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_persona_server.persona_dispatcher import PersonaDispatcher
from mcp_persona_server.persona_manager import PersonaManager
from mcp_persona_server.storage import PersonaStorage
from mcp_persona_server.context_integration import ContextIntegration

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section."""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_context_integration():
    """Demo the context integration features."""
    print_header("Context-Aware Persona Selection Demo")
    
    # Initialize components
    storage = PersonaStorage("./personas")
    persona_manager = PersonaManager(storage)
    persona_dispatcher = PersonaDispatcher(persona_manager)
    context_integration = ContextIntegration()
    
    print_section("1. Current Project Context")
    
    # Get current context
    context_summary = context_integration.get_context_summary()
    print(json.dumps(context_summary, indent=2))
    
    print_section("2. Task Priority Suggestions")
    
    # Get task suggestions
    suggestions = context_integration.suggest_task_priorities()
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    print_section("3. Context-Aware Persona Selection")
    
    # Test different tasks
    test_tasks = [
        "Implement database storage for the context manager",
        "Create a monitoring dashboard for the system",
        "Write documentation for the API endpoints",
        "Analyze performance bottlenecks in the current implementation",
        "Design a user interface for the persona management system"
    ]
    
    for task in test_tasks:
        print(f"\n🔍 Task: {task}")
        
        # Analyze context for the task
        analysis = context_integration.analyze_context_for_task(task)
        print(f"   Priority: {analysis.get('priority', 'unknown')}")
        print(f"   Domain: {analysis.get('domain', 'unknown')}")
        print(f"   Urgency: {analysis.get('urgency', 'unknown')}")
        print(f"   Context Relevance: {analysis.get('context_relevance', 0.0):.2f}")
        print(f"   Recommended Personas: {', '.join(analysis.get('recommended_personas', []))}")
        
        if analysis.get('context_insights'):
            print(f"   Context Insights:")
            for insight in analysis['context_insights']:
                print(f"     • {insight}")
        
        # Select persona using context-aware dispatcher
        try:
            recommendation = persona_dispatcher.select_persona(task)
            print(f"   Selected Persona: {recommendation.persona_data['name']} (ID: {recommendation.persona_id})")
            print(f"   Confidence: {recommendation.confidence_score:.2f}")
            print(f"   Reasoning: {recommendation.reasoning}")
        except Exception as e:
            print(f"   Error selecting persona: {e}")

def demo_context_update():
    """Demo context updating after task completion."""
    print_header("Context Update Demo")
    
    # Initialize components
    storage = PersonaStorage("./personas")
    persona_manager = PersonaManager(storage)
    persona_dispatcher = PersonaDispatcher(persona_manager)
    
    print_section("1. Before Task Completion")
    
    # Get current context
    context_summary = persona_dispatcher.get_context_summary()
    print("Current Issues:", context_summary.get("current_focus", {}).get("active_issues", []))
    print("Next Steps:", context_summary.get("current_focus", {}).get("next_priorities", []))
    
    print_section("2. Completing a Task")
    
    # Simulate completing a task
    task_description = "Implement database storage for the context manager"
    result = "Successfully implemented PostgreSQL storage with connection pooling and automatic context updates"
    persona_id = "tech_expert"
    
    print(f"Task: {task_description}")
    print(f"Result: {result}")
    print(f"Persona: {persona_id}")
    
    # Complete the task
    success = persona_dispatcher.complete_task_with_context_update(
        task_description, result, persona_id
    )
    
    if success:
        print("✅ Task completed and context updated successfully")
    else:
        print("⚠️ Task completed but context update failed")
    
    print_section("3. After Task Completion")
    
    # Get updated context
    updated_summary = persona_dispatcher.get_context_summary()
    print("Updated Issues:", updated_summary.get("current_focus", {}).get("active_issues", []))
    print("Updated Next Steps:", updated_summary.get("current_focus", {}).get("next_priorities", []))

def demo_api_endpoints():
    """Demo the new API endpoints."""
    print_header("API Endpoints Demo")
    
    base_url = "http://localhost:8000"
    
    print_section("1. Get Context Summary")
    try:
        response = requests.get(f"{base_url}/context/summary")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    print_section("2. Suggest Task Priorities")
    try:
        response = requests.get(f"{base_url}/context/suggestions")
        if response.status_code == 200:
            suggestions = response.json()
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    print_section("3. Context-Aware Persona Selection")
    try:
        task_data = {
            "task_description": "Implement monitoring dashboard for the system",
            "context": "This is part of the scalability improvements"
        }
        response = requests.post(f"{base_url}/persona/select", json=task_data)
        if response.status_code == 200:
            result = response.json()
            print(f"Selected Persona: {result['selected_persona']['name']}")
            print(f"Confidence: {result['confidence_score']:.2f}")
            print(f"Context Insights: {result.get('context_insights', [])}")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main demo function."""
    print("🚀 Context-Aware Persona Manager Demo")
    print("This demo showcases the new context integration features.")
    
    try:
        # Demo 1: Context Integration
        demo_context_integration()
        
        # Demo 2: Context Updates
        demo_context_update()
        
        # Demo 3: API Endpoints (if server is running)
        print("\n" + "="*60)
        print("🌐 API Endpoints Demo (requires running server)")
        print("="*60)
        print("To test API endpoints, start the server with:")
        print("python -m mcp_persona_server.server")
        print("Then run this demo again.")
        
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Basic usage example for the MCP Persona Server.

This example demonstrates how to:
1. Create personas
2. List personas
3. Search personas
4. Select the best persona for a task
5. Update personas
6. Delete personas
"""

import asyncio
import json
from mcp_persona_server import PersonaMCPServer


async def basic_usage_example():
    """Demonstrate basic usage of the persona server."""
    
    # Initialize the server
    server = PersonaMCPServer()
    
    print("🎭 MCP Persona Server - Basic Usage Example")
    print("=" * 50)
    
    # 1. List all personas
    print("\n1. Listing all personas:")
    personas = server.persona_manager.get_all_personas()
    for persona_id, persona_data in personas.items():
        print(f"  - {persona_data['name']} (ID: {persona_id})")
    
    # 2. Create a new persona
    print("\n2. Creating a new persona:")
    new_persona = {
        "name": "Data Scientist",
        "description": "A data expert specializing in machine learning and statistical analysis",
        "expertise": ["Machine Learning", "Statistics", "Data Analysis", "Python", "R"],
        "communication_style": "Analytical and data-driven",
        "context": "Use when working with data analysis, machine learning models, or statistical problems",
        "personality_traits": ["analytical", "data-driven", "curious", "methodical"]
    }
    
    success, result = server.persona_manager.create_persona(new_persona)
    if success:
        print(f"  ✅ Created persona with ID: {result}")
    else:
        print(f"  ❌ Failed to create persona: {result}")
    
    # 3. Search personas
    print("\n3. Searching for personas with 'data':")
    search_results = server.persona_manager.search_personas("data")
    for result in search_results:
        print(f"  - {result['name']} (Score: {result.get('score', 'N/A')})")
    
    # 4. Select best persona for a task
    print("\n4. Selecting best persona for 'analyze customer data':")
    best_persona = server.persona_manager.select_best_persona("analyze customer data")
    if best_persona:
        print(f"  🎯 Best persona: {best_persona['name']}")
        print(f"     Description: {best_persona['description']}")
        print(f"     Expertise: {', '.join(best_persona['expertise'])}")
    else:
        print("  ❌ No suitable persona found")
    
    # 5. Get persona suggestions
    print("\n5. Getting persona suggestions for 'write a blog post':")
    suggestions = server.persona_manager.get_persona_suggestions("write a blog post", limit=3)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion['name']} (Score: {suggestion['score']:.2f})")
        print(f"     {suggestion['description']}")
    
    # 6. Update a persona
    print("\n6. Updating a persona:")
    # Get the first persona to update
    first_persona_id = list(personas.keys())[0]
    updates = {
        "description": "Updated description for better clarity",
        "expertise": ["Updated Expertise 1", "Updated Expertise 2"]
    }
    
    success, message = server.persona_manager.update_persona(first_persona_id, updates)
    if success:
        print(f"  ✅ {message}")
    else:
        print(f"  ❌ {message}")
    
    # 7. Get persona statistics
    print("\n7. Getting persona statistics:")
    stats = server.persona_manager.get_persona_statistics()
    print(f"  Total personas: {stats['total_personas']}")
    print(f"  Top expertise areas: {list(stats['expertise_distribution'].keys())[:3]}")
    
    # 8. Backup personas
    print("\n8. Creating backup:")
    backup_success = server.storage.backup_personas("./examples/backup_example.json")
    if backup_success:
        print("  ✅ Backup created successfully")
    else:
        print("  ❌ Failed to create backup")
    
    print("\n🎉 Basic usage example completed!")


if __name__ == "__main__":
    asyncio.run(basic_usage_example())

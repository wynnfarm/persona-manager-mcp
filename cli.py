#!/usr/bin/env python3
"""
Command-line interface for the MCP Persona Server.

This CLI allows you to:
- Test the MCP server functionality
- Manage personas directly
- Run examples and demonstrations
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp_persona_server import PersonaMCPServer


def list_personas(server):
    """List all personas."""
    personas = server.persona_manager.get_all_personas()
    
    if not personas:
        print("No personas found.")
        return
    
    print(f"\n📋 Found {len(personas)} personas:")
    print("-" * 50)
    
    for persona_id, persona_data in personas.items():
        print(f"🎭 {persona_data['name']} (ID: {persona_id})")
        print(f"   📝 {persona_data['description']}")
        print(f"   🔧 Expertise: {', '.join(persona_data.get('expertise', []))}")
        if persona_data.get('communication_style'):
            print(f"   💬 Style: {persona_data['communication_style']}")
        print()


def create_persona(server, args):
    """Create a new persona."""
    persona_data = {
        "name": args.name,
        "description": args.description,
        "expertise": args.expertise.split(','),
        "communication_style": args.style or "",
        "context": args.context or "",
        "personality_traits": args.traits.split(',') if args.traits else []
    }
    
    success, result = server.persona_manager.create_persona(persona_data)
    
    if success:
        print(f"✅ Persona created successfully with ID: {result}")
    else:
        print(f"❌ Failed to create persona: {result}")


def get_persona(server, persona_id):
    """Get a specific persona."""
    persona = server.persona_manager.get_persona(persona_id)
    
    if persona:
        print(f"\n🎭 {persona['name']} (ID: {persona_id})")
        print("-" * 40)
        print(f"📝 Description: {persona['description']}")
        print(f"🔧 Expertise: {', '.join(persona.get('expertise', []))}")
        if persona.get('communication_style'):
            print(f"💬 Style: {persona['communication_style']}")
        if persona.get('context'):
            print(f"🎯 Context: {persona['context']}")
        if persona.get('personality_traits'):
            print(f"✨ Traits: {', '.join(persona['personality_traits'])}")
        if persona.get('created_at'):
            print(f"📅 Created: {persona['created_at']}")
    else:
        print(f"❌ Persona '{persona_id}' not found")


def search_personas(server, query):
    """Search personas."""
    results = server.persona_manager.search_personas(query)
    
    if not results:
        print(f"No personas found matching '{query}'")
        return
    
    print(f"\n🔍 Found {len(results)} personas matching '{query}':")
    print("-" * 50)
    
    for result in results:
        print(f"🎭 {result['name']} (ID: {result['id']})")
        print(f"   📝 {result['description']}")
        print(f"   🔧 Expertise: {', '.join(result.get('expertise', []))}")
        print()


def select_best_persona(server, task_description, context=""):
    """Select the best persona for a task."""
    best_persona = server.persona_manager.select_best_persona(task_description, context)
    
    if best_persona:
        print(f"\n🎯 Best persona for '{task_description}':")
        print("-" * 50)
        print(f"🎭 {best_persona['name']} (ID: {best_persona['id']})")
        print(f"📝 {best_persona['description']}")
        print(f"🔧 Expertise: {', '.join(best_persona.get('expertise', []))}")
        if best_persona.get('communication_style'):
            print(f"💬 Style: {best_persona['communication_style']}")
        if best_persona.get('context'):
            print(f"🎯 Context: {best_persona['context']}")
    else:
        print(f"❌ No suitable persona found for '{task_description}'")


def get_suggestions(server, task_description, limit=3):
    """Get persona suggestions for a task."""
    suggestions = server.persona_manager.get_persona_suggestions(task_description, limit)
    
    if not suggestions:
        print(f"No persona suggestions for '{task_description}'")
        return
    
    print(f"\n💡 Top {len(suggestions)} persona suggestions for '{task_description}':")
    print("-" * 60)
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. 🎭 {suggestion['name']} (Score: {suggestion['score']:.2f})")
        print(f"   📝 {suggestion['description']}")
        print(f"   🔧 Expertise: {', '.join(suggestion.get('expertise', []))}")
        print()


def update_persona(server, persona_id, updates):
    """Update a persona."""
    success, message = server.persona_manager.update_persona(persona_id, updates)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")


def delete_persona(server, persona_id):
    """Delete a persona."""
    success, message = server.persona_manager.delete_persona(persona_id)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")


def show_statistics(server):
    """Show persona statistics."""
    stats = server.persona_manager.get_persona_statistics()
    
    print(f"\n📊 Persona Statistics:")
    print("-" * 30)
    print(f"Total personas: {stats['total_personas']}")
    
    if stats['expertise_distribution']:
        print(f"\n🔧 Top expertise areas:")
        top_expertise = sorted(stats['expertise_distribution'].items(), 
                             key=lambda x: x[1], reverse=True)[:5]
        for expertise, count in top_expertise:
            print(f"   {expertise}: {count}")
    
    if stats['communication_style_distribution']:
        print(f"\n💬 Communication styles:")
        for style, count in stats['communication_style_distribution'].items():
            print(f"   {style}: {count}")


def run_demo(server):
    """Run a demonstration of the persona server."""
    print("🎭 MCP Persona Server Demo")
    print("=" * 40)
    
    # List personas
    print("\n1. Listing all personas:")
    personas = server.persona_manager.get_all_personas()
    for persona_id, persona_data in personas.items():
        print(f"   - {persona_data['name']}")
    
    # Create a new persona
    print("\n2. Creating a new persona:")
    new_persona = {
        "name": "Demo Persona",
        "description": "A persona created for demonstration purposes",
        "expertise": ["Demo", "Testing", "Examples"],
        "communication_style": "Demonstrative",
        "context": "Use for demonstration and testing",
        "personality_traits": ["helpful", "demonstrative", "clear"]
    }
    
    success, persona_id = server.persona_manager.create_persona(new_persona)
    if success:
        print(f"   ✅ Created: {persona_id}")
    
    # Search personas
    print("\n3. Searching for 'demo':")
    results = server.persona_manager.search_personas("demo")
    for result in results:
        print(f"   - {result['name']}")
    
    # Select best persona
    print("\n4. Selecting best persona for 'technical programming':")
    best = server.persona_manager.select_best_persona("technical programming")
    if best:
        print(f"   🎯 Best: {best['name']}")
    
    # Get suggestions
    print("\n5. Getting suggestions for 'creative writing':")
    suggestions = server.persona_manager.get_persona_suggestions("creative writing", limit=2)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"   {i}. {suggestion['name']} (Score: {suggestion['score']:.2f})")
    
    # Show statistics
    print("\n6. Statistics:")
    stats = server.persona_manager.get_persona_statistics()
    print(f"   Total personas: {stats['total_personas']}")
    
    print("\n🎉 Demo completed!")


def dispatch_persona(server, task_description, context=""):
    """Dispatch the best persona for a task."""
    try:
        recommendation = server.persona_dispatcher.select_persona(task_description, context)
        
        print(f"\n🎯 Persona Dispatch for: '{task_description}'")
        print("=" * 60)
        
        # Selected persona
        print(f"✅ Selected: {recommendation.persona_data['name']}")
        print(f"   Confidence: {recommendation.confidence_score:.2f}")
        print(f"   Category: {recommendation.task_category.value}")
        print(f"   Description: {recommendation.persona_data['description']}")
        print(f"   Expertise: {', '.join(recommendation.persona_data.get('expertise', []))}")
        
        # Reasoning
        if recommendation.reasoning:
            print(f"\n🔍 Reasoning:")
            for reason in recommendation.reasoning:
                print(f"   • {reason}")
        
        # Alternatives
        if recommendation.alternative_personas:
            print(f"\n🔄 Alternative personas:")
            for i, alt in enumerate(recommendation.alternative_personas, 1):
                print(f"   {i}. {alt['name']} - {alt['description']}")
        
    except Exception as e:
        print(f"❌ Error dispatching persona: {e}")


def analyze_task(server, task_description, context=""):
    """Analyze a task to understand its characteristics."""
    try:
        task_context = server.persona_dispatcher.analyze_task(task_description, context)
        task_category = server.persona_dispatcher.classify_task(task_context)
        
        print(f"\n🔍 Task Analysis: '{task_description}'")
        print("=" * 50)
        
        print(f"📋 Domain: {task_context.domain}")
        print(f"🎯 Category: {task_category.value}")
        print(f"📊 Complexity: {task_context.complexity}")
        print(f"⏰ Urgency: {task_context.urgency}")
        print(f"👥 Audience: {task_context.audience}")
        print(f"📝 Output Format: {task_context.output_format}")
        
        if context:
            print(f"📄 Context: {context}")
        
    except Exception as e:
        print(f"❌ Error analyzing task: {e}")


def show_analytics(server):
    """Show dispatcher analytics."""
    try:
        analytics = server.persona_dispatcher.get_selection_analytics()
        
        print(f"\n📊 Dispatcher Analytics")
        print("=" * 30)
        
        print(f"Total selections: {analytics['total_selections']}")
        
        if analytics['persona_usage_stats']:
            print(f"\n🎭 Persona Usage:")
            for persona_id, stats in analytics['persona_usage_stats'].items():
                print(f"   {persona_id}: {stats['usage_count']} uses "
                      f"(avg confidence: {stats['avg_confidence']:.2f})")
        
        if analytics['category_distribution']:
            print(f"\n📈 Category Distribution:")
            for category, count in analytics['category_distribution'].items():
                print(f"   {category}: {count}")
        
        if analytics['recent_selections']:
            print(f"\n🕒 Recent Selections:")
            for selection in analytics['recent_selections'][-5:]:
                print(f"   {selection['selected_persona']} for '{selection['task_description'][:30]}...'")
        
    except Exception as e:
        print(f"❌ Error getting analytics: {e}")


def suggest_improvements(server, task_description):
    """Get persona improvement suggestions."""
    try:
        suggestions = server.persona_dispatcher.suggest_persona_improvements(task_description)
        
        print(f"\n💡 Improvement Suggestions for: '{task_description}'")
        print("=" * 60)
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")
        else:
            print("✅ No specific improvements needed at this time.")
        
    except Exception as e:
        print(f"❌ Error getting suggestions: {e}")


def handle_auto_generation(server, args):
    """Handle auto-generation commands."""
    action = args.action
    
    if action == 'enable':
        server.persona_dispatcher.enable_auto_generation(True)
        print("✅ Auto-generation enabled")
        
    elif action == 'disable':
        server.persona_dispatcher.enable_auto_generation(False)
        print("❌ Auto-generation disabled")
        
    elif action == 'status':
        status = server.persona_dispatcher.get_auto_generation_status()
        print(f"\n🤖 Auto-Generation Status:")
        print("-" * 30)
        print(f"Enabled: {'Yes' if status['enabled'] else 'No'}")
        print(f"Confidence Threshold: {status['confidence_threshold']}")
        print(f"Total Generated: {status['total_generated']}")
        
    elif action == 'threshold':
        if args.threshold is None:
            print("❌ Please specify a threshold value with --threshold")
            return
        
        try:
            server.persona_dispatcher.set_confidence_threshold(args.threshold)
            print(f"✅ Confidence threshold set to {args.threshold}")
        except ValueError as e:
            print(f"❌ {e}")
            
    elif action == 'list':
        generated = server.persona_dispatcher.list_generated_personas()
        
        if not generated:
            print("📝 No auto-generated personas found")
            return
        
        print(f"\n🤖 Auto-Generated Personas ({len(generated)} total):")
        print("-" * 50)
        
        for persona in generated:
            print(f"🎭 {persona['name']} (ID: {persona['id']})")
            print(f"   📅 Created: {persona['created_at']}")
            print(f"   🎯 Category: {persona['task_category']}")
            print(f"   💡 Reason: {persona['generation_reason']}")
            print(f"   📝 Original Task: {persona['original_task'][:60]}...")
            print()


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="MCP Persona Server CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list
  %(prog)s create --name "Data Scientist" --description "Expert in data analysis" --expertise "Python,ML,Statistics"
  %(prog)s get tech_expert
  %(prog)s search "python"
  %(prog)s select "debug code"
  %(prog)s suggestions "write blog post" --limit 3
  %(prog)s demo
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    subparsers.add_parser('list', help='List all personas')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new persona')
    create_parser.add_argument('--name', required=True, help='Persona name')
    create_parser.add_argument('--description', required=True, help='Persona description')
    create_parser.add_argument('--expertise', required=True, help='Comma-separated expertise areas')
    create_parser.add_argument('--style', help='Communication style')
    create_parser.add_argument('--context', help='When to use this persona')
    create_parser.add_argument('--traits', help='Comma-separated personality traits')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get a specific persona')
    get_parser.add_argument('persona_id', help='Persona ID')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search personas')
    search_parser.add_argument('query', help='Search query')
    
    # Select command
    select_parser = subparsers.add_parser('select', help='Select best persona for a task')
    select_parser.add_argument('task', help='Task description')
    select_parser.add_argument('--context', help='Additional context')
    
    # Suggestions command
    suggestions_parser = subparsers.add_parser('suggestions', help='Get persona suggestions')
    suggestions_parser.add_argument('task', help='Task description')
    suggestions_parser.add_argument('--limit', type=int, default=3, help='Maximum suggestions')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a persona')
    update_parser.add_argument('persona_id', help='Persona ID')
    update_parser.add_argument('--name', help='New name')
    update_parser.add_argument('--description', help='New description')
    update_parser.add_argument('--expertise', help='New comma-separated expertise')
    update_parser.add_argument('--style', help='New communication style')
    update_parser.add_argument('--context', help='New context')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a persona')
    delete_parser.add_argument('persona_id', help='Persona ID')
    
    # Statistics command
    subparsers.add_parser('stats', help='Show persona statistics')
    
    # Demo command
    subparsers.add_parser('demo', help='Run a demonstration')
    
    # Dispatcher commands
    dispatch_parser = subparsers.add_parser('dispatch', help='Dispatch best persona for a task')
    dispatch_parser.add_argument('task', help='Task description')
    dispatch_parser.add_argument('--context', help='Additional context')
    
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a task')
    analyze_parser.add_argument('task', help='Task description')
    analyze_parser.add_argument('--context', help='Additional context')
    
    subparsers.add_parser('analytics', help='Show dispatcher analytics')
    
    improve_parser = subparsers.add_parser('improve', help='Get persona improvement suggestions')
    improve_parser.add_argument('task', help='Task description')
    
    # Auto-generation commands
    auto_parser = subparsers.add_parser('auto', help='Manage auto-generation settings')
    auto_parser.add_argument('action', choices=['enable', 'disable', 'status', 'threshold', 'list'], 
                            help='Action to perform')
    auto_parser.add_argument('--threshold', type=float, help='Confidence threshold (0.0-1.0)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize server
    server = PersonaMCPServer()
    
    try:
        if args.command == 'list':
            list_personas(server)
        elif args.command == 'create':
            create_persona(server, args)
        elif args.command == 'get':
            get_persona(server, args.persona_id)
        elif args.command == 'search':
            search_personas(server, args.query)
        elif args.command == 'select':
            select_best_persona(server, args.task, args.context or "")
        elif args.command == 'suggestions':
            get_suggestions(server, args.task, args.limit)
        elif args.command == 'update':
            updates = {}
            if args.name:
                updates['name'] = args.name
            if args.description:
                updates['description'] = args.description
            if args.expertise:
                updates['expertise'] = args.expertise.split(',')
            if args.style:
                updates['communication_style'] = args.style
            if args.context:
                updates['context'] = args.context
            
            if updates:
                update_persona(server, args.persona_id, updates)
            else:
                print("❌ No updates specified")
        elif args.command == 'delete':
            delete_persona(server, args.persona_id)
        elif args.command == 'stats':
            show_statistics(server)
        elif args.command == 'demo':
            run_demo(server)
        elif args.command == 'dispatch':
            dispatch_persona(server, args.task, args.context or "")
        elif args.command == 'analyze':
            analyze_task(server, args.task, args.context or "")
        elif args.command == 'analytics':
            show_analytics(server)
        elif args.command == 'improve':
            suggest_improvements(server, args.task)
        elif args.command == 'auto':
            handle_auto_generation(server, args)
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

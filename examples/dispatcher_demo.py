#!/usr/bin/env python3
"""
Persona Dispatcher Demo

This example demonstrates the intelligent persona dispatching system
that automatically selects the most appropriate persona based on task analysis.
"""

import asyncio
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_persona_server import PersonaMCPServer


def dispatcher_demo():
    """Demonstrate the persona dispatcher functionality."""
    
    print("🎯 Persona Dispatcher Demo")
    print("=" * 50)
    
    # Initialize the server
    server = PersonaMCPServer()
    
    # Test scenarios
    test_scenarios = [
        {
            "task": "debug Python code with complex algorithms",
            "context": "working on a machine learning project",
            "expected_category": "technical"
        },
        {
            "task": "write a creative story about time travel",
            "context": "for a science fiction magazine",
            "expected_category": "creative"
        },
        {
            "task": "analyze quarterly sales data and provide strategic recommendations",
            "context": "presentation to executive team",
            "expected_category": "business"
        },
        {
            "task": "explain quantum physics to a beginner",
            "context": "high school student learning advanced concepts",
            "expected_category": "educational"
        },
        {
            "task": "design a mobile app interface for healthcare",
            "context": "focusing on user experience and accessibility",
            "expected_category": "design"
        },
        {
            "task": "conduct research on climate change impacts",
            "context": "scientific study with peer review",
            "expected_category": "scientific"
        },
        {
            "task": "provide consulting advice on organizational restructuring",
            "context": "helping company improve efficiency",
            "expected_category": "consulting"
        },
        {
            "task": "mentor a junior developer in career growth",
            "context": "helping them advance to senior level",
            "expected_category": "mentoring"
        }
    ]
    
    print("\n🔍 Testing Task Analysis and Persona Dispatch")
    print("-" * 50)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. Task: '{scenario['task']}'")
        print(f"   Context: {scenario['context']}")
        
        # Analyze the task
        task_context = server.persona_dispatcher.analyze_task(scenario['task'], scenario['context'])
        task_category = server.persona_dispatcher.classify_task(task_context)
        
        print(f"   📋 Domain: {task_context.domain}")
        print(f"   🎯 Category: {task_category.value}")
        print(f"   📊 Complexity: {task_context.complexity}")
        print(f"   👥 Audience: {task_context.audience}")
        
        # Dispatch persona
        recommendation = server.persona_dispatcher.select_persona(scenario['task'], scenario['context'])
        
        print(f"   ✅ Selected: {recommendation.persona_data['name']}")
        print(f"   🎯 Confidence: {recommendation.confidence_score:.2f}")
        print(f"   🔧 Expertise: {', '.join(recommendation.persona_data.get('expertise', [])[:3])}")
        
        # Show reasoning
        if recommendation.reasoning:
            print(f"   🔍 Reasoning: {'; '.join(recommendation.reasoning[:2])}")
        
        print()
    
    # Test edge cases
    print("\n🧪 Testing Edge Cases")
    print("-" * 30)
    
    edge_cases = [
        "urgent emergency system failure",
        "simple hello world program",
        "complex multi-domain project",
        "creative technical documentation"
    ]
    
    for case in edge_cases:
        print(f"\nTask: '{case}'")
        
        task_context = server.persona_dispatcher.analyze_task(case)
        print(f"   Urgency: {task_context.urgency}")
        print(f"   Complexity: {task_context.complexity}")
        print(f"   Domain: {task_context.domain}")
        
        recommendation = server.persona_dispatcher.select_persona(case)
        print(f"   Selected: {recommendation.persona_data['name']} (confidence: {recommendation.confidence_score:.2f})")
    
    # Show analytics
    print("\n📊 Dispatcher Analytics")
    print("-" * 30)
    
    analytics = server.persona_dispatcher.get_selection_analytics()
    print(f"Total selections: {analytics['total_selections']}")
    
    if analytics['persona_usage_stats']:
        print("\nPersona Usage:")
        for persona_id, stats in analytics['persona_usage_stats'].items():
            print(f"   {persona_id}: {stats['usage_count']} uses")
    
    if analytics['category_distribution']:
        print("\nCategory Distribution:")
        for category, count in analytics['category_distribution'].items():
            print(f"   {category}: {count}")
    
    # Test improvement suggestions
    print("\n💡 Testing Improvement Suggestions")
    print("-" * 40)
    
    improvement_tasks = [
        "analyze medical imaging data for cancer detection",
        "create legal contracts for international business",
        "develop financial models for cryptocurrency trading",
        "design educational games for children with disabilities"
    ]
    
    for task in improvement_tasks:
        print(f"\nTask: '{task}'")
        suggestions = server.persona_dispatcher.suggest_persona_improvements(task)
        
        if suggestions:
            for suggestion in suggestions:
                print(f"   💡 {suggestion}")
        else:
            print("   ✅ No improvements needed")
    
    print("\n🎉 Dispatcher Demo Completed!")
    print("\nKey Features Demonstrated:")
    print("✅ Intelligent task analysis and categorization")
    print("✅ Sophisticated persona scoring algorithm")
    print("✅ Detailed reasoning for selections")
    print("✅ Alternative persona suggestions")
    print("✅ Usage analytics and tracking")
    print("✅ Improvement suggestions based on gaps")
    print("✅ Multi-domain task handling")


def advanced_dispatcher_features():
    """Demonstrate advanced dispatcher features."""
    
    print("\n🚀 Advanced Dispatcher Features")
    print("=" * 40)
    
    server = PersonaMCPServer()
    
    # Test confidence thresholds
    print("\n📊 Confidence Analysis")
    print("-" * 25)
    
    confidence_tests = [
        "debug Python code",  # Should have high confidence
        "write something creative",  # Should have medium confidence
        "analyze quantum physics data",  # Should have low confidence (no matching persona)
        "design a rocket engine",  # Should have low confidence
    ]
    
    for test in confidence_tests:
        recommendation = server.persona_dispatcher.select_persona(test)
        confidence_level = "High" if recommendation.confidence_score > 0.5 else \
                          "Medium" if recommendation.confidence_score > 0.3 else "Low"
        
        print(f"Task: '{test}'")
        print(f"   Selected: {recommendation.persona_data['name']}")
        print(f"   Confidence: {recommendation.confidence_score:.2f} ({confidence_level})")
        print(f"   Category: {recommendation.task_category.value}")
        print()
    
    # Test multi-context scenarios
    print("\n🔄 Multi-Context Scenarios")
    print("-" * 30)
    
    base_task = "analyze data"
    contexts = [
        "for a technical audience",
        "for business executives",
        "for educational purposes",
        "for creative storytelling"
    ]
    
    for context in contexts:
        full_task = f"{base_task} {context}"
        recommendation = server.persona_dispatcher.select_persona(base_task, context)
        
        print(f"Task: '{base_task}' with context: '{context}'")
        print(f"   Selected: {recommendation.persona_data['name']}")
        print(f"   Confidence: {recommendation.confidence_score:.2f}")
        print(f"   Audience: {recommendation.persona_data.get('communication_style', 'N/A')}")
        print()


if __name__ == "__main__":
    dispatcher_demo()
    advanced_dispatcher_features()

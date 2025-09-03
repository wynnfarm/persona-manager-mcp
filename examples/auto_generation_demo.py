#!/usr/bin/env python3
"""
Auto-Generation Demo - Showcase dynamic persona creation.

This script demonstrates how the Persona Manager automatically creates
new personas when existing ones don't match a task well enough.
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_persona_server import PersonaMCPServer


def main():
    """Run the auto-generation demo."""
    print("🤖 Auto-Generation Demo")
    print("=" * 50)
    print("This demo shows how the system automatically creates new personas")
    print("when existing ones don't match a task well enough.\n")
    
    # Initialize server
    server = PersonaMCPServer()
    
    # Show initial status
    print("📊 Initial Auto-Generation Status:")
    status = server.persona_dispatcher.get_auto_generation_status()
    print(f"   Enabled: {'Yes' if status['enabled'] else 'No'}")
    print(f"   Confidence Threshold: {status['confidence_threshold']}")
    print(f"   Total Generated: {status['total_generated']}")
    print()
    
    # List existing personas
    print("🎭 Existing Personas:")
    personas = server.persona_manager.get_all_personas()
    for persona_id, persona_data in personas.items():
        print(f"   - {persona_data['name']} (ID: {persona_id})")
    print()
    
    # Test cases that should trigger auto-generation
    test_cases = [
        {
            "task": "analyze cryptocurrency market trends and provide investment advice",
            "context": "for a fintech startup",
            "expected_domain": "finance",
            "description": "Cryptocurrency/DeFi specialist needed"
        },
        {
            "task": "conduct clinical trials for a new pharmaceutical drug",
            "context": "phase 3 study",
            "expected_domain": "healthcare",
            "description": "Medical research specialist needed"
        },
        {
            "task": "design a blockchain-based supply chain management system",
            "context": "for logistics company",
            "expected_domain": "technology",
            "description": "Blockchain/DevOps specialist needed"
        },
        {
            "task": "create compliance documentation for GDPR regulations",
            "context": "for European market entry",
            "expected_domain": "legal",
            "description": "Legal compliance specialist needed"
        },
        {
            "task": "develop machine learning models for predictive analytics",
            "context": "for e-commerce platform",
            "expected_domain": "technology",
            "description": "AI/ML specialist needed"
        }
    ]
    
    print("🧪 Testing Auto-Generation with Various Tasks:")
    print("-" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['description']}")
        print(f"   Task: {test_case['task']}")
        print(f"   Context: {test_case['context']}")
        
        try:
            # Dispatch persona (this may trigger auto-generation)
            recommendation = server.persona_dispatcher.select_persona(
                test_case['task'], test_case['context']
            )
            
            print(f"   🎯 Selected: {recommendation.persona_data['name']}")
            print(f"   📊 Confidence: {recommendation.confidence_score:.2f}")
            
            # Check if this was auto-generated
            if recommendation.persona_data.get('auto_generated', False):
                print(f"   🤖 Auto-Generated: YES")
                print(f"   💡 Reason: {recommendation.persona_data.get('generation_reason', 'N/A')}")
            else:
                print(f"   🤖 Auto-Generated: NO")
            
            print(f"   🎯 Category: {recommendation.task_category.value}")
            print(f"   💭 Reasoning: {recommendation.reasoning[:100]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    # Show final status
    print("📊 Final Auto-Generation Status:")
    final_status = server.persona_dispatcher.get_auto_generation_status()
    print(f"   Enabled: {'Yes' if final_status['enabled'] else 'No'}")
    print(f"   Confidence Threshold: {final_status['confidence_threshold']}")
    print(f"   Total Generated: {final_status['total_generated']}")
    print()
    
    # List generated personas
    if final_status['total_generated'] > 0:
        print("🤖 Auto-Generated Personas:")
        generated = server.persona_dispatcher.list_generated_personas()
        
        for persona in generated:
            print(f"   🎭 {persona['name']} (ID: {persona['id']})")
            print(f"      📅 Created: {persona['created_at']}")
            print(f"      🎯 Category: {persona['task_category']}")
            print(f"      💡 Reason: {persona['generation_reason']}")
            print(f"      📝 Original Task: {persona['original_task'][:50]}...")
            print()
    
    # Show analytics
    print("📈 Dispatcher Analytics:")
    analytics = server.persona_dispatcher.get_selection_analytics()
    print(f"   Total Selections: {analytics['total_selections']}")
    print(f"   Average Confidence: {analytics['average_confidence']:.2f}")
    print(f"   Auto-Generated Used: {analytics.get('auto_generated_used', 0)}")
    print()
    
    # Test configuration changes
    print("⚙️ Testing Configuration Changes:")
    print("-" * 40)
    
    # Test threshold adjustment
    print("1. Setting confidence threshold to 0.5 (more strict)...")
    server.persona_dispatcher.set_confidence_threshold(0.5)
    print("   ✅ Threshold updated")
    
    # Test disabling auto-generation
    print("2. Disabling auto-generation...")
    server.persona_dispatcher.enable_auto_generation(False)
    print("   ✅ Auto-generation disabled")
    
    # Test a task that would normally trigger generation
    print("3. Testing dispatch with auto-generation disabled...")
    try:
        recommendation = server.persona_dispatcher.select_persona(
            "analyze quantum computing algorithms for cryptography"
        )
        print(f"   🎯 Selected: {recommendation.persona_data['name']}")
        print(f"   📊 Confidence: {recommendation.confidence_score:.2f}")
        print(f"   🤖 Auto-Generated: {recommendation.persona_data.get('auto_generated', False)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Re-enable auto-generation
    print("4. Re-enabling auto-generation...")
    server.persona_dispatcher.enable_auto_generation(True)
    server.persona_dispatcher.set_confidence_threshold(0.3)
    print("   ✅ Auto-generation re-enabled")
    
    print("\n🎉 Auto-Generation Demo Complete!")
    print("\nKey Features Demonstrated:")
    print("✅ Automatic persona creation when confidence is low")
    print("✅ Domain-specific persona templates")
    print("✅ Configurable confidence thresholds")
    print("✅ Enable/disable auto-generation")
    print("✅ Tracking of generated personas")
    print("✅ Analytics and reporting")


if __name__ == "__main__":
    main()

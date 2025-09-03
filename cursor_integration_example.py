#!/usr/bin/env python3
"""
Cursor IDE Integration Example

This script demonstrates how Cursor IDE could automatically use the persona system
for every task. It shows the workflow that could be integrated into Cursor's
AI assistant behavior.
"""

import json
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from mcp_persona_server.persona_dispatcher import PersonaDispatcher
from mcp_persona_server.persona_manager import PersonaManager
from mcp_persona_server.storage import PersonaStorage

class CursorPersonaIntegration:
    """
    Demonstrates how Cursor IDE could automatically integrate with the persona system.
    """
    
    def __init__(self, storage_path="./personas"):
        self.storage = PersonaStorage(storage_path)
        self.persona_manager = PersonaManager(self.storage)
        self.persona_dispatcher = PersonaDispatcher(self.persona_manager)
    
    def process_user_request(self, user_request: str, context: str = "") -> dict:
        """
        Process a user request using automatic persona selection.
        
        This is what Cursor IDE could do automatically for every user request.
        """
        print(f"🎯 Processing request: '{user_request}'")
        print("=" * 60)
        
        # Step 1: Automatically select the best persona
        print("1️⃣ Selecting best persona...")
        recommendation = self.persona_dispatcher.select_persona(user_request, context)
        
        # Step 2: Display the selected persona
        selected_persona = recommendation.persona_data
        confidence = recommendation.confidence_score
        
        print(f"✅ Selected: {selected_persona['name']}")
        print(f"   Confidence: {confidence:.2f}")
        print(f"   Category: {recommendation.task_category.value}")
        print(f"   Description: {selected_persona['description']}")
        print(f"   Expertise: {', '.join(selected_persona.get('expertise', []))}")
        print(f"   Communication Style: {selected_persona.get('communication_style', 'N/A')}")
        
        # Step 3: Show reasoning
        if recommendation.reasoning:
            print(f"\n🔍 Reasoning:")
            for reason in recommendation.reasoning:
                print(f"   • {reason}")
        
        # Step 4: Generate persona-specific response
        print(f"\n2️⃣ Generating response as {selected_persona['name']}...")
        
        response = self._generate_persona_response(selected_persona, user_request, confidence)
        
        # Step 5: Show alternatives if confidence is low
        if confidence < 0.5 and recommendation.alternative_personas:
            print(f"\n⚠️  Low confidence ({confidence:.2f}). Consider alternatives:")
            for i, alt in enumerate(recommendation.alternative_personas[:3], 1):
                print(f"   {i}. {alt['name']} - {alt['description']}")
        
        return {
            "selected_persona": selected_persona,
            "confidence": confidence,
            "response": response,
            "reasoning": recommendation.reasoning,
            "alternatives": recommendation.alternative_personas
        }
    
    def _generate_persona_response(self, persona: dict, request: str, confidence: float) -> str:
        """
        Generate a response in the persona's style.
        """
        name = persona['name']
        expertise = persona.get('expertise', [])
        style = persona.get('communication_style', 'Professional')
        description = persona['description']
        
        # Create a persona-specific introduction
        if confidence > 0.7:
            intro = f"As {name}, I'm well-suited to help you with this task. "
        elif confidence > 0.4:
            intro = f"As {name}, I can assist you with this. "
        else:
            intro = f"As {name}, I'll do my best to help, though this may not be my primary expertise. "
        
        # Add expertise context
        if expertise:
            expertise_text = f"My expertise includes {', '.join(expertise[:3])}. "
        else:
            expertise_text = ""
        
        # Add communication style
        if style and style != "N/A":
            style_text = f"I communicate in a {style.lower()} manner. "
        else:
            style_text = ""
        
        # Combine into response
        response = f"{intro}{expertise_text}{style_text}\n\n{description}"
        
        print(f"📝 Response preview: {response[:100]}...")
        return response

def demonstrate_cursor_integration():
    """
    Demonstrate how Cursor IDE could automatically use personas.
    """
    print("🚀 Cursor IDE Persona Integration Demo")
    print("=" * 50)
    print("This shows how Cursor could automatically use personas for every task.\n")
    
    integration = CursorPersonaIntegration()
    
    # Example requests that Cursor might receive
    example_requests = [
        "Help me debug this Python code that's causing a segmentation fault",
        "Write a creative story about a time-traveling detective",
        "Analyze our quarterly sales data and provide strategic recommendations",
        "Explain quantum computing to a beginner high school student",
        "Design a user interface for a mobile banking app",
        "Create a comprehensive marketing strategy for our new product launch"
    ]
    
    for i, request in enumerate(example_requests, 1):
        print(f"\n📋 Example {i}: {request}")
        print("-" * 40)
        
        result = integration.process_user_request(request)
        
        print(f"\n✅ Final Result:")
        print(f"   Persona: {result['selected_persona']['name']}")
        print(f"   Confidence: {result['confidence']:.2f}")
        print(f"   Response Style: {result['selected_persona'].get('communication_style', 'N/A')}")
        
        if i < len(example_requests):
            print("\n" + "="*60 + "\n")

def create_cursor_instructions():
    """
    Create instructions that could be used in Cursor IDE.
    """
    instructions = """
# Cursor IDE Persona Integration Instructions

You have access to a sophisticated persona management system with 46 specialized personas. 
For every user request, automatically follow this workflow:

## Automatic Workflow:

1. **Analyze the task** - Understand what the user is asking for
2. **Select best persona** - Use the `select_persona` tool to find the most appropriate persona
3. **Adapt communication** - Respond in the selected persona's style and expertise area
4. **Provide expertise** - Use the persona's specialized knowledge and approach

## Available Personas:

### Technical Personas:
- **Tech Expert**: Python, AI, system architecture, code reviews
- **Software Engineer**: Programming, system design, debugging
- **Data Scientist**: Data analysis, machine learning, statistics

### Creative Personas:
- **Creative Writer**: Storytelling, content creation, marketing copy
- **Visual Designer**: Graphic design, visual communication, UI/UX

### Business Personas:
- **Business Analyst**: Business processes, data analysis, market research
- **Business Strategist**: Strategic planning, market analysis, competitive analysis

### Educational Personas:
- **Educator**: Teaching, curriculum design, explaining complex concepts

### Specialized Personas:
- **Medical Professional**: Healthcare, clinical expertise, patient care
- **Compliance Specialist**: Regulatory affairs, risk management, legal analysis
- **Research Scientist**: Scientific methodology, experimentation, analysis

## Response Format:

When responding, always:
1. Mention which persona you're using
2. Explain why this persona is appropriate
3. Respond in the persona's communication style
4. Use the persona's expertise areas

## Example:

User: "Help me debug this Python code"
Assistant: [Calls select_persona with "debug Python code"]
Assistant: "As a Tech Expert, I'm well-suited to help you debug this code. My expertise includes Python, system architecture, and problem-solving. Let me analyze this systematically..."

## Low Confidence Handling:

If the confidence score is below 0.5:
- Mention that this may not be your primary expertise
- Suggest alternative personas
- Offer to create a new specialized persona if needed

## Integration Commands:

- Use `select_persona` for automatic persona selection
- Use `list_personas` to see all available personas
- Use `create_persona` to create new specialized personas
- Use `search_personas` to find specific expertise areas
"""
    
    with open("cursor_persona_instructions.md", "w") as f:
        f.write(instructions)
    
    print("✅ Created cursor_persona_instructions.md")
    print("📝 You can use this as a .cursorrules file or system prompt")

if __name__ == "__main__":
    demonstrate_cursor_integration()
    create_cursor_instructions()
    
    print("\n🎉 Demo completed!")
    print("\nTo use this in Cursor IDE:")
    print("1. Copy the instructions from cursor_persona_instructions.md")
    print("2. Add them to your .cursorrules file or system prompt")
    print("3. Restart Cursor IDE")
    print("4. The AI will automatically use personas for every task!")




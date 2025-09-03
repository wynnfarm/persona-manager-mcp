"""
Persona management logic and intelligent persona selection.
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class PersonaManager:
    """Manages persona operations and intelligent selection."""
    
    def __init__(self, storage):
        self.storage = storage
        self._load_default_personas()
    
    def _load_default_personas(self):
        """Load default personas if storage is empty."""
        personas = self.storage.get_all_personas()
        if not personas:
            self._create_default_personas()
    
    def _create_default_personas(self):
        """Create default personas for demonstration."""
        default_personas = {
            "tech_expert": {
                "name": "Tech Expert",
                "description": "A knowledgeable software engineer with expertise in Python, AI, and system architecture",
                "expertise": ["Python", "Machine Learning", "Software Architecture", "API Design"],
                "communication_style": "Professional and technical",
                "context": "Use when discussing technical implementation details, code reviews, or system design",
                "personality_traits": ["analytical", "detail-oriented", "problem-solver"],
                "created_at": datetime.now().isoformat()
            },
            "creative_writer": {
                "name": "Creative Writer",
                "description": "An imaginative storyteller with a flair for engaging narratives and creative content",
                "expertise": ["Creative Writing", "Storytelling", "Content Creation", "Marketing Copy"],
                "communication_style": "Engaging and imaginative",
                "context": "Use when creating stories, marketing content, or creative writing projects",
                "personality_traits": ["creative", "imaginative", "expressive"],
                "created_at": datetime.now().isoformat()
            },
            "business_analyst": {
                "name": "Business Analyst",
                "description": "A strategic thinker focused on business processes, data analysis, and market insights",
                "expertise": ["Business Analysis", "Data Analysis", "Process Optimization", "Market Research"],
                "communication_style": "Strategic and analytical",
                "context": "Use when analyzing business processes, market trends, or strategic planning",
                "personality_traits": ["strategic", "analytical", "business-focused"],
                "created_at": datetime.now().isoformat()
            },
            "educator": {
                "name": "Educator",
                "description": "A patient teacher who excels at explaining complex concepts in simple terms",
                "expertise": ["Education", "Curriculum Design", "Instructional Design", "Learning Theory"],
                "communication_style": "Patient and explanatory",
                "context": "Use when teaching concepts, creating educational content, or explaining complex topics",
                "personality_traits": ["patient", "explanatory", "encouraging"],
                "created_at": datetime.now().isoformat()
            }
        }
        
        for persona_id, persona_data in default_personas.items():
            self.storage.save_persona(persona_id, persona_data)
        
        logger.info("Created default personas")
    
    def create_persona(self, persona_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Create a new persona."""
        try:
            # Validate required fields
            required_fields = ["name", "description", "expertise"]
            for field in required_fields:
                if field not in persona_data:
                    return False, f"Missing required field: {field}"
            
            # Generate persona ID
            persona_id = self._generate_persona_id(persona_data["name"])
            
            # Check if persona already exists
            if self.storage.get_persona(persona_id):
                return False, f"Persona with name '{persona_data['name']}' already exists"
            
            # Add metadata
            persona_data["created_at"] = datetime.now().isoformat()
            persona_data["updated_at"] = datetime.now().isoformat()
            
            # Save persona
            success = self.storage.save_persona(persona_id, persona_data)
            if success:
                return True, persona_id
            else:
                return False, "Failed to save persona"
                
        except Exception as e:
            logger.error(f"Error creating persona: {e}")
            return False, str(e)
    
    def _generate_persona_id(self, name: str) -> str:
        """Generate a unique persona ID from name."""
        # Convert to lowercase and replace spaces with underscores
        base_id = re.sub(r'[^a-zA-Z0-9\s]', '', name.lower()).replace(' ', '_')
        
        # Ensure uniqueness
        counter = 1
        persona_id = base_id
        while self.storage.get_persona(persona_id):
            persona_id = f"{base_id}_{counter}"
            counter += 1
        
        return persona_id
    
    def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific persona."""
        return self.storage.get_persona(persona_id)
    
    def get_all_personas(self) -> Dict[str, Any]:
        """Get all personas."""
        return self.storage.get_all_personas()
    
    def update_persona(self, persona_id: str, updates: Dict[str, Any]) -> Tuple[bool, str]:
        """Update an existing persona."""
        try:
            existing_persona = self.storage.get_persona(persona_id)
            if not existing_persona:
                return False, f"Persona '{persona_id}' not found"
            
            # Update fields
            updated_persona = {**existing_persona, **updates}
            updated_persona["updated_at"] = datetime.now().isoformat()
            
            # Save updated persona
            success = self.storage.save_persona(persona_id, updated_persona)
            if success:
                return True, "Persona updated successfully"
            else:
                return False, "Failed to update persona"
                
        except Exception as e:
            logger.error(f"Error updating persona {persona_id}: {e}")
            return False, str(e)
    
    def delete_persona(self, persona_id: str) -> Tuple[bool, str]:
        """Delete a persona."""
        try:
            success = self.storage.delete_persona(persona_id)
            if success:
                return True, "Persona deleted successfully"
            else:
                return False, f"Persona '{persona_id}' not found"
        except Exception as e:
            logger.error(f"Error deleting persona {persona_id}: {e}")
            return False, str(e)
    
    def search_personas(self, query: str) -> List[Dict[str, Any]]:
        """Search personas by query."""
        return self.storage.search_personas(query)
    
    def select_best_persona(self, task_description: str, context: str = "") -> Optional[Dict[str, Any]]:
        """Intelligently select the best persona for a given task."""
        try:
            personas = self.storage.get_all_personas()
            if not personas:
                return None
            
            best_match = None
            best_score = 0
            
            for persona_id, persona_data in personas.items():
                score = self._calculate_persona_match_score(
                    persona_data, task_description, context
                )
                
                if score > best_score:
                    best_score = score
                    best_match = {"id": persona_id, **persona_data}
            
            # Only return if score is above threshold
            if best_score > 0.3:  # 30% threshold
                logger.info(f"Selected persona '{best_match['name']}' with score {best_score:.2f}")
                return best_match
            else:
                logger.info(f"No suitable persona found (best score: {best_score:.2f})")
                return None
                
        except Exception as e:
            logger.error(f"Error selecting best persona: {e}")
            return None
    
    def _calculate_persona_match_score(self, persona_data: Dict[str, Any], 
                                     task_description: str, context: str = "") -> float:
        """Calculate how well a persona matches a task."""
        score = 0.0
        task_lower = (task_description + " " + context).lower()
        
        # Check expertise match
        expertise = persona_data.get("expertise", [])
        for exp in expertise:
            if exp.lower() in task_lower:
                score += 0.4  # High weight for expertise match
        
        # Check name match
        name = persona_data.get("name", "").lower()
        if name in task_lower:
            score += 0.3
        
        # Check description match
        description = persona_data.get("description", "").lower()
        description_score = SequenceMatcher(None, task_lower, description).ratio()
        score += description_score * 0.2
        
        # Check context match
        context_info = persona_data.get("context", "").lower()
        if context_info and any(word in task_lower for word in context_info.split()):
            score += 0.1
        
        # Check personality traits
        traits = persona_data.get("personality_traits", [])
        for trait in traits:
            if trait.lower() in task_lower:
                score += 0.05
        
        return min(score, 1.0)  # Cap at 1.0
    
    def get_persona_suggestions(self, task_description: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get multiple persona suggestions for a task, ranked by relevance."""
        try:
            personas = self.storage.get_all_personas()
            if not personas:
                return []
            
            scored_personas = []
            for persona_id, persona_data in personas.items():
                score = self._calculate_persona_match_score(persona_data, task_description)
                scored_personas.append({
                    "id": persona_id,
                    "score": score,
                    **persona_data
                })
            
            # Sort by score and return top matches
            scored_personas.sort(key=lambda x: x["score"], reverse=True)
            return scored_personas[:limit]
            
        except Exception as e:
            logger.error(f"Error getting persona suggestions: {e}")
            return []
    
    def get_persona_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored personas."""
        try:
            personas = self.storage.get_all_personas()
            metadata = self.storage.get_metadata()
            
            # Calculate statistics
            total_personas = len(personas)
            expertise_counts = {}
            communication_styles = {}
            
            for persona_data in personas.values():
                # Count expertise areas
                for expertise in persona_data.get("expertise", []):
                    expertise_counts[expertise] = expertise_counts.get(expertise, 0) + 1
                
                # Count communication styles
                style = persona_data.get("communication_style", "Unknown")
                communication_styles[style] = communication_styles.get(style, 0) + 1
            
            return {
                "total_personas": total_personas,
                "expertise_distribution": expertise_counts,
                "communication_style_distribution": communication_styles,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error getting persona statistics: {e}")
            return {}

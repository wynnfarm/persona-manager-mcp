"""
Utility functions for the MCP persona server.
"""

import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def validate_persona_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate persona data structure."""
    try:
        # Check required fields
        required_fields = ["name", "description", "expertise"]
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Validate name
        if not isinstance(data["name"], str) or len(data["name"].strip()) == 0:
            return False, "Name must be a non-empty string"
        
        # Validate description
        if not isinstance(data["description"], str) or len(data["description"].strip()) == 0:
            return False, "Description must be a non-empty string"
        
        # Validate expertise
        if not isinstance(data["expertise"], list) or len(data["expertise"]) == 0:
            return False, "Expertise must be a non-empty list"
        
        for exp in data["expertise"]:
            if not isinstance(exp, str) or len(exp.strip()) == 0:
                return False, "All expertise items must be non-empty strings"
        
        # Validate optional fields
        optional_fields = ["communication_style", "context", "personality_traits"]
        for field in optional_fields:
            if field in data:
                if field == "personality_traits":
                    if not isinstance(data[field], list):
                        return False, f"{field} must be a list"
                    for trait in data[field]:
                        if not isinstance(trait, str) or len(trait.strip()) == 0:
                            return False, f"All {field} items must be non-empty strings"
                else:
                    if not isinstance(data[field], str):
                        return False, f"{field} must be a string"
        
        return True, "Validation successful"
        
    except Exception as e:
        logger.error(f"Error validating persona data: {e}")
        return False, f"Validation error: {str(e)}"


def sanitize_persona_id(name: str) -> str:
    """Sanitize a name to create a valid persona ID."""
    # Remove special characters and convert to lowercase
    sanitized = re.sub(r'[^a-zA-Z0-9\s]', '', name.lower())
    # Replace spaces with underscores
    sanitized = re.sub(r'\s+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    return sanitized


def format_persona_display(persona: Dict[str, Any]) -> str:
    """Format a persona for display."""
    lines = []
    lines.append(f"🎭 {persona.get('name', 'Unknown')}")
    lines.append(f"📝 {persona.get('description', 'No description')}")
    
    expertise = persona.get('expertise', [])
    if expertise:
        lines.append(f"🔧 Expertise: {', '.join(expertise)}")
    
    communication_style = persona.get('communication_style')
    if communication_style:
        lines.append(f"💬 Style: {communication_style}")
    
    context = persona.get('context')
    if context:
        lines.append(f"🎯 Use when: {context}")
    
    personality_traits = persona.get('personality_traits', [])
    if personality_traits:
        lines.append(f"✨ Traits: {', '.join(personality_traits)}")
    
    created_at = persona.get('created_at')
    if created_at:
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            lines.append(f"📅 Created: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        except:
            pass
    
    return '\n'.join(lines)


def calculate_similarity_score(text1: str, text2: str) -> float:
    """Calculate similarity between two text strings."""
    try:
        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    except ImportError:
        # Fallback to simple word overlap
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union)


def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text for better matching."""
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
    }
    
    # Extract words and filter
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords


def merge_persona_updates(existing: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Merge updates into existing persona data."""
    merged = existing.copy()
    
    for key, value in updates.items():
        if key in ["expertise", "personality_traits"] and isinstance(value, list):
            # For list fields, replace the entire list
            merged[key] = value
        elif key in ["name", "description", "communication_style", "context"]:
            # For string fields, replace the value
            merged[key] = value
        else:
            # For other fields, update if provided
            merged[key] = value
    
    # Update timestamp
    merged["updated_at"] = datetime.now().isoformat()
    
    return merged


def create_persona_summary(personas: Dict[str, Any]) -> Dict[str, Any]:
    """Create a summary of all personas."""
    if not personas:
        return {"total": 0, "summary": "No personas available"}
    
    total = len(personas)
    expertise_counts = {}
    style_counts = {}
    
    for persona_data in personas.values():
        # Count expertise areas
        for expertise in persona_data.get("expertise", []):
            expertise_counts[expertise] = expertise_counts.get(expertise, 0) + 1
        
        # Count communication styles
        style = persona_data.get("communication_style", "Unknown")
        style_counts[style] = style_counts.get(style, 0) + 1
    
    # Get top expertise areas
    top_expertise = sorted(expertise_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Get top communication styles
    top_styles = sorted(style_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        "total": total,
        "top_expertise": top_expertise,
        "top_communication_styles": top_styles,
        "expertise_distribution": expertise_counts,
        "style_distribution": style_counts
    }


def export_personas_to_json(personas: Dict[str, Any], filepath: str) -> bool:
    """Export personas to a JSON file."""
    try:
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "total_personas": len(personas),
            "personas": personas
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(personas)} personas to {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Error exporting personas: {e}")
        return False


def import_personas_from_json(filepath: str) -> tuple[bool, str, Dict[str, Any]]:
    """Import personas from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        if "personas" not in import_data:
            return False, "Invalid file format: missing 'personas' key", {}
        
        personas = import_data["personas"]
        
        # Validate imported personas
        for persona_id, persona_data in personas.items():
            is_valid, error_msg = validate_persona_data(persona_data)
            if not is_valid:
                return False, f"Invalid persona data for {persona_id}: {error_msg}", {}
        
        logger.info(f"Imported {len(personas)} personas from {filepath}")
        return True, f"Successfully imported {len(personas)} personas", personas
        
    except FileNotFoundError:
        return False, f"File not found: {filepath}", {}
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {e}", {}
    except Exception as e:
        logger.error(f"Error importing personas: {e}")
        return False, f"Import error: {str(e)}", {}

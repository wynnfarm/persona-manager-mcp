"""
Storage layer for persona data persistence.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PersonaStorage:
    """Handles persistence of persona data to file system."""
    
    def __init__(self, storage_path: str = "./personas"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.personas_file = self.storage_path / "personas.json"
        self.metadata_file = self.storage_path / "metadata.json"
        
        # Initialize storage
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Ensure storage files exist with proper structure."""
        if not self.personas_file.exists():
            self._save_personas({})
        
        if not self.metadata_file.exists():
            self._save_metadata({
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0"
            })
    
    def _load_personas(self) -> Dict[str, Any]:
        """Load personas from storage."""
        try:
            with open(self.personas_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Error loading personas: {e}")
            return {}
    
    def _save_personas(self, personas: Dict[str, Any]):
        """Save personas to storage."""
        try:
            with open(self.personas_file, 'w', encoding='utf-8') as f:
                json.dump(personas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving personas: {e}")
            raise
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from storage."""
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Error loading metadata: {e}")
            return {}
    
    def _save_metadata(self, metadata: Dict[str, Any]):
        """Save metadata to storage."""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
            raise
    
    def save_persona(self, persona_id: str, persona_data: Dict[str, Any]) -> bool:
        """Save a single persona."""
        try:
            personas = self._load_personas()
            personas[persona_id] = {
                **persona_data,
                "updated_at": datetime.now().isoformat(),
                "id": persona_id
            }
            self._save_personas(personas)
            
            # Update metadata
            metadata = self._load_metadata()
            metadata["last_updated"] = datetime.now().isoformat()
            metadata["total_personas"] = len(personas)
            self._save_metadata(metadata)
            
            logger.info(f"Saved persona: {persona_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving persona {persona_id}: {e}")
            return False
    
    def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single persona."""
        try:
            personas = self._load_personas()
            return personas.get(persona_id)
        except Exception as e:
            logger.error(f"Error retrieving persona {persona_id}: {e}")
            return None
    
    def get_all_personas(self) -> Dict[str, Any]:
        """Retrieve all personas."""
        try:
            return self._load_personas()
        except Exception as e:
            logger.error(f"Error retrieving all personas: {e}")
            return {}
    
    def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona."""
        try:
            personas = self._load_personas()
            if persona_id in personas:
                del personas[persona_id]
                self._save_personas(personas)
                
                # Update metadata
                metadata = self._load_metadata()
                metadata["last_updated"] = datetime.now().isoformat()
                metadata["total_personas"] = len(personas)
                self._save_metadata(metadata)
                
                logger.info(f"Deleted persona: {persona_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting persona {persona_id}: {e}")
            return False
    
    def search_personas(self, query: str) -> List[Dict[str, Any]]:
        """Search personas by name, description, or expertise."""
        try:
            personas = self._load_personas()
            results = []
            query_lower = query.lower()
            
            for persona_id, persona_data in personas.items():
                # Search in name, description, and expertise
                if (query_lower in persona_data.get("name", "").lower() or
                    query_lower in persona_data.get("description", "").lower() or
                    any(query_lower in exp.lower() for exp in persona_data.get("expertise", []))):
                    results.append({"id": persona_id, **persona_data})
            
            return results
        except Exception as e:
            logger.error(f"Error searching personas: {e}")
            return []
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get storage metadata."""
        try:
            metadata = self._load_metadata()
            personas = self._load_personas()
            metadata["total_personas"] = len(personas)
            return metadata
        except Exception as e:
            logger.error(f"Error retrieving metadata: {e}")
            return {}
    
    def backup_personas(self, backup_path: str) -> bool:
        """Create a backup of all personas."""
        try:
            personas = self._load_personas()
            metadata = self._load_metadata()
            
            backup_data = {
                "personas": personas,
                "metadata": metadata,
                "backup_created_at": datetime.now().isoformat()
            }
            
            backup_file = Path(backup_path)
            backup_file.parent.mkdir(exist_ok=True)
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Created backup at: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False

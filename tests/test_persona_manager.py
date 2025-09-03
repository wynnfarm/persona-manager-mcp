"""
Unit tests for the PersonaManager class.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from mcp_persona_server.persona_manager import PersonaManager
from mcp_persona_server.storage import PersonaStorage


class TestPersonaManager:
    """Test cases for PersonaManager."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create a temporary storage directory for testing."""
        temp_dir = tempfile.mkdtemp()
        storage = PersonaStorage(temp_dir)
        yield storage
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def persona_manager(self, temp_storage):
        """Create a PersonaManager instance with temporary storage."""
        return PersonaManager(temp_storage)
    
    def test_create_persona_success(self, persona_manager):
        """Test successful persona creation."""
        persona_data = {
            "name": "Test Persona",
            "description": "A test persona for unit testing",
            "expertise": ["Testing", "Unit Tests", "Python"],
            "communication_style": "Test-oriented",
            "context": "Use for testing purposes",
            "personality_traits": ["thorough", "systematic"]
        }
        
        success, result = persona_manager.create_persona(persona_data)
        
        assert success is True
        assert isinstance(result, str)
        assert "test_persona" in result
        
        # Verify persona was saved
        saved_persona = persona_manager.get_persona(result)
        assert saved_persona is not None
        assert saved_persona["name"] == "Test Persona"
        assert saved_persona["expertise"] == ["Testing", "Unit Tests", "Python"]
    
    def test_create_persona_missing_required_fields(self, persona_manager):
        """Test persona creation with missing required fields."""
        # Missing name
        persona_data = {
            "description": "A test persona",
            "expertise": ["Testing"]
        }
        
        success, result = persona_manager.create_persona(persona_data)
        
        assert success is False
        assert "Missing required field" in result
        
        # Missing description
        persona_data = {
            "name": "Test Persona",
            "expertise": ["Testing"]
        }
        
        success, result = persona_manager.create_persona(persona_data)
        
        assert success is False
        assert "Missing required field" in result
    
    def test_create_duplicate_persona(self, persona_manager):
        """Test creating a persona with duplicate name."""
        persona_data = {
            "name": "Test Persona",
            "description": "A test persona",
            "expertise": ["Testing"]
        }
        
        # Create first persona
        success1, result1 = persona_manager.create_persona(persona_data)
        assert success1 is True
        
        # Try to create duplicate
        success2, result2 = persona_manager.create_persona(persona_data)
        assert success2 is False
        assert "already exists" in result2
    
    def test_get_persona(self, persona_manager):
        """Test retrieving a specific persona."""
        # Create a persona
        persona_data = {
            "name": "Test Persona",
            "description": "A test persona",
            "expertise": ["Testing"]
        }
        
        success, persona_id = persona_manager.create_persona(persona_data)
        assert success is True
        
        # Retrieve the persona
        persona = persona_manager.get_persona(persona_id)
        assert persona is not None
        assert persona["name"] == "Test Persona"
        assert persona["expertise"] == ["Testing"]
    
    def test_get_nonexistent_persona(self, persona_manager):
        """Test retrieving a persona that doesn't exist."""
        persona = persona_manager.get_persona("nonexistent_id")
        assert persona is None
    
    def test_get_all_personas(self, persona_manager):
        """Test retrieving all personas."""
        # Create multiple personas
        personas_data = [
            {
                "name": "Persona 1",
                "description": "First test persona",
                "expertise": ["Testing"]
            },
            {
                "name": "Persona 2",
                "description": "Second test persona",
                "expertise": ["Testing"]
            }
        ]
        
        for persona_data in personas_data:
            success, _ = persona_manager.create_persona(persona_data)
            assert success is True
        
        # Get all personas
        all_personas = persona_manager.get_all_personas()
        assert len(all_personas) >= 2  # Including default personas
    
    def test_update_persona(self, persona_manager):
        """Test updating an existing persona."""
        # Create a persona
        persona_data = {
            "name": "Test Persona",
            "description": "Original description",
            "expertise": ["Original"]
        }
        
        success, persona_id = persona_manager.create_persona(persona_data)
        assert success is True
        
        # Update the persona
        updates = {
            "description": "Updated description",
            "expertise": ["Updated", "New"]
        }
        
        success, message = persona_manager.update_persona(persona_id, updates)
        assert success is True
        assert "updated successfully" in message
        
        # Verify updates
        updated_persona = persona_manager.get_persona(persona_id)
        assert updated_persona["description"] == "Updated description"
        assert updated_persona["expertise"] == ["Updated", "New"]
    
    def test_update_nonexistent_persona(self, persona_manager):
        """Test updating a persona that doesn't exist."""
        updates = {"description": "Updated"}
        
        success, message = persona_manager.update_persona("nonexistent_id", updates)
        assert success is False
        assert "not found" in message
    
    def test_delete_persona(self, persona_manager):
        """Test deleting a persona."""
        # Create a persona
        persona_data = {
            "name": "Test Persona",
            "description": "A test persona",
            "expertise": ["Testing"]
        }
        
        success, persona_id = persona_manager.create_persona(persona_data)
        assert success is True
        
        # Delete the persona
        success, message = persona_manager.delete_persona(persona_id)
        assert success is True
        assert "deleted successfully" in message
        
        # Verify deletion
        persona = persona_manager.get_persona(persona_id)
        assert persona is None
    
    def test_delete_nonexistent_persona(self, persona_manager):
        """Test deleting a persona that doesn't exist."""
        success, message = persona_manager.delete_persona("nonexistent_id")
        assert success is False
        assert "not found" in message
    
    def test_search_personas(self, persona_manager):
        """Test searching personas."""
        # Create personas with different expertise
        personas_data = [
            {
                "name": "Python Developer",
                "description": "A Python expert",
                "expertise": ["Python", "Web Development"]
            },
            {
                "name": "Data Scientist",
                "description": "A data expert",
                "expertise": ["Data Analysis", "Machine Learning"]
            }
        ]
        
        for persona_data in personas_data:
            success, _ = persona_manager.create_persona(persona_data)
            assert success is True
        
        # Search for Python
        results = persona_manager.search_personas("Python")
        assert len(results) >= 1
        assert any("Python" in result["name"] for result in results)
        
        # Search for data
        results = persona_manager.search_personas("data")
        assert len(results) >= 1
        assert any("Data" in result["name"] for result in results)
    
    def test_select_best_persona(self, persona_manager):
        """Test selecting the best persona for a task."""
        # Create personas with specific expertise
        personas_data = [
            {
                "name": "Tech Expert",
                "description": "A technical expert",
                "expertise": ["Python", "Programming", "Debugging"],
                "context": "Use for technical tasks"
            },
            {
                "name": "Creative Writer",
                "description": "A creative writer",
                "expertise": ["Writing", "Creative Content"],
                "context": "Use for creative tasks"
            }
        ]
        
        for persona_data in personas_data:
            success, _ = persona_manager.create_persona(persona_data)
            assert success is True
        
        # Select best persona for technical task
        best_persona = persona_manager.select_best_persona("debug Python code")
        assert best_persona is not None
        assert "Tech" in best_persona["name"]
        
        # Select best persona for creative task
        best_persona = persona_manager.select_best_persona("write a story")
        assert best_persona is not None
        assert "Creative" in best_persona["name"]
    
    def test_get_persona_suggestions(self, persona_manager):
        """Test getting persona suggestions."""
        # Create multiple personas
        personas_data = [
            {
                "name": "Tech Expert",
                "description": "Technical expert",
                "expertise": ["Programming", "Technology"]
            },
            {
                "name": "Designer",
                "description": "Design expert",
                "expertise": ["Design", "UI/UX"]
            },
            {
                "name": "Writer",
                "description": "Writing expert",
                "expertise": ["Writing", "Content"]
            }
        ]
        
        for persona_data in personas_data:
            success, _ = persona_manager.create_persona(persona_data)
            assert success is True
        
        # Get suggestions
        suggestions = persona_manager.get_persona_suggestions("technical programming task", limit=2)
        assert len(suggestions) <= 2
        assert all("score" in suggestion for suggestion in suggestions)
        assert suggestions[0]["score"] >= suggestions[1]["score"]  # Sorted by score
    
    def test_get_persona_statistics(self, persona_manager):
        """Test getting persona statistics."""
        # Create personas
        personas_data = [
            {
                "name": "Tech Expert",
                "description": "Technical expert",
                "expertise": ["Programming", "Technology"],
                "communication_style": "Technical"
            },
            {
                "name": "Designer",
                "description": "Design expert",
                "expertise": ["Design", "UI/UX"],
                "communication_style": "Creative"
            }
        ]
        
        for persona_data in personas_data:
            success, _ = persona_manager.create_persona(persona_data)
            assert success is True
        
        # Get statistics
        stats = persona_manager.get_persona_statistics()
        
        assert "total_personas" in stats
        assert "expertise_distribution" in stats
        assert "communication_style_distribution" in stats
        assert stats["total_personas"] >= 2
        assert "Programming" in stats["expertise_distribution"]
        assert "Technical" in stats["communication_style_distribution"]

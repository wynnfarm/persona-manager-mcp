#!/usr/bin/env python3
"""
Context Integration for Persona Manager

This module provides active integration with the context_manager to enable
intelligent, context-aware persona selection and task routing.
"""

import os
import requests
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ProjectContext:
    """Project context data structure."""
    name: str
    current_goal: str
    completed_features: List[str]
    current_issues: List[str]
    next_steps: List[str]
    current_state: Dict[str, Any]
    key_files: List[str]
    context_anchors: List[str]
    conversation_history: List[Dict[str, Any]]
    created_at: str
    updated_at: str

class ContextIntegration:
    """
    Active integration with context_manager for intelligent decision-making.
    """
    
    def __init__(self, context_manager_url: str = None):
        self.context_manager_url = context_manager_url or os.getenv(
            "CONTEXT_MANAGER_URL", "http://localhost:8000"
        )
        self.project_name = os.getenv("CONTEXT_PROJECT_NAME", "persona-manager-mcp")
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes cache
    
    def get_project_context(self, force_refresh: bool = False) -> Optional[ProjectContext]:
        """Get current project context from context_manager."""
        try:
            # Check cache first
            if not force_refresh and self._is_cache_valid():
                return self.cache.get("context")
            
            # Fetch from context_manager
            response = requests.get(
                f"{self.context_manager_url}/project/{self.project_name}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                context_data = data.get("context", {})
                
                context = ProjectContext(
                    name=context_data.get("name", self.project_name),
                    current_goal=context_data.get("current_goal", ""),
                    completed_features=context_data.get("completed_features", []),
                    current_issues=context_data.get("current_issues", []),
                    next_steps=context_data.get("next_steps", []),
                    current_state=context_data.get("current_state", {}),
                    key_files=context_data.get("key_files", []),
                    context_anchors=context_data.get("context_anchors", []),
                    conversation_history=context_data.get("conversation_history", []),
                    created_at=context_data.get("created_at", ""),
                    updated_at=context_data.get("updated_at", "")
                )
                
                # Update cache
                self.cache["context"] = context
                self.cache["timestamp"] = datetime.now()
                
                logger.info(f"Retrieved context for project: {self.project_name}")
                return context
            else:
                logger.warning(f"Failed to get context: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting project context: {e}")
            return None
    
    def _is_cache_valid(self) -> bool:
        """Check if cached context is still valid."""
        if "timestamp" not in self.cache:
            return False
        
        cache_age = (datetime.now() - self.cache["timestamp"]).total_seconds()
        return cache_age < self.cache_ttl
    
    def analyze_context_for_task(self, task: str) -> Dict[str, Any]:
        """Analyze context to determine task requirements and priorities."""
        context = self.get_project_context()
        if not context:
            return {"priority": "medium", "domain": "general", "urgency": "normal"}
        
        analysis = {
            "priority": "medium",
            "domain": "general",
            "urgency": "normal",
            "context_relevance": 0.0,
            "recommended_personas": [],
            "context_insights": []
        }
        
        # Analyze task against current goal
        goal_relevance = self._calculate_text_similarity(task, context.current_goal)
        if goal_relevance > 0.3:
            analysis["priority"] = "high"
            analysis["context_relevance"] += goal_relevance
            analysis["context_insights"].append(f"Task aligns with current goal: {context.current_goal}")
        
        # Check if task addresses current issues
        for issue in context.current_issues:
            issue_relevance = self._calculate_text_similarity(task, issue)
            if issue_relevance > 0.4:
                analysis["urgency"] = "high"
                analysis["context_relevance"] += issue_relevance
                analysis["context_insights"].append(f"Task addresses current issue: {issue}")
        
        # Check if task supports next steps
        for step in context.next_steps:
            step_relevance = self._calculate_text_similarity(task, step)
            if step_relevance > 0.3:
                analysis["priority"] = "high"
                analysis["context_relevance"] += step_relevance
                analysis["context_insights"].append(f"Task supports next step: {step}")
        
        # Determine domain based on context
        analysis["domain"] = self._determine_domain_from_context(context, task)
        
        # Generate persona recommendations
        analysis["recommended_personas"] = self._recommend_personas_from_context(context, task)
        
        return analysis
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity score."""
        if not text1 or not text2:
            return 0.0
        
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _determine_domain_from_context(self, context: ProjectContext, task: str) -> str:
        """Determine the domain based on context and task."""
        domain_keywords = {
            "technical": ["code", "programming", "software", "technical", "implementation", "debug", "api", "database", "server", "deployment"],
            "business": ["business", "analysis", "strategy", "market", "process", "optimization", "roi", "efficiency"],
            "creative": ["write", "story", "creative", "narrative", "content", "marketing", "copy", "brand"],
            "educational": ["teach", "explain", "educate", "learn", "training", "curriculum", "tutorial"],
            "design": ["design", "ui", "ux", "visual", "graphic", "aesthetic", "interface", "prototype"],
            "scientific": ["research", "scientific", "methodology", "evidence", "analysis", "experiment", "data"],
            "consulting": ["consult", "advise", "strategy", "problem solving", "organizational", "solution"]
        }
        
        # Check task and context for domain keywords
        combined_text = f"{task} {context.current_goal} {' '.join(context.current_issues)} {' '.join(context.next_steps)}".lower()
        
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            domain_scores[domain] = score
        
        # Return domain with highest score
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        
        return "general"
    
    def _recommend_personas_from_context(self, context: ProjectContext, task: str) -> List[str]:
        """Recommend personas based on context and task."""
        recommendations = []
        
        # Technical personas
        if any(keyword in task.lower() for keyword in ["code", "programming", "software", "technical", "api", "database"]):
            recommendations.extend(["tech_expert", "software_engineer"])
        
        # Business personas
        if any(keyword in task.lower() for keyword in ["business", "analysis", "strategy", "market", "process"]):
            recommendations.extend(["business_analyst", "domain_specialist"])
        
        # Creative personas
        if any(keyword in task.lower() for keyword in ["write", "story", "creative", "content", "marketing"]):
            recommendations.extend(["creative_writer", "domain_specialist"])
        
        # Educational personas
        if any(keyword in task.lower() for keyword in ["teach", "explain", "educate", "learn", "tutorial"]):
            recommendations.extend(["educator", "domain_specialist"])
        
        # Data personas
        if any(keyword in task.lower() for keyword in ["data", "analysis", "statistics", "research"]):
            recommendations.extend(["data_scientist", "business_analyst"])
        
        # Remove duplicates and return
        return list(set(recommendations))
    
    def update_context_from_task(self, task: str, result: str, persona_used: str):
        """Update context based on task completion."""
        try:
            # Use the new comprehensive task completion endpoint
            task_data = {
                "task": task,
                "result": result,
                "persona_used": persona_used,
                "completion_type": "general"  # Let the API determine the type
            }
            
            response = requests.post(
                f"{self.context_manager_url}/project/{self.project_name}/task/complete",
                json=task_data,
                timeout=10
            )
            
            if response.status_code == 200:
                response_data = response.json()
                logger.info(f"Successfully updated context from task completion: {task[:50]}...")
                logger.info(f"Completion type: {response_data.get('data', {}).get('completion_type', 'unknown')}")
                return True
            else:
                logger.warning(f"Failed to update context from task: {response.status_code}")
                # Fallback to individual method calls
                return self._fallback_context_update(task, result, persona_used)
            
        except Exception as e:
            logger.error(f"Error updating context from task: {e}")
            # Fallback to individual method calls
            return self._fallback_context_update(task, result, persona_used)
    
    def _fallback_context_update(self, task: str, result: str, persona_used: str):
        """Fallback method using individual API calls."""
        try:
            context = self.get_project_context()
            if not context:
                return False
            
            # Analyze if task completion affects project state
            task_lower = task.lower()
            success_count = 0
            
            # Check if this was a feature completion
            if any(keyword in task_lower for keyword in ["implement", "complete", "finish", "done"]):
                if self._add_to_completed_features(task, result):
                    success_count += 1
            
            # Check if this resolves an issue
            if any(keyword in task_lower for keyword in ["fix", "resolve", "solve", "address"]):
                if self._resolve_issue(task, result):
                    success_count += 1
            
            # Check if this adds a new step
            if any(keyword in task_lower for keyword in ["plan", "next", "should", "need to"]):
                if self._add_next_step(task, result):
                    success_count += 1
            
            # Log the interaction
            if self._log_interaction(task, result, persona_used):
                success_count += 1
            
            logger.info(f"Fallback context update completed: {success_count} operations successful")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Error in fallback context update: {e}")
            return False
    
    def _add_to_completed_features(self, task: str, result: str):
        """Add completed feature to context."""
        try:
            response = requests.post(
                f"{self.context_manager_url}/project/{self.project_name}/complete-feature",
                json={"feature": task},
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"Added completed feature: {task}")
                return True
            else:
                logger.warning(f"Failed to add completed feature: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error adding completed feature: {e}")
            return False
    
    def _resolve_issue(self, task: str, result: str):
        """Resolve issue in context."""
        try:
            # Try to find matching issue from context
            context = self.get_project_context()
            if not context:
                return False
            
            matching_issue = None
            for issue in context.current_issues:
                if any(keyword in issue.lower() for keyword in task.lower().split()):
                    matching_issue = issue
                    break
            
            if matching_issue:
                response = requests.post(
                    f"{self.context_manager_url}/project/{self.project_name}/resolve-issue",
                    json={"issue": matching_issue},
                    timeout=5
                )
                if response.status_code == 200:
                    logger.info(f"Resolved issue: {matching_issue}")
                    return True
                else:
                    logger.warning(f"Failed to resolve issue: {response.status_code}")
                    return False
            else:
                logger.info(f"No matching issue found for task: {task}")
                return False
        except Exception as e:
            logger.error(f"Error resolving issue: {e}")
            return False
    
    def _add_next_step(self, task: str, result: str):
        """Add next step to context."""
        try:
            response = requests.post(
                f"{self.context_manager_url}/project/{self.project_name}/add-step",
                json={"step": task},
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"Added next step: {task}")
                return True
            else:
                logger.warning(f"Failed to add next step: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error adding next step: {e}")
            return False
    
    def _log_interaction(self, task: str, result: str, persona_used: str):
        """Log interaction in conversation history."""
        try:
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "type": "task_completion",
                "task": task,
                "result": result,
                "persona_used": persona_used
            }
            
            response = requests.post(
                f"{self.context_manager_url}/project/{self.project_name}/log-interaction",
                json=interaction,
                timeout=5
            )
            if response.status_code == 200:
                logger.info(f"Logged interaction for task: {task}")
                return True
            else:
                logger.warning(f"Failed to log interaction: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error logging interaction: {e}")
            return False
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of current project context."""
        context = self.get_project_context()
        if not context:
            return {"error": "No context available"}
        
        return {
            "project_name": context.name,
            "current_goal": context.current_goal,
            "progress": {
                "features_completed": len(context.completed_features),
                "issues_open": len(context.current_issues),
                "steps_pending": len(context.next_steps),
                "completion_percentage": len(context.completed_features) / max(len(context.completed_features) + len(context.next_steps), 1) * 100
            },
            "current_focus": {
                "primary_goal": context.current_goal,
                "active_issues": context.current_issues,
                "next_priorities": context.next_steps[:3]  # Top 3 next steps
            },
            "last_updated": context.updated_at
        }
    
    def suggest_task_priorities(self) -> List[str]:
        """Suggest task priorities based on context."""
        context = self.get_project_context()
        if not context:
            return ["No context available for suggestions"]
        
        suggestions = []
        
        # Suggest addressing current issues
        for issue in context.current_issues:
            suggestions.append(f"Address issue: {issue}")
        
        # Suggest next steps
        for step in context.next_steps:
            suggestions.append(f"Work on: {step}")
        
        # Suggest goal-related tasks
        if context.current_goal:
            suggestions.append(f"Progress toward goal: {context.current_goal}")
        
        return suggestions[:5]  # Return top 5 suggestions

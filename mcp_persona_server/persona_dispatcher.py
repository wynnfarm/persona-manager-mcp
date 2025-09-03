"""
Persona Dispatcher - Intelligent persona selection and management.

This module provides a high-level interface for automatically selecting
and managing personas based on task requirements. It acts as a smart
dispatcher that chooses the most appropriate persona for any given task.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from .persona_manager import PersonaManager
from .persona_generator import PersonaGenerator
from .utils import calculate_similarity_score, extract_keywords
from .types import TaskContext, TaskCategory, PersonaRecommendation
from .context_integration import ContextIntegration

logger = logging.getLogger(__name__)





class PersonaDispatcher:
    """
    Intelligent persona dispatcher that selects the most appropriate
    persona based on task analysis and context.
    """
    
    def __init__(self, persona_manager: PersonaManager):
        self.persona_manager = persona_manager
        self.persona_generator = PersonaGenerator()
        self.context_integration = ContextIntegration()
        self.task_history = []
        self.persona_usage_stats = {}
        self.auto_generation_enabled = True
        self.confidence_threshold = 0.3  # Threshold below which to generate new personas
        self.performance_metrics = {}  # Track persona performance
        self.feedback_history = []  # Track user feedback
        
        # Task category keywords for classification
        self.category_keywords = {
            TaskCategory.TECHNICAL: [
                "debug", "code", "programming", "software", "technical", "implementation",
                "algorithm", "system", "architecture", "development", "engineering",
                "python", "javascript", "api", "database", "server", "deployment"
            ],
            TaskCategory.CREATIVE: [
                "write", "story", "creative", "narrative", "content", "marketing",
                "copy", "brand", "imaginative", "artistic", "expressive", "engaging",
                "storytelling", "creative writing", "content creation"
            ],
            TaskCategory.BUSINESS: [
                "business", "analysis", "strategy", "market", "process", "optimization",
                "data analysis", "insights", "planning", "consulting", "management",
                "strategy", "business case", "roi", "efficiency"
            ],
            TaskCategory.EDUCATIONAL: [
                "teach", "explain", "educate", "learn", "training", "curriculum",
                "instructional", "pedagogy", "tutorial", "guide", "mentor",
                "educational", "learning", "teaching", "instruction", "how to",
                "step by step", "walkthrough", "demonstrate", "show", "instruct",
                "coach", "help", "assist", "support", "clarify", "break down",
                "simplify", "make easy", "understand", "comprehend", "grasp",
                "follow", "practice", "exercise", "workshop", "lesson", "course",
                "class", "workshop", "seminar", "presentation", "demo", "example"
            ],
            TaskCategory.DESIGN: [
                "design", "ui", "ux", "visual", "graphic", "aesthetic", "user experience",
                "interface", "branding", "layout", "prototype", "wireframe",
                "design system", "visual design"
            ],
            TaskCategory.SCIENTIFIC: [
                "research", "scientific", "methodology", "evidence", "analysis",
                "experiment", "hypothesis", "data", "statistics", "peer review",
                "scientific method", "empirical", "study"
            ],
            TaskCategory.CONSULTING: [
                "consult", "advise", "strategy", "problem solving", "organizational",
                "change management", "business consulting", "advisory", "solution",
                "recommendation", "best practices"
            ],
            TaskCategory.MENTORING: [
                "mentor", "coach", "guide", "support", "development", "career",
                "leadership", "personal development", "growth", "advice",
                "mentoring", "coaching", "guidance"
            ]
        }
    
    def analyze_task(self, task_description: str, context: str = "") -> TaskContext:
        """Analyze a task to determine its characteristics."""
        full_text = f"{task_description} {context}".lower()
        
        # Determine domain
        domain = self._identify_domain(full_text)
        
        # Determine complexity
        complexity = self._assess_complexity(full_text)
        
        # Determine urgency
        urgency = self._assess_urgency(full_text)
        
        # Determine audience
        audience = self._identify_audience(full_text)
        
        # Determine output format
        output_format = self._identify_output_format(full_text)
        
        return TaskContext(
            task_description=task_description,
            user_context=context,
            domain=domain,
            complexity=complexity,
            urgency=urgency,
            audience=audience,
            output_format=output_format
        )
    
    def _identify_domain(self, text: str) -> str:
        """Identify the primary domain of the task."""
        domain_keywords = {
            "technology": ["tech", "software", "programming", "code", "system"],
            "business": ["business", "market", "strategy", "process", "management"],
            "creative": ["creative", "art", "design", "content", "story"],
            "education": ["education", "teaching", "learning", "training", "how to", "tutorial", "guide", "instruct", "explain", "demonstrate"],
            "science": ["science", "research", "analysis", "data", "experiment"],
            "healthcare": ["health", "medical", "patient", "clinical", "diagnosis"],
            "finance": ["finance", "investment", "money", "budget", "financial"],
            "legal": ["legal", "law", "contract", "compliance", "regulation"]
        }
        
        scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[domain] = score
        
        if scores:
            return max(scores, key=scores.get)
        return "general"
    
    def _assess_complexity(self, text: str) -> str:
        """Assess the complexity level of the task."""
        complexity_indicators = {
            "high": ["complex", "advanced", "sophisticated", "intricate", "detailed", "comprehensive"],
            "low": ["simple", "basic", "easy", "straightforward", "quick", "simple"]
        }
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in text for indicator in indicators):
                return level
        
        return "medium"
    
    def _assess_urgency(self, text: str) -> str:
        """Assess the urgency level of the task."""
        urgency_indicators = {
            "high": ["urgent", "asap", "emergency", "critical", "immediate", "quickly"],
            "low": ["when convenient", "no rush", "take your time", "leisurely"]
        }
        
        for level, indicators in urgency_indicators.items():
            if any(indicator in text for indicator in indicators):
                return level
        
        return "normal"
    
    def _identify_audience(self, text: str) -> str:
        """Identify the target audience for the task."""
        audience_indicators = {
            "technical": ["developer", "engineer", "technical", "programmer", "architect"],
            "business": ["executive", "manager", "business", "stakeholder", "client"],
            "expert": ["expert", "specialist", "professional", "advanced"],
            "general": ["user", "customer", "general", "public", "beginner"]
        }
        
        for audience, indicators in audience_indicators.items():
            if any(indicator in text for indicator in indicators):
                return audience
        
        return "general"
    
    def _identify_output_format(self, text: str) -> str:
        """Identify the expected output format."""
        format_indicators = {
            "code": ["code", "script", "program", "function", "class", "implementation"],
            "analysis": ["analysis", "report", "insights", "findings", "evaluation"],
            "creative": ["story", "narrative", "creative", "artistic", "imaginative"],
            "documentation": ["documentation", "guide", "manual", "tutorial", "instructions"]
        }
        
        for format_type, indicators in format_indicators.items():
            if any(indicator in text for indicator in indicators):
                return format_type
        
        return "text"
    
    def classify_task(self, task_context: TaskContext) -> TaskCategory:
        """Classify the task into a category."""
        full_text = f"{task_context.task_description} {task_context.user_context}".lower()
        
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in full_text)
            category_scores[category] = score
        
        # Get the category with the highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category
        
        return TaskCategory.GENERAL
    
    def select_persona(self, task_description: str, context: str = "", project_name: str = None) -> PersonaRecommendation:
        """
        Select the most appropriate persona for a given task using real-time context-aware analysis.
        
        Returns a PersonaRecommendation with the selected persona,
        confidence score, reasoning, and alternatives.
        """
        # Use project-specific context if provided
        if project_name:
            original_project = self.context_integration.project_name
            self.context_integration.project_name = project_name
        
        # Analyze the task
        task_context = self.analyze_task(task_description, context)
        task_category = self.classify_task(task_context)
        
        # Get context-aware analysis with real-time project context
        context_analysis = self.context_integration.analyze_context_for_task(task_description)
        
        # Enhance context with project insights
        if context_analysis.get("context_insights"):
            enhanced_context = f"{context}\n\nProject Context: {'; '.join(context_analysis['context_insights'])}"
            task_context = self.analyze_task(task_description, enhanced_context)
        
        try:
            # Get all available personas
            all_personas = self.persona_manager.get_all_personas()
        except Exception as e:
            logger.error(f"Error getting personas: {e}")
            raise ValueError(f"Failed to retrieve personas: {e}")
        
        if not all_personas:
            raise ValueError("No personas available for selection")
        
        # Score each persona for this task
        persona_scores = []
        for persona_id, persona_data in all_personas.items():
            score, reasoning = self._calculate_persona_score(
                persona_data, task_context, task_category
            )
            
            # Boost score if persona is recommended by context
            if persona_id in context_analysis.get("recommended_personas", []):
                score *= 1.5  # 50% boost for context-recommended personas
                reasoning += f" (Context-boosted: {context_analysis.get('context_relevance', 0):.2f})"
                logger.info(f"Boosting {persona_id} score due to context recommendation")
            
            persona_scores.append({
                "persona_id": persona_id,
                "persona_data": persona_data,
                "score": score,
                "reasoning": reasoning
            })
        
        # Sort by score (highest first)
        persona_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Get the best persona
        best_persona = persona_scores[0]
        
        # Check if we should generate a new persona
        generated_persona = None
        if (self.auto_generation_enabled and 
            best_persona["score"] < self.confidence_threshold):
            
            # Generate a new persona
            generated_persona = self.persona_generator.generate_persona_for_task(
                task_context, task_category, best_persona["score"]
            )
            
            if generated_persona:
                # Save the generated persona
                persona_id = generated_persona["id"]
                success, _ = self.persona_manager.create_persona(generated_persona)
                
                if success:
                    # Score the new persona
                    score, reasoning = self._calculate_persona_score(
                        generated_persona, task_context, task_category
                    )
                    
                    # If the generated persona scores higher, use it
                    if score > best_persona["score"]:
                        best_persona = {
                            "persona_id": persona_id,
                            "persona_data": generated_persona,
                            "score": score,
                            "reasoning": reasoning
                        }
                        generated_persona = None  # Don't include in alternatives
                        logger.info(f"Generated and selected new persona '{generated_persona['name']}' "
                                  f"with confidence {score:.2f}")
                    else:
                        # Add to alternatives
                        alternatives = persona_scores[1:4]
                        alternatives.append({
                            "persona_id": persona_id,
                            "persona_data": generated_persona,
                            "score": score,
                            "reasoning": reasoning
                        })
                        # Re-sort alternatives
                        alternatives.sort(key=lambda x: x["score"], reverse=True)
                        alternatives = alternatives[:3]
        
        # Get alternatives (top 3 excluding the best)
        alternatives = persona_scores[1:4]
        
        # Create recommendation
        recommendation = PersonaRecommendation(
            persona_id=best_persona["persona_id"],
            persona_data=best_persona["persona_data"],
            confidence_score=best_persona["score"],
            reasoning=best_persona["reasoning"],
            alternative_personas=[p["persona_data"] for p in alternatives],
            task_category=task_category
        )
        
        # Add generation info if a new persona was created
        if generated_persona:
            recommendation.persona_data["auto_generated"] = True
            recommendation.persona_data["generation_reason"] = f"Low confidence ({best_persona['score']:.2f}) for task"
        
        # Add context insights to the recommendation
        if context_analysis.get("context_insights"):
            recommendation.persona_data["context_insights"] = context_analysis["context_insights"]
        
        # Log the selection
        self._log_persona_selection(task_context, recommendation)
        
        return recommendation
    
    def _calculate_persona_score(
        self, 
        persona_data: Dict[str, Any], 
        task_context: TaskContext,
        task_category: TaskCategory
    ) -> Tuple[float, List[str]]:
        """Calculate a score for how well a persona matches a task."""
        score = 0.0
        reasoning = []
        
        # Base expertise matching (35% weight)
        expertise_score = self._calculate_expertise_score(persona_data, task_context)
        score += expertise_score * 0.35
        if expertise_score > 0:
            reasoning.append(f"Expertise match: {expertise_score:.2f}")
        
        # Task category matching (25% weight) - Increased importance
        category_score = self._calculate_category_score(persona_data, task_category)
        score += category_score * 0.25
        if category_score > 0:
            reasoning.append(f"Category match: {category_score:.2f}")
        
        # Context alignment (20% weight)
        context_score = self._calculate_context_score(persona_data, task_context)
        score += context_score * 0.20
        if context_score > 0:
            reasoning.append(f"Context alignment: {context_score:.2f}")
        
        # Communication style matching (15% weight) - Reduced importance
        style_score = self._calculate_style_score(persona_data, task_context)
        score += style_score * 0.15
        if style_score > 0:
            reasoning.append(f"Style match: {style_score:.2f}")
        
        # Personality trait matching (5% weight)
        trait_score = self._calculate_trait_score(persona_data, task_context)
        score += trait_score * 0.05
        if trait_score > 0:
            reasoning.append(f"Trait match: {trait_score:.2f}")
        
        return min(score, 1.0), reasoning
    
    def record_feedback(self, task_description: str, selected_persona: str, feedback_score: int, feedback_comment: str = ""):
        """Record user feedback on persona selection performance."""
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_description": task_description,
            "selected_persona": selected_persona,
            "feedback_score": feedback_score,  # 1-5 scale
            "feedback_comment": feedback_comment,
            "task_category": self.classify_task(self.analyze_task(task_description)).value
        }
        
        self.feedback_history.append(feedback_entry)
        
        # Update performance metrics
        if selected_persona not in self.performance_metrics:
            self.performance_metrics[selected_persona] = {
                "total_selections": 0,
                "total_feedback": 0,
                "average_feedback": 0.0,
                "feedback_scores": [],
                "success_rate": 0.0
            }
        
        self.performance_metrics[selected_persona]["total_selections"] += 1
        self.performance_metrics[selected_persona]["total_feedback"] += 1
        self.performance_metrics[selected_persona]["feedback_scores"].append(feedback_score)
        
        # Calculate new average
        scores = self.performance_metrics[selected_persona]["feedback_scores"]
        self.performance_metrics[selected_persona]["average_feedback"] = sum(scores) / len(scores)
        
        # Calculate success rate (feedback >= 4 is considered successful)
        successful_feedback = sum(1 for score in scores if score >= 4)
        self.performance_metrics[selected_persona]["success_rate"] = successful_feedback / len(scores)
        
        logger.info(f"Recorded feedback for {selected_persona}: {feedback_score}/5")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for all personas."""
        return {
            "persona_performance": self.performance_metrics,
            "feedback_summary": {
                "total_feedback": len(self.feedback_history),
                "average_feedback": sum(f["feedback_score"] for f in self.feedback_history) / len(self.feedback_history) if self.feedback_history else 0,
                "feedback_distribution": self._get_feedback_distribution()
            },
            "top_performers": self._get_top_performers(),
            "improvement_suggestions": self._get_improvement_suggestions()
        }
    
    def _get_feedback_distribution(self) -> Dict[str, int]:
        """Get distribution of feedback scores."""
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for feedback in self.feedback_history:
            score = feedback["feedback_score"]
            distribution[score] = distribution.get(score, 0) + 1
        return distribution
    
    def _get_top_performers(self) -> List[Dict[str, Any]]:
        """Get top performing personas based on feedback."""
        performers = []
        for persona_id, metrics in self.performance_metrics.items():
            if metrics["total_feedback"] >= 2:  # Only include personas with at least 2 feedback entries
                performers.append({
                    "persona_id": persona_id,
                    "average_feedback": metrics["average_feedback"],
                    "success_rate": metrics["success_rate"],
                    "total_selections": metrics["total_selections"],
                    "total_feedback": metrics["total_feedback"]
                })
        
        # Sort by success rate, then by average feedback
        performers.sort(key=lambda x: (x["success_rate"], x["average_feedback"]), reverse=True)
        return performers[:5]  # Top 5 performers
    
    def _get_improvement_suggestions(self) -> List[str]:
        """Get suggestions for improving persona performance."""
        suggestions = []
        
        # Find personas with low performance
        low_performers = []
        for persona_id, metrics in self.performance_metrics.items():
            if metrics["total_feedback"] >= 3 and metrics["success_rate"] < 0.6:
                low_performers.append((persona_id, metrics))
        
        for persona_id, metrics in low_performers:
            suggestions.append(f"Consider improving {persona_id} (success rate: {metrics['success_rate']:.1%})")
        
        # Suggest based on feedback comments
        negative_feedback = [f for f in self.feedback_history if f["feedback_score"] <= 2]
        if negative_feedback:
            common_issues = self._analyze_feedback_patterns(negative_feedback)
            suggestions.extend(common_issues)
        
        return suggestions
    
    def _analyze_feedback_patterns(self, negative_feedback: List[Dict[str, Any]]) -> List[str]:
        """Analyze patterns in negative feedback to suggest improvements."""
        suggestions = []
        
        # Analyze by task category
        category_issues = {}
        for feedback in negative_feedback:
            category = feedback["task_category"]
            if category not in category_issues:
                category_issues[category] = []
            category_issues[category].append(feedback)
        
        for category, feedbacks in category_issues.items():
            if len(feedbacks) >= 2:
                suggestions.append(f"Improve persona selection for {category} tasks")
        
        return suggestions
    
    def _calculate_expertise_score(self, persona_data: Dict[str, Any], task_context: TaskContext) -> float:
        """Calculate expertise matching score."""
        expertise = persona_data.get("expertise", [])
        task_text = f"{task_context.task_description} {task_context.user_context}".lower()
        
        if not expertise:
            return 0.0
        
        matches = 0
        for exp in expertise:
            if exp.lower() in task_text:
                matches += 1
        
        return min(matches / len(expertise), 1.0)
    
    def _calculate_style_score(self, persona_data: Dict[str, Any], task_context: TaskContext) -> float:
        """Calculate communication style matching score."""
        style = persona_data.get("communication_style", "").lower()
        if not style:
            return 0.0
        
        # Map audience to preferred styles
        audience_style_preferences = {
            "technical": ["professional", "technical", "analytical"],
            "business": ["strategic", "analytical", "professional"],
            "general": ["patient", "explanatory", "engaging"],
            "expert": ["technical", "analytical", "professional"]
        }
        
        preferred_styles = audience_style_preferences.get(task_context.audience, [])
        
        for preferred in preferred_styles:
            if preferred in style:
                return 1.0
        
        return 0.0
    
    def _calculate_context_score(self, persona_data: Dict[str, Any], task_context: TaskContext) -> float:
        """Calculate context alignment score."""
        context = persona_data.get("context", "").lower()
        if not context:
            return 0.0
        
        task_text = f"{task_context.task_description} {task_context.user_context}".lower()
        
        # Use similarity scoring
        return calculate_similarity_score(context, task_text)
    
    def _calculate_category_score(self, persona_data: Dict[str, Any], task_category: TaskCategory) -> float:
        """Calculate task category matching score."""
        # Map personas to their primary categories
        persona_categories = {
            "tech_expert": TaskCategory.TECHNICAL,
            "creative_writer": TaskCategory.CREATIVE,
            "business_analyst": TaskCategory.BUSINESS,
            "educator": TaskCategory.EDUCATIONAL,
            "designer": TaskCategory.DESIGN,
            "scientist": TaskCategory.SCIENTIFIC,
            "consultant": TaskCategory.CONSULTING,
            "mentor": TaskCategory.MENTORING
        }
        
        persona_name = persona_data.get("name", "").lower()
        for key, category in persona_categories.items():
            if key.replace("_", " ") in persona_name or key in persona_name:
                return 1.0 if category == task_category else 0.0
        
        return 0.5  # Default score for uncategorized personas
    
    def _calculate_trait_score(self, persona_data: Dict[str, Any], task_context: TaskContext) -> float:
        """Calculate personality trait matching score."""
        traits = persona_data.get("personality_traits", [])
        if not traits:
            return 0.0
        
        task_text = f"{task_context.task_description} {task_context.user_context}".lower()
        
        matches = 0
        for trait in traits:
            if trait.lower() in task_text:
                matches += 1
        
        return min(matches / len(traits), 1.0) if traits else 0.0
    
    def _log_persona_selection(self, task_context: TaskContext, recommendation: PersonaRecommendation):
        """Log persona selection for analytics."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_description": task_context.task_description,
            "task_category": recommendation.task_category.value,
            "selected_persona": recommendation.persona_id,
            "confidence_score": recommendation.confidence_score,
            "domain": task_context.domain,
            "complexity": task_context.complexity,
            "audience": task_context.audience
        }
        
        self.task_history.append(log_entry)
        
        # Update usage statistics
        if recommendation.persona_id not in self.persona_usage_stats:
            self.persona_usage_stats[recommendation.persona_id] = {
                "usage_count": 0,
                "avg_confidence": 0.0,
                "task_categories": {}
            }
        
        stats = self.persona_usage_stats[recommendation.persona_id]
        stats["usage_count"] += 1
        stats["avg_confidence"] = (
            (stats["avg_confidence"] * (stats["usage_count"] - 1) + recommendation.confidence_score) 
            / stats["usage_count"]
        )
        
        category = recommendation.task_category.value
        if category not in stats["task_categories"]:
            stats["task_categories"][category] = 0
        stats["task_categories"][category] += 1
        
        logger.info(f"Selected persona '{recommendation.persona_id}' "
                   f"(confidence: {recommendation.confidence_score:.2f}) "
                   f"for task: {task_context.task_description[:50]}...")
    
    def get_selection_analytics(self) -> Dict[str, Any]:
        """Get analytics about persona selection patterns."""
        total_selections = len(self.task_history)
        
        if total_selections == 0:
            return {
                "total_selections": 0,
                "average_confidence": 0.0,
                "persona_usage": {},
                "auto_generated_used": 0,
                "task_categories": {},
                "domains": {}
            }
        
        # Calculate average confidence
        total_confidence = sum(entry.get("confidence_score", 0.0) for entry in self.task_history)
        average_confidence = total_confidence / total_selections if total_selections > 0 else 0.0
        
        # Count persona usage
        persona_usage = {}
        auto_generated_used = 0
        task_categories = {}
        domains = {}
        
        for entry in self.task_history:
            persona_id = entry.get("selected_persona", "unknown")
            persona_usage[persona_id] = persona_usage.get(persona_id, 0) + 1
            
            # Check if auto-generated persona was used
            if entry.get("auto_generated", False):
                auto_generated_used += 1
            
            # Count task categories
            category = entry.get("task_category", "unknown")
            task_categories[category] = task_categories.get(category, 0) + 1
            
            # Count domains
            domain = entry.get("domain", "unknown")
            domains[domain] = domains.get(domain, 0) + 1
        
        return {
            "total_selections": total_selections,
            "average_confidence": average_confidence,
            "persona_usage": persona_usage,
            "auto_generated_used": auto_generated_used,
            "task_categories": task_categories,
            "domains": domains,
            "recent_selections": self.task_history[-10:] if self.task_history else [],
            "performance_metrics": self.get_performance_metrics()
        }
    
    def _get_category_distribution(self) -> Dict[str, int]:
        """Get distribution of task categories."""
        distribution = {}
        for entry in self.task_history:
            category = entry["task_category"]
            distribution[category] = distribution.get(category, 0) + 1
        return distribution
    
    def suggest_persona_improvements(self, task_description: str) -> List[str]:
        """Suggest improvements to personas based on task requirements."""
        suggestions = []
        task_context = self.analyze_task(task_description)
        
        # Check if we have personas for the identified domain
        domain = task_context.domain
        all_personas = self.persona_manager.get_all_personas()
        
        domain_coverage = {
            "technology": ["tech_expert"],
            "business": ["business_analyst", "consultant"],
            "creative": ["creative_writer", "designer"],
            "education": ["educator", "mentor"],
            "science": ["scientist"],
            "general": []
        }
        
        if domain in domain_coverage:
            existing_personas = domain_coverage[domain]
            missing_personas = [p for p in existing_personas if p not in all_personas]
            
            if missing_personas:
                suggestions.append(f"Consider adding personas for {domain} domain: {', '.join(missing_personas)}")
        
        # Check for expertise gaps
        keywords = extract_keywords(task_description)
        covered_keywords = set()
        
        for persona_data in all_personas.values():
            expertise = persona_data.get("expertise", [])
            for exp in expertise:
                covered_keywords.add(exp.lower())
        
        missing_keywords = [kw for kw in keywords if kw not in covered_keywords]
        if missing_keywords:
            suggestions.append(f"Consider adding expertise areas: {', '.join(missing_keywords[:5])}")
        
        return suggestions
    
    def enable_auto_generation(self, enabled: bool = True):
        """Enable or disable automatic persona generation."""
        self.auto_generation_enabled = enabled
        logger.info(f"Auto-generation {'enabled' if enabled else 'disabled'}")
    
    def set_confidence_threshold(self, threshold: float):
        """Set the confidence threshold for auto-generation."""
        if 0.0 <= threshold <= 1.0:
            self.confidence_threshold = threshold
            logger.info(f"Confidence threshold set to {threshold}")
        else:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")
    
    def get_auto_generation_status(self) -> Dict[str, Any]:
        """Get the current auto-generation configuration."""
        return {
            "enabled": self.auto_generation_enabled,
            "confidence_threshold": self.confidence_threshold,
            "total_generated": self._count_generated_personas()
        }
    
    def _count_generated_personas(self) -> int:
        """Count the number of auto-generated personas."""
        all_personas = self.persona_manager.get_all_personas()
        return sum(1 for p in all_personas.values() if p.get("auto_generated", False))
    
    def list_generated_personas(self) -> List[Dict[str, Any]]:
        """List all auto-generated personas."""
        all_personas = self.persona_manager.get_all_personas()
        generated = []
        
        for persona_id, persona_data in all_personas.items():
            if persona_data.get("auto_generated", False):
                generated.append({
                    "id": persona_id,
                    "name": persona_data.get("name", ""),
                    "created_at": persona_data.get("created_at", ""),
                    "generation_reason": persona_data.get("generation_reason", ""),
                    "original_task": persona_data.get("original_task", ""),
                    "task_category": persona_data.get("task_category", "")
                })
        
        return generated
    
    def complete_task_with_context_update(self, task_description: str, result: str, persona_id: str):
        """
        Complete a task and update context based on the result.
        This method should be called after a task is completed to keep context up to date.
        """
        try:
            # Update context based on task completion
            success = self.context_integration.update_context_from_task(
                task_description, result, persona_id
            )
            
            if success:
                logger.info(f"Updated context from task completion: {task_description[:50]}...")
            else:
                logger.warning(f"Failed to update context from task: {task_description[:50]}...")
            
            # Log task completion
            self.task_history.append({
                "task": task_description,
                "result": result,
                "persona_id": persona_id,
                "timestamp": datetime.now().isoformat(),
                "context_updated": success
            })
            
            return success
            
        except Exception as e:
            logger.error(f"Error completing task with context update: {e}")
            return False
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of current project context."""
        return self.context_integration.get_context_summary()
    
    def suggest_task_priorities(self) -> List[str]:
        """Suggest task priorities based on context."""
        return self.context_integration.suggest_task_priorities()
    
    def get_context_summary_for_project(self, project_name: str) -> Optional[Dict[str, Any]]:
        """Get context summary for a specific project."""
        try:
            # Temporarily set the project name for context integration
            original_project = self.context_integration.project_name
            self.context_integration.project_name = project_name
            
            # Get context summary
            summary = self.context_integration.get_context_summary()
            
            # Restore original project name
            self.context_integration.project_name = original_project
            
            return summary
        except Exception as e:
            logger.error(f"Error getting context summary for project {project_name}: {e}")
            return None
    
    def get_task_suggestions_for_project(self, project_name: str) -> List[str]:
        """Get task suggestions for a specific project."""
        try:
            # Temporarily set the project name for context integration
            original_project = self.context_integration.project_name
            self.context_integration.project_name = project_name
            
            # Get task suggestions
            suggestions = self.context_integration.suggest_task_priorities()
            
            # Restore original project name
            self.context_integration.project_name = original_project
            
            return suggestions
        except Exception as e:
            logger.error(f"Error getting task suggestions for project {project_name}: {e}")
            return []

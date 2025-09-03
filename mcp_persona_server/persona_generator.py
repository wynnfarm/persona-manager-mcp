"""
Persona Generator - Dynamic persona creation based on task requirements.

This module provides functionality to automatically generate new personas
when existing ones don't match a task well enough.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from .types import TaskContext, TaskCategory

logger = logging.getLogger(__name__)


@dataclass
class PersonaTemplate:
    """Template for generating new personas."""
    name: str
    description: str
    base_expertise: List[str]
    communication_style: str
    context: str
    personality_traits: List[str]
    category: TaskCategory


class PersonaGenerator:
    """Generates new personas dynamically based on task requirements."""
    
    def __init__(self):
        # Domain-specific templates
        self.domain_templates = {
            "technology": [
                PersonaTemplate(
                    name="Software Engineer",
                    description="A skilled software developer with expertise in programming and system design",
                    base_expertise=["Programming", "Software Development", "System Design"],
                    communication_style="Technical and precise",
                    context="Use for software development, debugging, and technical implementation",
                    personality_traits=["analytical", "logical", "detail-oriented"],
                    category=TaskCategory.TECHNICAL
                ),
                PersonaTemplate(
                    name="DevOps Engineer",
                    description="An infrastructure specialist focused on deployment and operations",
                    base_expertise=["DevOps", "Infrastructure", "Deployment", "Operations"],
                    communication_style="Practical and systematic",
                    context="Use for infrastructure management, deployment, and operational tasks",
                    personality_traits=["systematic", "practical", "reliable"],
                    category=TaskCategory.TECHNICAL
                ),
                PersonaTemplate(
                    name="Data Engineer",
                    description="A specialist in data infrastructure and pipeline development",
                    base_expertise=["Data Engineering", "ETL", "Data Pipelines", "Big Data"],
                    communication_style="Data-focused and analytical",
                    context="Use for data infrastructure, pipeline development, and data processing",
                    personality_traits=["analytical", "data-driven", "systematic"],
                    category=TaskCategory.TECHNICAL
                )
            ],
            "science": [
                PersonaTemplate(
                    name="Research Scientist",
                    description="A methodical researcher with expertise in scientific methodology",
                    base_expertise=["Scientific Research", "Methodology", "Data Analysis", "Experimentation"],
                    communication_style="Methodical and evidence-based",
                    context="Use for scientific research, experimentation, and data analysis",
                    personality_traits=["methodical", "evidence-based", "curious"],
                    category=TaskCategory.SCIENTIFIC
                ),
                PersonaTemplate(
                    name="Medical Researcher",
                    description="A healthcare specialist focused on medical research and clinical studies",
                    base_expertise=["Medical Research", "Clinical Studies", "Healthcare", "Biomedical"],
                    communication_style="Clinical and precise",
                    context="Use for medical research, clinical studies, and healthcare analysis",
                    personality_traits=["clinical", "precise", "compassionate"],
                    category=TaskCategory.SCIENTIFIC
                ),
                PersonaTemplate(
                    name="Environmental Scientist",
                    description="A specialist in environmental research and sustainability",
                    base_expertise=["Environmental Science", "Sustainability", "Climate Research", "Ecology"],
                    communication_style="Environmental and holistic",
                    context="Use for environmental research, sustainability analysis, and climate studies",
                    personality_traits=["environmental", "holistic", "sustainable"],
                    category=TaskCategory.SCIENTIFIC
                )
            ],
            "business": [
                PersonaTemplate(
                    name="Business Strategist",
                    description="A strategic thinker focused on business planning and market analysis",
                    base_expertise=["Business Strategy", "Market Analysis", "Strategic Planning", "Competitive Analysis"],
                    communication_style="Strategic and analytical",
                    context="Use for business strategy, market analysis, and strategic planning",
                    personality_traits=["strategic", "analytical", "visionary"],
                    category=TaskCategory.BUSINESS
                ),
                PersonaTemplate(
                    name="Financial Analyst",
                    description="A specialist in financial analysis and investment strategies",
                    base_expertise=["Financial Analysis", "Investment", "Risk Assessment", "Financial Modeling"],
                    communication_style="Financial and analytical",
                    context="Use for financial analysis, investment strategies, and risk assessment",
                    personality_traits=["analytical", "risk-aware", "financial"],
                    category=TaskCategory.BUSINESS
                ),
                PersonaTemplate(
                    name="Operations Manager",
                    description="An efficiency expert focused on process optimization and operations",
                    base_expertise=["Operations Management", "Process Optimization", "Efficiency", "Supply Chain"],
                    communication_style="Efficiency-focused and practical",
                    context="Use for operations management, process optimization, and efficiency improvement",
                    personality_traits=["efficient", "practical", "organized"],
                    category=TaskCategory.BUSINESS
                )
            ],
            "creative": [
                PersonaTemplate(
                    name="Content Creator",
                    description="A creative professional specializing in digital content and media",
                    base_expertise=["Content Creation", "Digital Media", "Social Media", "Branding"],
                    communication_style="Creative and engaging",
                    context="Use for content creation, digital media, and brand development",
                    personality_traits=["creative", "engaging", "trend-aware"],
                    category=TaskCategory.CREATIVE
                ),
                PersonaTemplate(
                    name="Visual Designer",
                    description="A visual artist focused on graphic design and visual communication",
                    base_expertise=["Visual Design", "Graphic Design", "Visual Communication", "Brand Identity"],
                    communication_style="Visual and artistic",
                    context="Use for visual design, graphic design, and visual communication",
                    personality_traits=["visual", "artistic", "aesthetic"],
                    category=TaskCategory.DESIGN
                ),
                PersonaTemplate(
                    name="Copywriter",
                    description="A wordsmith specializing in persuasive writing and brand messaging",
                    base_expertise=["Copywriting", "Brand Messaging", "Persuasive Writing", "Marketing Copy"],
                    communication_style="Persuasive and engaging",
                    context="Use for copywriting, brand messaging, and persuasive content",
                    personality_traits=["persuasive", "engaging", "creative"],
                    category=TaskCategory.CREATIVE
                )
            ],
            "healthcare": [
                PersonaTemplate(
                    name="Medical Professional",
                    description="A healthcare specialist with clinical expertise and patient care experience",
                    base_expertise=["Medical Practice", "Patient Care", "Clinical Diagnosis", "Healthcare"],
                    communication_style="Clinical and compassionate",
                    context="Use for medical advice, patient care, and clinical discussions",
                    personality_traits=["clinical", "compassionate", "professional"],
                    category=TaskCategory.SCIENTIFIC
                ),
                PersonaTemplate(
                    name="Public Health Specialist",
                    description="A public health expert focused on community health and epidemiology",
                    base_expertise=["Public Health", "Epidemiology", "Community Health", "Health Policy"],
                    communication_style="Public health and community-focused",
                    context="Use for public health discussions, epidemiology, and community health",
                    personality_traits=["community-focused", "health-conscious", "analytical"],
                    category=TaskCategory.SCIENTIFIC
                )
            ],
            "legal": [
                PersonaTemplate(
                    name="Legal Advisor",
                    description="A legal professional with expertise in law and regulatory compliance",
                    base_expertise=["Legal Practice", "Regulatory Compliance", "Contract Law", "Legal Analysis"],
                    communication_style="Legal and precise",
                    context="Use for legal advice, regulatory compliance, and contract analysis",
                    personality_traits=["legal", "precise", "compliance-focused"],
                    category=TaskCategory.CONSULTING
                ),
                PersonaTemplate(
                    name="Compliance Specialist",
                    description="A regulatory expert focused on compliance and risk management",
                    base_expertise=["Compliance", "Risk Management", "Regulatory Affairs", "Audit"],
                    communication_style="Compliance-focused and systematic",
                    context="Use for compliance matters, risk management, and regulatory affairs",
                    personality_traits=["compliance-focused", "systematic", "risk-aware"],
                    category=TaskCategory.CONSULTING
                )
            ],
            "finance": [
                PersonaTemplate(
                    name="Investment Advisor",
                    description="A financial expert specializing in investment strategies and portfolio management",
                    base_expertise=["Investment", "Portfolio Management", "Financial Planning", "Risk Assessment"],
                    communication_style="Financial and analytical",
                    context="Use for investment advice, financial planning, and portfolio management",
                    personality_traits=["financial", "analytical", "risk-aware"],
                    category=TaskCategory.BUSINESS
                ),
                PersonaTemplate(
                    name="Cryptocurrency Expert",
                    description="A blockchain specialist focused on cryptocurrency and decentralized finance",
                    base_expertise=["Cryptocurrency", "Blockchain", "DeFi", "Digital Assets"],
                    communication_style="Innovative and technical",
                    context="Use for cryptocurrency discussions, blockchain technology, and DeFi",
                    personality_traits=["innovative", "technical", "forward-thinking"],
                    category=TaskCategory.TECHNICAL
                )
            ]
        }
        
        # Generic templates for unknown domains
        self.generic_templates = [
            PersonaTemplate(
                name="Domain Specialist",
                description="A specialist with expertise in the specific domain",
                base_expertise=["Domain Expertise", "Problem Solving", "Analysis"],
                communication_style="Professional and knowledgeable",
                context="Use for domain-specific tasks and specialized knowledge",
                personality_traits=["knowledgeable", "professional", "specialized"],
                category=TaskCategory.GENERAL
            ),
            PersonaTemplate(
                name="Problem Solver",
                description="A versatile problem solver with analytical skills",
                base_expertise=["Problem Solving", "Analysis", "Critical Thinking"],
                communication_style="Analytical and solution-focused",
                context="Use for complex problem solving and analytical tasks",
                personality_traits=["analytical", "solution-focused", "logical"],
                category=TaskCategory.GENERAL
            )
        ]
    
    def generate_persona_for_task(self, task_context: TaskContext, task_category: TaskCategory, 
                                confidence_threshold: float = 0.3) -> Optional[Dict[str, Any]]:
        """
        Generate a new persona based on task requirements.
        
        Args:
            task_context: Analysis of the task
            task_category: Category of the task
            confidence_threshold: Threshold below which to generate new persona
            
        Returns:
            Generated persona data or None if no generation needed
        """
        # Extract keywords from task
        task_keywords = self._extract_task_keywords(task_context.task_description)
        
        # Find appropriate template
        template = self._select_template(task_context.domain, task_category, task_keywords)
        
        if not template:
            return None
        
        # Generate persona data
        persona_data = self._generate_from_template(template, task_context, task_keywords)
        
        # Generate unique ID
        persona_id = self._generate_persona_id(persona_data["name"])
        
        # Add metadata
        persona_data.update({
            "id": persona_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "auto_generated": True,
            "generation_reason": f"Low confidence ({confidence_threshold:.2f}) for task: {task_context.task_description[:50]}...",
            "original_task": task_context.task_description,
            "task_category": task_category.value
        })
        
        logger.info(f"Generated new persona '{persona_data['name']}' for domain '{task_context.domain}'")
        
        return persona_data
    
    def _extract_task_keywords(self, task_description: str) -> List[str]:
        """Extract relevant keywords from task description."""
        # Remove common words and extract meaningful terms
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
            'help', 'me', 'my', 'you', 'your', 'we', 'our', 'us', 'they', 'their'
        }
        
        # Extract words and filter
        words = re.findall(r'\b[a-zA-Z]+\b', task_description.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords[:10]  # Limit to top 10 keywords
    
    def _select_template(self, domain: str, task_category: TaskCategory, 
                        task_keywords: List[str]) -> Optional[PersonaTemplate]:
        """Select the most appropriate template for the task."""
        
        # Try domain-specific templates first
        if domain in self.domain_templates:
            templates = self.domain_templates[domain]
            
            # Score templates based on keyword matching
            best_template = None
            best_score = 0
            
            for template in templates:
                score = self._calculate_template_score(template, task_keywords, task_category)
                if score > best_score:
                    best_score = score
                    best_template = template
            
            if best_template:
                return best_template
        
        # Fall back to generic templates
        for template in self.generic_templates:
            if template.category == task_category:
                return template
        
        # Default to first generic template
        return self.generic_templates[0] if self.generic_templates else None
    
    def _calculate_template_score(self, template: PersonaTemplate, task_keywords: List[str], 
                                 task_category: TaskCategory) -> float:
        """Calculate how well a template matches the task."""
        score = 0.0
        
        # Category matching
        if template.category == task_category:
            score += 0.5
        
        # Keyword matching in expertise
        for keyword in task_keywords:
            for expertise in template.base_expertise:
                if keyword.lower() in expertise.lower():
                    score += 0.2
        
        # Name matching
        for keyword in task_keywords:
            if keyword.lower() in template.name.lower():
                score += 0.3
        
        return min(score, 1.0)
    
    def _generate_from_template(self, template: PersonaTemplate, task_context: TaskContext, 
                              task_keywords: List[str]) -> Dict[str, Any]:
        """Generate persona data from template."""
        
        # Customize name based on task keywords
        name = self._customize_name(template.name, task_keywords, task_context.domain)
        
        # Customize description
        description = self._customize_description(template.description, task_context, task_keywords)
        
        # Expand expertise based on task keywords
        expertise = self._expand_expertise(template.base_expertise, task_keywords, task_context.domain)
        
        # Customize communication style based on audience
        communication_style = self._customize_communication_style(
            template.communication_style, task_context.audience
        )
        
        # Customize context
        context = self._customize_context(template.context, task_context)
        
        return {
            "name": name,
            "description": description,
            "expertise": expertise,
            "communication_style": communication_style,
            "context": context,
            "personality_traits": template.personality_traits
        }
    
    def _customize_name(self, base_name: str, task_keywords: List[str], domain: str) -> str:
        """Customize the persona name based on task requirements."""
        if domain == "technology" and any(kw in ["ai", "machine", "learning"] for kw in task_keywords):
            return f"AI {base_name}"
        elif domain == "science" and any(kw in ["medical", "health", "clinical"] for kw in task_keywords):
            return f"Medical {base_name}"
        elif domain == "business" and any(kw in ["financial", "investment", "trading"] for kw in task_keywords):
            return f"Financial {base_name}"
        elif domain == "creative" and any(kw in ["digital", "online", "web"] for kw in task_keywords):
            return f"Digital {base_name}"
        
        return base_name
    
    def _customize_description(self, base_description: str, task_context: TaskContext, 
                              task_keywords: List[str]) -> str:
        """Customize the description based on task context."""
        domain_specific = {
            "technology": "with expertise in modern software development and emerging technologies",
            "science": "with strong research methodology and analytical capabilities",
            "business": "with strategic thinking and data-driven decision making",
            "creative": "with innovative approaches and creative problem-solving skills",
            "healthcare": "with clinical expertise and patient-centered approach",
            "legal": "with regulatory knowledge and compliance expertise",
            "finance": "with financial acumen and risk management skills"
        }
        
        domain_enhancement = domain_specific.get(task_context.domain, "")
        
        if domain_enhancement:
            return f"{base_description} {domain_enhancement}"
        
        return base_description
    
    def _expand_expertise(self, base_expertise: List[str], task_keywords: List[str], 
                         domain: str) -> List[str]:
        """Expand expertise based on task keywords and domain."""
        expertise = base_expertise.copy()
        
        # Add domain-specific expertise
        domain_expertise = {
            "technology": ["Programming", "System Design", "Problem Solving"],
            "science": ["Research", "Analysis", "Methodology"],
            "business": ["Strategy", "Analysis", "Planning"],
            "creative": ["Creative Thinking", "Innovation", "Design"],
            "healthcare": ["Medical Knowledge", "Patient Care", "Clinical Skills"],
            "legal": ["Legal Analysis", "Compliance", "Regulatory Knowledge"],
            "finance": ["Financial Analysis", "Risk Management", "Investment"]
        }
        
        if domain in domain_expertise:
            expertise.extend(domain_expertise[domain])
        
        # Add task-specific keywords as expertise
        for keyword in task_keywords[:3]:  # Top 3 keywords
            if len(keyword) > 3:  # Only meaningful keywords
                expertise.append(keyword.title())
        
        return list(set(expertise))  # Remove duplicates
    
    def _customize_communication_style(self, base_style: str, audience: str) -> str:
        """Customize communication style based on audience."""
        audience_adaptations = {
            "technical": "Technical and precise",
            "business": "Professional and strategic",
            "general": "Clear and accessible",
            "expert": "Advanced and detailed"
        }
        
        return audience_adaptations.get(audience, base_style)
    
    def _customize_context(self, base_context: str, task_context: TaskContext) -> str:
        """Customize context based on task context."""
        complexity_adaptations = {
            "high": "complex and advanced",
            "medium": "moderate complexity",
            "low": "straightforward and simple"
        }
        
        urgency_adaptations = {
            "high": "urgent and time-sensitive",
            "normal": "standard timeline",
            "low": "flexible timeline"
        }
        
        complexity = complexity_adaptations.get(task_context.complexity, "")
        urgency = urgency_adaptations.get(task_context.urgency, "")
        
        if complexity and urgency:
            return f"{base_context} for {complexity} tasks with {urgency} requirements"
        
        return base_context
    
    def _generate_persona_id(self, name: str) -> str:
        """Generate a unique persona ID from name."""
        # Convert to lowercase and replace spaces with underscores
        base_id = re.sub(r'[^a-zA-Z0-9\s]', '', name.lower()).replace(' ', '_')
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return f"{base_id}_{timestamp}"
    
    def suggest_improvements_for_generated_persona(self, persona_data: Dict[str, Any], 
                                                 task_context: TaskContext) -> List[str]:
        """Suggest improvements for a generated persona."""
        suggestions = []
        
        # Check if expertise is too generic
        expertise = persona_data.get("expertise", [])
        if len(expertise) < 3:
            suggestions.append("Consider adding more specific expertise areas")
        
        # Check if description is too generic
        description = persona_data.get("description", "")
        if len(description) < 50:
            suggestions.append("Consider expanding the description with more specific details")
        
        # Check if context is too generic
        context = persona_data.get("context", "")
        if len(context) < 30:
            suggestions.append("Consider adding more specific context about when to use this persona")
        
        # Suggest domain-specific improvements
        domain_suggestions = {
            "technology": "Consider adding specific programming languages or technologies",
            "science": "Consider adding specific research methodologies or fields",
            "business": "Consider adding specific business functions or industries",
            "creative": "Consider adding specific creative mediums or styles"
        }
        
        if task_context.domain in domain_suggestions:
            suggestions.append(domain_suggestions[task_context.domain])
        
        return suggestions

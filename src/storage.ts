import { promises as fs } from 'fs';
import { join } from 'path';
import { z } from 'zod';

// Enhanced persona schema with detailed instructions and behavior patterns
export const PersonaSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  description: z.string().min(1),
  expertise: z.array(z.string()).min(1),
  communication_style: z.string().min(1),
  context: z.string().optional(),
  personality_traits: z.array(z.string()).optional(),
  created_at: z.string().optional(),
  updated_at: z.string().optional(),
  
  // NEW: Enhanced fields for better task performance
  detailed_instructions: z.string().optional().describe("Detailed instructions on how this persona should behave and approach tasks"),
  behavior_patterns: z.array(z.string()).optional().describe("Specific behavior patterns and approaches this persona should follow"),
  conversation_starters: z.array(z.string()).optional().describe("Example conversation starters this persona might use"),
  response_templates: z.array(z.string()).optional().describe("Template responses for common scenarios"),
  decision_frameworks: z.array(z.string()).optional().describe("Decision-making frameworks this persona should use"),
  task_templates: z.record(z.string(), z.object({
    description: z.string(),
    steps: z.array(z.string()),
    best_practices: z.array(z.string()),
    common_pitfalls: z.array(z.string()),
    success_metrics: z.array(z.string()),
  })).optional().describe("Pre-defined task templates for common scenarios"),
  expertise_details: z.record(z.string(), z.object({
    proficiency_level: z.enum(["beginner", "intermediate", "advanced", "expert"]),
    sub_skills: z.array(z.string()),
    tools: z.array(z.string()),
    methodologies: z.array(z.string()),
  })).optional().describe("Detailed breakdown of expertise areas"),
  communication_guidelines: z.object({
    tone: z.string(),
    approach: z.string(),
    formality_level: z.enum(["casual", "professional", "formal", "technical"]),
    preferred_examples: z.boolean(),
    explanation_style: z.enum(["detailed", "concise", "step-by-step", "conceptual"]),
    response_length: z.enum(["brief", "moderate", "comprehensive"]),
  }).optional().describe("Detailed communication preferences"),
  role_specific_instructions: z.string().optional().describe("Role-specific instructions for this persona's domain"),
});

export type Persona = z.infer<typeof PersonaSchema>;

// Add task recommendation interfaces
export interface TaskRecommendationRequest {
  task_description: string;
  task_type?: string;
  complexity_level?: 'simple' | 'moderate' | 'complex' | 'expert';
  domain?: string;
}

export interface TaskRecommendation {
  persona_id: string;
  persona_name: string;
  confidence_score: number;
  matching_expertise: string[];
  reasoning: string;
}

export interface TaskRecommendationResult {
  recommendations: TaskRecommendation[];
  analysis: string;
  confidence_score: number;
  reasoning: string;
}

// Storage configuration
const PERSONAS_DIR = join(process.cwd(), 'personas');
const PERSONAS_FILE = join(PERSONAS_DIR, 'personas.json');
const DEFAULT_PERSONAS_FILE = join(PERSONAS_DIR, 'default_personas.json');
const ENHANCED_DEFAULT_PERSONAS_FILE = join(PERSONAS_DIR, 'enhanced_default_personas.json');

export class PersonaStorage {
  private personas: Map<string, Persona> = new Map();

  constructor() {}

  // Initialize storage and load existing personas
  async initialize(): Promise<void> {
    try {
      // Ensure personas directory exists
      await fs.mkdir(PERSONAS_DIR, { recursive: true });
      
      // Load personas from file
      await this.loadPersonas();
      
      console.error(`📁 Persona storage initialized. Loaded ${this.personas.size} personas.`);
    } catch (error) {
      console.error('❌ Error initializing persona storage:', error);
      // Load default personas as fallback
      await this.loadDefaultPersonas();
    }
  }

  // Load personas from the main personas file
  private async loadPersonas(): Promise<void> {
    try {
      const data = await fs.readFile(PERSONAS_FILE, 'utf-8');
      const parsed = JSON.parse(data);
      
      if (parsed.personas && typeof parsed.personas === 'object') {
        this.personas.clear();
        for (const [id, personaData] of Object.entries(parsed.personas)) {
          try {
            const persona = PersonaSchema.parse({ id, ...personaData as any });
            this.personas.set(id, persona);
          } catch (error) {
            console.error(`⚠️ Skipping invalid persona ${id}:`, error);
          }
        }
      }
    } catch (error) {
      if ((error as any).code === 'ENOENT') {
        // File doesn't exist, load defaults
        await this.loadDefaultPersonas();
      } else {
        throw error;
      }
    }
  }

  // Load default personas as fallback
  private async loadDefaultPersonas(): Promise<void> {
    try {
      // Try enhanced personas first
      const enhancedData = await fs.readFile(ENHANCED_DEFAULT_PERSONAS_FILE, 'utf-8');
      const enhancedParsed = JSON.parse(enhancedData);
      
      if (enhancedParsed.personas && typeof enhancedParsed.personas === 'object') {
        this.personas.clear();
        for (const [id, personaData] of Object.entries(enhancedParsed.personas)) {
          try {
            const persona = PersonaSchema.parse({ id, ...personaData as any });
            this.personas.set(id, persona);
          } catch (error) {
            console.error(`⚠️ Skipping invalid enhanced persona ${id}:`, error);
          }
        }
        console.error(`📁 Loaded ${this.personas.size} enhanced personas`);
        return;
      }
    } catch (error) {
      console.error('⚠️ Enhanced personas not found, trying regular defaults:', error);
    }

    try {
      const data = await fs.readFile(DEFAULT_PERSONAS_FILE, 'utf-8');
      const parsed = JSON.parse(data);
      
      if (parsed.personas && typeof parsed.personas === 'object') {
        this.personas.clear();
        for (const [id, personaData] of Object.entries(parsed.personas)) {
          try {
            const persona = PersonaSchema.parse({ id, ...personaData as any });
            this.personas.set(id, persona);
          } catch (error) {
            console.error(`⚠️ Skipping invalid default persona ${id}:`, error);
          }
        }
      }
    } catch (error) {
      console.error('❌ Error loading default personas:', error);
      // Set minimal fallback personas
      this.setFallbackPersonas();
    }
  }

  // Set minimal fallback personas if all else fails
  private setFallbackPersonas(): void {
    this.personas.clear();
    const fallbackPersonas: Persona[] = [
      {
        id: "tech-expert",
        name: "Tech Expert",
        description: "Technical expert with deep knowledge of software development",
        expertise: ["Python", "JavaScript", "System Architecture"],
        communication_style: "Technical and precise",
        created_at: new Date().toISOString(),
      },
      {
        id: "creative-writer",
        name: "Creative Writer",
        description: "Creative writer with expertise in storytelling and content creation",
        expertise: ["Creative Writing", "Content Strategy", "Storytelling"],
        communication_style: "Engaging and narrative-driven",
        created_at: new Date().toISOString(),
      },
    ];
    
    for (const persona of fallbackPersonas) {
      this.personas.set(persona.id, persona);
    }
  }

  // Save personas to file
  private async savePersonas(): Promise<void> {
    try {
      const personasObject: Record<string, Omit<Persona, 'id'>> = {};
      for (const [id, persona] of this.personas) {
        const { id: _, ...personaData } = persona;
        personasObject[id] = personaData;
      }
      
      const data = {
        exported_at: new Date().toISOString(),
        description: "Personas managed by Persona Manager MCP",
        personas: personasObject,
      };
      
      await fs.writeFile(PERSONAS_FILE, JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('❌ Error saving personas:', error);
      throw new Error('Failed to save personas to file');
    }
  }

  // Get all personas
  getAllPersonas(): Persona[] {
    return Array.from(this.personas.values());
  }

  // Get persona by ID
  getPersona(id: string): Persona | undefined {
    return this.personas.get(id);
  }

  // Create new persona
  async createPersona(personaData: Omit<Persona, 'id' | 'created_at' | 'updated_at'>, id?: string): Promise<Persona> {
    const personaId = id || this.generateId(personaData.name);
    
    // Check if persona already exists
    if (this.personas.has(personaId)) {
      throw new Error(`Persona with ID '${personaId}' already exists`);
    }

    const persona: Persona = {
      ...personaData,
      id: personaId,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    // Validate persona
    const validatedPersona = PersonaSchema.parse(persona);
    
    // Add to storage
    this.personas.set(personaId, validatedPersona);
    
    // Save to file
    await this.savePersonas();
    
    console.error(`✅ Created new persona: ${persona.name} (${personaId})`);
    return validatedPersona;
  }

  // Update existing persona
  async updatePersona(id: string, updates: Partial<Omit<Persona, 'id' | 'created_at'>>): Promise<Persona> {
    const existingPersona = this.personas.get(id);
    if (!existingPersona) {
      throw new Error(`Persona with ID '${id}' not found`);
    }

    const updatedPersona: Persona = {
      ...existingPersona,
      ...updates,
      updated_at: new Date().toISOString(),
    };

    // Validate updated persona
    const validatedPersona = PersonaSchema.parse(updatedPersona);
    
    // Update in storage
    this.personas.set(id, validatedPersona);
    
    // Save to file
    await this.savePersonas();
    
    console.error(`✅ Updated persona: ${updatedPersona.name} (${id})`);
    return validatedPersona;
  }

  // Delete persona
  async deletePersona(id: string): Promise<boolean> {
    const persona = this.personas.get(id);
    if (!persona) {
      throw new Error(`Persona with ID '${id}' not found`);
    }

    // Remove from storage
    this.personas.delete(id);
    
    // Save to file
    await this.savePersonas();
    
    console.error(`🗑️ Deleted persona: ${persona.name} (${id})`);
    return true;
  }

  // Generate ID from name
  private generateId(name: string): string {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
  }

  // Get statistics
  getStatistics(): {
    total_personas: number;
    categories: string[];
    last_updated: string;
  } {
    const categories = new Set<string>();
    for (const persona of this.personas.values()) {
      if (persona.expertise) {
        persona.expertise.forEach(exp => categories.add(exp));
      }
    }

    return {
      total_personas: this.personas.size,
      categories: Array.from(categories),
      last_updated: new Date().toISOString(),
    };
  }

  // Search personas
  searchPersonas(query: string): Persona[] {
    const searchTerm = query.toLowerCase();
    return Array.from(this.personas.values()).filter(persona => 
      persona.name.toLowerCase().includes(searchTerm) ||
      persona.description.toLowerCase().includes(searchTerm) ||
      persona.expertise.some(exp => exp.toLowerCase().includes(searchTerm))
    );
  }

  // NEW: Get task template for a persona
  getTaskTemplate(personaId: string, taskType: string): any {
    const persona = this.personas.get(personaId);
    if (!persona || !persona.task_templates) {
      return null;
    }
    return persona.task_templates[taskType] || null;
  }

  // NEW: Get communication guidelines for a persona
  getCommunicationGuidelines(personaId: string): any {
    const persona = this.personas.get(personaId);
    return persona?.communication_guidelines || null;
  }

  // NEW: Get expertise details for a persona
  getExpertiseDetails(personaId: string): any {
    const persona = this.personas.get(personaId);
    return persona?.expertise_details || null;
  }

  // AI-powered task matching
  async recommendPersonaForTask(request: TaskRecommendationRequest): Promise<TaskRecommendationResult> {
    const { task_description, task_type, complexity_level, domain } = request;
    
    // Convert task description to lowercase for matching
    const taskLower = task_description.toLowerCase();
    const taskWords = taskLower.split(/\s+/);
    
    const recommendations: TaskRecommendation[] = [];
    
    // Score each persona based on expertise matching
    for (const [id, persona] of this.personas) {
      let score = 0;
      const matchingExpertise: string[] = [];
      
      // Check expertise areas
      if (persona.expertise) {
        for (const expertise of persona.expertise) {
          const expertiseLower = expertise.toLowerCase();
          
          // Direct expertise match
          if (taskLower.includes(expertiseLower)) {
            score += 10;
            matchingExpertise.push(expertise);
          }
          
          // Partial word match
          const expertiseWords = expertiseLower.split(/\s+/);
          for (const word of expertiseWords) {
            if (word.length > 3 && taskWords.includes(word)) {
              score += 5;
              if (!matchingExpertise.includes(expertise)) {
                matchingExpertise.push(expertise);
              }
            }
          }
        }
      }
      
      // Check detailed instructions for task-specific keywords
      if (persona.detailed_instructions) {
        const instructionsLower = persona.detailed_instructions.toLowerCase();
        
        // Task-specific keywords
        const taskKeywords = ['code', 'programming', 'debug', 'design', 'analyze', 'write', 'create', 'build', 'test'];
        for (const keyword of taskKeywords) {
          if (taskLower.includes(keyword) && instructionsLower.includes(keyword)) {
            score += 3;
          }
        }
      }
      
      // Check task templates
      if (persona.task_templates) {
        for (const [templateName, template] of Object.entries(persona.task_templates)) {
          const templateLower = templateName.toLowerCase();
          if (taskLower.includes(templateLower) || taskLower.includes(template.description.toLowerCase())) {
            score += 8;
          }
        }
      }
      
      // Domain matching
      if (domain && persona.context) {
        const contextLower = persona.context.toLowerCase();
        const domainLower = domain.toLowerCase();
        if (contextLower.includes(domainLower) || domainLower.includes(contextLower)) {
          score += 5;
        }
      }
      
      // Task type matching
      if (task_type) {
        const taskTypeLower = task_type.toLowerCase();
        if (persona.expertise?.some(exp => exp.toLowerCase().includes(taskTypeLower))) {
          score += 6;
        }
      }
      
      // Complexity level matching
      if (complexity_level && persona.expertise_details) {
        const complexityScores = {
          'simple': 1,
          'moderate': 2,
          'complex': 3,
          'expert': 4,
        };
        
        const avgProficiency = Object.values(persona.expertise_details)
          .map(detail => {
            const levelScores = { 'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4 };
            return levelScores[detail.proficiency_level] || 2;
          })
          .reduce((a, b) => a + b, 0) / Object.keys(persona.expertise_details).length;
        
        const targetComplexity = complexityScores[complexity_level];
        const complexityMatch = Math.max(0, 5 - Math.abs(avgProficiency - targetComplexity));
        score += complexityMatch;
      }
      
      // Only include personas with meaningful matches
      if (score > 0) {
        recommendations.push({
          persona_id: id,
          persona_name: persona.name,
          confidence_score: Math.min(score, 100) / 100, // Normalize to 0-1
          matching_expertise: matchingExpertise,
          reasoning: this.generateRecommendationReasoning(persona, matchingExpertise, score),
        });
      }
    }
    
    // Sort by confidence score (highest first)
    recommendations.sort((a, b) => b.confidence_score - a.confidence_score);
    
    // Take top 3 recommendations
    const topRecommendations = recommendations.slice(0, 3);
    
    // Generate overall analysis
    const analysis = this.generateTaskAnalysis(request, topRecommendations);
    const overallConfidence = topRecommendations.length > 0 ? topRecommendations[0].confidence_score : 0;
    const reasoning = this.generateOverallReasoning(request, topRecommendations);
    
    return {
      recommendations: topRecommendations,
      analysis,
      confidence_score: overallConfidence,
      reasoning,
    };
  }
  
  private generateRecommendationReasoning(persona: Persona, matchingExpertise: string[], score: number): string {
    const reasons: string[] = [];
    
    if (matchingExpertise.length > 0) {
      reasons.push(`Matches expertise in: ${matchingExpertise.join(', ')}`);
    }
    
    if (persona.detailed_instructions) {
      reasons.push('Has detailed task-specific instructions');
    }
    
    if (persona.task_templates && Object.keys(persona.task_templates).length > 0) {
      reasons.push(`Has ${Object.keys(persona.task_templates).length} task templates available`);
    }
    
    if (persona.expertise_details && Object.keys(persona.expertise_details).length > 0) {
      reasons.push('Has detailed expertise breakdown');
    }
    
    return reasons.join('. ');
  }
  
  private generateTaskAnalysis(request: TaskRecommendationRequest, recommendations: TaskRecommendation[]): string {
    const { task_description, task_type, complexity_level, domain } = request;
    
    let analysis = `Task: "${task_description}"`;
    
    if (task_type) {
      analysis += `\nType: ${task_type}`;
    }
    
    if (complexity_level) {
      analysis += `\nComplexity: ${complexity_level}`;
    }
    
    if (domain) {
      analysis += `\nDomain: ${domain}`;
    }
    
    analysis += `\n\nFound ${recommendations.length} suitable personas with confidence scores:`;
    
    for (const rec of recommendations) {
      analysis += `\n- ${rec.persona_name} (${Math.round(rec.confidence_score * 100)}%)`;
    }
    
    return analysis;
  }
  
  private generateOverallReasoning(request: TaskRecommendationRequest, recommendations: TaskRecommendation[]): string {
    if (recommendations.length === 0) {
      return "No personas found that match the task requirements. Consider creating a new persona or broadening the task description.";
    }
    
    const topRec = recommendations[0];
    let reasoning = `Top recommendation: ${topRec.persona_name} with ${Math.round(topRec.confidence_score * 100)}% confidence. `;
    
    if (topRec.matching_expertise.length > 0) {
      reasoning += `This persona excels in: ${topRec.matching_expertise.join(', ')}. `;
    }
    
    reasoning += topRec.reasoning;
    
    if (recommendations.length > 1) {
      reasoning += `\n\nAlternative options: ${recommendations.slice(1).map(r => r.persona_name).join(', ')}`;
    }
    
    return reasoning;
  }
}

// ... existing code ...

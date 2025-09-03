import { promises as fs } from 'fs';
import { join } from 'path';
import { z } from 'zod';

// Persona schema validation
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
});

export type Persona = z.infer<typeof PersonaSchema>;

// Storage configuration
const PERSONAS_DIR = join(process.cwd(), 'personas');
const PERSONAS_FILE = join(PERSONAS_DIR, 'personas.json');
const DEFAULT_PERSONAS_FILE = join(PERSONAS_DIR, 'default_personas.json');

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
}

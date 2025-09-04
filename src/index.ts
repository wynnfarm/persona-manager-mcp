#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { Command } from "commander";
import { PersonaStorage, Persona, TaskRecommendationRequest, TaskRecommendationResult } from "./storage.js";

// Parse CLI arguments using commander
const program = new Command()
  .option("--transport <stdio|http>", "transport type", "stdio")
  .option("--port <number>", "port for HTTP transport", "3000")
  .allowUnknownOption() // let MCP Inspector / other wrappers pass through extra flags
  .parse(process.argv);

const cliOptions = program.opts<{
  transport: string;
  port: string;
}>();

// Validate transport option
const allowedTransports = ["stdio", "http"];
if (!allowedTransports.includes(cliOptions.transport)) {
  console.error(`Invalid --transport value: '${cliOptions.transport}'. Must be one of: stdio, http.`);
  process.exit(1);
}

// Transport configuration
const TRANSPORT_TYPE = (cliOptions.transport || "stdio") as "stdio" | "http";

// Disallow incompatible flags based on transport
const passedPortFlag = process.argv.includes("--port");

if (TRANSPORT_TYPE === "stdio" && passedPortFlag) {
  console.error("The --port flag is not allowed when using --transport stdio.");
  process.exit(1);
}

// HTTP port configuration
const CLI_PORT = (() => {
  const parsed = parseInt(cliOptions.port, 10);
  return isNaN(parsed) ? undefined : parsed;
})();

// Global persona state
let currentPersona: Persona | null = null;
let personaStorage: PersonaStorage;

// Function to echo current persona
function echoCurrentPersona() {
  if (currentPersona) {
    console.error(`🎭 Currently using persona: ${currentPersona.name} (${currentPersona.id})`);
    console.error(`   Description: ${currentPersona.description}`);
    console.error(`   Expertise: ${currentPersona.expertise.join(", ")}`);
    console.error(`   Communication Style: ${currentPersona.communication_style}`);
  } else {
    console.error("🎭 No persona currently selected");
  }
}

// Function to create a new server instance with all tools registered
function createServerInstance() {
  const server = new McpServer({
    name: "persona-manager",
    version: "1.0.0",
  });

  // Tool: List all personas
  server.tool(
    "list_personas",
    {
      include_metadata: z.boolean().optional().describe("Include metadata in response"),
    },
    async ({ include_metadata }) => {
      const personas = personaStorage.getAllPersonas();
      const stats = personaStorage.getStatistics();

      const result = include_metadata
        ? { personas, metadata: stats }
        : { personas };

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    },
  );

  // Tool: Select best persona for a task
  server.tool(
    "select_persona",
    {
      task_description: z.string().describe("Description of the task"),
      context: z.string().optional().describe("Additional context"),
    },
    async ({ task_description, context }) => {
      const personas = personaStorage.getAllPersonas();
      
      // Simple persona selection logic (can be enhanced with AI later)
      let selectedPersona = personas[0]; // Default to first persona
      let confidence = 0.5;
      let reason = "Default selection";

      // Search for better matches based on task description
      const searchTerm = task_description.toLowerCase();
      
      for (const persona of personas) {
        let score = 0;
        
        // Check expertise matches
        for (const expertise of persona.expertise) {
          if (searchTerm.includes(expertise.toLowerCase())) {
            score += 2;
          }
        }
        
        // Check description matches
        if (persona.description.toLowerCase().includes(searchTerm)) {
          score += 1;
        }
        
        // Check context matches
        if (persona.context && persona.context.toLowerCase().includes(searchTerm)) {
          score += 1.5;
        }
        
        if (score > confidence) {
          selectedPersona = persona;
          confidence = score;
          reason = `Matched expertise: ${persona.expertise.join(", ")}`;
        }
      }

      // Set current persona and echo it
      currentPersona = selectedPersona;
      echoCurrentPersona();

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              id: selectedPersona.id,
              name: selectedPersona.name,
              confidence: Math.min(confidence / 3, 1), // Normalize to 0-1
              reason,
            }, null, 2),
          },
        ],
      };
    },
  );

  // Tool: Get persona statistics
  server.tool("get_persona_statistics", {}, async () => {
    const stats = personaStorage.getStatistics();
    const result = {
      ...stats,
      current_persona: currentPersona,
    };

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  });

  // Tool: Echo current persona
  server.tool("echo_current_persona", {}, async () => {
    if (currentPersona) {
      return {
        content: [
          {
            type: "text",
            text: `🎭 Currently using persona: ${currentPersona.name} (${currentPersona.id})\nDescription: ${currentPersona.description}\nExpertise: ${currentPersona.expertise.join(", ")}\nCommunication Style: ${currentPersona.communication_style}`,
          },
        ],
      };
    } else {
      return {
        content: [
          {
            type: "text",
            text: "🎭 No persona currently selected",
          },
        ],
      };
    }
  });

  // Tool: Set persona manually
  server.tool(
    "set_persona",
    {
      persona_id: z.string().describe("ID of the persona to set"),
    },
    async ({ persona_id }) => {
      const persona = personaStorage.getPersona(persona_id);
      if (persona) {
        currentPersona = persona;
        echoCurrentPersona();
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, persona: currentPersona }, null, 2),
            },
          ],
        };
      } else {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: false, error: `Persona with ID '${persona_id}' not found` }, null, 2),
            },
          ],
        };
      }
    },
  );

  // NEW TOOL: Create new persona
  server.tool(
    "create_persona",
    {
      name: z.string().describe("Name of the persona"),
      description: z.string().describe("Description of the persona"),
      expertise: z.array(z.string()).describe("Areas of expertise"),
      communication_style: z.string().describe("Communication style"),
      context: z.string().optional().describe("Context for when to use this persona"),
      personality_traits: z.array(z.string()).optional().describe("Personality traits"),
      id: z.string().optional().describe("Custom ID for the persona (auto-generated if not provided)"),
    },
    async (personaData) => {
      try {
        const persona = await personaStorage.createPersona(personaData);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, persona }, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: false, error: (error as Error).message }, null, 2),
            },
          ],
        };
      }
    },
  );

  // NEW TOOL: Update existing persona
  server.tool(
    "update_persona",
    {
      persona_id: z.string().describe("ID of the persona to update"),
      name: z.string().optional().describe("New name for the persona"),
      description: z.string().optional().describe("New description for the persona"),
      expertise: z.array(z.string()).optional().describe("New areas of expertise"),
      communication_style: z.string().optional().describe("New communication style"),
      context: z.string().optional().describe("New context for when to use this persona"),
      personality_traits: z.array(z.string()).optional().describe("New personality traits"),
    },
    async ({ persona_id, ...updates }) => {
      try {
        const persona = await personaStorage.updatePersona(persona_id, updates);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, persona }, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: false, error: (error as Error).message }, null, 2),
            },
          ],
        };
      }
    },
  );

  // NEW TOOL: Delete persona
  server.tool(
    "delete_persona",
    {
      persona_id: z.string().describe("ID of the persona to delete"),
    },
    async ({ persona_id }) => {
      try {
        await personaStorage.deletePersona(persona_id);
        
        // Clear current persona if it was deleted
        if (currentPersona?.id === persona_id) {
          currentPersona = null;
          console.error("🎭 Current persona was deleted, clearing selection");
        }
        
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, message: `Persona '${persona_id}' deleted successfully` }, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: false, error: (error as Error).message }, null, 2),
            },
          ],
        };
      }
    },
  );

  // NEW TOOL: Search personas
  server.tool(
    "search_personas",
    {
      query: z.string().describe("Search query to find matching personas"),
    },
    async ({ query }) => {
      const results = personaStorage.searchPersonas(query);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ results, count: results.length }, null, 2),
          },
        ],
      };
    },
  );

  // NEW TOOL: Get persona by ID
  server.tool(
    "get_persona",
    {
      persona_id: z.string().describe("ID of the persona to retrieve"),
    },
    async ({ persona_id }) => {
      const persona = personaStorage.getPersona(persona_id);
      if (persona) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, persona }, null, 2),
            },
          ],
        };
      } else {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: false, error: `Persona with ID '${persona_id}' not found` }, null, 2),
            },
          ],
        };
      }
    },
  );

  // NEW TOOL: Get task template for a persona
  server.tool(
    "get_task_template",
    {
      persona_id: z.string().describe("ID of the persona"),
      task_type: z.string().describe("Type of task template to retrieve"),
    },
    async ({ persona_id, task_type }) => {
      const template = personaStorage.getTaskTemplate(persona_id, task_type);
      if (template) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, template }, null, 2),
            },
          ],
        };
      } else {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: false, error: `Task template '${task_type}' not found for persona '${persona_id}'` }, null, 2),
            },
          ],
        };
      }
    },
  );

  // NEW TOOL: Get communication guidelines for a persona
  server.tool(
    "get_communication_guidelines",
    {
      persona_id: z.string().describe("ID of the persona"),
    },
    async ({ persona_id }) => {
      const guidelines = personaStorage.getCommunicationGuidelines(persona_id);
      if (guidelines) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, guidelines }, null, 2),
            },
          ],
        };
      } else {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: false, error: `Communication guidelines not found for persona '${persona_id}'` }, null, 2),
            },
          ],
        };
      }
    },
  );

  // NEW TOOL: Get expertise details for a persona
  server.tool(
    "get_expertise_details",
    {
      persona_id: z.string().describe("ID of the persona"),
    },
    async ({ persona_id }) => {
      const expertise = personaStorage.getExpertiseDetails(persona_id);
      if (expertise) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, expertise }, null, 2),
            },
          ],
        };
      } else {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: false, error: `Expertise details not found for persona '${persona_id}'` }, null, 2),
            },
          ],
        };
      }
    },
  );

  // NEW TOOL: Get detailed persona instructions
  server.tool(
    "get_persona_instructions",
    {
      persona_id: z.string().describe("ID of the persona"),
    },
    async ({ persona_id }) => {
      const persona = personaStorage.getPersona(persona_id);
      if (persona) {
        const instructions = {
          detailed_instructions: persona.detailed_instructions,
          behavior_patterns: persona.behavior_patterns,
          conversation_starters: persona.conversation_starters,
          response_templates: persona.response_templates,
          decision_frameworks: persona.decision_frameworks,
          role_specific_instructions: persona.role_specific_instructions,
        };
        
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: true, instructions }, null, 2),
            },
          ],
        };
      } else {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ success: false, error: `Persona with ID '${persona_id}' not found` }, null, 2),
            },
          ],
        };
      }
    },
  );

  // Add new tool for AI-powered task matching
  server.tool(
    "recommend_persona_for_task",
    {
      task_description: z.string().describe("Detailed description of the task to be performed"),
      task_type: z.string().optional().describe("Optional task type category (e.g., 'coding', 'writing', 'analysis')"),
      complexity_level: z.enum(["simple", "moderate", "complex", "expert"]).optional().describe("Task complexity level"),
      domain: z.string().optional().describe("Optional domain or industry context"),
    },
    async ({ task_description, task_type, complexity_level, domain }) => {
      try {
        const recommendations = await personaStorage.recommendPersonaForTask({
          task_description,
          task_type,
          complexity_level,
          domain,
        });

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({
                recommendations: recommendations.recommendations,
                analysis: recommendations.analysis,
                confidence_score: recommendations.confidence_score,
                reasoning: recommendations.reasoning,
              }, null, 2),
            },
          ],
        };
      } catch (error) {
        console.error("Error recommending persona for task:", error);
        throw new Error(`Failed to recommend persona: ${error}`);
      }
    },
  );

  return server;
}

async function main() {
  // Initialize persona storage
  personaStorage = new PersonaStorage();
  await personaStorage.initialize();

  const server = createServerInstance();

  if (TRANSPORT_TYPE === "stdio") {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Persona Manager MCP Server started on stdio");
  } else {
    throw new Error("HTTP transport not implemented yet");
  }
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});

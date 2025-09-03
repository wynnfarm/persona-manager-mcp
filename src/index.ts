#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { Command } from "commander";

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
let currentPersona: any = null;

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
      const personas = [
        {
          id: "tech-expert",
          name: "Tech Expert",
          description: "Technical expert with deep knowledge of software development",
          expertise: ["Python", "JavaScript", "System Architecture"],
          communication_style: "Technical and precise",
        },
        {
          id: "creative-writer",
          name: "Creative Writer",
          description: "Creative writer with expertise in storytelling and content creation",
          expertise: ["Creative Writing", "Content Strategy", "Storytelling"],
          communication_style: "Engaging and narrative-driven",
        },
      ];

      const result = include_metadata
        ? { personas, metadata: { total: personas.length, timestamp: new Date().toISOString() } }
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
      // Simple persona selection logic
      let selectedPersona = {
        id: "tech-expert",
        name: "Tech Expert",
        confidence: 0.8,
        reason: "Default technical persona",
      };

      if (
        task_description.toLowerCase().includes("creative") ||
        task_description.toLowerCase().includes("writing") ||
        task_description.toLowerCase().includes("story")
      ) {
        selectedPersona = {
          id: "creative-writer",
          name: "Creative Writer",
          confidence: 0.9,
          reason: "Task involves creative writing or storytelling",
        };
      }

      // Set current persona and echo it
      currentPersona = selectedPersona;
      echoCurrentPersona();

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(selectedPersona, null, 2),
          },
        ],
      };
    },
  );

  // Tool: Get persona statistics
  server.tool("get_persona_statistics", {}, async () => {
    const stats = {
      total_personas: 2,
      categories: ["technical", "creative"],
      last_updated: new Date().toISOString(),
      current_persona: currentPersona,
    };

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(stats, null, 2),
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
      const personas = [
        {
          id: "tech-expert",
          name: "Tech Expert",
          description: "Technical expert with deep knowledge of software development",
          expertise: ["Python", "JavaScript", "System Architecture"],
          communication_style: "Technical and precise",
        },
        {
          id: "creative-writer",
          name: "Creative Writer",
          description: "Creative writer with expertise in storytelling and content creation",
          expertise: ["Creative Writing", "Content Strategy", "Storytelling"],
          communication_style: "Engaging and narrative-driven",
        },
      ];

      const persona = personas.find((p) => p.id === persona_id);
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

  return server;
}

async function main() {
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

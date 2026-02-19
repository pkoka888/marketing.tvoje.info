#!/usr/bin/env node
/**
 * MCP Server Wrapper - Cross-platform .env loader
 * Loads .env file and executes MCP server with environment variables
 *
 * Usage: node mcp-wrapper.js <server-type>
 *   server-type: redis | firecrawl | github
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env file
function loadEnv() {
  const projectRoot = path.resolve(__dirname, '..', '..');
  const envPath = path.join(projectRoot, '.env');

  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    const lines = envContent.split('\n');

    for (const line of lines) {
      const trimmed = line.trim();
      // Skip comments and empty lines
      if (trimmed.startsWith('#') || trimmed === '') continue;

      const match = trimmed.match(/^([^=]+)=(.*)$/);
      if (match) {
        const key = match[1].trim();
        const value = match[2].trim().replace(/^["']|["']$/g, ''); // Remove quotes

        // Only set if not already set in environment
        if (process.env[key] === undefined) {
          process.env[key] = value;
        }
      }
    }
    console.error('[MCP-WRAPPER] Loaded .env from:', envPath);
  } else {
    console.error('[MCP-WRAPPER] Warning: .env file not found at:', envPath);
  }
}

// Server configurations
const servers = {
  redis: {
    command: 'node',
    args: [path.join(__dirname, 'redis-server.js')],
    required: ['PROJECT_NAME', 'REDIS_PASSWORD'],
  },
  firecrawl: {
    command: 'node',
    args: [path.join('/c/nvm4w/nodejs/node_modules/firecrawl-mcp/dist/index.js')],
    required: ['FIRECRAWL_API_KEY'],
  },
  github: {
    command: 'node',
    args: [
      path.join('/c/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-github/dist/index.js'),
    ],
    required: ['GITHUB_TOKEN'],
  },
};

function main() {
  const serverType = process.argv[2];

  if (!serverType || !servers[serverType]) {
    console.error('Usage: node mcp-wrapper.js <server-type>');
    console.error('Available servers:', Object.keys(servers).join(', '));
    process.exit(1);
  }

  // Load environment variables from .env
  loadEnv();

  const config = servers[serverType];

  // Verify required environment variables
  const missing = config.required.filter((key) => !process.env[key]);
  if (missing.length > 0) {
    console.error(
      `[MCP-WRAPPER] Error: Missing required environment variables: ${missing.join(', ')}`
    );
    process.exit(1);
  }

  console.error(`[MCP-WRAPPER] Starting ${serverType} MCP server...`);
  console.error(`[MCP-WRAPPER] Command: ${config.command} ${config.args.join(' ')}`);

  // Spawn the server process
  const child = spawn(config.command, config.args, {
    stdio: ['pipe', 'pipe', 'pipe'],
    env: process.env,
  });

  // Forward stdin/stdout for MCP protocol
  process.stdin.pipe(child.stdin);
  child.stdout.pipe(process.stdout);
  child.stderr.pipe(process.stderr);

  child.on('exit', (code) => {
    process.exit(code);
  });

  child.on('error', (err) => {
    console.error(`[MCP-WRAPPER] Failed to start ${serverType}:`, err.message);
    process.exit(1);
  });
}

main();

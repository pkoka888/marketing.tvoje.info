/**
 * ONE-AND-ONLY-REDIS MCP Server
 *
 * Professional Redis MCP Server with project context isolation.
 * Prevents mixed context between different projects using key prefixes.
 *
 * Features:
 *   - Project context isolation via key prefixes
 *   - Automatic key namespacing: project:{PROJECT_NAME}:{key}
 *   - Support for local Redis (REDIS_URL) or individual params
 *   - Connection health monitoring
 *   - TTL support for expiring keys
 *
 * Environment Variables:
 *   - REDIS_URL: Redis connection URL (e.g., redis://localhost:6379)
 *   - REDIS_HOST: Redis host (default: 0.0.0.0 for Docker compatibility)
 *   - REDIS_PORT: Redis port (default: 6379)
 *   - PROJECT_NAME: Project identifier for key isolation (required)
 *
 * Usage:
 *   All keys are automatically prefixed with project namespace:
 *   - Input key: "user:session"
 *   - Stored as: "project:marketing-tvoje-info:user:session"
 *
 * Required npm packages:
 *   npm install @modelcontextprotocol/sdk ioredis
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import Redis from 'ioredis';

// Project context isolation - get project name from environment
const PROJECT_NAME = process.env.PROJECT_NAME || 'default';
const KEY_PREFIX = `project:${PROJECT_NAME}:`;

console.error(`[ONE-AND-ONLY-REDIS] Project context: ${PROJECT_NAME}`);
console.error(`[ONE-AND-ONLY-REDIS] Key prefix: ${KEY_PREFIX}`);

// Initialize Redis client
function getRedisClient() {
  const redisUrl = process.env.REDIS_URL;
  const redisHost = process.env.REDIS_HOST || '0.0.0.0'; // Default to 0.0.0.0 for Docker compatibility
  const redisPort = parseInt(process.env.REDIS_PORT || '6379', 10);

  // Option 1: Use REDIS_URL if provided (takes precedence)
  if (redisUrl) {
    console.error('[ONE-AND-ONLY-REDIS] Using Redis URL:', redisUrl);
    return new Redis(redisUrl, {
      maxRetriesPerRequest: 3,
      retryStrategy(times) {
        if (times > 3) {
          console.error('[ONE-AND-ONLY-REDIS] Failed to connect after 3 attempts');
          return null;
        }
        return Math.min(times * 200, 1000);
      },
      commandTimeout: 5000,
      enableReadyCheck: true,
      maxRedirections: 3,
    });
  }

  // Option 2: Use individual parameters (REDIS_HOST, REDIS_PORT)
  // Default host is 0.0.0.0 for Docker container access
  console.error(`[ONE-AND-ONLY-REDIS] Using Redis host: ${redisHost}:${redisPort}`);
  return new Redis({
    host: redisHost,
    port: redisPort,
    maxRetriesPerRequest: 3,
    retryStrategy(times) {
      if (times > 3) {
        console.error('[ONE-AND-ONLY-REDIS] Failed to connect after 3 attempts');
        return null;
      }
      return Math.min(times * 200, 1000);
    },
    commandTimeout: 5000,
    enableReadyCheck: true,
    maxRedirections: 3,
    // Add these for robust connection
    connectTimeout: 10000,
    keepAlive: 1000,
  });
}

let redis;

async function initializeRedis() {
  try {
    redis = getRedisClient();

    redis.on('error', (err) => {
      console.error('[ONE-AND-ONLY-REDIS] Redis error:', err.message);
    });

    redis.on('connect', () => {
      console.error('[ONE-AND-ONLY-REDIS] Connected to Redis');
    });

    // Test connection
    await redis.ping();
    console.error('[ONE-AND-ONLY-REDIS] Connection verified successfully');
  } catch (error) {
    console.error('[ONE-AND-ONLY-REDIS] Failed to initialize:', error.message);
    process.exit(1);
  }
}

// Helper: Add project prefix to key
function prefixKey(key) {
  return `${KEY_PREFIX}${key}`;
}

// Helper: Add project prefix to multiple keys
function prefixKeys(keys) {
  return keys.map((key) => prefixKey(key));
}

// Helper: Remove project prefix from key (for display)
function unprefixKey(key) {
  if (key.startsWith(KEY_PREFIX)) {
    return key.slice(KEY_PREFIX.length);
  }
  return key;
}

// Create MCP server
console.error('[ONE-AND-ONLY-REDIS] Initializing Server class...');
let server;
try {
  server = new Server(
    {
      name: 'one-and-only-redis',
      version: '2.0.0',
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );
  console.error('[ONE-AND-ONLY-REDIS] Server class initialized.');
} catch (error) {
  console.error('[ONE-AND-ONLY-REDIS] Failed to initialize Server class:', error);
  process.exit(1);
}

// Tool definitions
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'redis_get',
        description: `Get value from Redis by key. Keys are automatically prefixed with project namespace (${KEY_PREFIX}).`,
        inputSchema: {
          type: 'object',
          properties: {
            key: {
              type: 'string',
              description: 'Redis key (will be prefixed with project namespace)',
            },
          },
          required: ['key'],
        },
      },
      {
        name: 'redis_set',
        description: `Set key-value pair in Redis. Keys are automatically prefixed with project namespace (${KEY_PREFIX}).`,
        inputSchema: {
          type: 'object',
          properties: {
            key: {
              type: 'string',
              description: 'Redis key (will be prefixed with project namespace)',
            },
            value: { type: 'string', description: 'Value to store' },
            ttl: { type: 'number', description: 'Optional TTL in seconds' },
          },
          required: ['key', 'value'],
        },
      },
      {
        name: 'redis_del',
        description: `Delete key(s) from Redis. Keys are automatically prefixed with project namespace.`,
        inputSchema: {
          type: 'object',
          properties: {
            keys: {
              type: 'array',
              items: { type: 'string' },
              description: 'Array of keys to delete (will be prefixed with project namespace)',
            },
          },
          required: ['keys'],
        },
      },
      {
        name: 'redis_keys',
        description: `Find all keys matching pattern within project namespace. Pattern is applied after project prefix.`,
        inputSchema: {
          type: 'object',
          properties: {
            pattern: {
              type: 'string',
              description: 'Key pattern to match within project namespace (e.g., user:*)',
            },
          },
          required: ['pattern'],
        },
      },
      {
        name: 'redis_exists',
        description: `Check if key(s) exist in Redis within project namespace.`,
        inputSchema: {
          type: 'object',
          properties: {
            keys: {
              type: 'array',
              items: { type: 'string' },
              description: 'Array of keys to check (will be prefixed with project namespace)',
            },
          },
          required: ['keys'],
        },
      },
      {
        name: 'redis_ttl',
        description: `Get TTL (time to live) of a key within project namespace.`,
        inputSchema: {
          type: 'object',
          properties: {
            key: {
              type: 'string',
              description: 'Redis key (will be prefixed with project namespace)',
            },
          },
          required: ['key'],
        },
      },
      {
        name: 'redis_expire',
        description: `Set expiration on a key within project namespace.`,
        inputSchema: {
          type: 'object',
          properties: {
            key: {
              type: 'string',
              description: 'Redis key (will be prefixed with project namespace)',
            },
            seconds: { type: 'number', description: 'TTL in seconds' },
          },
          required: ['key', 'seconds'],
        },
      },
      {
        name: 'redis_ping',
        description: 'Ping Redis server to check connection health.',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'redis_info',
        description: 'Get Redis server information including project context.',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'redis_list_projects',
        description:
          'List all project namespaces currently in Redis (keys starting with project:).',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
    ],
  };
});

// Tool handlers
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'redis_get': {
        const prefixedKey = prefixKey(args.key);
        const value = await redis.get(prefixedKey);
        return {
          content: [
            {
              type: 'text',
              text: value || `(key not found: ${args.key})`,
            },
          ],
        };
      }

      case 'redis_set': {
        const prefixedKey = prefixKey(args.key);
        if (args.ttl) {
          await redis.set(prefixedKey, args.value, 'EX', args.ttl);
        } else {
          await redis.set(prefixedKey, args.value);
        }
        return {
          content: [
            {
              type: 'text',
              text: `OK - Key "${args.key}" stored with project namespace "${PROJECT_NAME}"`,
            },
          ],
        };
      }

      case 'redis_del': {
        const prefixedKeys = prefixKeys(args.keys);
        const result = await redis.del(...prefixedKeys);
        return {
          content: [
            {
              type: 'text',
              text: `Deleted ${result} key(s) from project "${PROJECT_NAME}"`,
            },
          ],
        };
      }

      case 'redis_keys': {
        // Search within project namespace only
        const prefixedPattern = prefixKey(args.pattern);
        const keys = await redis.keys(prefixedPattern);
        // Remove prefix for display
        const displayKeys = keys.map(unprefixKey);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                {
                  project: PROJECT_NAME,
                  pattern: args.pattern,
                  count: displayKeys.length,
                  keys: displayKeys,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      case 'redis_exists': {
        const prefixedKeys = prefixKeys(args.keys);
        const result = await redis.exists(...prefixedKeys);
        return {
          content: [
            {
              type: 'text',
              text: `${result} of ${args.keys.length} key(s) exist in project "${PROJECT_NAME}"`,
            },
          ],
        };
      }

      case 'redis_ttl': {
        const prefixedKey = prefixKey(args.key);
        const ttl = await redis.ttl(prefixedKey);
        let message;
        if (ttl === -2) {
          message = `Key "${args.key}" does not exist`;
        } else if (ttl === -1) {
          message = `Key "${args.key}" exists but has no expiration`;
        } else {
          message = `Key "${args.key}" has TTL of ${ttl} seconds`;
        }
        return { content: [{ type: 'text', text: message }] };
      }

      case 'redis_expire': {
        const prefixedKey = prefixKey(args.key);
        const result = await redis.expire(prefixedKey, args.seconds);
        if (result === 1) {
          return {
            content: [
              {
                type: 'text',
                text: `OK - Key "${args.key}" will expire in ${args.seconds} seconds`,
              },
            ],
          };
        } else {
          return {
            content: [
              {
                type: 'text',
                text: `Key "${args.key}" does not exist`,
              },
            ],
          };
        }
      }

      case 'redis_ping': {
        const result = await redis.ping();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                {
                  status: result,
                  project: PROJECT_NAME,
                  keyPrefix: KEY_PREFIX,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      case 'redis_info': {
        const info = await redis.info();
        const dbSize = await redis.dbsize();
        const projectKeys = await redis.keys(`${KEY_PREFIX}*`);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                {
                  project: PROJECT_NAME,
                  keyPrefix: KEY_PREFIX,
                  projectKeyCount: projectKeys.length,
                  totalKeys: dbSize,
                  redisVersion: info.match(/redis_version:([^\r\n]+)/)?.[1] || 'unknown',
                  connectedClients: info.match(/connected_clients:([^\r\n]+)/)?.[1] || 'unknown',
                  usedMemory: info.match(/used_memory_human:([^\r\n]+)/)?.[1] || 'unknown',
                },
                null,
                2
              ),
            },
          ],
        };
      }

      case 'redis_list_projects': {
        // Get all project namespaces
        const allProjectKeys = await redis.keys('project:*');
        const projects = new Set();
        allProjectKeys.forEach((key) => {
          const match = key.match(/^project:([^:]+):/);
          if (match) {
            projects.add(match[1]);
          }
        });
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                {
                  currentProject: PROJECT_NAME,
                  allProjects: Array.from(projects).sort(),
                  projectCount: projects.size,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      default:
        return { content: [{ type: 'text', text: `Unknown tool: ${name}` }] };
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
    };
  }
});

// Start server
async function main() {
  await initializeRedis();

  // Start the MCP server
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('[ONE-AND-ONLY-REDIS] MCP server started');
}

main().catch((error) => {
  console.error('[ONE-AND-ONLY-REDIS] Fatal error:', error);
  process.exit(1);
});

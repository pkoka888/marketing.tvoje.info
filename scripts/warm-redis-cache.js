#!/usr/bin/env node
/**
 * Redis Cache Warming Script
 * Pre-populates cache after Redis restart
 *
 * Usage: node scripts/warm-redis-cache.js
 */

import Redis from 'ioredis';

const PROJECT_NAME = process.env.PROJECT_NAME || 'marketing-tvoje-info';
const REDIS_URL = process.env.REDIS_URL || 'redis://:marketing@localhost:36379';
const KEY_PREFIX = `project:${PROJECT_NAME}:`;

const redis = new Redis(REDIS_URL, {
  maxRetriesPerRequest: 3,
  connectTimeout: 10000,
});

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function warmCache() {
  log('\n🔥 Warming up Redis cache...', 'cyan');
  log('═'.repeat(50), 'cyan');

  try {
    // Test connection first
    const ping = await redis.ping();
    if (ping !== 'PONG') {
      throw new Error('Redis not responding to PING');
    }
    log('✅ Redis connection established', 'green');

    // 1. Warm project metadata
    await redis.setex(`${KEY_PREFIX}meta:version`, 3600, '1.0.0');
    await redis.setex(`${KEY_PREFIX}meta:last-deploy`, 3600, new Date().toISOString());
    log('✅ Project metadata cached', 'green');

    // 2. Warm rate limit counters (initialize to 0 with daily expiration)
    await redis.setex(`${KEY_PREFIX}rate-limit:daily:count`, 86400, '0');
    await redis.setex(`${KEY_PREFIX}rate-limit:hourly:count`, 3600, '0');
    log('✅ Rate limit counters initialized', 'green');

    // 3. Warm MCP server health status
    const servers = ['filesystem', 'memory', 'git', 'github', 'redis', 'bmad-mcp'];
    for (const server of servers) {
      await redis.setex(`${KEY_PREFIX}mcp:${server}:status`, 300, 'ready');
      await redis.setex(`${KEY_PREFIX}mcp:${server}:last-check`, 300, Date.now().toString());
    }
    log(`✅ ${servers.length} MCP server statuses cached`, 'green');

    // 4. Set cache warming timestamp
    await redis.set(`${KEY_PREFIX}meta:last-warmed`, new Date().toISOString());

    // 5. Warm common configuration
    await redis.setex(`${KEY_PREFIX}config:cache-ttl`, 3600, '3600');
    await redis.setex(`${KEY_PREFIX}config:rate-limit`, 3600, '100');
    log('✅ Configuration cached', 'green');

    log('\n' + '═'.repeat(50), 'cyan');
    log('✨ Cache warming complete!', 'green');

    // Show stats
    const keys = await redis.keys(`${KEY_PREFIX}*`);
    log(`📊 Total keys for project: ${keys.length}`, 'cyan');
  } catch (error) {
    log(`\n❌ Error: ${error.message}`, 'red');
    process.exit(1);
  } finally {
    redis.disconnect();
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  warmCache();
}

export { warmCache };

#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const MCP_CONFIG_PATH = '.kilocode/mcp.json';
const REQUIRED_REDIS_PORT = '36379';
const REQUIRED_PLAYWRIGHT_PKG = '@playwright/mcp';
const REQUIRED_REDIS_PKG = '@modelcontextprotocol/server-redis';
const REQUIRED_MEMORY_PKG = 'mcp-memory-keeper';

let errors = [];
let warnings = [];

function validateMCPConfig() {
  console.log('🔍 Validating MCP Configuration...\n');

  if (!fs.existsSync(MCP_CONFIG_PATH)) {
    errors.push(`MCP config not found: ${MCP_CONFIG_PATH}`);
    return;
  }

  let mcp;
  try {
    mcp = JSON.parse(fs.readFileSync(MCP_CONFIG_PATH, 'utf8'));
  } catch (e) {
    errors.push(`Invalid JSON: ${e.message}`);
    return;
  }

  const servers = mcp.mcpServers || {};

  // Validate Redis
  const redis = servers.redis;
  if (!redis) {
    errors.push('Redis MCP server not found');
  } else {
    const redisPort = redis.env?.REDIS_PORT || redis.args?.join(' ').match(/--port\s+(\d+)/)?.[1];
    if (redisPort !== REQUIRED_REDIS_PORT) {
      errors.push(`Redis port must be ${REQUIRED_REDIS_PORT}, got: ${redisPort}`);
    }

    if (!redis.command?.includes('cmd')) {
      warnings.push('Redis should use "cmd" command for Windows');
    }

    const args = redis.args?.join(' ') || '';
    if (!args.includes(REQUIRED_REDIS_PKG)) {
      errors.push(`Redis must use package: ${REQUIRED_REDIS_PKG}`);
    }
  }

  // Validate Playwright
  const playwright = servers['playwright-mcp'];
  if (!playwright) {
    warnings.push('Playwright MCP server not found');
  } else {
    const args = playwright.args?.join(' ') || '';
    if (!args.includes(REQUIRED_PLAYWRIGHT_PKG)) {
      errors.push(`Playwright must use package: ${REQUIRED_PLAYWRIGHT_PKG}`);
    }

    if (!playwright.command?.includes('cmd')) {
      warnings.push('Playwright should use "cmd" command for Windows');
    }
  }

  // Validate Memory (should be persistent, not in-memory)
  const memory = servers.memory;
  if (!memory) {
    warnings.push('Memory MCP server not found - using session memory only');
  } else {
    const args = memory.args?.join(' ') || '';
    if (args.includes('@modelcontextprotocol/server-memory')) {
      warnings.push(
        'Memory uses in-memory storage - will forget on session end. Use mcp-memory-keeper for persistence'
      );
    }

    if (!memory.command?.includes('cmd')) {
      warnings.push('Memory should use "cmd" command for Windows');
    }
  }

  // Print results
  console.log('📋 Results:\n');

  if (errors.length === 0 && warnings.length === 0) {
    console.log('✅ MCP Configuration is VALID\n');
    console.log('   Redis Port:', redis?.env?.REDIS_PORT || 'default');
    console.log('   Redis Package:', REQUIRED_REDIS_PKG);
    console.log('   Playwright Package:', REQUIRED_PLAYWRIGHT_PKG);
    process.exit(0);
  }

  if (errors.length > 0) {
    console.log('❌ ERRORS:');
    errors.forEach((e) => console.log(`   - ${e}`));
  }

  if (warnings.length > 0) {
    console.log('\n⚠️  WARNINGS:');
    warnings.forEach((w) => console.log(`   - ${w}`));
  }

  console.log('\n❌ Validation FAILED\n');
  process.exit(1);
}

validateMCPConfig();

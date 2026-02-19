#!/usr/bin/env node

/**
 * MCP Server Verification Script
 * 
 * This script tests all MCP servers to ensure they start correctly after path fixes.
 * Run this script to verify that the hardcoded path issues have been resolved.
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// MCP servers to test
const mcpServers = [
  {
    name: 'filesystem-projects',
    command: 'node',
    args: ['C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js', 'C:/Users/pavel/projects'],
    timeout: 5000
  },
  {
    name: 'filesystem-agentic', 
    command: 'node',
    args: ['C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js', 'C:/Users/pavel/vscodeportable/agentic'],
    timeout: 5000
  },
  {
    name: 'memory',
    command: 'node', 
    args: ['C:/nvm4w/nodejs/node_modules/@modelcontextprotocol/server-memory/dist/index.js'],
    timeout: 5000
  },
  {
    name: 'git',
    command: 'node',
    args: ['C:/nvm4w/nodejs/node_modules/git-mcp/dist/index.js'],
    timeout: 5000
  },
  {
    name: 'github',
    command: 'node',
    args: ['./.kilocode/mcp-servers/mcp-wrapper.js', 'github'],
    timeout: 5000
  },
  {
    name: 'redis',
    command: 'node',
    args: ['./.kilocode/mcp-servers/mcp-wrapper.js', 'redis'],
    timeout: 5000
  },
  {
    name: 'bmad-mcp',
    command: 'node',
    args: ['C:/nvm4w/nodejs/node_modules/bmad-mcp/dist/index.js'],
    timeout: 5000
  },
  {
    name: 'firecrawl-local',
    command: 'node',
    args: ['./.kilocode/mcp-servers/mcp-wrapper.js', 'firecrawl'],
    timeout: 5000
  },
  {
    name: 'playwright-mcp',
    command: 'node',
    args: ['C:/nvm4w/nodejs/node_modules/@playwright/mcp/cli.js'],
    timeout: 5000
  }
];

let passed = 0;
let failed = 0;

console.log('🔍 MCP Server Verification Script');
console.log('==================================\n');

async function testServer(server) {
  return new Promise((resolve) => {
    console.log(`Testing ${server.name}...`);
    
    // Check if command file exists
    const commandPath = server.args[0];
    if (!fs.existsSync(commandPath)) {
      console.log(`❌ ${server.name}: Command file not found: ${commandPath}`);
      failed++;
      resolve(false);
      return;
    }

    const child = spawn(server.command, server.args, {
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: server.timeout
    });

    let output = '';
    let errorOutput = '';

    child.stdout.on('data', (data) => {
      output += data.toString();
    });

    child.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    const timeout = setTimeout(() => {
      child.kill();
      console.log(`❌ ${server.name}: Timeout after ${server.timeout}ms`);
      failed++;
      resolve(false);
    }, server.timeout);

    child.on('close', (code) => {
      clearTimeout(timeout);
      
      if (code === 0) {
        console.log(`✅ ${server.name}: OK`);
        passed++;
        resolve(true);
      } else {
        console.log(`❌ ${server.name}: Failed with code ${code}`);
        if (errorOutput) {
          console.log(`   Error: ${errorOutput.trim()}`);
        }
        failed++;
        resolve(false);
      }
    });

    child.on('error', (err) => {
      clearTimeout(timeout);
      console.log(`❌ ${server.name}: Error: ${err.message}`);
      failed++;
      resolve(false);
    });
  });
}

async function runTests() {
  console.log('Testing MCP server path resolution...\n');
  
  for (const server of mcpServers) {
    await testServer(server);
  }

  console.log('\n==================================');
  console.log('📊 Test Results');
  console.log('==================================');
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📈 Success Rate: ${Math.round((passed / (passed + failed)) * 100)}%`);
  
  if (failed === 0) {
    console.log('\n🎉 All MCP servers are working correctly!');
    console.log('The hardcoded path issues have been resolved.');
  } else {
    console.log('\n⚠️  Some MCP servers are still failing.');
    console.log('Please check the error messages above.');
  }
}

// Run the tests
runTests().catch(console.error);
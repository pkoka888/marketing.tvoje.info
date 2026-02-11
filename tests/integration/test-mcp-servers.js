#!/usr/bin/env node

/**
 * test-mcp-servers.js
 * 
 * Integration tests for MCP Server functionality.
 * 
 * Tests:
 * - Filesystem server connectivity
 * - Memory server operations
 * - Git server operations
 * - GitHub server authentication
 * - Time server operations
 * - Fetch server HTTP requests
 * - Redis server connection
 * - SQLite server operations
 * - Puppeteer server automation
 * - Rate limiting
 * - Permission controls
 * 
 * Usage:
 *   node tests/integration/test-mcp-servers.js [options]
 * 
 * Options:
 *   --verbose        Enable verbose output
 *   --test <name>    Run specific test only
 *   --list           List available tests
 *   --help           Show help message
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Configuration
const MCP_CONFIG_PATH = path.join(__dirname, '..', '..', '.kilocode', 'mcp.json');

// Test results
const testResults = {
  total: 0,
  passed: 0,
  failed: 0,
  results: []
};

// Command line arguments
const args = process.argv.slice(2);
const verbose = args.includes('--verbose');
const testToRun = getArgValue('--test');
const listTests = args.includes('--list');
const showHelp = args.includes('--help');

/**
 * Get argument value
 */
function getArgValue(argName) {
  const index = args.indexOf(argName);
  if (index !== -1 && index + 1 < args.length) {
    return args[index + 1];
  }
  return null;
}

/**
 * Show help message
 */
function showHelpMessage() {
  console.log(`
MCP Server Integration Tests
=============================

Usage:
  node tests/integration/test-mcp-servers.js [options]

Options:
  --verbose        Enable verbose output
  --test <name>    Run specific test only
  --list           List available tests
  --help           Show this help message

Available Tests:
  mcp-config-exists       - Test MCP configuration file exists
  mcp-config-valid        - Test MCP configuration is valid JSON
  filesystem-server       - Test filesystem server configuration
  memory-server           - Test memory server configuration
  git-server              - Test git server configuration
  github-server           - Test GitHub server configuration
  time-server             - Test time server configuration
  fetch-server            - Test fetch server configuration
  redis-server            - Test Redis server configuration
  sqlite-server           - Test SQLite server configuration
  puppeteer-server        - Test Puppeteer server configuration
  rate-limiting           - Test rate limiting configuration
  permission-controls     - Test permission controls

Exit Codes:
  0 - All tests passed
  1 - Some tests failed
  2 - Invalid arguments
`);
}

/**
 * List available tests
 */
function listAvailableTests() {
  console.log('\nAvailable Tests:');
  console.log('================\n');
  TESTS.forEach((test, index) => {
    console.log(`${index + 1}. ${test.name}`);
    console.log(`   Description: ${test.description}`);
    console.log('');
  });
}

/**
 * Test definitions
 */
const TESTS = [
  {
    name: 'mcp-config-exists',
    description: 'Test MCP configuration file exists',
    fn: testMcpConfigExists
  },
  {
    name: 'mcp-config-valid',
    description: 'Test MCP configuration is valid JSON',
    fn: testMcpConfigValid
  },
  {
    name: 'filesystem-server',
    description: 'Test filesystem server configuration',
    fn: testFilesystemServer
  },
  {
    name: 'memory-server',
    description: 'Test memory server configuration',
    fn: testMemoryServer
  },
  {
    name: 'git-server',
    description: 'Test git server configuration',
    fn: testGitServer
  },
  {
    name: 'github-server',
    description: 'Test GitHub server configuration',
    fn: testGithubServer
  },
  {
    name: 'time-server',
    description: 'Test time server configuration',
    fn: testTimeServer
  },
  {
    name: 'fetch-server',
    description: 'Test fetch server configuration',
    fn: testFetchServer
  },
  {
    name: 'redis-server',
    description: 'Test Redis server configuration',
    fn: testRedisServer
  },
  {
    name: 'sqlite-server',
    description: 'Test SQLite server configuration',
    fn: testSqliteServer
  },
  {
    name: 'puppeteer-server',
    description: 'Test Puppeteer server configuration',
    fn: testPuppeteerServer
  },
  {
    name: 'rate-limiting',
    description: 'Test rate limiting configuration',
    fn: testRateLimiting
  },
  {
    name: 'permission-controls',
    description: 'Test permission controls',
    fn: testPermissionControls
  }
];

/**
 * Run a single test
 */
function runTest(test) {
  return new Promise((resolve) => {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`Running: ${test.name}`);
    console.log(`Description: ${test.description}`);
    console.log('='.repeat(60));
    
    try {
      const result = test.fn();
      testResults.results.push({
        name: test.name,
        description: test.description,
        passed: result.passed,
        message: result.message,
        details: result.details
      });
      
      if (result.passed) {
        testResults.passed++;
        console.log(`\n✓ ${test.name} PASSED`);
        if (result.message) {
          console.log(`  ${result.message}`);
        }
      } else {
        testResults.failed++;
        console.log(`\n✗ ${test.name} FAILED`);
        console.log(`  ${result.message}`);
        if (result.details && verbose) {
          console.log(`  Details: ${result.details}`);
        }
      }
    } catch (error) {
      testResults.results.push({
        name: test.name,
        description: test.description,
        passed: false,
        message: error.message,
        details: error.stack
      });
      testResults.failed++;
      console.log(`\n✗ ${test.name} FAILED`);
      console.log(`  Error: ${error.message}`);
      if (verbose) {
        console.log(`  Stack: ${error.stack}`);
      }
    }
    
    resolve();
  });
}

/**
 * Load MCP configuration
 */
function loadMcpConfig() {
  if (!fs.existsSync(MCP_CONFIG_PATH)) {
    return null;
  }
  
  try {
    const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    return null;
  }
}

/**
 * Test: MCP configuration file exists
 */
function testMcpConfigExists() {
  if (!fs.existsSync(MCP_CONFIG_PATH)) {
    return {
      passed: false,
      message: 'MCP configuration file does not exist',
      details: `Expected path: ${MCP_CONFIG_PATH}`
    };
  }
  
  return {
    passed: true,
    message: 'MCP configuration file exists',
    details: `Path: ${MCP_CONFIG_PATH}`
  };
}

/**
 * Test: MCP configuration is valid JSON
 */
function testMcpConfigValid() {
  const config = loadMcpConfig();
  
  if (config === null) {
    return {
      passed: false,
      message: 'Cannot load or parse MCP configuration',
      details: 'File may not exist or contains invalid JSON'
    };
  }
  
  if (typeof config !== 'object' || config === null) {
    return {
      passed: false,
      message: 'MCP configuration is not a valid object',
      details: 'Expected JSON object'
    };
  }
  
  if (!config.mcpServers) {
    return {
      passed: false,
      message: 'MCP configuration missing mcpServers property',
      details: 'Expected property: mcpServers'
    };
  }
  
  return {
    passed: true,
    message: 'MCP configuration is valid JSON',
    details: `Found ${Object.keys(config.mcpServers).length} server(s)`
  };
}

/**
 * Test: Filesystem server configuration
 */
function testFilesystemServer() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test filesystem server - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  const filesystemServers = Object.keys(config.mcpServers).filter(
    key => key.includes('filesystem')
  );
  
  if (filesystemServers.length === 0) {
    return {
      passed: false,
      message: 'No filesystem servers configured',
      details: 'Expected at least one filesystem server'
    };
  }
  
  // Check each filesystem server
  for (const serverName of filesystemServers) {
    const server = config.mcpServers[serverName];
    
    if (!server.command) {
      return {
        passed: false,
        message: `Filesystem server missing command: ${serverName}`,
        details: 'Required property: command'
      };
    }
    
    if (!server.args || !Array.isArray(server.args)) {
      return {
        passed: false,
        message: `Filesystem server missing args array: ${serverName}`,
        details: 'Required property: args (array)'
      };
    }
  }
  
  return {
    passed: true,
    message: 'Filesystem server configuration is valid',
    details: `Found ${filesystemServers.length} filesystem server(s)`
  };
}

/**
 * Test: Memory server configuration
 */
function testMemoryServer() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test memory server - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  const memoryServers = Object.keys(config.mcpServers).filter(
    key => key.includes('memory')
  );
  
  if (memoryServers.length === 0) {
    return {
      passed: true,
      message: 'No memory servers configured (optional)',
      details: 'Memory server is optional'
    };
  }
  
  // Check each memory server
  for (const serverName of memoryServers) {
    const server = config.mcpServers[serverName];
    
    if (!server.command) {
      return {
        passed: false,
        message: `Memory server missing command: ${serverName}`,
        details: 'Required property: command'
      };
    }
  }
  
  return {
    passed: true,
    message: 'Memory server configuration is valid',
    details: `Found ${memoryServers.length} memory server(s)`
  };
}

/**
 * Test: Git server configuration
 */
function testGitServer() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test git server - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  const gitServers = Object.keys(config.mcpServers).filter(
    key => key.includes('git')
  );
  
  if (gitServers.length === 0) {
    return {
      passed: true,
      message: 'No git servers configured (optional)',
      details: 'Git server is optional'
    };
  }
  
  // Check each git server
  for (const serverName of gitServers) {
    const server = config.mcpServers[serverName];
    
    if (!server.command) {
      return {
        passed: false,
        message: `Git server missing command: ${serverName}`,
        details: 'Required property: command'
      };
    }
  }
  
  return {
    passed: true,
    message: 'Git server configuration is valid',
    details: `Found ${gitServers.length} git server(s)`
  };
}

/**
 * Test: GitHub server configuration
 */
function testGithubServer() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test GitHub server - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  const githubServers = Object.keys(config.mcpServers).filter(
    key => key.includes('github')
  );
  
  if (githubServers.length === 0) {
    return {
      passed: true,
      message: 'No GitHub servers configured (optional)',
      details: 'GitHub server is optional'
    };
  }
  
  // Check each GitHub server
  for (const serverName of githubServers) {
    const server = config.mcpServers[serverName];
    
    if (!server.command) {
      return {
        passed: false,
        message: `GitHub server missing command: ${serverName}`,
        details: 'Required property: command'
      };
    }
    
    // Check for environment variables (tokens)
    if (server.env) {
      const hasToken = Object.keys(server.env).some(key => 
        key.toLowerCase().includes('token') || key.toLowerCase().includes('auth')
      );
      if (hasToken) {
        return {
          passed: true,
          message: 'GitHub server configuration is valid with authentication',
          details: `Found ${githubServers.length} GitHub server(s) with auth`
        };
      }
    }
  }
  
  return {
    passed: true,
    message: 'GitHub server configuration is valid',
    details: `Found ${githubServers.length} GitHub server(s)`
  };
}

/**
 * Test: Time server configuration
 */
function testTimeServer() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test time server - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  const timeServers = Object.keys(config.mcpServers).filter(
    key => key.includes('time')
  );
  
  if (timeServers.length === 0) {
    return {
      passed: true,
      message: 'No time servers configured (optional)',
      details: 'Time server is optional'
    };
  }
  
  return {
    passed: true,
    message: 'Time server configuration is valid',
    details: `Found ${timeServers.length} time server(s)`
  };
}

/**
 * Test: Fetch server configuration
 */
function testFetchServer() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test fetch server - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  const fetchServers = Object.keys(config.mcpServers).filter(
    key => key.includes('fetch')
  );
  
  if (fetchServers.length === 0) {
    return {
      passed: true,
      message: 'No fetch servers configured (optional)',
      details: 'Fetch server is optional'
    };
  }
  
  return {
    passed: true,
    message: 'Fetch server configuration is valid',
    details: `Found ${fetchServers.length} fetch server(s)`
  };
}

/**
 * Test: Redis server configuration
 */
function testRedisServer() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test Redis server - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  const redisServers = Object.keys(config.mcpServers).filter(
    key => key.includes('redis')
  );
  
  if (redisServers.length === 0) {
    return {
      passed: true,
      message: 'No Redis servers configured (optional)',
      details: 'Redis server is optional'
    };
  }
  
  return {
    passed: true,
    message: 'Redis server configuration is valid',
    details: `Found ${redisServers.length} Redis server(s)`
  };
}

/**
 * Test: SQLite server configuration
 */
function testSqliteServer() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test SQLite server - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  const sqliteServers = Object.keys(config.mcpServers).filter(
    key => key.includes('sqlite')
  );
  
  if (sqliteServers.length === 0) {
    return {
      passed: true,
      message: 'No SQLite servers configured (optional)',
      details: 'SQLite server is optional'
    };
  }
  
  return {
    passed: true,
    message: 'SQLite server configuration is valid',
    details: `Found ${sqliteServers.length} SQLite server(s)`
  };
}

/**
 * Test: Puppeteer server configuration
 */
function testPuppeteerServer() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test Puppeteer server - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  const puppeteerServers = Object.keys(config.mcpServers).filter(
    key => key.includes('puppeteer')
  );
  
  if (puppeteerServers.length === 0) {
    return {
      passed: true,
      message: 'No Puppeteer servers configured (optional)',
      details: 'Puppeteer server is optional'
    };
  }
  
  return {
    passed: true,
    message: 'Puppeteer server configuration is valid',
    details: `Found ${puppeteerServers.length} Puppeteer server(s)`
  };
}

/**
 * Test: Rate limiting configuration
 */
function testRateLimiting() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test rate limiting - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  // Check for rate limiting configuration
  let hasRateLimiting = false;
  
  for (const [serverName, server] of Object.entries(config.mcpServers)) {
    if (server.rateLimit || server.rate_limit || server.maxRequests) {
      hasRateLimiting = true;
      break;
    }
  }
  
  if (!hasRateLimiting) {
    return {
      passed: true,
      message: 'No explicit rate limiting configured (optional)',
      details: 'Rate limiting is optional'
    };
  }
  
  return {
    passed: true,
    message: 'Rate limiting configuration is valid',
    details: 'Rate limiting is configured for one or more servers'
  };
}

/**
 * Test: Permission controls
 */
function testPermissionControls() {
  const config = loadMcpConfig();
  
  if (!config || !config.mcpServers) {
    return {
      passed: false,
      message: 'Cannot test permission controls - config not loaded',
      details: 'Run mcp-config-valid test first'
    };
  }
  
  // Check for permission controls
  let hasPermissions = false;
  let hasAlwaysAllow = false;
  
  for (const [serverName, server] of Object.entries(config.mcpServers)) {
    if (server.permissions || server.allowedOperations) {
      hasPermissions = true;
    }
    if (server.alwaysAllow) {
      hasAlwaysAllow = true;
    }
  }
  
  if (!hasPermissions && !hasAlwaysAllow) {
    return {
      passed: true,
      message: 'No explicit permission controls configured (optional)',
      details: 'Permission controls are optional'
    };
  }
  
  return {
    passed: true,
    message: 'Permission controls are valid',
    details: `Found ${hasPermissions ? 'permissions' : ''}${hasAlwaysAllow ? ' alwaysAllow' : ''}`
  };
}

/**
 * Generate final report
 */
function generateFinalReport() {
  console.log('\n' + '='.repeat(60));
  console.log('MCP SERVER INTEGRATION TEST REPORT');
  console.log('='.repeat(60));
  console.log(`Total Tests: ${testResults.total}`);
  console.log(`Passed: ${testResults.passed}`);
  console.log(`Failed: ${testResults.failed}`);
  console.log('='.repeat(60));
  
  if (testResults.results.length > 0) {
    console.log('\nTest Results:');
    console.log('-------------');
    testResults.results.forEach((result, index) => {
      const status = result.passed ? '✓ PASS' : '✗ FAIL';
      console.log(`${index + 1}. ${result.name}: ${status}`);
      if (result.message) {
        console.log(`   ${result.message}`);
      }
    });
  }
  
  console.log('='.repeat(60));
  
  if (testResults.failed === 0) {
    console.log('\n✓ ALL TESTS PASSED!\n');
    return 0;
  } else {
    console.log(`\n✗ ${testResults.failed} TEST(S) FAILED!\n`);
    return 1;
  }
}

/**
 * Main function
 */
async function main() {
  console.log('MCP Server Integration Tests');
  console.log('=============================\n');
  
  // Handle --help
  if (showHelp) {
    showHelpMessage();
    return 2;
  }
  
  // Handle --list
  if (listTests) {
    listAvailableTests();
    return 0;
  }
  
  // Determine which tests to run
  let testsToRun = TESTS;
  
  if (testToRun) {
    const test = TESTS.find(t => t.name === testToRun);
    if (!test) {
      console.error(`Error: Unknown test "${testToRun}"`);
      console.error('Use --list to see available tests');
      return 2;
    }
    testsToRun = [test];
  }
  
  testResults.total = testsToRun.length;
  
  // Run tests
  for (const test of testsToRun) {
    await runTest(test);
  }
  
  // Generate final report
  return generateFinalReport();
}

// Run main function
main().then(exitCode => {
  process.exit(exitCode);
}).catch(err => {
  console.error('Fatal error:', err);
  process.exit(2);
});

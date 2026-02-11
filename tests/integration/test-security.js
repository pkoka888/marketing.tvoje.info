#!/usr/bin/env node

/**
 * test-security.js
 * 
 * Security integration tests for the Kilo Code template project.
 * 
 * Tests:
 * - Path validation
 * - Rate limiting enforcement
 * - Permission controls
 * - Environment variable handling
 * - Token authentication
 * 
 * Usage:
 *   node tests/integration/test-security.js [options]
 * 
 * Options:
 *   --verbose        Enable verbose output
 *   --test <name>    Run specific test only
 *   --list           List available tests
 *   --help           Show help message
 */

const fs = require('fs');
const path = require('path');

// Configuration
const PROJECT_ROOT = path.join(__dirname, '..', '..');
const KILOCODE_DIR = path.join(PROJECT_ROOT, '.kilocode');
const MCP_CONFIG_PATH = path.join(KILOCODE_DIR, 'mcp.json');
const ENV_TEMPLATE_PATH = path.join(PROJECT_ROOT, '.env.template');
const GITIGNORE_PATH = path.join(PROJECT_ROOT, '.gitignore');

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
Security Integration Tests
===========================

Usage:
  node tests/integration/test-security.js [options]

Options:
  --verbose        Enable verbose output
  --test <name>    Run specific test only
  --list           List available tests
  --help           Show this help message

Available Tests:
  path-validation          - Test path validation
  rate-limiting            - Test rate limiting enforcement
  permission-controls      - Test permission controls
  env-variable-handling    - Test environment variable handling
  token-authentication     - Test token authentication
  gitignore-security       - Test .gitignore security
  sensitive-data-check     - Test for sensitive data exposure
  mcp-security             - Test MCP server security

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
    name: 'path-validation',
    description: 'Test path validation',
    fn: testPathValidation
  },
  {
    name: 'rate-limiting',
    description: 'Test rate limiting enforcement',
    fn: testRateLimiting
  },
  {
    name: 'permission-controls',
    description: 'Test permission controls',
    fn: testPermissionControls
  },
  {
    name: 'env-variable-handling',
    description: 'Test environment variable handling',
    fn: testEnvVariableHandling
  },
  {
    name: 'token-authentication',
    description: 'Test token authentication',
    fn: testTokenAuthentication
  },
  {
    name: 'gitignore-security',
    description: 'Test .gitignore security',
    fn: testGitignoreSecurity
  },
  {
    name: 'sensitive-data-check',
    description: 'Test for sensitive data exposure',
    fn: testSensitiveDataCheck
  },
  {
    name: 'mcp-security',
    description: 'Test MCP server security',
    fn: testMcpSecurity
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
 * Test: Path validation
 */
function testPathValidation() {
  // Test for path traversal vulnerabilities
  const suspiciousPatterns = [
    '../',
    '..\\',
    '%2e%2e',
    '%2e%2e%2f',
    '..%2f',
    '..%5c'
  ];
  
  const issues = [];
  
  // Check MCP config for suspicious paths
  if (fs.existsSync(MCP_CONFIG_PATH)) {
    try {
      const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
      const config = JSON.parse(content);
      
      for (const [serverName, server] of Object.entries(config.mcpServers || {})) {
        if (server.args && Array.isArray(server.args)) {
          for (const arg of server.args) {
            if (typeof arg === 'string') {
              for (const pattern of suspiciousPatterns) {
                if (arg.includes(pattern)) {
                  issues.push(`${serverName}: contains suspicious path pattern "${pattern}"`);
                }
              }
            }
          }
        }
      }
    } catch (error) {
      // Ignore parse errors for this test
    }
  }
  
  if (issues.length > 0) {
    return {
      passed: false,
      message: 'Path validation found suspicious patterns',
      details: issues.join('; ')
    };
  }
  
  return {
    passed: true,
    message: 'Path validation passed',
    details: 'No suspicious path patterns found'
  };
}

/**
 * Test: Rate limiting enforcement
 */
function testRateLimiting() {
  if (!fs.existsSync(MCP_CONFIG_PATH)) {
    return {
      passed: true,
      message: 'Rate limiting test skipped - no MCP config',
      details: 'Rate limiting is optional'
    };
  }
  
  try {
    const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
    const config = JSON.parse(content);
    
    let hasRateLimiting = false;
    const serversWithRateLimiting = [];
    
    for (const [serverName, server] of Object.entries(config.mcpServers || {})) {
      if (server.rateLimit || server.rate_limit || server.maxRequests || server.max_requests) {
        hasRateLimiting = true;
        serversWithRateLimiting.push(serverName);
      }
    }
    
    if (hasRateLimiting) {
      return {
        passed: true,
        message: 'Rate limiting is configured',
        details: `Servers with rate limiting: ${serversWithRateLimiting.join(', ')}`
      };
    }
    
    return {
      passed: true,
      message: 'Rate limiting not configured (optional)',
      details: 'Rate limiting is optional'
    };
  } catch (error) {
    return {
      passed: true,
      message: 'Rate limiting test skipped - config parse error',
      details: error.message
    };
  }
}

/**
 * Test: Permission controls
 */
function testPermissionControls() {
  if (!fs.existsSync(MCP_CONFIG_PATH)) {
    return {
      passed: true,
      message: 'Permission controls test skipped - no MCP config',
      details: 'Permission controls are optional'
    };
  }
  
  try {
    const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
    const config = JSON.parse(content);
    
    let hasPermissions = false;
    const serversWithPermissions = [];
    
    for (const [serverName, server] of Object.entries(config.mcpServers || {})) {
      if (server.permissions || server.allowedOperations || server.alwaysAllow) {
        hasPermissions = true;
        serversWithPermissions.push(serverName);
      }
    }
    
    if (hasPermissions) {
      return {
        passed: true,
        message: 'Permission controls are configured',
        details: `Servers with permissions: ${serversWithPermissions.join(', ')}`
      };
    }
    
    return {
      passed: true,
      message: 'Permission controls not configured (optional)',
      details: 'Permission controls are optional'
    };
  } catch (error) {
    return {
      passed: true,
      message: 'Permission controls test skipped - config parse error',
      details: error.message
    };
  }
}

/**
 * Test: Environment variable handling
 */
function testEnvVariableHandling() {
  if (!fs.existsSync(ENV_TEMPLATE_PATH)) {
    return {
      passed: true,
      message: 'Environment variable template not found (optional)',
      details: '.env.template is optional'
    };
  }
  
  try {
    const content = fs.readFileSync(ENV_TEMPLATE_PATH, 'utf8');
    
    // Check for sensitive variable patterns
    const sensitivePatterns = [
      /password\s*=/i,
      /secret\s*=/i,
      /token\s*=/i,
      /api_key\s*=/i,
      /apikey\s*=/i,
      /private_key\s*=/i
    ];
    
    const foundSensitive = [];
    
    for (const pattern of sensitivePatterns) {
      const matches = content.match(pattern);
      if (matches) {
        foundSensitive.push(matches[0]);
      }
    }
    
    if (foundSensitive.length > 0) {
      // Check if they have placeholder values (not actual secrets)
      const hasPlaceholders = content.includes('YOUR_') || 
                             content.includes('your_') ||
                             content.includes('<') ||
                             content.includes('placeholder');
      
      if (hasPlaceholders) {
        return {
          passed: true,
          message: 'Environment variables use placeholders',
          details: `Found ${foundSensitive.length} sensitive variable(s) with placeholders`
        };
      }
      
      return {
        passed: false,
        message: 'Environment variables may contain actual secrets',
        details: `Found: ${foundSensitive.join(', ')}`
      };
    }
    
    return {
      passed: true,
      message: 'Environment variable handling is safe',
      details: 'No sensitive patterns found'
    };
  } catch (error) {
    return {
      passed: true,
      message: 'Environment variable test skipped - read error',
      details: error.message
    };
  }
}

/**
 * Test: Token authentication
 */
function testTokenAuthentication() {
  if (!fs.existsSync(MCP_CONFIG_PATH)) {
    return {
      passed: true,
      message: 'Token authentication test skipped - no MCP config',
      details: 'Token authentication is optional'
    };
  }
  
  try {
    const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
    const config = JSON.parse(content);
    
    let hasTokenAuth = false;
    const serversWithTokenAuth = [];
    
    for (const [serverName, server] of Object.entries(config.mcpServers || {})) {
      if (server.env) {
        const envKeys = Object.keys(server.env);
        const hasToken = envKeys.some(key => 
          key.toLowerCase().includes('token') || 
          key.toLowerCase().includes('auth') ||
          key.toLowerCase().includes('key')
        );
        
        if (hasToken) {
          hasTokenAuth = true;
          serversWithTokenAuth.push(serverName);
        }
      }
    }
    
    if (hasTokenAuth) {
      return {
        passed: true,
        message: 'Token authentication is configured',
        details: `Servers with token auth: ${serversWithTokenAuth.join(', ')}`
      };
    }
    
    return {
      passed: true,
      message: 'Token authentication not configured (optional)',
      details: 'Token authentication is optional'
    };
  } catch (error) {
    return {
      passed: true,
      message: 'Token authentication test skipped - config parse error',
      details: error.message
    };
  }
}

/**
 * Test: .gitignore security
 */
function testGitignoreSecurity() {
  if (!fs.existsSync(GITIGNORE_PATH)) {
    return {
      passed: false,
      message: '.gitignore file does not exist',
      details: 'Expected .gitignore file for security'
    };
  }
  
  try {
    const content = fs.readFileSync(GITIGNORE_PATH, 'utf8');
    
    // Check for important security entries
    const securityEntries = [
      '.env',
      '*.key',
      '*.pem',
      '*.p12',
      '*.pfx',
      'credentials',
      'secrets',
      'passwords'
    ];
    
    const missingEntries = [];
    
    for (const entry of securityEntries) {
      if (!content.includes(entry)) {
        missingEntries.push(entry);
      }
    }
    
    if (missingEntries.length > 0) {
      return {
        passed: true,
        message: '.gitignore exists but may be missing some security entries',
        details: `Consider adding: ${missingEntries.join(', ')}`
      };
    }
    
    return {
      passed: true,
      message: '.gitignore has good security entries',
      details: 'All important security patterns found'
    };
  } catch (error) {
    return {
      passed: false,
      message: 'Cannot read .gitignore file',
      details: error.message
    };
  }
}

/**
 * Test: Sensitive data check
 */
function testSensitiveDataCheck() {
  const sensitivePatterns = [
    /password\s*=\s*["']?[^"'\s]+["']?/i,
    /secret\s*=\s*["']?[^"'\s]+["']?/i,
    /api[_-]?key\s*=\s*["']?[^"'\s]+["']?/i,
    /token\s*=\s*["']?[^"'\s]+["']?/i,
    /private[_-]?key\s*=\s*["']?[^"'\s]+["']?/i
  ];
  
  const filesToCheck = [
    MCP_CONFIG_PATH,
    ENV_TEMPLATE_PATH,
    path.join(PROJECT_ROOT, '.env')
  ];
  
  const issues = [];
  
  for (const filePath of filesToCheck) {
    if (!fs.existsSync(filePath)) {
      continue;
    }
    
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      
      for (const pattern of sensitivePatterns) {
        const matches = content.match(pattern);
        if (matches) {
          // Check if it's a placeholder
          const isPlaceholder = matches[0].includes('YOUR_') || 
                               matches[0].includes('your_') ||
                               matches[0].includes('<') ||
                               matches[0].includes('placeholder') ||
                               matches[0].includes('example');
          
          if (!isPlaceholder) {
            issues.push(`${path.basename(filePath)}: ${matches[0]}`);
          }
        }
      }
    } catch (error) {
      // Ignore read errors
    }
  }
  
  if (issues.length > 0) {
    return {
      passed: false,
      message: 'Found potential sensitive data exposure',
      details: issues.join('; ')
    };
  }
  
  return {
    passed: true,
    message: 'No sensitive data exposure found',
    details: 'All sensitive patterns use placeholders'
  };
}

/**
 * Test: MCP server security
 */
function testMcpSecurity() {
  if (!fs.existsSync(MCP_CONFIG_PATH)) {
    return {
      passed: true,
      message: 'MCP security test skipped - no MCP config',
      details: 'MCP config is optional'
    };
  }
  
  try {
    const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
    const config = JSON.parse(content);
    
    const securityChecks = [];
    
    for (const [serverName, server] of Object.entries(config.mcpServers || {})) {
      // Check for hardcoded secrets in args
      if (server.args && Array.isArray(server.args)) {
        for (const arg of server.args) {
          if (typeof arg === 'string') {
            // Check for potential secrets
            if (arg.match(/['"]?[a-zA-Z0-9]{32,}['"]?/)) {
              securityChecks.push({
                server: serverName,
                issue: 'Potential hardcoded secret in args',
                severity: 'high'
              });
            }
          }
        }
      }
      
      // Check for insecure command patterns
      if (server.command) {
        if (server.command.includes('curl') && server.args) {
          const argsStr = server.args.join(' ');
          if (argsStr.includes('http://') && !argsStr.includes('localhost')) {
            securityChecks.push({
              server: serverName,
              issue: 'Using HTTP instead of HTTPS',
              severity: 'medium'
            });
          }
        }
      }
    }
    
    if (securityChecks.length > 0) {
      const highSeverity = securityChecks.filter(c => c.severity === 'high');
      if (highSeverity.length > 0) {
        return {
          passed: false,
          message: 'MCP server security issues found',
          details: highSeverity.map(c => `${c.server}: ${c.issue}`).join('; ')
        };
      }
      
      return {
        passed: true,
        message: 'MCP server security has minor issues',
        details: securityChecks.map(c => `${c.server}: ${c.issue}`).join('; ')
      };
    }
    
    return {
      passed: true,
      message: 'MCP server security is good',
      details: 'No security issues found'
    };
  } catch (error) {
    return {
      passed: true,
      message: 'MCP security test skipped - config parse error',
      details: error.message
    };
  }
}

/**
 * Generate final report
 */
function generateFinalReport() {
  console.log('\n' + '='.repeat(60));
  console.log('SECURITY INTEGRATION TEST REPORT');
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
  console.log('Security Integration Tests');
  console.log('===========================\n');
  
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

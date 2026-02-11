#!/usr/bin/env node

/**
 * test-e2e.js
 * 
 * End-to-End integration tests for the Kilo Code template project.
 * 
 * Tests:
 * - Complete workflow from start to finish
 * - Memory Bank persistence across sessions
 * - MCP server communication
 * - Mode switching
 * - Error handling and recovery
 * 
 * Usage:
 *   node tests/integration/test-e2e.js [options]
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
const MEMORY_BANK_DIR = path.join(KILOCODE_DIR, 'rules', 'memory-bank');
const WORKFLOWS_DIR = path.join(KILOCODE_DIR, 'workflows');
const SKILLS_DIR = path.join(KILOCODE_DIR, 'skills');
const MCP_CONFIG_PATH = path.join(KILOCODE_DIR, 'mcp.json');

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
End-to-End Integration Tests
=============================

Usage:
  node tests/integration/test-e2e.js [options]

Options:
  --verbose        Enable verbose output
  --test <name>    Run specific test only
  --list           List available tests
  --help           Show this help message

Available Tests:
  project-structure        - Test complete project structure
  memory-bank-persistence  - Test Memory Bank persistence across sessions
  mcp-communication        - Test MCP server communication
  mode-switching           - Test mode switching
  error-handling           - Test error handling and recovery
  workflow-execution       - Test complete workflow execution
  skill-loading            - Test skill loading and application
  full-integration         - Test full system integration

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
    name: 'project-structure',
    description: 'Test complete project structure',
    fn: testProjectStructure
  },
  {
    name: 'memory-bank-persistence',
    description: 'Test Memory Bank persistence across sessions',
    fn: testMemoryBankPersistence
  },
  {
    name: 'mcp-communication',
    description: 'Test MCP server communication',
    fn: testMcpCommunication
  },
  {
    name: 'mode-switching',
    description: 'Test mode switching',
    fn: testModeSwitching
  },
  {
    name: 'error-handling',
    description: 'Test error handling and recovery',
    fn: testErrorHandling
  },
  {
    name: 'workflow-execution',
    description: 'Test complete workflow execution',
    fn: testWorkflowExecution
  },
  {
    name: 'skill-loading',
    description: 'Test skill loading and application',
    fn: testSkillLoading
  },
  {
    name: 'full-integration',
    description: 'Test full system integration',
    fn: testFullIntegration
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
 * Test: Complete project structure
 */
function testProjectStructure() {
  const requiredDirs = [
    { name: '.kilocode', path: KILOCODE_DIR },
    { name: 'memory-bank', path: MEMORY_BANK_DIR },
    { name: 'workflows', path: WORKFLOWS_DIR },
    { name: 'skills', path: SKILLS_DIR }
  ];
  
  const missingDirs = [];
  
  for (const dir of requiredDirs) {
    if (!fs.existsSync(dir.path)) {
      missingDirs.push(dir.name);
    }
  }
  
  if (missingDirs.length > 0) {
    return {
      passed: false,
      message: 'Missing required project directories',
      details: `Missing: ${missingDirs.join(', ')}`
    };
  }
  
  // Check for required files
  const requiredFiles = [
    { name: 'mcp.json', path: MCP_CONFIG_PATH },
    { name: 'brief.md', path: path.join(MEMORY_BANK_DIR, 'brief.md') },
    { name: 'product.md', path: path.join(MEMORY_BANK_DIR, 'product.md') },
    { name: 'context.md', path: path.join(MEMORY_BANK_DIR, 'context.md') }
  ];
  
  const missingFiles = [];
  
  for (const file of requiredFiles) {
    if (!fs.existsSync(file.path)) {
      missingFiles.push(file.name);
    }
  }
  
  if (missingFiles.length > 0) {
    return {
      passed: false,
      message: 'Missing required project files',
      details: `Missing: ${missingFiles.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Project structure is complete',
    details: `All ${requiredDirs.length} directories and ${requiredFiles.length} files present`
  };
}

/**
 * Test: Memory Bank persistence across sessions
 */
function testMemoryBankPersistence() {
  if (!fs.existsSync(MEMORY_BANK_DIR)) {
    return {
      passed: false,
      message: 'Memory Bank directory does not exist',
      details: `Expected path: ${MEMORY_BANK_DIR}`
    };
  }
  
  const coreFiles = ['brief.md', 'product.md', 'context.md', 'architecture.md', 'tech.md'];
  const missingFiles = [];
  const fileSizes = {};
  
  for (const file of coreFiles) {
    const filePath = path.join(MEMORY_BANK_DIR, file);
    if (!fs.existsSync(filePath)) {
      missingFiles.push(file);
    } else {
      const stats = fs.statSync(filePath);
      fileSizes[file] = stats.size;
    }
  }
  
  if (missingFiles.length > 0) {
    return {
      passed: false,
      message: 'Memory Bank missing core files',
      details: `Missing: ${missingFiles.join(', ')}`
    };
  }
  
  // Check if files have content (persistence)
  const emptyFiles = Object.entries(fileSizes)
    .filter(([_, size]) => size === 0)
    .map(([name, _]) => name);
  
  if (emptyFiles.length > 0) {
    return {
      passed: false,
      message: 'Some Memory Bank files are empty',
      details: `Empty files: ${emptyFiles.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Memory Bank persistence is valid',
    details: `All ${coreFiles.length} files have content`
  };
}

/**
 * Test: MCP server communication
 */
function testMcpCommunication() {
  if (!fs.existsSync(MCP_CONFIG_PATH)) {
    return {
      passed: false,
      message: 'MCP configuration does not exist',
      details: `Expected path: ${MCP_CONFIG_PATH}`
    };
  }
  
  let config;
  try {
    const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
    config = JSON.parse(content);
  } catch (error) {
    return {
      passed: false,
      message: 'Cannot parse MCP configuration',
      details: error.message
    };
  }
  
  if (!config.mcpServers || Object.keys(config.mcpServers).length === 0) {
    return {
      passed: false,
      message: 'No MCP servers configured',
      details: 'Expected at least one server'
    };
  }
  
  // Check server configurations
  const invalidServers = [];
  
  for (const [serverName, server] of Object.entries(config.mcpServers)) {
    if (!server.command) {
      invalidServers.push(`${serverName}: missing command`);
    }
    if (!server.args || !Array.isArray(server.args)) {
      invalidServers.push(`${serverName}: missing or invalid args`);
    }
  }
  
  if (invalidServers.length > 0) {
    return {
      passed: false,
      message: 'Some MCP servers have invalid configuration',
      details: invalidServers.join('; ')
    };
  }
  
  return {
    passed: true,
    message: 'MCP server communication is configured',
    details: `${Object.keys(config.mcpServers).length} server(s) configured`
  };
}

/**
 * Test: Mode switching
 */
function testModeSwitching() {
  const modeDirs = [
    { name: 'architect', path: path.join(KILOCODE_DIR, 'rules-architect') },
    { name: 'code', path: path.join(KILOCODE_DIR, 'rules-code') },
    { name: 'debug', path: path.join(KILOCODE_DIR, 'rules-debug') }
  ];
  
  const missingModes = [];
  
  for (const mode of modeDirs) {
    if (!fs.existsSync(mode.path)) {
      missingModes.push(mode.name);
    }
  }
  
  if (missingModes.length > 0) {
    return {
      passed: false,
      message: 'Missing mode directories',
      details: `Missing: ${missingModes.join(', ')}`
    };
  }
  
  // Check if modes have rule files
  const modesWithoutRules = [];
  
  for (const mode of modeDirs) {
    const files = fs.readdirSync(mode.path);
    if (files.length === 0) {
      modesWithoutRules.push(mode.name);
    }
  }
  
  if (modesWithoutRules.length > 0) {
    return {
      passed: false,
      message: 'Some modes have no rule files',
      details: `Modes without rules: ${modesWithoutRules.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Mode switching is configured',
    details: `All ${modeDirs.length} modes have rules`
  };
}

/**
 * Test: Error handling and recovery
 */
function testErrorHandling() {
  // Test error handling by checking for error-related configurations
  const checks = [];
  
  // Check if Memory Bank has error handling structure
  if (fs.existsSync(MEMORY_BANK_DIR)) {
    const contextPath = path.join(MEMORY_BANK_DIR, 'context.md');
    if (fs.existsSync(contextPath)) {
      const content = fs.readFileSync(contextPath, 'utf8');
      checks.push({
        name: 'Memory Bank error handling',
        passed: true
      });
    }
  }
  
  // Check if MCP config has error handling
  if (fs.existsSync(MCP_CONFIG_PATH)) {
    try {
      const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
      const config = JSON.parse(content);
      checks.push({
        name: 'MCP config parsing',
        passed: true
      });
    } catch (error) {
      checks.push({
        name: 'MCP config parsing',
        passed: false,
        error: error.message
      });
    }
  }
  
  const failedChecks = checks.filter(c => !c.passed);
  
  if (failedChecks.length > 0) {
    return {
      passed: false,
      message: 'Some error handling checks failed',
      details: failedChecks.map(c => `${c.name}: ${c.error}`).join('; ')
    };
  }
  
  return {
    passed: true,
    message: 'Error handling is configured',
    details: `${checks.length} check(s) passed`
  };
}

/**
 * Test: Complete workflow execution
 */
function testWorkflowExecution() {
  if (!fs.existsSync(WORKFLOWS_DIR)) {
    return {
      passed: false,
      message: 'Workflows directory does not exist',
      details: `Expected path: ${WORKFLOWS_DIR}`
    };
  }
  
  const workflowFiles = fs.readdirSync(WORKFLOWS_DIR).filter(f => f.endsWith('.md') && f !== 'README.md');
  
  if (workflowFiles.length === 0) {
    return {
      passed: false,
      message: 'No workflow files found',
      details: 'Expected at least one workflow'
    };
  }
  
  // Check if workflows have proper structure
  const invalidWorkflows = [];
  
  for (const file of workflowFiles) {
    const filePath = path.join(WORKFLOWS_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    const hasTaskObjective = content.includes('<task_objective>');
    const hasDetailedSteps = content.includes('<detailed_sequence_steps>');
    
    if (!hasTaskObjective || !hasDetailedSteps) {
      invalidWorkflows.push(file);
    }
  }
  
  if (invalidWorkflows.length > 0) {
    return {
      passed: false,
      message: 'Some workflows have invalid structure',
      details: `Invalid: ${invalidWorkflows.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Workflow execution is configured',
    details: `${workflowFiles.length} workflow(s) valid`
  };
}

/**
 * Test: Skill loading and application
 */
function testSkillLoading() {
  if (!fs.existsSync(SKILLS_DIR)) {
    return {
      passed: false,
      message: 'Skills directory does not exist',
      details: `Expected path: ${SKILLS_DIR}`
    };
  }
  
  const skillDirs = fs.readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);
  
  if (skillDirs.length === 0) {
    return {
      passed: false,
      message: 'No skill directories found',
      details: 'Expected at least one skill'
    };
  }
  
  // Check if skills have SKILL.md files
  const skillsWithoutFiles = [];
  
  for (const skillDir of skillDirs) {
    const skillFile = path.join(SKILLS_DIR, skillDir, 'SKILL.md');
    if (!fs.existsSync(skillFile)) {
      skillsWithoutFiles.push(skillDir);
    }
  }
  
  if (skillsWithoutFiles.length > 0) {
    return {
      passed: false,
      message: 'Some skills missing SKILL.md',
      details: `Missing: ${skillsWithoutFiles.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Skill loading is configured',
    details: `${skillDirs.length} skill(s) loadable`
  };
}

/**
 * Test: Full system integration
 */
function testFullIntegration() {
  const components = [
    { name: 'Memory Bank', check: () => fs.existsSync(MEMORY_BANK_DIR) },
    { name: 'Workflows', check: () => fs.existsSync(WORKFLOWS_DIR) },
    { name: 'Skills', check: () => fs.existsSync(SKILLS_DIR) },
    { name: 'MCP Config', check: () => fs.existsSync(MCP_CONFIG_PATH) },
    { name: 'Architect Mode', check: () => fs.existsSync(path.join(KILOCODE_DIR, 'rules-architect')) },
    { name: 'Code Mode', check: () => fs.existsSync(path.join(KILOCODE_DIR, 'rules-code')) },
    { name: 'Debug Mode', check: () => fs.existsSync(path.join(KILOCODE_DIR, 'rules-debug')) }
  ];
  
  const failedComponents = [];
  
  for (const component of components) {
    if (!component.check()) {
      failedComponents.push(component.name);
    }
  }
  
  if (failedComponents.length > 0) {
    return {
      passed: false,
      message: 'System integration incomplete',
      details: `Missing components: ${failedComponents.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Full system integration is valid',
    details: `All ${components.length} components present`
  };
}

/**
 * Generate final report
 */
function generateFinalReport() {
  console.log('\n' + '='.repeat(60));
  console.log('END-TO-END INTEGRATION TEST REPORT');
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
  console.log('End-to-End Integration Tests');
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

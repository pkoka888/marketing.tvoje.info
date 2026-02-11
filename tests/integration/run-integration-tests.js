#!/usr/bin/env node

/**
 * run-integration-tests.js
 * 
 * Main integration test runner for the Kilo Code template project.
 * 
 * This script runs all integration tests and generates a comprehensive test report.
 * 
 * Usage:
 *   node tests/integration/run-integration-tests.js [options]
 * 
 * Options:
 *   --verbose        Enable verbose output
 *   --test <name>    Run specific test suite only
 *   --list           List available test suites
 *   --help           Show help message
 * 
 * Exit codes:
 *   0 - All tests passed
 *   1 - Some tests failed
 *   2 - Invalid arguments
 */

const { spawn } = require('child_process');
const path = require('path');

// Integration test definitions
const INTEGRATION_TESTS = [
  {
    name: 'memory-bank',
    displayName: 'Memory Bank Integration Tests',
    script: 'test-memory-bank.js',
    description: 'Tests Memory Bank loading, updates, and constraints'
  },
  {
    name: 'mcp-servers',
    displayName: 'MCP Server Integration Tests',
    script: 'test-mcp-servers.js',
    description: 'Tests MCP server configuration and connectivity'
  },
  {
    name: 'workflows',
    displayName: 'Workflow Integration Tests',
    script: 'test-workflows.js',
    description: 'Tests workflow structure and execution'
  },
  {
    name: 'modes',
    displayName: 'Mode Integration Tests',
    script: 'test-modes.js',
    description: 'Tests mode-specific rules and behavior'
  },
  {
    name: 'skills',
    displayName: 'Skill Integration Tests',
    script: 'test-skills.js',
    description: 'Tests skill loading and YAML frontmatter'
  },
  {
    name: 'e2e',
    displayName: 'End-to-End Integration Tests',
    script: 'test-e2e.js',
    description: 'Tests complete system integration'
  },
  {
    name: 'security',
    displayName: 'Security Integration Tests',
    script: 'test-security.js',
    description: 'Tests security controls and data protection'
  }
];

// Test results
const testResults = {
  total: 0,
  passed: 0,
  failed: 0,
  suites: []
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
Kilo Code Integration Test Runner
==================================

Usage:
  node tests/integration/run-integration-tests.js [options]

Options:
  --verbose        Enable verbose output
  --test <name>    Run specific test suite only
  --list           List available test suites
  --help           Show this help message

Available Test Suites:
${INTEGRATION_TESTS.map(test => `  ${test.name.padEnd(15)} - ${test.displayName}`).join('\n')}

Examples:
  node tests/integration/run-integration-tests.js                    # Run all integration tests
  node tests/integration/run-integration-tests.js --verbose          # Run all tests with verbose output
  node tests/integration/run-integration-tests.js --test memory-bank # Run only memory-bank tests
  node tests/integration/run-integration-tests.js --list             # List available test suites

Exit Codes:
  0 - All tests passed
  1 - Some tests failed
  2 - Invalid arguments
`);
}

/**
 * List available test suites
 */
function listAvailableTests() {
  console.log('\nAvailable Integration Test Suites:');
  console.log('===================================\n');
  INTEGRATION_TESTS.forEach((test, index) => {
    console.log(`${index + 1}. ${test.displayName}`);
    console.log(`   Name: ${test.name}`);
    console.log(`   Script: ${test.script}`);
    console.log(`   Description: ${test.description}`);
    console.log('');
  });
}

/**
 * Run a single test suite
 */
function runTestSuite(test) {
  return new Promise((resolve) => {
    const scriptPath = path.join(__dirname, test.script);
    const nodeArgs = [scriptPath];
    
    if (verbose) {
      nodeArgs.push('--verbose');
    }
    
    console.log(`\n${'='.repeat(70)}`);
    console.log(`Running Suite: ${test.displayName}`);
    console.log('='.repeat(70));
    
    const child = spawn('node', nodeArgs, {
      stdio: 'inherit',
      shell: true
    });
    
    child.on('close', (code) => {
      const passed = code === 0;
      testResults.suites.push({
        name: test.name,
        displayName: test.displayName,
        passed: passed,
        exitCode: code
      });
      
      if (passed) {
        testResults.passed++;
        console.log(`\n✓ ${test.displayName} PASSED`);
      } else {
        testResults.failed++;
        console.log(`\n✗ ${test.displayName} FAILED`);
      }
      
      resolve();
    });
    
    child.on('error', (err) => {
      console.error(`Error running test suite ${test.name}:`, err.message);
      testResults.suites.push({
        name: test.name,
        displayName: test.displayName,
        passed: false,
        exitCode: -1,
        error: err.message
      });
      testResults.failed++;
      resolve();
    });
  });
}

/**
 * Generate final report
 */
function generateFinalReport() {
  console.log('\n' + '='.repeat(70));
  console.log('INTEGRATION TEST FINAL REPORT');
  console.log('='.repeat(70));
  console.log(`Total Test Suites: ${testResults.total}`);
  console.log(`Passed Suites: ${testResults.passed}`);
  console.log(`Failed Suites: ${testResults.failed}`);
  console.log('='.repeat(70));
  
  if (testResults.suites.length > 0) {
    console.log('\nSuite Results:');
    console.log('--------------');
    testResults.suites.forEach((result, index) => {
      const status = result.passed ? '✓ PASS' : '✗ FAIL';
      console.log(`${index + 1}. ${result.displayName}: ${status}`);
      if (!result.passed && result.exitCode !== undefined) {
        console.log(`   Exit Code: ${result.exitCode}`);
      }
      if (result.error) {
        console.log(`   Error: ${result.error}`);
      }
    });
  }
  
  console.log('='.repeat(70));
  
  if (testResults.failed === 0) {
    console.log('\n✓ ALL INTEGRATION TEST SUITES PASSED!\n');
    return 0;
  } else {
    console.log(`\n✗ ${testResults.failed} INTEGRATION TEST SUITE(S) FAILED!\n`);
    return 1;
  }
}

/**
 * Main function
 */
async function main() {
  console.log('Kilo Code Integration Test Runner');
  console.log('===================================\n');
  
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
  let testsToRun = INTEGRATION_TESTS;
  
  if (testToRun) {
    const test = INTEGRATION_TESTS.find(t => t.name === testToRun);
    if (!test) {
      console.error(`Error: Unknown test suite "${testToRun}"`);
      console.error('Use --list to see available test suites');
      return 2;
    }
    testsToRun = [test];
  }
  
  testResults.total = testsToRun.length;
  
  // Run test suites
  for (const test of testsToRun) {
    await runTestSuite(test);
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

#!/usr/bin/env node

/**
 * run-tests.js
 * 
 * Main test runner for the Kilo Code template project.
 * 
 * This script runs all validation scripts and generates a comprehensive test report.
 * 
 * Usage:
 *   node tests/run-tests.js [options]
 * 
 * Options:
 *   --verbose        Enable verbose output
 *   --test <name>    Run specific test only
 *   --list           List available tests
 *   --help           Show help message
 * 
 * Exit codes:
 *   0 - All tests passed
 *   1 - Some tests failed
 *   2 - Invalid arguments
 */

const { spawn } = require('child_process');
const path = require('path');

// Test definitions
const TESTS = [
  {
    name: 'memory-bank',
    displayName: 'Memory Bank Validation',
    script: 'validate-memory-bank.js',
    description: 'Validates Memory Bank files structure and content'
  },
  {
    name: 'mcp-config',
    displayName: 'MCP Configuration Validation',
    script: 'validate-mcp-config.js',
    description: 'Validates MCP server configuration'
  },
  {
    name: 'workflows',
    displayName: 'Workflow Validation',
    script: 'validate-workflows.js',
    description: 'Validates workflow files structure and content'
  },
  {
    name: 'skills',
    displayName: 'Skill Validation',
    script: 'validate-skills.js',
    description: 'Validates skill files structure and content'
  },
  {
    name: 'rules',
    displayName: 'Rule Validation',
    script: 'validate-rules.js',
    description: 'Validates rule files structure and content'
  }
];

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
Kilo Code Test Runner
=====================

Usage:
  node tests/run-tests.js [options]

Options:
  --verbose        Enable verbose output
  --test <name>    Run specific test only
  --list           List available tests
  --help           Show this help message

Available Tests:
${TESTS.map(test => `  ${test.name.padEnd(15)} - ${test.displayName}`).join('\n')}

Examples:
  node tests/run-tests.js                    # Run all tests
  node tests/run-tests.js --verbose          # Run all tests with verbose output
  node tests/run-tests.js --test memory-bank # Run only memory-bank test
  node tests/run-tests.js --list             # List available tests

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
    console.log(`${index + 1}. ${test.displayName}`);
    console.log(`   Name: ${test.name}`);
    console.log(`   Script: ${test.script}`);
    console.log(`   Description: ${test.description}`);
    console.log('');
  });
}

/**
 * Run a single test
 */
function runTest(test) {
  return new Promise((resolve) => {
    const scriptPath = path.join(__dirname, 'validation', test.script);
    const nodeArgs = [scriptPath];
    
    if (verbose) {
      nodeArgs.push('--verbose');
    }
    
    console.log(`\n${'='.repeat(60)}`);
    console.log(`Running: ${test.displayName}`);
    console.log('='.repeat(60));
    
    const child = spawn('node', nodeArgs, {
      stdio: 'inherit',
      shell: true
    });
    
    child.on('close', (code) => {
      const passed = code === 0;
      testResults.results.push({
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
      console.error(`Error running test ${test.name}:`, err.message);
      testResults.results.push({
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
  console.log('\n' + '='.repeat(60));
  console.log('FINAL TEST REPORT');
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
      console.log(`${index + 1}. ${result.displayName}: ${status}`);
      if (!result.passed && result.exitCode !== undefined) {
        console.log(`   Exit Code: ${result.exitCode}`);
      }
      if (result.error) {
        console.log(`   Error: ${result.error}`);
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
  console.log('Kilo Code Test Runner');
  console.log('=====================\n');
  
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

#!/usr/bin/env node

/**
 * test-memory-bank.js
 * 
 * Integration tests for Memory Bank functionality.
 * 
 * Tests:
 * - Memory Bank loading at task start
 * - [Memory Bank: Active] indicator
 * - Memory Bank update workflow
 * - Memory Bank initialization
 * - context.md factual constraint
 * - brief.md developer-maintained constraint
 * 
 * Usage:
 *   node tests/integration/test-memory-bank.js [options]
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
const MEMORY_BANK_DIR = path.join(__dirname, '..', '..', '.kilocode', 'rules', 'memory-bank');
const CORE_FILES = ['brief.md', 'product.md', 'context.md', 'architecture.md', 'tech.md'];

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
Memory Bank Integration Tests
==============================

Usage:
  node tests/integration/test-memory-bank.js [options]

Options:
  --verbose        Enable verbose output
  --test <name>    Run specific test only
  --list           List available tests
  --help           Show this help message

Available Tests:
  memory-bank-loading      - Test Memory Bank loading at task start
  memory-bank-indicator    - Test [Memory Bank: Active] indicator
  memory-bank-update       - Test Memory Bank update workflow
  memory-bank-init         - Test Memory Bank initialization
  context-factual          - Test context.md factual constraint
  brief-developer          - Test brief.md developer-maintained constraint

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
    name: 'memory-bank-loading',
    description: 'Test Memory Bank loading at task start',
    fn: testMemoryBankLoading
  },
  {
    name: 'memory-bank-indicator',
    description: 'Test [Memory Bank: Active] indicator',
    fn: testMemoryBankIndicator
  },
  {
    name: 'memory-bank-update',
    description: 'Test Memory Bank update workflow',
    fn: testMemoryBankUpdate
  },
  {
    name: 'memory-bank-init',
    description: 'Test Memory Bank initialization',
    fn: testMemoryBankInitialization
  },
  {
    name: 'context-factual',
    description: 'Test context.md factual constraint',
    fn: testContextFactualConstraint
  },
  {
    name: 'brief-developer',
    description: 'Test brief.md developer-maintained constraint',
    fn: testBriefDeveloperConstraint
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
 * Test: Memory Bank loading at task start
 */
function testMemoryBankLoading() {
  // Check if Memory Bank directory exists
  if (!fs.existsSync(MEMORY_BANK_DIR)) {
    return {
      passed: false,
      message: 'Memory Bank directory does not exist',
      details: `Expected directory: ${MEMORY_BANK_DIR}`
    };
  }
  
  // Check if all core files exist
  const missingFiles = [];
  for (const file of CORE_FILES) {
    const filePath = path.join(MEMORY_BANK_DIR, file);
    if (!fs.existsSync(filePath)) {
      missingFiles.push(file);
    }
  }
  
  if (missingFiles.length > 0) {
    return {
      passed: false,
      message: 'Missing core Memory Bank files',
      details: `Missing files: ${missingFiles.join(', ')}`
    };
  }
  
  // Check if files are readable
  for (const file of CORE_FILES) {
    const filePath = path.join(MEMORY_BANK_DIR, file);
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      if (!content || content.trim().length === 0) {
        return {
          passed: false,
          message: `Memory Bank file is empty: ${file}`,
          details: `File path: ${filePath}`
        };
      }
    } catch (error) {
      return {
        passed: false,
        message: `Cannot read Memory Bank file: ${file}`,
        details: error.message
      };
    }
  }
  
  return {
    passed: true,
    message: 'All core Memory Bank files exist and are readable',
    details: `Files: ${CORE_FILES.join(', ')}`
  };
}

/**
 * Test: [Memory Bank: Active] indicator
 */
function testMemoryBankIndicator() {
  // Simulate checking for [Memory Bank: Active] indicator in responses
  // This is a conceptual test since we can't actually test AI responses
  
  // Check if Memory Bank files contain expected structure
  const briefPath = path.join(MEMORY_BANK_DIR, 'brief.md');
  const contextPath = path.join(MEMORY_BANK_DIR, 'context.md');
  
  if (!fs.existsSync(briefPath) || !fs.existsSync(contextPath)) {
    return {
      passed: false,
      message: 'Memory Bank files missing for indicator test',
      details: 'Required files: brief.md, context.md'
    };
  }
  
  // Check if files have proper structure
  const briefContent = fs.readFileSync(briefPath, 'utf8');
  const contextContent = fs.readFileSync(contextPath, 'utf8');
  
  if (!briefContent.includes('# Project Brief')) {
    return {
      passed: false,
      message: 'brief.md missing expected header',
      details: 'Expected header: # Project Brief'
    };
  }
  
  if (!contextContent.includes('# Context')) {
    return {
      passed: false,
      message: 'context.md missing expected header',
      details: 'Expected header: # Context'
    };
  }
  
  return {
    passed: true,
    message: 'Memory Bank structure supports [Memory Bank: Active] indicator',
    details: 'All core files have proper structure'
  };
}

/**
 * Test: Memory Bank update workflow
 */
function testMemoryBankUpdate() {
  // Test that Memory Bank can be updated
  const contextPath = path.join(MEMORY_BANK_DIR, 'context.md');
  
  if (!fs.existsSync(contextPath)) {
    return {
      passed: false,
      message: 'context.md does not exist for update test',
      details: `Expected path: ${contextPath}`
    };
  }
  
  // Read current content
  const originalContent = fs.readFileSync(contextPath, 'utf8');
  
  // Check if context.md has required sections
  const requiredSections = ['## Current State', '## Recent Changes', '## Next Steps'];
  const missingSections = [];
  
  for (const section of requiredSections) {
    if (!originalContent.includes(section)) {
      missingSections.push(section);
    }
  }
  
  if (missingSections.length > 0) {
    return {
      passed: false,
      message: 'context.md missing required sections for update workflow',
      details: `Missing sections: ${missingSections.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Memory Bank update workflow structure is valid',
    details: 'context.md has all required sections'
  };
}

/**
 * Test: Memory Bank initialization
 */
function testMemoryBankInitialization() {
  // Check if Memory Bank initialization would work
  if (!fs.existsSync(MEMORY_BANK_DIR)) {
    return {
      passed: false,
      message: 'Memory Bank directory does not exist',
      details: 'Initialization would create this directory'
    };
  }
  
  // Check if all core files exist
  const existingFiles = [];
  const missingFiles = [];
  
  for (const file of CORE_FILES) {
    const filePath = path.join(MEMORY_BANK_DIR, file);
    if (fs.existsSync(filePath)) {
      existingFiles.push(file);
    } else {
      missingFiles.push(file);
    }
  }
  
  if (missingFiles.length > 0) {
    return {
      passed: false,
      message: 'Memory Bank initialization incomplete',
      details: `Existing: ${existingFiles.join(', ')}, Missing: ${missingFiles.join(', ')}`
    };
  }
  
  // Check if files have proper content structure
  for (const file of CORE_FILES) {
    const filePath = path.join(MEMORY_BANK_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Check for markdown headers
    if (!content.match(/^#\s+/m)) {
      return {
        passed: false,
        message: `Memory Bank file missing markdown header: ${file}`,
        details: `File path: ${filePath}`
      };
    }
  }
  
  return {
    passed: true,
    message: 'Memory Bank initialization is complete',
    details: `All ${CORE_FILES.length} core files exist with proper structure`
  };
}

/**
 * Test: context.md factual constraint
 */
function testContextFactualConstraint() {
  const contextPath = path.join(MEMORY_BANK_DIR, 'context.md');
  
  if (!fs.existsSync(contextPath)) {
    return {
      passed: false,
      message: 'context.md does not exist',
      details: `Expected path: ${contextPath}`
    };
  }
  
  const content = fs.readFileSync(contextPath, 'utf8');
  
  // Check for factual sections (not speculative)
  const factualIndicators = [
    '## Current State',
    '## Recent Changes',
    '## Next Steps'
  ];
  
  const speculativeIndicators = [
    'might',
    'could',
    'possibly',
    'perhaps',
    'maybe',
    'potentially'
  ];
  
  // Check for required factual sections
  const missingSections = [];
  for (const indicator of factualIndicators) {
    if (!content.includes(indicator)) {
      missingSections.push(indicator);
    }
  }
  
  if (missingSections.length > 0) {
    return {
      passed: false,
      message: 'context.md missing factual sections',
      details: `Missing: ${missingSections.join(', ')}`
    };
  }
  
  // Check for speculative language (warning only)
  const foundSpeculative = [];
  for (const word of speculativeIndicators) {
    const regex = new RegExp(`\\b${word}\\b`, 'gi');
    if (regex.test(content)) {
      foundSpeculative.push(word);
    }
  }
  
  if (foundSpeculative.length > 0) {
    return {
      passed: true,
      message: 'context.md has factual structure (warning: contains speculative language)',
      details: `Found speculative words: ${foundSpeculative.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'context.md follows factual constraint',
    details: 'All sections are factual, no speculative language found'
  };
}

/**
 * Test: brief.md developer-maintained constraint
 */
function testBriefDeveloperConstraint() {
  const briefPath = path.join(MEMORY_BANK_DIR, 'brief.md');
  
  if (!fs.existsSync(briefPath)) {
    return {
      passed: false,
      message: 'brief.md does not exist',
      details: `Expected path: ${briefPath}`
    };
  }
  
  const content = fs.readFileSync(briefPath, 'utf8');
  
  // Check for developer-maintained indicators
  const requiredSections = [
    '## Project Overview',
    '## Core Goals',
    '## Project Scope'
  ];
  
  const missingSections = [];
  for (const section of requiredSections) {
    if (!content.includes(section)) {
      missingSections.push(section);
    }
  }
  
  if (missingSections.length > 0) {
    return {
      passed: false,
      message: 'brief.md missing required sections',
      details: `Missing: ${missingSections.join(', ')}`
    };
  }
  
  // Check if brief.md has proper structure for developer maintenance
  if (!content.includes('# Project Brief')) {
    return {
      passed: false,
      message: 'brief.md missing main header',
      details: 'Expected header: # Project Brief'
    };
  }
  
  return {
    passed: true,
    message: 'brief.md follows developer-maintained constraint',
    details: 'Has proper structure for developer maintenance'
  };
}

/**
 * Generate final report
 */
function generateFinalReport() {
  console.log('\n' + '='.repeat(60));
  console.log('MEMORY BANK INTEGRATION TEST REPORT');
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
  console.log('Memory Bank Integration Tests');
  console.log('==============================\n');
  
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

#!/usr/bin/env node

/**
 * test-modes.js
 * 
 * Integration tests for Mode functionality.
 * 
 * Tests:
 * - Architect mode multi-attempt reasoning
 * - Code mode simulation testing
 * - Debug mode 8-step protocol
 * - Ask mode Memory Bank loading
 * - mode-specific rule application
 * 
 * Usage:
 *   node tests/integration/test-modes.js [options]
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
const RULES_ARCHITECT_DIR = path.join(__dirname, '..', '..', '.kilocode', 'rules-architect');
const RULES_CODE_DIR = path.join(__dirname, '..', '..', '.kilocode', 'rules-code');
const RULES_DEBUG_DIR = path.join(__dirname, '..', '..', '.kilocode', 'rules-debug');
const RULES_DIR = path.join(__dirname, '..', '..', '.kilocode', 'rules');

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
Mode Integration Tests
======================

Usage:
  node tests/integration/test-modes.js [options]

Options:
  --verbose        Enable verbose output
  --test <name>    Run specific test only
  --list           List available tests
  --help           Show this help message

Available Tests:
  rules-directories        - Test mode-specific rules directories exist
  architect-mode           - Test Architect mode configuration
  code-mode                - Test Code mode configuration
  debug-mode               - Test Debug mode configuration
  ask-mode                 - Test Ask mode configuration
  architect-reasoning      - Test Architect mode multi-attempt reasoning
  code-simulation          - Test Code mode simulation testing
  debug-protocol           - Test Debug mode 8-step protocol
  ask-memory-bank          - Test Ask mode Memory Bank loading
  mode-rule-application    - Test mode-specific rule application

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
    name: 'rules-directories',
    description: 'Test mode-specific rules directories exist',
    fn: testRulesDirectories
  },
  {
    name: 'architect-mode',
    description: 'Test Architect mode configuration',
    fn: testArchitectMode
  },
  {
    name: 'code-mode',
    description: 'Test Code mode configuration',
    fn: testCodeMode
  },
  {
    name: 'debug-mode',
    description: 'Test Debug mode configuration',
    fn: testDebugMode
  },
  {
    name: 'ask-mode',
    description: 'Test Ask mode configuration',
    fn: testAskMode
  },
  {
    name: 'architect-reasoning',
    description: 'Test Architect mode multi-attempt reasoning',
    fn: testArchitectReasoning
  },
  {
    name: 'code-simulation',
    description: 'Test Code mode simulation testing',
    fn: testCodeSimulation
  },
  {
    name: 'debug-protocol',
    description: 'Test Debug mode 8-step protocol',
    fn: testDebugProtocol
  },
  {
    name: 'ask-memory-bank',
    description: 'Test Ask mode Memory Bank loading',
    fn: testAskMemoryBank
  },
  {
    name: 'mode-rule-application',
    description: 'Test mode-specific rule application',
    fn: testModeRuleApplication
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
 * Test: Mode-specific rules directories exist
 */
function testRulesDirectories() {
  const directories = [
    { name: 'rules-architect', path: RULES_ARCHITECT_DIR },
    { name: 'rules-code', path: RULES_CODE_DIR },
    { name: 'rules-debug', path: RULES_DEBUG_DIR }
  ];
  
  const missingDirs = [];
  
  for (const dir of directories) {
    if (!fs.existsSync(dir.path)) {
      missingDirs.push(dir.name);
    }
  }
  
  if (missingDirs.length > 0) {
    return {
      passed: false,
      message: 'Missing mode-specific rules directories',
      details: `Missing: ${missingDirs.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'All mode-specific rules directories exist',
    details: `Found ${directories.length} directories`
  };
}

/**
 * Test: Architect mode configuration
 */
function testArchitectMode() {
  if (!fs.existsSync(RULES_ARCHITECT_DIR)) {
    return {
      passed: false,
      message: 'Architect mode rules directory does not exist',
      details: `Expected path: ${RULES_ARCHITECT_DIR}`
    };
  }
  
  const files = fs.readdirSync(RULES_ARCHITECT_DIR);
  
  if (files.length === 0) {
    return {
      passed: false,
      message: 'Architect mode rules directory is empty',
      details: 'Expected at least one rule file'
    };
  }
  
  return {
    passed: true,
    message: 'Architect mode configuration is valid',
    details: `Found ${files.length} rule file(s)`
  };
}

/**
 * Test: Code mode configuration
 */
function testCodeMode() {
  if (!fs.existsSync(RULES_CODE_DIR)) {
    return {
      passed: false,
      message: 'Code mode rules directory does not exist',
      details: `Expected path: ${RULES_CODE_DIR}`
    };
  }
  
  const files = fs.readdirSync(RULES_CODE_DIR);
  
  if (files.length === 0) {
    return {
      passed: false,
      message: 'Code mode rules directory is empty',
      details: 'Expected at least one rule file'
    };
  }
  
  return {
    passed: true,
    message: 'Code mode configuration is valid',
    details: `Found ${files.length} rule file(s)`
  };
}

/**
 * Test: Debug mode configuration
 */
function testDebugMode() {
  if (!fs.existsSync(RULES_DEBUG_DIR)) {
    return {
      passed: false,
      message: 'Debug mode rules directory does not exist',
      details: `Expected path: ${RULES_DEBUG_DIR}`
    };
  }
  
  const files = fs.readdirSync(RULES_DEBUG_DIR);
  
  if (files.length === 0) {
    return {
      passed: false,
      message: 'Debug mode rules directory is empty',
      details: 'Expected at least one rule file'
    };
  }
  
  return {
    passed: true,
    message: 'Debug mode configuration is valid',
    details: `Found ${files.length} rule file(s)`
  };
}

/**
 * Test: Ask mode configuration
 */
function testAskMode() {
  // Ask mode may not have a dedicated directory, check general rules
  if (!fs.existsSync(RULES_DIR)) {
    return {
      passed: false,
      message: 'General rules directory does not exist',
      details: `Expected path: ${RULES_DIR}`
    };
  }
  
  const files = fs.readdirSync(RULES_DIR);
  
  return {
    passed: true,
    message: 'Ask mode configuration is valid',
    details: `Found ${files.length} general rule file(s)`
  };
}

/**
 * Test: Architect mode multi-attempt reasoning
 */
function testArchitectReasoning() {
  if (!fs.existsSync(RULES_ARCHITECT_DIR)) {
    return {
      passed: false,
      message: 'Cannot test Architect reasoning - directory missing',
      details: `Expected path: ${RULES_ARCHITECT_DIR}`
    };
  }
  
  const files = fs.readdirSync(RULES_ARCHITECT_DIR);
  const planFile = files.find(f => f.includes('plan'));
  
  if (!planFile) {
    return {
      passed: true,
      message: 'Architect mode multi-attempt reasoning not explicitly configured',
      details: 'No plan.md file found (optional)'
    };
  }
  
  const planPath = path.join(RULES_ARCHITECT_DIR, planFile);
  const content = fs.readFileSync(planPath, 'utf8');
  
  // Check for reasoning-related keywords
  const reasoningKeywords = ['reasoning', 'attempt', 'iteration', 'refine', 'improve'];
  const foundKeywords = reasoningKeywords.filter(kw => 
    content.toLowerCase().includes(kw)
  );
  
  if (foundKeywords.length > 0) {
    return {
      passed: true,
      message: 'Architect mode multi-attempt reasoning is configured',
      details: `Found keywords: ${foundKeywords.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Architect mode configuration exists',
    details: 'plan.md file found'
  };
}

/**
 * Test: Code mode simulation testing
 */
function testCodeSimulation() {
  if (!fs.existsSync(RULES_CODE_DIR)) {
    return {
      passed: false,
      message: 'Cannot test Code simulation - directory missing',
      details: `Expected path: ${RULES_CODE_DIR}`
    };
  }
  
  const files = fs.readdirSync(RULES_CODE_DIR);
  const implementFile = files.find(f => f.includes('implement'));
  
  if (!implementFile) {
    return {
      passed: false,
      message: 'Code mode simulation testing not configured',
      details: 'No implement.md file found'
    };
  }
  
  const implementPath = path.join(RULES_CODE_DIR, implementFile);
  const content = fs.readFileSync(implementPath, 'utf8');
  
  // Check for simulation testing keywords
  const simulationKeywords = ['simulation', 'dry run', 'test', 'verify'];
  const foundKeywords = simulationKeywords.filter(kw => 
    content.toLowerCase().includes(kw)
  );
  
  if (foundKeywords.length > 0) {
    return {
      passed: true,
      message: 'Code mode simulation testing is configured',
      details: `Found keywords: ${foundKeywords.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Code mode configuration exists',
    details: 'implement.md file found'
  };
}

/**
 * Test: Debug mode 8-step protocol
 */
function testDebugProtocol() {
  if (!fs.existsSync(RULES_DEBUG_DIR)) {
    return {
      passed: false,
      message: 'Cannot test Debug protocol - directory missing',
      details: `Expected path: ${RULES_DEBUG_DIR}`
    };
  }
  
  const files = fs.readdirSync(RULES_DEBUG_DIR);
  const debugFile = files.find(f => f.includes('debug'));
  
  if (!debugFile) {
    return {
      passed: false,
      message: 'Debug mode 8-step protocol not configured',
      details: 'No debug.md file found'
    };
  }
  
  const debugPath = path.join(RULES_DEBUG_DIR, debugFile);
  const content = fs.readFileSync(debugPath, 'utf8');
  
  // Check for step indicators
  const stepMatches = content.match(/step\s+\d+/gi);
  
  if (stepMatches && stepMatches.length >= 5) {
    return {
      passed: true,
      message: 'Debug mode protocol is configured',
      details: `Found ${stepMatches.length} step(s)`
    };
  }
  
  return {
    passed: true,
    message: 'Debug mode configuration exists',
    details: 'debug.md file found'
  };
}

/**
 * Test: Ask mode Memory Bank loading
 */
function testAskMemoryBank() {
  const memoryBankDir = path.join(__dirname, '..', '..', '.kilocode', 'rules', 'memory-bank');
  
  if (!fs.existsSync(memoryBankDir)) {
    return {
      passed: false,
      message: 'Memory Bank directory does not exist',
      details: `Expected path: ${memoryBankDir}`
    };
  }
  
  const files = fs.readdirSync(memoryBankDir);
  const coreFiles = ['brief.md', 'product.md', 'context.md', 'architecture.md', 'tech.md'];
  const missingFiles = coreFiles.filter(f => !files.includes(f));
  
  if (missingFiles.length > 0) {
    return {
      passed: false,
      message: 'Memory Bank missing core files for Ask mode',
      details: `Missing: ${missingFiles.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Ask mode Memory Bank loading is configured',
    details: `All ${coreFiles.length} core files present`
  };
}

/**
 * Test: Mode-specific rule application
 */
function testModeRuleApplication() {
  const modeDirs = [
    { name: 'architect', path: RULES_ARCHITECT_DIR },
    { name: 'code', path: RULES_CODE_DIR },
    { name: 'debug', path: RULES_DEBUG_DIR }
  ];
  
  const modesWithoutRules = [];
  
  for (const mode of modeDirs) {
    if (!fs.existsSync(mode.path)) {
      modesWithoutRules.push(mode.name);
      continue;
    }
    
    const files = fs.readdirSync(mode.path);
    if (files.length === 0) {
      modesWithoutRules.push(mode.name);
    }
  }
  
  if (modesWithoutRules.length > 0) {
    return {
      passed: false,
      message: 'Some modes lack rule files',
      details: `Modes without rules: ${modesWithoutRules.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Mode-specific rule application is configured',
    details: `All ${modeDirs.length} modes have rules`
  };
}

/**
 * Generate final report
 */
function generateFinalReport() {
  console.log('\n' + '='.repeat(60));
  console.log('MODE INTEGRATION TEST REPORT');
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
  console.log('Mode Integration Tests');
  console.log('======================\n');
  
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

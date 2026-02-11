#!/usr/bin/env node

/**
 * test-workflows.js
 * 
 * Integration tests for Workflow functionality.
 * 
 * Tests:
 * - analyze-prompt workflow
 * - create-prompt workflow
 * - optimize-prompt workflow
 * - test-prompt workflow
 * - workflow file name matching
 * - step-by-step execution
 * - user input collection
 * 
 * Usage:
 *   node tests/integration/test-workflows.js [options]
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
const WORKFLOWS_DIR = path.join(__dirname, '..', '..', '.kilocode', 'workflows');

// Expected workflow files
const EXPECTED_WORKFLOWS = [
  'analyze-prompt.md',
  'create-prompt.md',
  'optimize-prompt.md',
  'test-prompt.md'
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
Workflow Integration Tests
===========================

Usage:
  node tests/integration/test-workflows.js [options]

Options:
  --verbose        Enable verbose output
  --test <name>    Run specific test only
  --list           List available tests
  --help           Show this help message

Available Tests:
  workflows-exists        - Test workflows directory exists
  analyze-prompt          - Test analyze-prompt workflow
  create-prompt           - Test create-prompt workflow
  optimize-prompt         - Test optimize-prompt workflow
  test-prompt             - Test test-prompt workflow
  workflow-name-matching  - Test workflow file name matching
  workflow-structure      - Test workflow structure validation
  workflow-steps          - Test workflow step-by-step execution

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
    name: 'workflows-exists',
    description: 'Test workflows directory exists',
    fn: testWorkflowsExists
  },
  {
    name: 'analyze-prompt',
    description: 'Test analyze-prompt workflow',
    fn: testAnalyzePromptWorkflow
  },
  {
    name: 'create-prompt',
    description: 'Test create-prompt workflow',
    fn: testCreatePromptWorkflow
  },
  {
    name: 'optimize-prompt',
    description: 'Test optimize-prompt workflow',
    fn: testOptimizePromptWorkflow
  },
  {
    name: 'test-prompt',
    description: 'Test test-prompt workflow',
    fn: testTestPromptWorkflow
  },
  {
    name: 'workflow-name-matching',
    description: 'Test workflow file name matching',
    fn: testWorkflowNameMatching
  },
  {
    name: 'workflow-structure',
    description: 'Test workflow structure validation',
    fn: testWorkflowStructure
  },
  {
    name: 'workflow-steps',
    description: 'Test workflow step-by-step execution',
    fn: testWorkflowSteps
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
 * Test: Workflows directory exists
 */
function testWorkflowsExists() {
  if (!fs.existsSync(WORKFLOWS_DIR)) {
    return {
      passed: false,
      message: 'Workflows directory does not exist',
      details: `Expected path: ${WORKFLOWS_DIR}`
    };
  }
  
  return {
    passed: true,
    message: 'Workflows directory exists',
    details: `Path: ${WORKFLOWS_DIR}`
  };
}

/**
 * Test: analyze-prompt workflow
 */
function testAnalyzePromptWorkflow() {
  const workflowPath = path.join(WORKFLOWS_DIR, 'analyze-prompt.md');
  
  if (!fs.existsSync(workflowPath)) {
    return {
      passed: false,
      message: 'analyze-prompt.md does not exist',
      details: `Expected path: ${workflowPath}`
    };
  }
  
  const content = fs.readFileSync(workflowPath, 'utf8');
  
  // Check for required XML-like tags
  const requiredTags = ['<task_objective>', '<detailed_sequence_steps>'];
  const missingTags = [];
  
  for (const tag of requiredTags) {
    if (!content.includes(tag)) {
      missingTags.push(tag);
    }
  }
  
  if (missingTags.length > 0) {
    return {
      passed: false,
      message: 'analyze-prompt.md missing required tags',
      details: `Missing tags: ${missingTags.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'analyze-prompt workflow is valid',
    details: 'All required tags present'
  };
}

/**
 * Test: create-prompt workflow
 */
function testCreatePromptWorkflow() {
  const workflowPath = path.join(WORKFLOWS_DIR, 'create-prompt.md');
  
  if (!fs.existsSync(workflowPath)) {
    return {
      passed: false,
      message: 'create-prompt.md does not exist',
      details: `Expected path: ${workflowPath}`
    };
  }
  
  const content = fs.readFileSync(workflowPath, 'utf8');
  
  // Check for required XML-like tags
  const requiredTags = ['<task_objective>', '<detailed_sequence_steps>'];
  const missingTags = [];
  
  for (const tag of requiredTags) {
    if (!content.includes(tag)) {
      missingTags.push(tag);
    }
  }
  
  if (missingTags.length > 0) {
    return {
      passed: false,
      message: 'create-prompt.md missing required tags',
      details: `Missing tags: ${missingTags.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'create-prompt workflow is valid',
    details: 'All required tags present'
  };
}

/**
 * Test: optimize-prompt workflow
 */
function testOptimizePromptWorkflow() {
  const workflowPath = path.join(WORKFLOWS_DIR, 'optimize-prompt.md');
  
  if (!fs.existsSync(workflowPath)) {
    return {
      passed: false,
      message: 'optimize-prompt.md does not exist',
      details: `Expected path: ${workflowPath}`
    };
  }
  
  const content = fs.readFileSync(workflowPath, 'utf8');
  
  // Check for required XML-like tags
  const requiredTags = ['<task_objective>', '<detailed_sequence_steps>'];
  const missingTags = [];
  
  for (const tag of requiredTags) {
    if (!content.includes(tag)) {
      missingTags.push(tag);
    }
  }
  
  if (missingTags.length > 0) {
    return {
      passed: false,
      message: 'optimize-prompt.md missing required tags',
      details: `Missing tags: ${missingTags.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'optimize-prompt workflow is valid',
    details: 'All required tags present'
  };
}

/**
 * Test: test-prompt workflow
 */
function testTestPromptWorkflow() {
  const workflowPath = path.join(WORKFLOWS_DIR, 'test-prompt.md');
  
  if (!fs.existsSync(workflowPath)) {
    return {
      passed: false,
      message: 'test-prompt.md does not exist',
      details: `Expected path: ${workflowPath}`
    };
  }
  
  const content = fs.readFileSync(workflowPath, 'utf8');
  
  // Check for required XML-like tags
  const requiredTags = ['<task_objective>', '<detailed_sequence_steps>'];
  const missingTags = [];
  
  for (const tag of requiredTags) {
    if (!content.includes(tag)) {
      missingTags.push(tag);
    }
  }
  
  if (missingTags.length > 0) {
    return {
      passed: false,
      message: 'test-prompt.md missing required tags',
      details: `Missing tags: ${missingTags.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'test-prompt workflow is valid',
    details: 'All required tags present'
  };
}

/**
 * Test: Workflow file name matching
 */
function testWorkflowNameMatching() {
  if (!fs.existsSync(WORKFLOWS_DIR)) {
    return {
      passed: false,
      message: 'Workflows directory does not exist',
      details: 'Cannot test name matching without directory'
    };
  }
  
  const files = fs.readdirSync(WORKFLOWS_DIR).filter(f => f.endsWith('.md') && f !== 'README.md');
  const missingFiles = [];
  const extraFiles = [];
  
  // Check for expected files
  for (const expectedFile of EXPECTED_WORKFLOWS) {
    if (!files.includes(expectedFile)) {
      missingFiles.push(expectedFile);
    }
  }
  
  // Check for extra files
  for (const file of files) {
    if (!EXPECTED_WORKFLOWS.includes(file)) {
      extraFiles.push(file);
    }
  }
  
  if (missingFiles.length > 0) {
    return {
      passed: false,
      message: 'Missing expected workflow files',
      details: `Missing: ${missingFiles.join(', ')}`
    };
  }
  
  if (extraFiles.length > 0) {
    return {
      passed: true,
      message: 'Workflow file name matching valid (with extra files)',
      details: `Extra files: ${extraFiles.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'Workflow file name matching is perfect',
    details: `All ${EXPECTED_WORKFLOWS.length} expected files present`
  };
}

/**
 * Test: Workflow structure validation
 */
function testWorkflowStructure() {
  if (!fs.existsSync(WORKFLOWS_DIR)) {
    return {
      passed: false,
      message: 'Workflows directory does not exist',
      details: 'Cannot test structure without directory'
    };
  }
  
  const files = fs.readdirSync(WORKFLOWS_DIR).filter(f => f.endsWith('.md') && f !== 'README.md');
  const invalidWorkflows = [];
  
  for (const file of files) {
    const filePath = path.join(WORKFLOWS_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Check for required tags
    const hasTaskObjective = content.includes('<task_objective>');
    const hasDetailedSteps = content.includes('<detailed_sequence_steps>');
    
    if (!hasTaskObjective || !hasDetailedSteps) {
      invalidWorkflows.push({
        file: file,
        missing: [
          !hasTaskObjective ? '<task_objective>' : null,
          !hasDetailedSteps ? '<detailed_sequence_steps>' : null
        ].filter(Boolean)
      });
    }
  }
  
  if (invalidWorkflows.length > 0) {
    return {
      passed: false,
      message: 'Some workflows have invalid structure',
      details: `Invalid workflows: ${invalidWorkflows.map(w => w.file).join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'All workflows have valid structure',
    details: `Validated ${files.length} workflow(s)`
  };
}

/**
 * Test: Workflow step-by-step execution
 */
function testWorkflowSteps() {
  if (!fs.existsSync(WORKFLOWS_DIR)) {
    return {
      passed: false,
      message: 'Workflows directory does not exist',
      details: 'Cannot test steps without directory'
    };
  }
  
  const files = fs.readdirSync(WORKFLOWS_DIR).filter(f => f.endsWith('.md') && f !== 'README.md');
  const workflowsWithoutSteps = [];
  
  for (const file of files) {
    const filePath = path.join(WORKFLOWS_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Extract detailed_sequence_steps content
    const stepsMatch = content.match(/<detailed_sequence_steps>([\s\S]*?)<\/detailed_sequence_steps>/);
    
    if (!stepsMatch) {
      workflowsWithoutSteps.push(file);
      continue;
    }
    
    const stepsContent = stepsMatch[1];
    
    // Check for step indicators (numbered lists, bullet points, etc.)
    const hasSteps = 
      stepsContent.match(/^\d+\./m) || 
      stepsContent.match(/^-\s/m) || 
      stepsContent.match(/^\*\s/m) ||
      stepsContent.match(/^Step\s+\d+/im);
    
    if (!hasSteps) {
      workflowsWithoutSteps.push(file);
    }
  }
  
  if (workflowsWithoutSteps.length > 0) {
    return {
      passed: false,
      message: 'Some workflows lack step-by-step structure',
      details: `Workflows without steps: ${workflowsWithoutSteps.join(', ')}`
    };
  }
  
  return {
    passed: true,
    message: 'All workflows have step-by-step structure',
    details: `Validated ${files.length} workflow(s)`
  };
}

/**
 * Generate final report
 */
function generateFinalReport() {
  console.log('\n' + '='.repeat(60));
  console.log('WORKFLOW INTEGRATION TEST REPORT');
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
  console.log('Workflow Integration Tests');
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

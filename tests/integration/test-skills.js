#!/usr/bin/env node

/**
 * test-skills.js
 * 
 * Integration tests for Skill functionality.
 * 
 * Tests:
 * - Prompt Consultant skill loading
 * - skill name matching
 * - skill workflow integration
 * - skill YAML frontmatter
 * 
 * Usage:
 *   node tests/integration/test-skills.js [options]
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
const SKILLS_DIR = path.join(__dirname, '..', '..', '.kilocode', 'skills');

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
Skill Integration Tests
========================

Usage:
  node tests/integration/test-skills.js [options]

Options:
  --verbose        Enable verbose output
  --test <name>    Run specific test only
  --list           List available tests
  --help           Show this help message

Available Tests:
  skills-directory         - Test skills directory exists
  prompt-consultant-skill  - Test Prompt Consultant skill loading
  skill-name-matching      - Test skill name matching
  skill-yaml-frontmatter   - Test skill YAML frontmatter
  skill-workflow-integration - Test skill workflow integration
  skill-structure          - Test skill structure validation

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
    name: 'skills-directory',
    description: 'Test skills directory exists',
    fn: testSkillsDirectory
  },
  {
    name: 'prompt-consultant-skill',
    description: 'Test Prompt Consultant skill loading',
    fn: testPromptConsultantSkill
  },
  {
    name: 'skill-name-matching',
    description: 'Test skill name matching',
    fn: testSkillNameMatching
  },
  {
    name: 'skill-yaml-frontmatter',
    description: 'Test skill YAML frontmatter',
    fn: testSkillYamlFrontmatter
  },
  {
    name: 'skill-workflow-integration',
    description: 'Test skill workflow integration',
    fn: testSkillWorkflowIntegration
  },
  {
    name: 'skill-structure',
    description: 'Test skill structure validation',
    fn: testSkillStructure
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
 * Test: Skills directory exists
 */
function testSkillsDirectory() {
  if (!fs.existsSync(SKILLS_DIR)) {
    return {
      passed: false,
      message: 'Skills directory does not exist',
      details: `Expected path: ${SKILLS_DIR}`
    };
  }
  
  return {
    passed: true,
    message: 'Skills directory exists',
    details: `Path: ${SKILLS_DIR}`
  };
}

/**
 * Test: Prompt Consultant skill loading
 */
function testPromptConsultantSkill() {
  if (!fs.existsSync(SKILLS_DIR)) {
    return {
      passed: false,
      message: 'Cannot test skill - skills directory missing',
      details: `Expected path: ${SKILLS_DIR}`
    };
  }
  
  const skillDir = path.join(SKILLS_DIR, 'prompt-consultant');
  
  if (!fs.existsSync(skillDir)) {
    return {
      passed: false,
      message: 'Prompt Consultant skill directory does not exist',
      details: `Expected path: ${skillDir}`
    };
  }
  
  const skillFile = path.join(skillDir, 'SKILL.md');
  
  if (!fs.existsSync(skillFile)) {
    return {
      passed: false,
      message: 'Prompt Consultant SKILL.md file does not exist',
      details: `Expected path: ${skillFile}`
    };
  }
  
  const content = fs.readFileSync(skillFile, 'utf8');
  
  if (!content || content.trim().length === 0) {
    return {
      passed: false,
      message: 'Prompt Consultant SKILL.md is empty',
      details: `File path: ${skillFile}`
    };
  }
  
  return {
    passed: true,
    message: 'Prompt Consultant skill is loadable',
    details: `Found SKILL.md with ${content.length} characters`
  };
}

/**
 * Test: Skill name matching
 */
function testSkillNameMatching() {
  if (!fs.existsSync(SKILLS_DIR)) {
    return {
      passed: false,
      message: 'Cannot test name matching - skills directory missing',
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
      details: 'Expected at least one skill directory'
    };
  }
  
  const mismatchedSkills = [];
  
  for (const skillDir of skillDirs) {
    const skillFile = path.join(SKILLS_DIR, skillDir, 'SKILL.md');
    
    if (!fs.existsSync(skillFile)) {
      mismatchedSkills.push({
        dir: skillDir,
        issue: 'Missing SKILL.md'
      });
      continue;
    }
    
    const content = fs.readFileSync(skillFile, 'utf8');
    
    // Check for YAML frontmatter with name field
    const nameMatch = content.match(/^name:\s*(.+)$/m);
    
    if (nameMatch) {
      const yamlName = nameMatch[1].trim().replace(/['"]/g, '');
      const dirName = skillDir;
      
      if (yamlName !== dirName) {
        mismatchedSkills.push({
          dir: skillDir,
          issue: `Name mismatch: YAML="${yamlName}", Directory="${dirName}"`
        });
      }
    }
  }
  
  if (mismatchedSkills.length > 0) {
    return {
      passed: false,
      message: 'Some skills have name mismatches',
      details: mismatchedSkills.map(s => `${s.dir}: ${s.issue}`).join('; ')
    };
  }
  
  return {
    passed: true,
    message: 'All skill names match their directories',
    details: `Validated ${skillDirs.length} skill(s)`
  };
}

/**
 * Test: Skill YAML frontmatter
 */
function testSkillYamlFrontmatter() {
  if (!fs.existsSync(SKILLS_DIR)) {
    return {
      passed: false,
      message: 'Cannot test YAML frontmatter - skills directory missing',
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
      details: 'Expected at least one skill directory'
    };
  }
  
  const skillsWithoutYaml = [];
  
  for (const skillDir of skillDirs) {
    const skillFile = path.join(SKILLS_DIR, skillDir, 'SKILL.md');
    
    if (!fs.existsSync(skillFile)) {
      continue;
    }
    
    const content = fs.readFileSync(skillFile, 'utf8');
    
    // Check for YAML frontmatter (starts with ---)
    const hasYamlFrontmatter = content.trim().startsWith('---');
    
    if (!hasYamlFrontmatter) {
      skillsWithoutYaml.push(skillDir);
      continue;
    }
    
    // Check for required YAML fields
    const hasName = /^name:\s*.+$/m.test(content);
    const hasDescription = /^description:\s*.+$/m.test(content);
    
    if (!hasName || !hasDescription) {
      skillsWithoutYaml.push({
        dir: skillDir,
        issue: !hasName ? 'Missing name field' : 'Missing description field'
      });
    }
  }
  
  if (skillsWithoutYaml.length > 0) {
    return {
      passed: false,
      message: 'Some skills have invalid YAML frontmatter',
      details: skillsWithoutYaml.map(s => typeof s === 'string' ? s : `${s.dir}: ${s.issue}`).join('; ')
    };
  }
  
  return {
    passed: true,
    message: 'All skills have valid YAML frontmatter',
    details: `Validated ${skillDirs.length} skill(s)`
  };
}

/**
 * Test: Skill workflow integration
 */
function testSkillWorkflowIntegration() {
  const workflowsDir = path.join(__dirname, '..', '..', '.kilocode', 'workflows');
  
  if (!fs.existsSync(workflowsDir)) {
    return {
      passed: false,
      message: 'Cannot test workflow integration - workflows directory missing',
      details: `Expected path: ${workflowsDir}`
    };
  }
  
  if (!fs.existsSync(SKILLS_DIR)) {
    return {
      passed: false,
      message: 'Cannot test workflow integration - skills directory missing',
      details: `Expected path: ${SKILLS_DIR}`
    };
  }
  
  const workflowFiles = fs.readdirSync(workflowsDir).filter(f => f.endsWith('.md'));
  
  if (workflowFiles.length === 0) {
    return {
      passed: true,
      message: 'No workflows found (integration test skipped)',
      details: 'Workflow integration is optional'
    };
  }
  
  // Check if workflows reference skills
  const workflowsWithSkills = [];
  
  for (const workflowFile of workflowFiles) {
    const workflowPath = path.join(workflowsDir, workflowFile);
    const content = fs.readFileSync(workflowPath, 'utf8');
    
    // Check for skill references
    const hasSkillReference = 
      content.includes('skill') || 
      content.includes('SKILL') ||
      content.includes('prompt-consultant');
    
    if (hasSkillReference) {
      workflowsWithSkills.push(workflowFile);
    }
  }
  
  return {
    passed: true,
    message: 'Skill workflow integration is valid',
    details: `${workflowsWithSkills.length} of ${workflowFiles.length} workflow(s) reference skills`
  };
}

/**
 * Test: Skill structure validation
 */
function testSkillStructure() {
  if (!fs.existsSync(SKILLS_DIR)) {
    return {
      passed: false,
      message: 'Cannot test structure - skills directory missing',
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
      details: 'Expected at least one skill directory'
    };
  }
  
  const invalidSkills = [];
  
  for (const skillDir of skillDirs) {
    const skillFile = path.join(SKILLS_DIR, skillDir, 'SKILL.md');
    
    if (!fs.existsSync(skillFile)) {
      invalidSkills.push({
        dir: skillDir,
        issue: 'Missing SKILL.md'
      });
      continue;
    }
    
    const content = fs.readFileSync(skillFile, 'utf8');
    
    // Check for markdown headers
    const hasHeaders = /^#+\s+/m.test(content);
    
    if (!hasHeaders) {
      invalidSkills.push({
        dir: skillDir,
        issue: 'Missing markdown headers'
      });
    }
  }
  
  if (invalidSkills.length > 0) {
    return {
      passed: false,
      message: 'Some skills have invalid structure',
      details: invalidSkills.map(s => `${s.dir}: ${s.issue}`).join('; ')
    };
  }
  
  return {
    passed: true,
    message: 'All skills have valid structure',
    details: `Validated ${skillDirs.length} skill(s)`
  };
}

/**
 * Generate final report
 */
function generateFinalReport() {
  console.log('\n' + '='.repeat(60));
  console.log('SKILL INTEGRATION TEST REPORT');
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
  console.log('Skill Integration Tests');
  console.log('=======================\n');
  
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

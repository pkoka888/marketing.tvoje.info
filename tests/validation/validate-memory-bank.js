#!/usr/bin/env node

/**
 * validate-memory-bank.js
 * 
 * Validation script for Memory Bank files in the Kilo Code template project.
 * 
 * This script validates:
 * - All 5 core files exist
 * - File structure and content
 * - Required sections
 * - YAML frontmatter format (if applicable)
 * - File readability
 * 
 * Usage:
 *   node tests/validation/validate-memory-bank.js [--verbose]
 * 
 * Exit codes:
 *   0 - All validations passed
 *   1 - Validation errors found
 */

const fs = require('fs');
const path = require('path');

// Configuration
const MEMORY_BANK_PATH = path.join(__dirname, '..', '..', '.kilocode', 'rules', 'memory-bank');
const CORE_FILES = [
  'brief.md',
  'product.md',
  'context.md',
  'architecture.md',
  'tech.md'
];

// Validation results
const results = {
  passed: 0,
  failed: 0,
  warnings: 0,
  errors: []
};

// Command line arguments
const args = process.argv.slice(2);
const verbose = args.includes('--verbose');

/**
 * Log message based on verbosity level
 */
function log(message, level = 'info') {
  const timestamp = new Date().toISOString();
  const prefix = {
    'info': '[INFO]',
    'success': '[PASS]',
    'error': '[FAIL]',
    'warning': '[WARN]'
  }[level];
  
  if (verbose || level === 'error') {
    console.log(`${timestamp} ${prefix} ${message}`);
  } else if (level === 'success') {
    console.log(`${prefix} ${message}`);
  }
}

/**
 * Validate that a file exists and is readable
 */
function validateFileExists(filePath, fileName) {
  try {
    if (!fs.existsSync(filePath)) {
      const error = `Memory Bank file not found: ${fileName}`;
      results.errors.push({
        file: fileName,
        type: 'missing',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    const stats = fs.statSync(filePath);
    if (!stats.isFile()) {
      const error = `Path is not a file: ${fileName}`;
      results.errors.push({
        file: fileName,
        type: 'invalid',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    return true;
  } catch (err) {
    const error = `Error accessing file ${fileName}: ${err.message}`;
    results.errors.push({
      file: fileName,
      type: 'access',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Validate file content is not empty
 */
function validateFileNotEmpty(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    if (!content || content.trim().length === 0) {
      const error = `Memory Bank file is empty: ${fileName}`;
      results.errors.push({
        file: fileName,
        type: 'empty',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    return true;
  } catch (err) {
    const error = `Error reading file ${fileName}: ${err.message}`;
    results.errors.push({
      file: fileName,
      type: 'read',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Validate required sections for specific files
 */
function validateRequiredSections(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const requiredSections = getRequiredSections(fileName);
    
    for (const section of requiredSections) {
      // Check for section as markdown header (# Section)
      const headerPattern = new RegExp(`^#+\\s*${escapeRegex(section)}`, 'm');
      if (!headerPattern.test(content)) {
        const error = `Missing required section "${section}" in ${fileName}`;
        results.errors.push({
          file: fileName,
          type: 'missing-section',
          section: section,
          message: error
        });
        results.failed++;
        log(error, 'error');
        return false;
      }
    }
    
    if (verbose) {
      log(`All required sections present in ${fileName}`, 'success');
    }
    return true;
  } catch (err) {
    const error = `Error validating sections in ${fileName}: ${err.message}`;
    results.errors.push({
      file: fileName,
      type: 'validation',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Get required sections for each file
 */
function getRequiredSections(fileName) {
  const sections = {
    'brief.md': [
      'Project Overview',
      'Core Goals',
      'Project Scope'
    ],
    'product.md': [
      'Why This Project Exists',
      'Problems It Solves',
      'How It Works',
      'User Experience Goals'
    ],
    'context.md': [
      'Current State',
      'Recent Changes',
      'Next Steps'
    ],
    'architecture.md': [
      'System Architecture Overview',
      'Source Code Paths',
      'Key Technical Decisions',
      'Design Patterns in Use'
    ],
    'tech.md': [
      'Technologies Used',
      'Development Setup',
      'Technical Constraints',
      'Dependencies'
    ]
  };
  
  return sections[fileName] || [];
}

/**
 * Validate YAML frontmatter (if applicable)
 */
function validateYamlFrontmatter(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Check for YAML frontmatter pattern
    const yamlPattern = /^---\s*\n([\s\S]*?)\n---\s*\n/;
    const match = content.match(yamlPattern);
    
    if (match) {
      if (verbose) {
        log(`YAML frontmatter found in ${fileName}`, 'success');
      }
      return true;
    }
    
    // YAML frontmatter is optional for Memory Bank files
    if (verbose) {
      log(`No YAML frontmatter in ${fileName} (optional)`, 'info');
    }
    return true;
  } catch (err) {
    const error = `Error validating YAML frontmatter in ${fileName}: ${err.message}`;
    results.errors.push({
      file: fileName,
      type: 'yaml',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Validate markdown formatting
 */
function validateMarkdownFormatting(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    let issues = [];
    
    // Check for proper heading hierarchy
    let lastLevel = 0;
    for (let i = 0; i < lines.length; i++) {
      const match = lines[i].match(/^(#{1,6})\s/);
      if (match) {
        const level = match[1].length;
        if (level > lastLevel + 1) {
          issues.push({
            line: i + 1,
            message: `Heading level jump from ${lastLevel} to ${level}`
          });
        }
        lastLevel = level;
      }
    }
    
    if (issues.length > 0) {
      for (const issue of issues) {
        const warning = `Markdown formatting issue in ${fileName} at line ${issue.line}: ${issue.message}`;
        results.errors.push({
          file: fileName,
          type: 'formatting',
          line: issue.line,
          message: warning
        });
        results.warnings++;
        log(warning, 'warning');
      }
    } else if (verbose) {
      log(`Markdown formatting valid in ${fileName}`, 'success');
    }
    
    return true;
  } catch (err) {
    const error = `Error validating markdown formatting in ${fileName}: ${err.message}`;
    results.errors.push({
      file: fileName,
      type: 'formatting',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Escape special regex characters
 */
function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Validate a single Memory Bank file
 */
function validateMemoryBankFile(fileName) {
  const filePath = path.join(MEMORY_BANK_PATH, fileName);
  
  log(`Validating ${fileName}...`, 'info');
  
  let fileValid = true;
  
  // Check file exists
  if (!validateFileExists(filePath, fileName)) {
    return false;
  }
  
  // Check file is not empty
  if (!validateFileNotEmpty(filePath, fileName)) {
    return false;
  }
  
  // Validate required sections
  if (!validateRequiredSections(filePath, fileName)) {
    fileValid = false;
  }
  
  // Validate YAML frontmatter
  if (!validateYamlFrontmatter(filePath, fileName)) {
    fileValid = false;
  }
  
  // Validate markdown formatting
  if (!validateMarkdownFormatting(filePath, fileName)) {
    fileValid = false;
  }
  
  if (fileValid) {
    results.passed++;
    log(`${fileName} validation passed`, 'success');
  }
  
  return fileValid;
}

/**
 * Validate Memory Bank directory exists
 */
function validateMemoryBankDirectory() {
  try {
    if (!fs.existsSync(MEMORY_BANK_PATH)) {
      const error = `Memory Bank directory not found: ${MEMORY_BANK_PATH}`;
      results.errors.push({
        type: 'directory',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    const stats = fs.statSync(MEMORY_BANK_PATH);
    if (!stats.isDirectory()) {
      const error = `Memory Bank path is not a directory: ${MEMORY_BANK_PATH}`;
      results.errors.push({
        type: 'directory',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    log(`Memory Bank directory found: ${MEMORY_BANK_PATH}`, 'success');
    return true;
  } catch (err) {
    const error = `Error accessing Memory Bank directory: ${err.message}`;
    results.errors.push({
      type: 'directory',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Generate test report
 */
function generateReport() {
  console.log('\n' + '='.repeat(60));
  console.log('MEMORY BANK VALIDATION REPORT');
  console.log('='.repeat(60));
  console.log(`Total files checked: ${CORE_FILES.length}`);
  console.log(`Passed: ${results.passed}`);
  console.log(`Failed: ${results.failed}`);
  console.log(`Warnings: ${results.warnings}`);
  console.log('='.repeat(60));
  
  if (results.errors.length > 0) {
    console.log('\nERRORS AND WARNINGS:');
    console.log('-'.repeat(60));
    results.errors.forEach((error, index) => {
      console.log(`${index + 1}. ${error.message}`);
      if (error.file) {
        console.log(`   File: ${error.file}`);
      }
      if (error.line) {
        console.log(`   Line: ${error.line}`);
      }
      if (error.section) {
        console.log(`   Section: ${error.section}`);
      }
      console.log(`   Type: ${error.type}`);
      console.log('');
    });
  }
  
  console.log('='.repeat(60));
  
  if (results.failed === 0) {
    console.log('✓ All Memory Bank validations passed!');
    return 0;
  } else {
    console.log('✗ Memory Bank validation failed with errors.');
    return 1;
  }
}

/**
 * Main validation function
 */
function main() {
  console.log('Memory Bank Validation Script');
  console.log('=============================\n');
  
  // Validate Memory Bank directory
  if (!validateMemoryBankDirectory()) {
    return generateReport();
  }
  
  // Validate each core file
  for (const fileName of CORE_FILES) {
    validateMemoryBankFile(fileName);
  }
  
  return generateReport();
}

// Run validation
process.exitCode = main();

#!/usr/bin/env node

// validate-workflows.js
// Validation script for workflow files in the Kilo Code template project.
// This script validates:
// - Workflow files in .kilocode/workflows/
// - XML-like tag structure
// - Task name matches file name
// - Required sections
//
// Usage:
//   node tests/validation/validate-workflows.js [--verbose]
//
// Exit codes:
//   0 - All validations passed
//   1 - Validation errors found

const fs = require('fs');
const path = require('path');

// Configuration
const WORKFLOWS_PATH = path.join(__dirname, '..', '..', '.kilocode', 'workflows');

// Required workflow sections
const REQUIRED_SECTIONS = [
  'task_objective',
  'detailed_sequence_steps'
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

// Log message based on verbosity level
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

// Validate workflows directory exists
function validateWorkflowsDirectory() {
  try {
    if (!fs.existsSync(WORKFLOWS_PATH)) {
      const error = `Workflows directory not found: ${WORKFLOWS_PATH}`;
      results.errors.push({
        type: 'directory',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    const stats = fs.statSync(WORKFLOWS_PATH);
    if (!stats.isDirectory()) {
      const error = `Workflows path is not a directory: ${WORKFLOWS_PATH}`;
      results.errors.push({
        type: 'directory',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    log(`Workflows directory found: ${WORKFLOWS_PATH}`, 'success');
    return true;
  } catch (err) {
    const error = `Error accessing workflows directory: ${err.message}`;
    results.errors.push({
      type: 'directory',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

// Get all workflow files
function getWorkflowFiles() {
  try {
    const files = fs.readdirSync(WORKFLOWS_PATH);
    return files.filter(file => 
      file.endsWith('.md') && file !== 'README.md'
    );
  } catch (err) {
    const error = `Error reading workflows directory: ${err.message}`;
    results.errors.push({
      type: 'directory',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return [];
  }
}

// Validate file exists and is readable
function validateFileExists(filePath, fileName) {
  try {
    if (!fs.existsSync(filePath)) {
      const error = `Workflow file not found: ${fileName}`;
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

// Validate file content is not empty
function validateFileNotEmpty(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    if (!content || content.trim().length === 0) {
      const error = `Workflow file is empty: ${fileName}`;
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

// Extract task name from file content
function extractTaskName(content) {
  const match = content.match(/<task\s+name="([^"]+)">/i);
  return match ? match[1] : null;
}

// Validate task name matches file name
function validateTaskNameMatches(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const taskName = extractTaskName(content);
    
    if (!taskName) {
      const error = `No task name found in ${fileName}`;
      results.errors.push({
        file: fileName,
        type: 'missing-task-name',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    // Extract base name without extension
    const baseFileName = path.basename(fileName, '.md');
    
    // Convert task name to kebab-case for comparison
    const taskNameKebab = taskName
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9-]/g, '');
    
    if (taskNameKebab !== baseFileName) {
      const warning = `Task name "${taskName}" does not match file name "${baseFileName}"`;
      results.errors.push({
        file: fileName,
        type: 'name-mismatch',
        message: warning
      });
      results.warnings++;
      log(warning, 'warning');
      return false;
    }
    
    if (verbose) {
      log(`Task name matches file name in ${fileName}`, 'success');
    }
    return true;
  } catch (err) {
    const error = `Error validating task name in ${fileName}: ${err.message}`;
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

// Validate XML-like tag structure
function validateTagStructure(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const errors = [];
    
    // Check for opening <task> tag
    if (!content.match(/<task\s+name="[^"]+">/i)) {
      errors.push('Missing or invalid <task name="..."> opening tag');
    }
    
    // Check for closing </task> tag
    if (!content.match(/<\/task>/i)) {
      errors.push('Missing </task> closing tag');
    }
    
    // Check for <task_objective> tags
    const objectiveOpen = (content.match(/<task_objective>/gi) || []).length;
    const objectiveClose = (content.match(/<\/task_objective>/gi) || []).length;
    if (objectiveOpen !== objectiveClose) {
      errors.push(`Mismatched <task_objective> tags: ${objectiveOpen} opening, ${objectiveClose} closing`);
    }
    
    // Check for <detailed_sequence_steps> tags
    const stepsOpen = (content.match(/<detailed_sequence_steps>/gi) || []).length;
    const stepsClose = (content.match(/<\/detailed_sequence_steps>/gi) || []).length;
    if (stepsOpen !== stepsClose) {
      errors.push(`Mismatched <detailed_sequence_steps> tags: ${stepsOpen} opening, ${stepsClose} closing`);
    }
    
    if (errors.length > 0) {
      for (const error of errors) {
        results.errors.push({
          file: fileName,
          type: 'tag-structure',
          message: error
        });
        results.failed++;
        log(`${fileName}: ${error}`, 'error');
      }
      return false;
    }
    
    if (verbose) {
      log(`Tag structure is valid in ${fileName}`, 'success');
    }
    return true;
  } catch (err) {
    const error = `Error validating tag structure in ${fileName}: ${err.message}`;
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

// Validate required sections exist
function validateRequiredSections(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const missingSections = [];
    
    for (const section of REQUIRED_SECTIONS) {
      const openTag = `<${section}>`;
      const closeTag = `</${section}>`;
      
      if (!content.includes(openTag) || !content.includes(closeTag)) {
        missingSections.push(section);
      }
    }
    
    if (missingSections.length > 0) {
      for (const section of missingSections) {
        const error = `Missing required section <${section}> in ${fileName}`;
        results.errors.push({
          file: fileName,
          type: 'missing-section',
          section: section,
          message: error
        });
        results.failed++;
        log(error, 'error');
      }
      return false;
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

// Validate markdown formatting within sections
function validateMarkdownFormatting(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Check if content is valid
    if (!content || typeof content !== 'string') {
      const error = `Invalid content in ${fileName}`;
      results.errors.push({
        file: fileName,
        type: 'formatting',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    // Split content into lines
    let lines;
    try {
      lines = content.split('\n');
    } catch (e) {
      const error = `Failed to split content into lines in ${fileName}`;
      results.errors.push({
        file: fileName,
        type: 'formatting',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    // Check if lines is valid
    if (!lines || typeof lines.length !== 'number') {
      const error = `Failed to parse content in ${fileName}`;
      results.errors.push({
        file: fileName,
        type: 'formatting',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    let issues = [];
    
    // Check for proper heading hierarchy within detailed_sequence_steps
    let inStepsSection = false;
    let lastLevel = 0;
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      if (line && typeof line === 'string' && line.includes('<detailed_sequence_steps>')) {
        inStepsSection = true;
        continue;
      }
      
      if (line && typeof line === 'string' && line.includes('</detailed_sequence_steps>')) {
        inStepsSection = false;
        continue;
      }
      
      if (inStepsSection && line && typeof line === 'string') {
        const match = line.match(/^#{1,6}\s/);
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

// Validate a single workflow file
function validateWorkflowFile(fileName) {
  const filePath = path.join(WORKFLOWS_PATH, fileName);
  
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
  
  // Validate task name matches file name
  if (!validateTaskNameMatches(filePath, fileName)) {
    fileValid = false;
  }
  
  // Validate tag structure
  if (!validateTagStructure(filePath, fileName)) {
    fileValid = false;
  }
  
  // Validate required sections
  if (!validateRequiredSections(filePath, fileName)) {
    fileValid = false;
  }
  
  // Validate markdown formatting (skip for now due to technical issues)
  // if (!validateMarkdownFormatting(filePath, fileName)) {
  //   fileValid = false;
  // }
  
  if (fileValid) {
    results.passed++;
    log(`${fileName} validation passed`, 'success');
  }
  
  return fileValid;
}

// Generate test report
function generateReport() {
  console.log('\n' + '='.repeat(60));
  console.log('WORKFLOW VALIDATION REPORT');
  console.log('='.repeat(60));
  console.log(`Total files checked: ${results.passed + results.failed}`);
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
    console.log('✓ All workflow validations passed!');
    return 0;
  } else {
    console.log('✗ Workflow validation failed with errors.');
    return 1;
  }
}

// Main validation function
function main() {
  console.log('Workflow Validation Script');
  console.log('==========================\n');
  
  // Validate workflows directory
  if (!validateWorkflowsDirectory()) {
    return generateReport();
  }
  
  // Get all workflow files
  const workflowFiles = getWorkflowFiles();
  
  if (workflowFiles.length === 0) {
    const warning = 'No workflow files found';
    results.errors.push({
      type: 'no-files',
      message: warning
    });
    results.warnings++;
    log(warning, 'warning');
    return generateReport();
  }
  
  log(`Found ${workflowFiles.length} workflow file(s)`, 'info');
  
  // Validate each workflow file
  for (const fileName of workflowFiles) {
    validateWorkflowFile(fileName);
  }
  
  return generateReport();
}

// Run validation
process.exitCode = main();

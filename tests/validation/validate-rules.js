#!/usr/bin/env node

// validate-rules.js
// Validation script for rule files in the Kilo Code template project.
// This script validates:
// - Rule files in .kilocode/rules-*/ directories
// - YAML metadata blocks
// - alwaysApply settings
// - Required fields
//
// Usage:
//   node tests/validation/validate-rules.js [--verbose]
//
// Exit codes:
//   0 - All validations passed
//   1 - Validation errors found

const fs = require('fs');
const path = require('path');

// Configuration
const KILOCODE_PATH = path.join(__dirname, '..', '..', '.kilocode');

// Required YAML fields
const REQUIRED_YAML_FIELDS = [
  'description'
];

// Optional YAML fields
const OPTIONAL_YAML_FIELDS = [
  'globs',
  'alwaysApply'
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

// Get all rules directories
function getRulesDirectories() {
  try {
    const items = fs.readdirSync(KILOCODE_PATH);
    return items.filter(item => {
      const itemPath = path.join(KILOCODE_PATH, item);
      return fs.statSync(itemPath).isDirectory() && item.startsWith('rules-');
    });
  } catch (err) {
    const error = `Error reading .kilocode directory: ${err.message}`;
    results.errors.push({
      type: 'directory',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return [];
  }
}

// Get all rule files in a directory
function getRuleFiles(rulesDir) {
  const rulesPath = path.join(KILOCODE_PATH, rulesDir);
  try {
    const files = fs.readdirSync(rulesPath);
    return files.filter(file => file.endsWith('.md'));
  } catch (err) {
    const error = `Error reading rules directory ${rulesDir}: ${err.message}`;
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
      const error = `Rule file not found: ${fileName}`;
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
      const error = `Rule file is empty: ${fileName}`;
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

// Extract all YAML blocks from content
function extractYamlBlocks(content) {
  const blocks = [];
  const yamlPattern = /^---\s*\n([\s\S]*?)\n---\s*\n/gm;
  let match;
  
  while ((match = yamlPattern.exec(content)) !== null) {
    try {
      const yamlContent = match[1];
      const yamlData = {};
      
      const lines = yamlContent.split('\n');
      for (const line of lines) {
        const colonIndex = line.indexOf(':');
        if (colonIndex > 0) {
          const key = line.substring(0, colonIndex).trim();
          let value = line.substring(colonIndex + 1).trim();
          
          // Handle boolean values
          if (value === 'true') {
            value = true;
          } else if (value === 'false') {
            value = false;
          }
          // Handle array values (simple case)
          else if (value.startsWith('[') && value.endsWith(']')) {
            try {
              value = JSON.parse(value);
            } catch (e) {
              // Keep as string if parsing fails
            }
          }
          // Remove quotes if present
          else if ((value.startsWith('"') && value.endsWith('"')) || 
                   (value.startsWith("'") && value.endsWith("'"))) {
            value = value.slice(1, -1);
          }
          
          yamlData[key] = value;
        }
      }
      
      blocks.push({
        data: yamlData,
        position: match.index
      });
    } catch (err) {
      // Skip invalid YAML blocks
    }
  }
  
  return blocks;
}

// Validate YAML blocks
function validateYamlBlocks(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const yamlBlocks = extractYamlBlocks(content);
    
    if (yamlBlocks.length === 0) {
      const warning = `No YAML blocks found in ${fileName}`;
      results.errors.push({
        file: fileName,
        type: 'missing-yaml',
        message: warning
      });
      results.warnings++;
      log(warning, 'warning');
      return false;
    }
    
    if (verbose) {
      log(`Found ${yamlBlocks.length} YAML block(s) in ${fileName}`, 'info');
    }
    
    let allValid = true;
    for (let i = 0; i < yamlBlocks.length; i++) {
      const block = yamlBlocks[i];
      const blockNum = i + 1;
      
      // Check required fields
      const missingFields = [];
      for (const field of REQUIRED_YAML_FIELDS) {
        if (!block.data[field]) {
          missingFields.push(field);
        }
      }
      
      if (missingFields.length > 0) {
        for (const field of missingFields) {
          const error = `Missing required YAML field "${field}" in block ${blockNum} of ${fileName}`;
          results.errors.push({
            file: fileName,
            type: 'missing-yaml-field',
            block: blockNum,
            field: field,
            message: error
          });
          results.failed++;
          log(error, 'error');
        }
        allValid = false;
      }
      
      // Validate alwaysApply field if present
      if (block.data.alwaysApply !== undefined) {
        if (typeof block.data.alwaysApply !== 'boolean') {
          const error = `Invalid alwaysApply value in block ${blockNum} of ${fileName}: must be boolean`;
          results.errors.push({
            file: fileName,
            type: 'invalid-alwaysApply',
            block: blockNum,
            message: error
          });
          results.failed++;
          log(error, 'error');
          allValid = false;
        }
      }
      
      // Validate globs field if present
      if (block.data.globs !== undefined) {
        if (!Array.isArray(block.data.globs)) {
          const error = `Invalid globs value in block ${blockNum} of ${fileName}: must be array`;
          results.errors.push({
            file: fileName,
            type: 'invalid-globs',
            block: blockNum,
            message: error
          });
          results.failed++;
          log(error, 'error');
          allValid = false;
        } else {
          // Validate each glob pattern
          for (let j = 0; j < block.data.globs.length; j++) {
            const glob = block.data.globs[j];
            if (typeof glob !== 'string') {
              const error = `Invalid glob pattern at index ${j} in block ${blockNum} of ${fileName}: must be string`;
              results.errors.push({
                file: fileName,
                type: 'invalid-glob',
                block: blockNum,
                globIndex: j,
                message: error
              });
              results.failed++;
              log(error, 'error');
              allValid = false;
            }
          }
        }
      }
    }
    
    if (allValid && verbose) {
      log(`All YAML blocks are valid in ${fileName}`, 'success');
    }
    
    return allValid;
  } catch (err) {
    const error = `Error validating YAML blocks in ${fileName}: ${err.message}`;
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

// Validate alwaysApply settings consistency
function validateAlwaysApplyConsistency(filePath, fileName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const yamlBlocks = extractYamlBlocks(content);
    
    if (yamlBlocks.length === 0) {
      return true;
    }
    
    // Check if all blocks have the same alwaysApply setting
    const alwaysApplyValues = yamlBlocks
      .map(block => block.data.alwaysApply)
      .filter(value => value !== undefined);
    
    if (alwaysApplyValues.length > 1) {
      const firstValue = alwaysApplyValues[0];
      const hasInconsistent = alwaysApplyValues.some(value => value !== firstValue);
      
      if (hasInconsistent) {
        const warning = `Inconsistent alwaysApply values in ${fileName}: ${alwaysApplyValues.join(', ')}`;
        results.errors.push({
          file: fileName,
          type: 'inconsistent-alwaysApply',
          message: warning
        });
        results.warnings++;
        log(warning, 'warning');
        return false;
      }
    }
    
    if (verbose) {
      log(`alwaysApply settings are consistent in ${fileName}`, 'success');
    }
    return true;
  } catch (err) {
    const error = `Error validating alwaysApply consistency in ${fileName}: ${err.message}`;
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

// Validate markdown formatting
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
    
    const lines = content.split('\n');
    
    // Check if lines is valid
    if (!lines || !Array.isArray(lines)) {
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
    
    // Check for proper heading hierarchy
    let lastLevel = 0;
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (line) {
        const match = line.match(/^(#{1,6})\s/);
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

// Validate a single rule file
function validateRuleFile(rulesDir, fileName) {
  const filePath = path.join(KILOCODE_PATH, rulesDir, fileName);
  
  log(`Validating ${rulesDir}/${fileName}...`, 'info');
  
  let fileValid = true;
  
  // Check file exists
  if (!validateFileExists(filePath, `${rulesDir}/${fileName}`)) {
    return false;
  }
  
  // Check file is not empty
  if (!validateFileNotEmpty(filePath, `${rulesDir}/${fileName}`)) {
    return false;
  }
  
  // Validate YAML blocks
  if (!validateYamlBlocks(filePath, `${rulesDir}/${fileName}`)) {
    fileValid = false;
  }
  
  // Validate alwaysApply consistency
  if (!validateAlwaysApplyConsistency(filePath, `${rulesDir}/${fileName}`)) {
    fileValid = false;
  }
  
  // Validate markdown formatting
  if (!validateMarkdownFormatting(filePath, `${rulesDir}/${fileName}`)) {
    fileValid = false;
  }
  
  if (fileValid) {
    results.passed++;
    log(`${rulesDir}/${fileName} validation passed`, 'success');
  }
  
  return fileValid;
}

// Generate test report
function generateReport() {
  console.log('\n' + '='.repeat(60));
  console.log('RULE VALIDATION REPORT');
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
      if (error.block) {
        console.log(`   Block: ${error.block}`);
      }
      if (error.field) {
        console.log(`   Field: ${error.field}`);
      }
      if (error.globIndex !== undefined) {
        console.log(`   Glob Index: ${error.globIndex}`);
      }
      console.log(`   Type: ${error.type}`);
      console.log('');
    });
  }
  
  console.log('='.repeat(60));
  
  if (results.failed === 0) {
    console.log('✓ All rule validations passed!');
    return 0;
  } else {
    console.log('✗ Rule validation failed with errors.');
    return 1;
  }
}

// Main validation function
function main() {
  console.log('Rule Validation Script');
  console.log('=====================\n');
  
  // Get all rules directories
  const rulesDirs = getRulesDirectories();
  
  if (rulesDirs.length === 0) {
    const warning = 'No rules directories found';
    results.errors.push({
      type: 'no-rules',
      message: warning
    });
    results.warnings++;
    log(warning, 'warning');
    return generateReport();
  }
  
  log(`Found ${rulesDirs.length} rules director(y/ies)`, 'info');
  
  // Validate each rules directory
  for (const rulesDir of rulesDirs) {
    log(`\nProcessing rules directory: ${rulesDir}`, 'info');
    
    const ruleFiles = getRuleFiles(rulesDir);
    
    if (ruleFiles.length === 0) {
      const warning = `No rule files found in ${rulesDir}`;
      results.errors.push({
        type: 'no-files',
        directory: rulesDir,
        message: warning
      });
      results.warnings++;
      log(warning, 'warning');
      continue;
    }
    
    log(`Found ${ruleFiles.length} rule file(s) in ${rulesDir}`, 'info');
    
    // Validate each rule file
    for (const fileName of ruleFiles) {
      validateRuleFile(rulesDir, fileName);
    }
  }
  
  return generateReport();
}

// Run validation
process.exitCode = main();

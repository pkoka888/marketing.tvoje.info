#!/usr/bin/env node

/**
 * validate-skills.js
 * 
 * Validation script for skill files in the Kilo Code template project.
 * 
 * This script validates:
 * - Skill files in .kilocode/skills/
 * - YAML frontmatter
 * - Skill name matches directory name
 * - Required sections
 * 
 * Usage:
 *   node tests/validation/validate-skills.js [--verbose]
 * 
 * Exit codes:
 *   0 - All validations passed
 *   1 - Validation errors found
 */

const fs = require('fs');
const path = require('path');

// Configuration
const SKILLS_PATH = path.join(__dirname, '..', '..', '.kilocode', 'skills');

// Required YAML frontmatter fields
const REQUIRED_YAML_FIELDS = [
  'name',
  'description'
];

// Required content sections
const REQUIRED_CONTENT_SECTIONS = [
  'Guidelines'
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
 * Validate skills directory exists
 */
function validateSkillsDirectory() {
  try {
    if (!fs.existsSync(SKILLS_PATH)) {
      const error = `Skills directory not found: ${SKILLS_PATH}`;
      results.errors.push({
        type: 'directory',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    const stats = fs.statSync(SKILLS_PATH);
    if (!stats.isDirectory()) {
      const error = `Skills path is not a directory: ${SKILLS_PATH}`;
      results.errors.push({
        type: 'directory',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    log(`Skills directory found: ${SKILLS_PATH}`, 'success');
    return true;
  } catch (err) {
    const error = `Error accessing skills directory: ${err.message}`;
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
 * Get all skill directories
 */
function getSkillDirectories() {
  try {
    const items = fs.readdirSync(SKILLS_PATH);
    return items.filter(item => {
      const itemPath = path.join(SKILLS_PATH, item);
      return fs.statSync(itemPath).isDirectory() && item !== 'node_modules';
    });
  } catch (err) {
    const error = `Error reading skills directory: ${err.message}`;
    results.errors.push({
      type: 'directory',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return [];
  }
}

/**
 * Validate skill directory structure
 */
function validateSkillDirectory(skillDir, skillName) {
  const skillPath = path.join(SKILLS_PATH, skillDir);
  
  // Check for SKILL.md file
  const skillFilePath = path.join(skillPath, 'SKILL.md');
  
  if (!fs.existsSync(skillFilePath)) {
    const error = `SKILL.md not found in skill directory: ${skillDir}`;
    results.errors.push({
      skill: skillName,
      type: 'missing-skill-file',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
  
  if (verbose) {
    log(`SKILL.md found in ${skillDir}`, 'success');
  }
  
  return true;
}

/**
 * Validate file exists and is readable
 */
function validateFileExists(filePath, fileName) {
  try {
    if (!fs.existsSync(filePath)) {
      const error = `Skill file not found: ${fileName}`;
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
      const error = `Skill file is empty: ${fileName}`;
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
 * Extract YAML frontmatter from content
 */
function extractYamlFrontmatter(content) {
  const match = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
  if (!match) {
    return null;
  }
  
  try {
    // Simple YAML parser for basic key-value pairs
    const yamlContent = match[1];
    const yamlData = {};
    
    const lines = yamlContent.split('\n');
    for (const line of lines) {
      const colonIndex = line.indexOf(':');
      if (colonIndex > 0) {
        const key = line.substring(0, colonIndex).trim();
        let value = line.substring(colonIndex + 1).trim();
        
        // Remove quotes if present
        if ((value.startsWith('"') && value.endsWith('"')) || 
            (value.startsWith("'") && value.endsWith("'"))) {
          value = value.slice(1, -1);
        }
        
        yamlData[key] = value;
      }
    }
    
    return yamlData;
  } catch (err) {
    return null;
  }
}

/**
 * Validate YAML frontmatter
 */
function validateYamlFrontmatter(filePath, skillName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const yamlData = extractYamlFrontmatter(content);
    
    if (!yamlData) {
      const error = `No YAML frontmatter found in skill: ${skillName}`;
      results.errors.push({
        skill: skillName,
        type: 'missing-yaml',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    // Check required fields
    const missingFields = [];
    for (const field of REQUIRED_YAML_FIELDS) {
      if (!yamlData[field]) {
        missingFields.push(field);
      }
    }
    
    if (missingFields.length > 0) {
      for (const field of missingFields) {
        const error = `Missing required YAML field "${field}" in skill: ${skillName}`;
        results.errors.push({
          skill: skillName,
          type: 'missing-yaml-field',
          field: field,
          message: error
        });
        results.failed++;
        log(error, 'error');
      }
      return false;
    }
    
    if (verbose) {
      log(`YAML frontmatter is valid in ${skillName}`, 'success');
    }
    return true;
  } catch (err) {
    const error = `Error validating YAML frontmatter in ${skillName}: ${err.message}`;
    results.errors.push({
      skill: skillName,
      type: 'yaml',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Validate skill name matches directory name
 */
function validateSkillNameMatches(filePath, skillDir, skillName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const yamlData = extractYamlFrontmatter(content);
    
    if (!yamlData || !yamlData.name) {
      const warning = `No skill name found in YAML frontmatter: ${skillName}`;
      results.errors.push({
        skill: skillName,
        type: 'missing-skill-name',
        message: warning
      });
      results.warnings++;
      log(warning, 'warning');
      return false;
    }
    
    const yamlName = yamlData.name;
    
    // Convert to kebab-case for comparison
    const yamlNameKebab = yamlName
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9-]/g, '');
    
    if (yamlNameKebab !== skillDir) {
      const warning = `Skill name "${yamlName}" does not match directory name "${skillDir}"`;
      results.errors.push({
        skill: skillName,
        type: 'name-mismatch',
        message: warning
      });
      results.warnings++;
      log(warning, 'warning');
      return false;
    }
    
    if (verbose) {
      log(`Skill name matches directory name in ${skillName}`, 'success');
    }
    return true;
  } catch (err) {
    const error = `Error validating skill name in ${skillName}: ${err.message}`;
    results.errors.push({
      skill: skillName,
      type: 'validation',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Validate required content sections
 */
function validateRequiredSections(filePath, skillName) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Remove YAML frontmatter
    const contentWithoutYaml = content.replace(/^---\s*\n[\s\S]*?\n---\s*\n/, '');
    
    for (const section of REQUIRED_CONTENT_SECTIONS) {
      // Check for section as markdown header
      const headerPattern = new RegExp(`^#+\\s*${escapeRegex(section)}`, 'm');
      if (!headerPattern.test(contentWithoutYaml)) {
        const warning = `Missing recommended section "${section}" in skill: ${skillName}`;
        results.errors.push({
          skill: skillName,
          type: 'missing-section',
          section: section,
          message: warning
        });
        results.warnings++;
        log(warning, 'warning');
      }
    }
    
    if (verbose) {
      log(`Content sections validated in ${skillName}`, 'success');
    }
    return true;
  } catch (err) {
    const error = `Error validating sections in ${skillName}: ${err.message}`;
    results.errors.push({
      skill: skillName,
      type: 'validation',
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
function validateMarkdownFormatting(filePath, skillName) {
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
        const warning = `Markdown formatting issue in ${skillName} at line ${issue.line}: ${issue.message}`;
        results.errors.push({
          skill: skillName,
          type: 'formatting',
          line: issue.line,
          message: warning
        });
        results.warnings++;
        log(warning, 'warning');
      }
    } else if (verbose) {
      log(`Markdown formatting valid in ${skillName}`, 'success');
    }
    
    return true;
  } catch (err) {
    const error = `Error validating markdown formatting in ${skillName}: ${err.message}`;
    results.errors.push({
      skill: skillName,
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
 * Validate a single skill
 */
function validateSkill(skillDir) {
  const skillPath = path.join(SKILLS_PATH, skillDir);
  const skillFilePath = path.join(skillPath, 'SKILL.md');
  
  log(`Validating skill: ${skillDir}...`, 'info');
  
  let skillValid = true;
  
  // Validate skill directory structure
  if (!validateSkillDirectory(skillDir, skillDir)) {
    return false;
  }
  
  // Check file exists
  if (!validateFileExists(skillFilePath, `${skillDir}/SKILL.md`)) {
    return false;
  }
  
  // Check file is not empty
  if (!validateFileNotEmpty(skillFilePath, `${skillDir}/SKILL.md`)) {
    return false;
  }
  
  // Validate YAML frontmatter
  if (!validateYamlFrontmatter(skillFilePath, skillDir)) {
    skillValid = false;
  }
  
  // Validate skill name matches directory name
  if (!validateSkillNameMatches(skillFilePath, skillDir, skillDir)) {
    skillValid = false;
  }
  
  // Validate required sections
  if (!validateRequiredSections(skillFilePath, skillDir)) {
    skillValid = false;
  }
  
  // Validate markdown formatting
  if (!validateMarkdownFormatting(skillFilePath, skillDir)) {
    skillValid = false;
  }
  
  if (skillValid) {
    results.passed++;
    log(`Skill ${skillDir} validation passed`, 'success');
  }
  
  return skillValid;
}

/**
 * Generate test report
 */
function generateReport() {
  console.log('\n' + '='.repeat(60));
  console.log('SKILL VALIDATION REPORT');
  console.log('='.repeat(60));
  console.log(`Total skills checked: ${results.passed + results.failed}`);
  console.log(`Passed: ${results.passed}`);
  console.log(`Failed: ${results.failed}`);
  console.log(`Warnings: ${results.warnings}`);
  console.log('='.repeat(60));
  
  if (results.errors.length > 0) {
    console.log('\nERRORS AND WARNINGS:');
    console.log('-'.repeat(60));
    results.errors.forEach((error, index) => {
      console.log(`${index + 1}. ${error.message}`);
      if (error.skill) {
        console.log(`   Skill: ${error.skill}`);
      }
      if (error.file) {
        console.log(`   File: ${error.file}`);
      }
      if (error.line) {
        console.log(`   Line: ${error.line}`);
      }
      if (error.section) {
        console.log(`   Section: ${error.section}`);
      }
      if (error.field) {
        console.log(`   Field: ${error.field}`);
      }
      console.log(`   Type: ${error.type}`);
      console.log('');
    });
  }
  
  console.log('='.repeat(60));
  
  if (results.failed === 0) {
    console.log('✓ All skill validations passed!');
    return 0;
  } else {
    console.log('✗ Skill validation failed with errors.');
    return 1;
  }
}

/**
 * Main validation function
 */
function main() {
  console.log('Skill Validation Script');
  console.log('=======================\n');
  
  // Validate skills directory
  if (!validateSkillsDirectory()) {
    return generateReport();
  }
  
  // Get all skill directories
  const skillDirs = getSkillDirectories();
  
  if (skillDirs.length === 0) {
    const warning = 'No skill directories found';
    results.errors.push({
      type: 'no-skills',
      message: warning
    });
    results.warnings++;
    log(warning, 'warning');
    return generateReport();
  }
  
  log(`Found ${skillDirs.length} skill director(y/ies)`, 'info');
  
  // Validate each skill
  for (const skillDir of skillDirs) {
    validateSkill(skillDir);
  }
  
  return generateReport();
}

// Run validation
process.exitCode = main();

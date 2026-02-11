#!/usr/bin/env node

/**
 * validate-mcp-config.js
 * 
 * Validation script for MCP configuration in the Kilo Code template project.
 * 
 * This script validates:
 * - .kilocode/mcp.json syntax
 * - Server configurations
 * - Required servers
 * - Security measures (rate limiting, permissions)
 * - Path validation rules
 * 
 * Usage:
 *   node tests/validation/validate-mcp-config.js [--verbose]
 * 
 * Exit codes:
 *   0 - All validations passed
 *   1 - Validation errors found
 */

const fs = require('fs');
const path = require('path');

// Configuration
const MCP_CONFIG_PATH = path.join(__dirname, '..', '..', '.kilocode', 'mcp.json');

// Required MCP servers
const REQUIRED_SERVERS = [
  'filesystem-projects',
  'filesystem-agentic'
];

// Optional but recommended servers
const RECOMMENDED_SERVERS = [
  'memory',
  'git',
  'github',
  'time',
  'fetch'
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
 * Validate MCP config file exists and is readable
 */
function validateConfigExists() {
  try {
    if (!fs.existsSync(MCP_CONFIG_PATH)) {
      const error = `MCP configuration file not found: ${MCP_CONFIG_PATH}`;
      results.errors.push({
        type: 'missing',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    const stats = fs.statSync(MCP_CONFIG_PATH);
    if (!stats.isFile()) {
      const error = `MCP config path is not a file: ${MCP_CONFIG_PATH}`;
      results.errors.push({
        type: 'invalid',
        message: error
      });
      results.failed++;
      log(error, 'error');
      return false;
    }
    
    log(`MCP configuration file found: ${MCP_CONFIG_PATH}`, 'success');
    return true;
  } catch (err) {
    const error = `Error accessing MCP config file: ${err.message}`;
    results.errors.push({
      type: 'access',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Validate JSON syntax
 */
function validateJsonSyntax() {
  try {
    const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
    JSON.parse(content);
    log('JSON syntax is valid', 'success');
    results.passed++;
    return true;
  } catch (err) {
    const error = `Invalid JSON syntax: ${err.message}`;
    results.errors.push({
      type: 'syntax',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
}

/**
 * Load and parse MCP configuration
 */
function loadConfig() {
  try {
    const content = fs.readFileSync(MCP_CONFIG_PATH, 'utf8');
    return JSON.parse(content);
  } catch (err) {
    return null;
  }
}

/**
 * Validate top-level structure
 */
function validateTopLevelStructure(config) {
  if (!config.mcpServers) {
    const error = 'Missing required "mcpServers" property';
    results.errors.push({
      type: 'structure',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
  
  if (typeof config.mcpServers !== 'object') {
    const error = '"mcpServers" must be an object';
    results.errors.push({
      type: 'structure',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
  
  log('Top-level structure is valid', 'success');
  results.passed++;
  return true;
}

/**
 * Validate server configuration
 */
function validateServerConfig(serverName, serverConfig) {
  const errors = [];
  
  // Check required fields
  if (!serverConfig.command) {
    errors.push('Missing "command" field');
  }
  
  if (!serverConfig.args) {
    errors.push('Missing "args" field');
  } else if (!Array.isArray(serverConfig.args)) {
    errors.push('"args" must be an array');
  }
  
  // Validate command is a string
  if (serverConfig.command && typeof serverConfig.command !== 'string') {
    errors.push('"command" must be a string');
  }
  
  // Validate description if present
  if (serverConfig.description && typeof serverConfig.description !== 'string') {
    errors.push('"description" must be a string');
  }
  
  // Validate alwaysAllow if present
  if (serverConfig.alwaysAllow && !Array.isArray(serverConfig.alwaysAllow)) {
    errors.push('"alwaysAllow" must be an array');
  }
  
  // Validate env if present
  if (serverConfig.env && typeof serverConfig.env !== 'object') {
    errors.push('"env" must be an object');
  }
  
  return errors;
}

/**
 * Validate all server configurations
 */
function validateServerConfigurations(config) {
  const servers = config.mcpServers;
  const serverNames = Object.keys(servers);
  
  if (serverNames.length === 0) {
    const error = 'No MCP servers configured';
    results.errors.push({
      type: 'servers',
      message: error
    });
    results.failed++;
    log(error, 'error');
    return false;
  }
  
  log(`Found ${serverNames.length} configured server(s)`, 'info');
  
  let allValid = true;
  for (const serverName of serverNames) {
    const serverConfig = servers[serverName];
    const errors = validateServerConfig(serverName, serverConfig);
    
    if (errors.length > 0) {
      allValid = false;
      for (const error of errors) {
        const errorMsg = `Server "${serverName}": ${error}`;
        results.errors.push({
          type: 'server-config',
          server: serverName,
          message: errorMsg
        });
        results.failed++;
        log(errorMsg, 'error');
      }
    } else {
      if (verbose) {
        log(`Server "${serverName}" configuration is valid`, 'success');
      }
      results.passed++;
    }
  }
  
  if (allValid) {
    log('All server configurations are valid', 'success');
  }
  
  return allValid;
}

/**
 * Validate required servers are present
 */
function validateRequiredServers(config) {
  const servers = config.mcpServers;
  const serverNames = Object.keys(servers);
  
  let allPresent = true;
  for (const requiredServer of REQUIRED_SERVERS) {
    if (!serverNames.includes(requiredServer)) {
      const error = `Required server "${requiredServer}" is not configured`;
      results.errors.push({
        type: 'required-server',
        server: requiredServer,
        message: error
      });
      results.failed++;
      log(error, 'error');
      allPresent = false;
    } else {
      if (verbose) {
        log(`Required server "${requiredServer}" is present`, 'success');
      }
    }
  }
  
  if (allPresent) {
    log('All required servers are present', 'success');
    results.passed++;
  }
  
  return allPresent;
}

/**
 * Check for recommended servers
 */
function validateRecommendedServers(config) {
  const servers = config.mcpServers;
  const serverNames = Object.keys(servers);
  
  for (const recommendedServer of RECOMMENDED_SERVERS) {
    if (!serverNames.includes(recommendedServer)) {
      const warning = `Recommended server "${recommendedServer}" is not configured`;
      results.errors.push({
        type: 'recommended-server',
        server: recommendedServer,
        message: warning
      });
      results.warnings++;
      log(warning, 'warning');
    } else {
      if (verbose) {
        log(`Recommended server "${recommendedServer}" is present`, 'success');
      }
    }
  }
}

/**
 * Validate security configuration
 */
function validateSecurityConfig(config) {
  if (!config.security) {
    const warning = 'No security configuration found';
    results.errors.push({
      type: 'security',
      message: warning
    });
    results.warnings++;
    log(warning, 'warning');
    return false;
  }
  
  const security = config.security;
  let securityValid = true;
  
  // Validate pathValidation
  if (security.pathValidation) {
    const pv = security.pathValidation;
    
    if (pv.enabled !== undefined && typeof pv.enabled !== 'boolean') {
      const error = 'pathValidation.enabled must be a boolean';
      results.errors.push({
        type: 'security',
        message: error
      });
      results.failed++;
      log(error, 'error');
      securityValid = false;
    }
    
    if (pv.allowedPaths && !Array.isArray(pv.allowedPaths)) {
      const error = 'pathValidation.allowedPaths must be an array';
      results.errors.push({
        type: 'security',
        message: error
      });
      results.failed++;
      log(error, 'error');
      securityValid = false;
    }
    
    if (pv.blockedPaths && !Array.isArray(pv.blockedPaths)) {
      const error = 'pathValidation.blockedPaths must be an array';
      results.errors.push({
        type: 'security',
        message: error
      });
      results.failed++;
      log(error, 'error');
      securityValid = false;
    }
  } else {
    const warning = 'pathValidation configuration not found';
    results.errors.push({
      type: 'security',
      message: warning
    });
    results.warnings++;
    log(warning, 'warning');
  }
  
  // Validate rateLimiting
  if (security.rateLimiting) {
    const rl = security.rateLimiting;
    
    if (rl.enabled !== undefined && typeof rl.enabled !== 'boolean') {
      const error = 'rateLimiting.enabled must be a boolean';
      results.errors.push({
        type: 'security',
        message: error
      });
      results.failed++;
      log(error, 'error');
      securityValid = false;
    }
    
    if (rl.maxRequestsPerMinute !== undefined && typeof rl.maxRequestsPerMinute !== 'number') {
      const error = 'rateLimiting.maxRequestsPerMinute must be a number';
      results.errors.push({
        type: 'security',
        message: error
      });
      results.failed++;
      log(error, 'error');
      securityValid = false;
    }
    
    if (rl.maxRequestsPerHour !== undefined && typeof rl.maxRequestsPerHour !== 'number') {
      const error = 'rateLimiting.maxRequestsPerHour must be a number';
      results.errors.push({
        type: 'security',
        message: error
      });
      results.failed++;
      log(error, 'error');
      securityValid = false;
    }
  } else {
    const warning = 'rateLimiting configuration not found';
    results.errors.push({
      type: 'security',
      message: warning
    });
    results.warnings++;
    log(warning, 'warning');
  }
  
  // Validate permissionControl
  if (security.permissionControl) {
    const pc = security.permissionControl;
    
    if (pc.writeOperationsRequireApproval !== undefined && typeof pc.writeOperationsRequireApproval !== 'boolean') {
      const error = 'permissionControl.writeOperationsRequireApproval must be a boolean';
      results.errors.push({
        type: 'security',
        message: error
      });
      results.failed++;
      log(error, 'error');
      securityValid = false;
    }
    
    if (pc.dangerousOperationsRequireApproval !== undefined && typeof pc.dangerousOperationsRequireApproval !== 'boolean') {
      const error = 'permissionControl.dangerousOperationsRequireApproval must be a boolean';
      results.errors.push({
        type: 'security',
        message: error
      });
      results.failed++;
      log(error, 'error');
      securityValid = false;
    }
    
    if (pc.safeReadOperations && !Array.isArray(pc.safeReadOperations)) {
      const error = 'permissionControl.safeReadOperations must be an array';
      results.errors.push({
        type: 'security',
        message: error
      });
      results.failed++;
      log(error, 'error');
      securityValid = false;
    }
  } else {
    const warning = 'permissionControl configuration not found';
    results.errors.push({
      type: 'security',
      message: warning
    });
    results.warnings++;
    log(warning, 'warning');
  }
  
  if (securityValid) {
    log('Security configuration is valid', 'success');
    results.passed++;
  }
  
  return securityValid;
}

/**
 * Validate path validation rules
 */
function validatePathValidationRules(config) {
  if (!config.security || !config.security.pathValidation) {
    return true;
  }
  
  const pv = config.security.pathValidation;
  
  if (!pv.enabled) {
    log('Path validation is disabled', 'warning');
    return true;
  }
  
  // Check that allowedPaths are valid
  if (pv.allowedPaths) {
    for (const allowedPath of pv.allowedPaths) {
      if (typeof allowedPath !== 'string') {
        const error = `Invalid allowed path: ${allowedPath}`;
        results.errors.push({
          type: 'path-validation',
          message: error
        });
        results.failed++;
        log(error, 'error');
      }
    }
  }
  
  // Check that blockedPaths are valid
  if (pv.blockedPaths) {
    for (const blockedPath of pv.blockedPaths) {
      if (typeof blockedPath !== 'string') {
        const error = `Invalid blocked path: ${blockedPath}`;
        results.errors.push({
          type: 'path-validation',
          message: error
        });
        results.failed++;
        log(error, 'error');
      }
    }
  }
  
  log('Path validation rules are valid', 'success');
  results.passed++;
  return true;
}

/**
 * Validate environment variable references
 */
function validateEnvironmentVariables(config) {
  const servers = config.mcpServers;
  let hasEnvVars = false;
  
  for (const [serverName, serverConfig] of Object.entries(servers)) {
    if (serverConfig.env) {
      hasEnvVars = true;
      for (const [key, value] of Object.entries(serverConfig.env)) {
        if (typeof value !== 'string') {
          const error = `Environment variable "${key}" in server "${serverName}" must be a string`;
          results.errors.push({
            type: 'env-var',
            server: serverName,
            message: error
          });
          results.failed++;
          log(error, 'error');
        } else if (!value.startsWith('${') || !value.endsWith('}')) {
          const warning = `Environment variable "${key}" in server "${serverName}" should use ${VAR} syntax`;
          results.errors.push({
            type: 'env-var',
            server: serverName,
            message: warning
          });
          results.warnings++;
          log(warning, 'warning');
        }
      }
    }
  }
  
  if (hasEnvVars) {
    log('Environment variable references validated', 'success');
    results.passed++;
  }
  
  return true;
}

/**
 * Generate test report
 */
function generateReport() {
  console.log('\n' + '='.repeat(60));
  console.log('MCP CONFIGURATION VALIDATION REPORT');
  console.log('='.repeat(60));
  console.log(`Passed: ${results.passed}`);
  console.log(`Failed: ${results.failed}`);
  console.log(`Warnings: ${results.warnings}`);
  console.log('='.repeat(60));
  
  if (results.errors.length > 0) {
    console.log('\nERRORS AND WARNINGS:');
    console.log('-'.repeat(60));
    results.errors.forEach((error, index) => {
      console.log(`${index + 1}. ${error.message}`);
      if (error.server) {
        console.log(`   Server: ${error.server}`);
      }
      console.log(`   Type: ${error.type}`);
      console.log('');
    });
  }
  
  console.log('='.repeat(60));
  
  if (results.failed === 0) {
    console.log('✓ All MCP configuration validations passed!');
    return 0;
  } else {
    console.log('✗ MCP configuration validation failed with errors.');
    return 1;
  }
}

/**
 * Main validation function
 */
function main() {
  console.log('MCP Configuration Validation Script');
  console.log('====================================\n');
  
  // Validate config file exists
  if (!validateConfigExists()) {
    return generateReport();
  }
  
  // Validate JSON syntax
  if (!validateJsonSyntax()) {
    return generateReport();
  }
  
  // Load configuration
  const config = loadConfig();
  if (!config) {
    return generateReport();
  }
  
  // Validate top-level structure
  validateTopLevelStructure(config);
  
  // Validate server configurations
  validateServerConfigurations(config);
  
  // Validate required servers
  validateRequiredServers(config);
  
  // Validate recommended servers
  validateRecommendedServers(config);
  
  // Validate security configuration
  validateSecurityConfig(config);
  
  // Validate path validation rules
  validatePathValidationRules(config);
  
  // Validate environment variables
  validateEnvironmentVariables(config);
  
  return generateReport();
}

// Run validation
process.exitCode = main();

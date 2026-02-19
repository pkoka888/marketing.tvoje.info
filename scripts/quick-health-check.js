#!/usr/bin/env node
/**
 * Quick Health Check Script
 * Runs all verification checks for the project
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function check(description, fn) {
  process.stdout.write(`  ${description}... `);
  try {
    fn();
    log('✅', 'green');
    return true;
  } catch (error) {
    log('❌', 'red');
    if (error.message) {
      console.log(`     ${colors.red}${error.message}${colors.reset}`);
    }
    return false;
  }
}

function runCommand(cmd, options = {}) {
  try {
    return execSync(cmd, { encoding: 'utf8', stdio: 'pipe', ...options });
  } catch (error) {
    throw new Error(error.stderr || error.message);
  }
}

// Main checks
const checks = {
  memoryBank: () => {
    const required = ['brief.md', 'product.md', 'context.md', 'architecture.md', 'tech.md'];
    const basePath = path.join('.kilocode', 'rules', 'memory-bank');
    for (const file of required) {
      if (!fs.existsSync(path.join(basePath, file))) {
        throw new Error(`Missing: ${file}`);
      }
    }
  },

  mcpConfig: () => {
    const configPath = path.join('.kilocode', 'mcp.json');
    if (!fs.existsSync(configPath)) {
      throw new Error('MCP config not found');
    }
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    if (!config.mcpServers || Object.keys(config.mcpServers).length === 0) {
      throw new Error('No MCP servers configured');
    }
  },

  envFile: () => {
    if (!fs.existsSync('.env')) {
      throw new Error('.env file not found');
    }
  },

  nodeModules: () => {
    if (!fs.existsSync('node_modules')) {
      throw new Error('node_modules not found. Run: npm install');
    }
  },

  gitConfig: () => {
    const autocrlf = runCommand('git config core.autocrlf').trim();
    if (autocrlf !== 'false') {
      throw new Error(`core.autocrlf is "${autocrlf}", should be "false"`);
    }
  },

  packageJson: () => {
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    if (!pkg.scripts || !pkg.scripts.build) {
      throw new Error('No build script in package.json');
    }
  },

  verifyScript: () => {
    const scriptPath = path.join('scripts', 'verify_agentic_platform.py');
    if (!fs.existsSync(scriptPath)) {
      throw new Error('verify_agentic_platform.py not found');
    }
  },

  mcpWrapper: () => {
    const wrapperPath = path.join('.kilocode', 'mcp-servers', 'mcp-wrapper.js');
    if (!fs.existsSync(wrapperPath)) {
      throw new Error('mcp-wrapper.js not found');
    }
  },
};

// Main function
function main() {
  log('\n🏥 Quick Health Check', 'cyan');
  log('═'.repeat(50), 'cyan');

  let passed = 0;
  let failed = 0;

  // Memory Bank
  log('\n📚 Memory Bank:', 'blue');
  if (check('All required files present', checks.memoryBank)) passed++;
  else failed++;

  // Configuration
  log('\n⚙️  Configuration:', 'blue');
  if (check('MCP config valid', checks.mcpConfig)) passed++;
  else failed++;
  if (check('.env file exists', checks.envFile)) passed++;
  else failed++;
  if (check('package.json valid', checks.packageJson)) passed++;
  else failed++;

  // Dependencies
  log('\n📦 Dependencies:', 'blue');
  if (check('node_modules installed', checks.nodeModules)) passed++;
  else failed++;
  if (check('MCP wrapper script exists', checks.mcpWrapper)) passed++;
  else failed++;

  // Git
  log('\n🌿 Git Configuration:', 'blue');
  if (check('core.autocrlf is false', checks.gitConfig)) passed++;
  else failed++;

  // Scripts
  log('\n🔧 Scripts:', 'blue');
  if (check('Platform verification script exists', checks.verifyScript)) passed++;
  else failed++;

  // Summary
  log('\n' + '═'.repeat(50), 'cyan');
  log(`📊 Results: ${passed} passed, ${failed} failed`, 'cyan');

  if (failed === 0) {
    log('\n✅ All health checks passed!', 'green');
    log('\n💡 Next steps:', 'yellow');
    log('   - Run: node scripts/verify-mcp-servers.js', 'reset');
    log('   - Run: python scripts/verify_agentic_platform.py', 'reset');
    return 0;
  } else {
    log('\n❌ Some health checks failed', 'red');
    return 1;
  }
}

process.exit(main());

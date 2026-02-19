#!/usr/bin/env node
/**
 * Consolidated MCP Fix Script
 * Fixes path issues and validates MCP configurations
 *
 * Usage: node scripts/fix-mcp-paths.js [--check-only]
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
  cyan: '\x1b[36m',
  gray: '\x1b[90m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// Files to fix
const configFiles = [
  '.kilocode/mcp.json',
  '.clinerules/mcp.json',
  '.antigravity/mcp.json',
  'opencode.json',
  '.kilocode/mcp-servers/mcp-wrapper.js',
];

// Path conversions
const conversions = [
  { from: /\/c\//g, to: 'C:/' },
  { from: /\/{2,}/g, to: '/' }, // Fix double slashes
];

function fixFile(filePath) {
  const fullPath = path.join(process.cwd(), filePath);

  if (!fs.existsSync(fullPath)) {
    log(`  ⚠️  Not found: ${filePath}`, 'yellow');
    return { fixed: false, exists: false };
  }

  let content = fs.readFileSync(fullPath, 'utf8');
  let modified = false;

  for (const conversion of conversions) {
    if (conversion.from.test(content)) {
      content = content.replace(conversion.from, conversion.to);
      modified = true;
    }
  }

  if (modified) {
    fs.writeFileSync(fullPath, content, 'utf8');
    log(`  ✅ Fixed: ${filePath}`, 'green');
    return { fixed: true, exists: true };
  } else {
    log(`  ⏭️  No changes: ${filePath}`, 'gray');
    return { fixed: false, exists: true };
  }
}

function checkOnly() {
  log('\n🔍 Checking MCP Configuration Files', 'cyan');
  log('═'.repeat(50), 'cyan');

  let issuesFound = 0;

  for (const file of configFiles) {
    const fullPath = path.join(process.cwd(), file);

    if (!fs.existsSync(fullPath)) {
      log(`  ❌ Missing: ${file}`, 'red');
      issuesFound++;
      continue;
    }

    const content = fs.readFileSync(fullPath, 'utf8');
    const hasWrongPaths = /\/c\//.test(content);

    if (hasWrongPaths) {
      log(`  ⚠️  Issues found in: ${file}`, 'yellow');

      // Show first few issues
      const lines = content.split('\n');
      lines.forEach((line, index) => {
        if (/\/c\//.test(line)) {
          log(`     Line ${index + 1}: ${line.trim().substring(0, 60)}...`, 'gray');
        }
      });

      issuesFound++;
    } else {
      log(`  ✅ OK: ${file}`, 'green');
    }
  }

  log('\n' + '═'.repeat(50), 'cyan');
  if (issuesFound > 0) {
    log(`⚠️  Found issues in ${issuesFound} file(s)`, 'yellow');
    log('Run without --check-only to fix', 'cyan');
    return 1;
  } else {
    log('✅ All files look good!', 'green');
    return 0;
  }
}

function fixAll() {
  log('\n🔧 Fixing MCP Path Issues', 'cyan');
  log('═'.repeat(50), 'cyan');
  log('Converting /c/ paths to C:/ format for Node compatibility\n', 'gray');

  let fixed = 0;
  let unchanged = 0;
  let missing = 0;

  for (const file of configFiles) {
    const result = fixFile(file);
    if (result.fixed) fixed++;
    else if (result.exists) unchanged++;
    else missing++;
  }

  log('\n' + '═'.repeat(50), 'cyan');
  log(`📊 Results: ${fixed} fixed, ${unchanged} unchanged, ${missing} missing`, 'cyan');

  if (fixed > 0) {
    log('\n✅ Path fixes applied!', 'green');
    log('\n💡 Next steps:', 'yellow');
    log('   1. Restart your IDE to reload MCP configs', 'reset');
    log('   2. Run: node scripts/verify-mcp-servers.js', 'reset');
    log('   3. Test MCP tools in your IDE', 'reset');
  }

  return 0;
}

function main() {
  const args = process.argv.slice(2);
  const checkOnlyFlag = args.includes('--check-only');

  if (checkOnlyFlag) {
    return checkOnly();
  } else {
    return fixAll();
  }
}

process.exit(main());

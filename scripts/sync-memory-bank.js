#!/usr/bin/env node

/**
 * sync-memory-bank.js
 * 
 * Validates and synchronizes the Memory Bank structure (.kilocode/rules/memory-bank).
 * Used by Antigravity and Kilo to ensure knowledge base consistency.
 */

const fs = require('fs');
const path = require('path');

// Configuration
const PROJECT_ROOT = path.resolve(__dirname, '..');
const MEMORY_BANK_DIR = path.join(PROJECT_ROOT, '.kilocode', 'rules', 'memory-bank');
const CORE_FILES = ['brief.md', 'product.md', 'context.md', 'architecture.md', 'tech.md'];

console.log('Memory Bank Sync & Validation Tool');
console.log('==================================');
console.log(`Target: ${MEMORY_BANK_DIR}\n`);

// 1. Check Directory Existence
if (!fs.existsSync(MEMORY_BANK_DIR)) {
  console.log('❌ Memory Bank directory missing.');
  console.log('   Run "kilo run \'Initialize Memory Bank\'" to create it via Kilo,');
  console.log('   or use the template in .kilocode/templates if available.');
  process.exit(1);
} else {
  console.log('✅ Memory Bank directory exists.');
}

// 2. Validate Core Files
let missingFiles = [];
let emptyFiles = [];

CORE_FILES.forEach(file => {
  const filePath = path.join(MEMORY_BANK_DIR, file);
  if (!fs.existsSync(filePath)) {
    missingFiles.push(file);
  } else {
    const content = fs.readFileSync(filePath, 'utf8');
    if (content.trim().length === 0) {
      emptyFiles.push(file);
    }
  }
});

if (missingFiles.length > 0) {
  console.log('❌ Missing Core Files:', missingFiles.join(', '));
} else {
  console.log('✅ All core files present.');
}

if (emptyFiles.length > 0) {
  console.log('⚠️  Empty Files:', emptyFiles.join(', '));
}

// 3. Validation Logic (Simplified from test-memory-bank.js)
const contextPath = path.join(MEMORY_BANK_DIR, 'context.md');
if (fs.existsSync(contextPath)) {
  const content = fs.readFileSync(contextPath, 'utf8');
  const requiredSections = ['## Current State', '## Recent Changes', '## Next Steps'];
  const missingSections = requiredSections.filter(s => !content.includes(s));
  
  if (missingSections.length > 0) {
    console.log(`❌ context.md is missing sections: ${missingSections.join(', ')}`);
  } else {
    console.log('✅ context.md structure is valid.');
  }
}

// 4. Summary
const status = (missingFiles.length === 0 && emptyFiles.length === 0) ? 'HEALTHY' : 'NEEDS ATTENTION';
console.log(`\nMemory Bank Status: [${status}]`);

if (status === 'HEALTHY') {
    // Determine active context mode
    console.log('\n[Memory Bank: Active] - Ready for Agent use.');
} else {
    process.exit(1);
}

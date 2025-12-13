#!/usr/bin/env node
/**
 * Firebase Helper CLI
 *
 * Quick helper commands for Firebase operations
 *
 * Usage:
 *   node scripts/firebase-helper.js sync           # Sync with diff and history
 *   node scripts/firebase-helper.js upload         # Full upload (all data)
 *   node scripts/firebase-helper.js validate       # Validated push
 *   node scripts/firebase-helper.js test           # Test sync locally
 *   node scripts/firebase-helper.js help           # Show this help
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

const { spawn } = require('child_process');
const path = require('path');

// Colors
const c = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

const SCRIPTS_DIR = __dirname;

/**
 * Run a script and stream output
 */
function runScript(scriptPath, args = []) {
  return new Promise((resolve, reject) => {
    console.log(`${c.dim}Running: node ${path.basename(scriptPath)} ${args.join(' ')}${c.reset}\n`);

    const child = spawn('node', [scriptPath, ...args], {
      stdio: 'inherit',
      shell: true
    });

    child.on('close', (code) => {
      if (code === 0) {
        resolve(code);
      } else {
        reject(new Error(`Script exited with code ${code}`));
      }
    });

    child.on('error', (error) => {
      reject(error);
    });
  });
}

/**
 * Show help
 */
function showHelp() {
  console.log('═'.repeat(80));
  console.log(`${c.bright}${c.cyan}  Firebase Helper - Quick Commands${c.reset}`);
  console.log('═'.repeat(80));
  console.log();
  console.log(`${c.bright}Available commands:${c.reset}`);
  console.log();
  console.log(`  ${c.green}sync${c.reset}       Sync theory constants with diff and version history`);
  console.log(`             ${c.dim}→ Runs: firebase-sync-with-history.js${c.reset}`);
  console.log();
  console.log(`  ${c.green}upload${c.reset}     Full upload (theory constants, formulas, pages)`);
  console.log(`             ${c.dim}→ Runs: firebase-upload-all.js${c.reset}`);
  console.log();
  console.log(`  ${c.green}validate${c.reset}   Validated push with OOM checks and derivation validation`);
  console.log(`             ${c.dim}→ Runs: firebase-push-validated.js${c.reset}`);
  console.log();
  console.log(`  ${c.green}test${c.reset}       Test sync logic locally (no Firebase connection)`);
  console.log(`             ${c.dim}→ Runs: test-firebase-sync.js${c.reset}`);
  console.log();
  console.log(`  ${c.green}help${c.reset}       Show this help message`);
  console.log();
  console.log('─'.repeat(80));
  console.log(`${c.bright}Examples:${c.reset}`);
  console.log();
  console.log(`  ${c.cyan}node scripts/firebase-helper.js sync${c.reset}`);
  console.log(`  ${c.dim}# Syncs theory constants, shows diff, backs up to history${c.reset}`);
  console.log();
  console.log(`  ${c.cyan}node scripts/firebase-helper.js sync --force${c.reset}`);
  console.log(`  ${c.dim}# Same as above, but shows ALL changes (detailed output)${c.reset}`);
  console.log();
  console.log(`  ${c.cyan}node scripts/firebase-helper.js validate${c.reset}`);
  console.log(`  ${c.dim}# Full validation + sync (production-ready push)${c.reset}`);
  console.log();
  console.log(`  ${c.cyan}node scripts/firebase-helper.js test${c.reset}`);
  console.log(`  ${c.dim}# Test sync locally without connecting to Firebase${c.reset}`);
  console.log();
  console.log('─'.repeat(80));
  console.log(`${c.bright}What each command does:${c.reset}`);
  console.log();
  console.log(`${c.yellow}sync${c.reset}       - Reads theory-constants-enhanced.js`);
  console.log(`           - Fetches current Firebase data`);
  console.log(`           - Shows detailed diff (added/removed/changed)`);
  console.log(`           - Backs up current data to history/backups/`);
  console.log(`           - Updates Firebase if changes detected`);
  console.log();
  console.log(`${c.yellow}upload${c.reset}     - Syncs theory constants (with diff and history)`);
  console.log(`           - Uploads formulas from formula-definitions.js`);
  console.log(`           - Uploads page content from HTML files`);
  console.log(`           - Creates validation history entry`);
  console.log();
  console.log(`${c.yellow}validate${c.reset}   - Validates derivation chains`);
  console.log(`           - Checks OOM accuracy for critical parameters`);
  console.log(`           - Shows diff of all changes`);
  console.log(`           - Requires confirmation before pushing`);
  console.log(`           - Syncs with version history`);
  console.log();
  console.log(`${c.yellow}test${c.reset}       - Tests sync logic without Firebase`);
  console.log(`           - Verifies theory-constants-enhanced.js loads correctly`);
  console.log(`           - Tests diff algorithm`);
  console.log(`           - Safe to run anytime (no side effects)`);
  console.log();
  console.log('═'.repeat(80));
  console.log();
}

/**
 * Main function
 */
async function main() {
  const command = process.argv[2];
  const extraArgs = process.argv.slice(3);

  if (!command || command === 'help' || command === '--help' || command === '-h') {
    showHelp();
    process.exit(0);
  }

  try {
    switch (command) {
      case 'sync':
        await runScript(
          path.join(SCRIPTS_DIR, 'firebase-sync-with-history.js'),
          extraArgs
        );
        break;

      case 'upload':
        await runScript(
          path.join(SCRIPTS_DIR, 'firebase-upload-all.js'),
          extraArgs
        );
        break;

      case 'validate':
        await runScript(
          path.join(SCRIPTS_DIR, 'firebase-push-validated.js'),
          extraArgs
        );
        break;

      case 'test':
        await runScript(
          path.join(SCRIPTS_DIR, 'test-firebase-sync.js'),
          extraArgs
        );
        break;

      default:
        console.error(`${c.red}Error: Unknown command '${command}'${c.reset}\n`);
        console.log(`Run ${c.cyan}node scripts/firebase-helper.js help${c.reset} for available commands.\n`);
        process.exit(1);
    }

    console.log();
    console.log(`${c.green}${c.bright}✓ Command completed successfully${c.reset}`);
    process.exit(0);

  } catch (error) {
    console.error();
    console.error(`${c.red}${c.bright}✗ Command failed${c.reset}`);
    console.error(`${c.red}Error: ${error.message}${c.reset}`);
    process.exit(1);
  }
}

main();

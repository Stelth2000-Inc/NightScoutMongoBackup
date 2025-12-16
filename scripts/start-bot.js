#!/usr/bin/env node
/**
 * PM2 wrapper script for starting the NightScout Backup Bot.
 * This wrapper allows PM2 to properly track version metadata.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

// Create a package.json in the scripts directory for PM2 to read version from
const packageJsonPath = path.resolve(__dirname, 'package.json');
const botPackageJson = require('./package-bot.json');
fs.writeFileSync(packageJsonPath, JSON.stringify(botPackageJson, null, 2));

// Read bot version
function getBotVersion() {
  try {
    const scriptPath = path.resolve(__dirname, 'get_version.js');
    const result = spawnSync('node', [scriptPath, 'bot'], {
      encoding: 'utf8',
      cwd: path.resolve(__dirname, '..')
    });
    if (result.error || result.status !== 0) {
      return 'unknown';
    }
    return result.stdout.trim() || 'unknown';
  } catch (error) {
    return 'unknown';
  }
}

const version = getBotVersion();
console.log(`Starting NightScout Backup Bot v${version}`);

// Spawn poetry process
const poetryProcess = spawn('poetry', ['run', 'nightscout-backup-bot'], {
  stdio: 'inherit',
  cwd: path.resolve(__dirname, '..'),
  env: { ...process.env, VERSION: version }
});

poetryProcess.on('exit', (code) => {
  process.exit(code || 0);
});

poetryProcess.on('error', (error) => {
  console.error('Failed to start bot:', error);
  process.exit(1);
});


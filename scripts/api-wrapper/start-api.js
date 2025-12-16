#!/usr/bin/env node
/**
 * PM2 wrapper script for starting the NightScout Backup API.
 * This wrapper allows PM2 to properly track version metadata.
 */

const { spawn } = require('child_process');
const path = require('path');
const { spawnSync } = require('child_process');

// PM2 will read version from package.json in this directory

// Read API version
function getApiVersion() {
  try {
    const scriptPath = path.resolve(__dirname, '..', 'get_version.js');
    const result = spawnSync('node', [scriptPath, 'api'], {
      encoding: 'utf8',
      cwd: path.resolve(__dirname, '../..')
    });
    if (result.error || result.status !== 0) {
      return 'unknown';
    }
    return result.stdout.trim() || 'unknown';
  } catch (error) {
    return 'unknown';
  }
}

// Sync version from Python __init__.py to package.json on startup (silently)
try {
  const syncScriptPath = path.resolve(__dirname, '..', 'sync_versions.js');
  spawnSync('node', [syncScriptPath], {
    encoding: 'utf8',
    cwd: path.resolve(__dirname, '../..'),
    stdio: 'pipe' // Suppress output
  });
} catch (error) {
  // Ignore sync errors - use existing package.json
}

const version = getApiVersion();
console.log(`Starting NightScout Backup API v${version}`);

// Spawn poetry process
const poetryProcess = spawn('poetry', ['run', 'nightscout-backup-api'], {
  stdio: 'inherit',
  cwd: path.resolve(__dirname, '../..'),
  env: { ...process.env, VERSION: version }
});

poetryProcess.on('exit', (code) => {
  process.exit(code || 0);
});

poetryProcess.on('error', (error) => {
  console.error('Failed to start API:', error);
  process.exit(1);
});


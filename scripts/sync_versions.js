#!/usr/bin/env node
/**
 * Script to sync versions from Python __init__.py files to wrapper package.json files.
 * This ensures the wrapper package.json files always match the Python versions.
 *
 * Usage:
 *   node scripts/sync_versions.js
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function getVersion(app) {
  try {
    const scriptPath = path.resolve(__dirname, 'get_version.js');
    const result = spawnSync('node', [scriptPath, app], {
      encoding: 'utf8',
      cwd: path.resolve(__dirname, '..')
    });
    if (result.error || result.status !== 0) {
      console.error(`Error reading ${app} version:`, result.error || result.stderr);
      return null;
    }
    return result.stdout.trim();
  } catch (error) {
    console.error(`Error reading ${app} version:`, error.message);
    return null;
  }
}

function updatePackageJson(wrapperDir, appName, version) {
  const packageJsonPath = path.resolve(__dirname, wrapperDir, 'package.json');
  const packageJson = {
    name: appName,
    version: version
  };

  try {
    fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2) + '\n');
    console.log(`✅ Updated ${wrapperDir}/package.json → version ${version}`);
    return true;
  } catch (error) {
    console.error(`❌ Error updating ${packageJsonPath}:`, error.message);
    return false;
  }
}

console.log('🔄 Syncing versions from Python __init__.py files to wrapper package.json files...\n');

// Get versions from Python files
const botVersion = getVersion('bot');
const apiVersion = getVersion('api');

if (!botVersion || !apiVersion) {
  console.error('❌ Failed to read versions from Python files');
  process.exit(1);
}

// Update wrapper package.json files
const botUpdated = updatePackageJson('bot-wrapper', 'nightscout-backup-bot', botVersion);
const apiUpdated = updatePackageJson('api-wrapper', 'nightscout-backup-api', apiVersion);

if (botUpdated && apiUpdated) {
  console.log('\n✅ Version sync completed successfully!');
  console.log(`   Bot: ${botVersion}`);
  console.log(`   API: ${apiVersion}`);
  process.exit(0);
} else {
  console.error('\n❌ Version sync failed');
  process.exit(1);
}


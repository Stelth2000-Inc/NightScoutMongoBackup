#!/usr/bin/env node
/**
 * Script to read version from Python __init__.py files.
 *
 * Usage:
 *   node scripts/get_version.js bot    # Returns bot version
 *   node scripts/get_version.js api    # Returns API version
 */

const fs = require('fs');
const path = require('path');

const app = process.argv[2];

if (!app || (app !== 'bot' && app !== 'api')) {
  console.error('Usage: node scripts/get_version.js [bot|api]');
  process.exit(1);
}

let versionFile;
if (app === 'bot') {
  versionFile = path.resolve(__dirname, '..', 'src', 'nightscout_backup_bot', '__init__.py');
} else {
  versionFile = path.resolve(__dirname, '..', 'src', 'nightscout_backup_bot', 'api', '__init__.py');
}

try {
  const content = fs.readFileSync(versionFile, 'utf8');
  // Match __version__ = "x.x.x" or __version__ = 'x.x.x'
  const match = content.match(/__version__\s*=\s*["']([^"']+)["']/);

  if (match && match[1]) {
    console.log(match[1]);
  } else {
    console.error(`Could not find version in ${versionFile}`);
    process.exit(1);
  }
} catch (error) {
  console.error(`Error reading version file: ${error.message}`);
  process.exit(1);
}


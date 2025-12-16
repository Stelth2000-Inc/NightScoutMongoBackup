#!/usr/bin/env node
/**
 * Custom semantic-release plugin to update Python version files.
 * Supports separate versioning for bot and API based on commit message prefixes.
 * 
 * Commit message prefixes:
 * - "bot:" or "feat(bot):" or "fix(bot):" etc. → bumps bot version
 * - "api:" or "feat(api):" or "fix(api):" etc. → bumps API version
 * - No prefix → bumps both versions
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * Read current version from Python __init__.py file
 */
function readPythonVersion(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const match = content.match(/__version__\s*=\s*["']([^"']+)["']/);
    return match ? match[1] : null;
  } catch (error) {
    return null;
  }
}

/**
 * Update version in Python __init__.py file
 */
function updatePythonVersion(filePath, newVersion) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    content = content.replace(
      /__version__\s*=\s*["'][^"']+["']/,
      `__version__ = "${newVersion}"`
    );
    fs.writeFileSync(filePath, content, 'utf8');
    return true;
  } catch (error) {
    console.error(`Error updating ${filePath}:`, error.message);
    return false;
  }
}

/**
 * Update version in pyproject.toml
 */
function updatePyprojectVersion(filePath, newVersion) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    content = content.replace(
      /^version\s*=\s*["'][^"']+["']/m,
      `version = "${newVersion}"`
    );
    fs.writeFileSync(filePath, content, 'utf8');
    return true;
  } catch (error) {
    console.error(`Error updating ${filePath}:`, error.message);
    return false;
  }
}

/**
 * Determine which components to bump based on commits
 */
function analyzeCommits(commits) {
  const hasBotCommits = commits.some(commit => 
    commit.message.match(/^(bot|feat\(bot\)|fix\(bot\)|perf\(bot\)|refactor\(bot\))/i)
  );
  const hasApiCommits = commits.some(commit =>
    commit.message.match(/^(api|feat\(api\)|fix\(api\)|perf\(api\)|refactor\(api\))/i)
  );
  
  return {
    bumpBot: hasBotCommits || (!hasBotCommits && !hasApiCommits),
    bumpApi: hasApiCommits || (!hasBotCommits && !hasApiCommits)
  };
}

/**
 * Calculate next version based on release type
 */
function calculateNextVersion(currentVersion, releaseType) {
  const [major, minor, patch] = currentVersion.split('.').map(Number);
  
  switch (releaseType) {
    case 'major':
      return `${major + 1}.0.0`;
    case 'minor':
      return `${major}.${minor + 1}.0`;
    case 'patch':
      return `${major}.${minor}.${patch + 1}`;
    default:
      return currentVersion;
  }
}

/**
 * Sync wrapper package.json files
 */
function syncWrapperVersions(botVersion, apiVersion) {
  try {
    const { spawnSync } = require('child_process');
    const syncScriptPath = path.resolve(__dirname, 'sync_versions.js');
    const result = spawnSync('node', [syncScriptPath], {
      encoding: 'utf8',
      cwd: path.resolve(__dirname, '..'),
      stdio: 'pipe'
    });
    return result.status === 0;
  } catch (error) {
    console.error('Error syncing wrapper versions:', error.message);
    return false;
  }
}

// Semantic-release plugin structure
async function prepare(pluginConfig, context) {
  const { logger, commits, nextRelease } = context;
  const { botVersionFile, apiVersionFile, pyprojectFile } = pluginConfig;
  
  logger.log('Updating Python version files...');
  
  // Read current versions
  const currentBotVersion = readPythonVersion(botVersionFile);
  const currentApiVersion = readPythonVersion(apiVersionFile);
  
  if (!currentBotVersion || !currentApiVersion) {
    throw new Error('Could not read current versions from Python files');
  }
  
  logger.log(`Current bot version: ${currentBotVersion}`);
  logger.log(`Current API version: ${currentApiVersion}`);
  
  // Determine which components to bump
  const { bumpBot, bumpApi } = analyzeCommits(commits);
  const releaseType = nextRelease.type; // 'major', 'minor', or 'patch'
  
  let botVersion = currentBotVersion;
  let apiVersion = currentApiVersion;
  
  // Calculate new versions
  if (bumpBot) {
    botVersion = calculateNextVersion(currentBotVersion, releaseType);
    logger.log(`Bumping bot version: ${currentBotVersion} → ${botVersion}`);
  }
  
  if (bumpApi) {
    apiVersion = calculateNextVersion(currentApiVersion, releaseType);
    logger.log(`Bumping API version: ${currentApiVersion} → ${apiVersion}`);
  }
  
  // Update Python files
  if (bumpBot) {
    if (!updatePythonVersion(botVersionFile, botVersion)) {
      throw new Error(`Failed to update bot version in ${botVersionFile}`);
    }
    logger.log(`✅ Updated ${botVersionFile} to ${botVersion}`);
    
    // Update pyproject.toml to match bot version
    if (pyprojectFile && fs.existsSync(pyprojectFile)) {
      if (!updatePyprojectVersion(pyprojectFile, botVersion)) {
        throw new Error(`Failed to update pyproject.toml`);
      }
      logger.log(`✅ Updated ${pyprojectFile} to ${botVersion}`);
    }
  }
  
  if (bumpApi) {
    if (!updatePythonVersion(apiVersionFile, apiVersion)) {
      throw new Error(`Failed to update API version in ${apiVersionFile}`);
    }
    logger.log(`✅ Updated ${apiVersionFile} to ${apiVersion}`);
  }
  
  // Sync wrapper package.json files
  logger.log('Syncing wrapper package.json files...');
  if (!syncWrapperVersions(botVersion, apiVersion)) {
    logger.warn('Warning: Failed to sync wrapper package.json files');
  } else {
    logger.log('✅ Synced wrapper package.json files');
  }
  
  return {
    botVersion,
    apiVersion,
    version: botVersion // Return bot version as primary version for semantic-release
  };
}

module.exports = { prepare };

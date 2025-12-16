// PM2 ecosystem configuration for development
//
// You have two options for running the API server:
//
// Option 1: Run API in the same process as the bot (recommended for simplicity)
//   - Set ENABLE_API_IN_BOT=true in your .env file
//   - Only start the 'nightscout-backup-bot' process
//   - The API will run in a background thread
//
// Option 2: Run API as a separate process (recommended for production)
//   - Set ENABLE_API_IN_BOT=false (or omit it)
//   - Start both 'nightscout-backup-bot' and 'nightscout-backup-api' processes
//   - Better isolation and independent scaling

const path = require('path');
const { spawnSync } = require('child_process');

// Read versions from Python __init__.py files
function getVersion(app) {
  try {
    // Validate app parameter to prevent command injection
    if (app !== 'bot' && app !== 'api') {
      console.error(`Invalid app parameter: ${app}. Must be 'bot' or 'api'.`);
      return 'unknown';
    }
    const scriptPath = path.resolve(__dirname, 'scripts', 'get_version.js');
    // Use spawnSync with separate arguments to prevent command injection
    const result = spawnSync('node', [scriptPath, app], {
      encoding: 'utf8',
      cwd: __dirname
    });
    if (result.error) {
      throw result.error;
    }
    if (result.status !== 0) {
      throw new Error(`Script exited with code ${result.status}`);
    }
    const version = result.stdout.trim();
    return version || 'unknown';
  } catch (error) {
    console.error(`Error reading ${app} version:`, error.message);
    return 'unknown';
  }
}

const botVersion = getVersion('bot');
const apiVersion = getVersion('api');

module.exports = {
  apps: [
    {
      name: 'nightscout-backup-bot',
      script: path.resolve(__dirname, 'scripts', 'bot-wrapper', 'start-bot.js'),
      cwd: path.resolve(__dirname),
      exec_mode: 'fork',
      interpreter: 'node',
      watch: ['src/'],
      instances: 1,
      autorestart: true,
      max_memory_restart: '500M',
      error_file: './logs/error.log',
      out_file: './logs/output.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      version_metadata: true,
      version: botVersion,  // Set version directly for PM2 metadata
      env: {
        NODE_ENV: 'development',
        watch: ['src/'],
        ENABLE_API_IN_BOT: 'false',
        VERSION: botVersion,
        // Add other development environment variables here
      }
    },
    {
      name: 'nightscout-backup-api',
      script: path.resolve(__dirname, 'scripts', 'start-api.js'),
      cwd: path.resolve(__dirname),
      exec_mode: 'fork',
      interpreter: 'node',
      watch: ['src/'],
      instances: 1,
      autorestart: true,
      error_file: './logs/api-error.log',
      out_file: './logs/api-output.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      version_metadata: true,
      version: apiVersion,  // Set version directly for PM2 metadata
      env: {
        NODE_ENV: 'development',
        VERSION: apiVersion,
      }
    }
  ]
};

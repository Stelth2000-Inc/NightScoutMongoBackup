# Version Synchronization Guide

## Overview

The Python applications (bot and API) maintain their versions in `__init__.py` files:
- Bot: `src/nightscout_backup_bot/__init__.py`
- API: `src/nightscout_backup_bot/api/__init__.py`

PM2 wrapper scripts need `package.json` files in their directories to display versions correctly:
- Bot: `scripts/bot-wrapper/package.json`
- API: `scripts/api-wrapper/package.json`

## Syncing Versions

When you update versions in the Python `__init__.py` files, run the sync script to update the wrapper `package.json` files:

```bash
npm run sync-versions
# or
node scripts/sync_versions.js
```

This script:
1. Reads versions from Python `__init__.py` files
2. Updates the corresponding `package.json` files in wrapper directories
3. Ensures PM2 displays the correct versions

## Workflow

### When Updating Versions:

1. **Update Python versions** in `__init__.py` files:
   ```python
   # src/nightscout_backup_bot/__init__.py
   __version__ = "2.1.0"  # Bot version
   
   # src/nightscout_backup_bot/api/__init__.py
   __version__ = "1.1.0"  # API version
   ```

2. **Update pyproject.toml** (if needed):
   ```toml
   [tool.poetry]
   version = "2.1.0"  # Should match bot version
   ```

3. **Sync wrapper package.json files**:
   ```bash
   npm run sync-versions
   ```

4. **Commit all changes together**:
   ```bash
   git add src/nightscout_backup_bot/__init__.py
   git add src/nightscout_backup_bot/api/__init__.py
   git add scripts/bot-wrapper/package.json
   git add scripts/api-wrapper/package.json
   git add pyproject.toml  # if updated
   git commit -m "chore: bump versions to 2.1.0 (bot) and 1.1.0 (api)"
   ```

## Automatic Sync

The wrapper scripts (`start-bot.js` and `start-api.js`) will automatically sync versions when they start, ensuring PM2 always has the correct version even if you forget to run the sync script manually.

## Integration with CI/CD

You can add the sync step to your deployment workflow:

```yaml
- name: Sync wrapper versions
  run: npm run sync-versions
```

This ensures wrapper versions are always up-to-date before PM2 starts the processes.


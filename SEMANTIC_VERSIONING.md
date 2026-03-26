# Semantic Versioning Guide

This project uses semantic-release to automatically manage versions for both the bot and API based on conventional commit messages.

## How It Works

### Commit Message Format

Use conventional commit messages with optional scope prefixes:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Component-Specific Versioning

- **Bot changes**: Use `bot` scope
  - `feat(bot): add new command`
  - `fix(bot): resolve issue`
  - `perf(bot): improve performance`

- **API changes**: Use `api` scope
  - `feat(api): add new endpoint`
  - `fix(api): fix bug`
  - `refactor(api): improve code`

- **Both components**: Omit scope or use general scope
  - `feat: add feature` (bumps both)
  - `fix: fix bug` (bumps both)
  - `chore: update dependencies` (bumps both)

### Version Bump Rules

- **Major** (`x.0.0`): Breaking changes (`BREAKING CHANGE:` in footer or `!` after type)
- **Minor** (`x.y.0`): New features (`feat:`)
- **Patch** (`x.y.z`): Bug fixes (`fix:`), performance (`perf:`), refactoring (`refactor:`)

### Examples

```bash
# Bot only - patch bump
git commit -m "fix(bot): resolve command parsing issue"

# API only - minor bump
git commit -m "feat(api): add health check endpoint"

# Both - patch bump
git commit -m "fix: resolve authentication bug"

# Bot - major bump (breaking change)
git commit -m "feat(bot)!: change command structure"
```

## Release Process

1. **Make commits** with conventional commit messages
2. **Push to main/python3** branch
3. **semantic-release** automatically:
   - Analyzes commits
   - Determines version bumps (bot, API, or both)
   - Updates Python `__init__.py` files
   - Updates `pyproject.toml` (bot version)
   - Syncs wrapper `package.json` files
   - Generates CHANGELOG.md
   - Creates GitHub release
   - Tags the release

## Current Versions

- **Bot**: `src/nightscout_backup_bot/__init__.py`
- **API**: `src/nightscout_backup_bot/api/__init__.py`
- **Poetry**: `pyproject.toml` (matches bot version)

## Manual Version Sync

If you need to manually sync wrapper versions:

```bash
npm run sync-versions
```

This updates the PM2 wrapper `package.json` files from the Python versions.

## GitHub Actions

The release workflow (`.github/workflows/release.yml`) runs automatically on push to `main` or `python3` branches and handles the entire release process.


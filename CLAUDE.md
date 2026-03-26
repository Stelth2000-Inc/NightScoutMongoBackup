# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Discord bot that provides automated and on-demand MongoDB backup functionality for NightScout databases. Backups are compressed (gzip or Brotli) and uploaded to AWS S3. A secondary FastAPI HTTP server exposes a trigger endpoint.

## Common Commands

```bash
# Install dependencies
poetry install

# Run the bot
poetry run nightscout-backup-bot

# Run the API server
poetry run nightscout-backup-api

# Run all tests
poetry run pytest

# Run a single test file
poetry run pytest tests/unit/services/test_backup_service.py

# Run a single test by name
poetry run pytest -k "test_backup_creates_file"

# Run only unit tests (exclude integration)
poetry run pytest -m "not integration"

# Run with coverage
poetry run pytest --cov=src/nightscout_backup_bot --cov-report=term-missing

# Lint and format
poetry run black src/ tests/
poetry run ruff check src/ tests/
poetry run mypy src/
```

## Architecture

### Two Entry Points
- **Bot** (`main.py` → `bot.py`): Discord bot using `disnake`. Runs a nightly backup loop via `disnake.ext.tasks` and loads 9 cogs.
- **API** (`api/main.py` → `api/server.py`): FastAPI server that can trigger backups via HTTP. Optionally started as a background thread from `main.py`.

### Service Layer
All business logic lives in `src/nightscout_backup_bot/services/`. The `BackupService` is the orchestrator — it sequences: MongoDB export → compression → S3 upload, coordinating the other services via constructor injection.

| Service | Responsibility |
|---|---|
| `BackupService` | Orchestrates full backup workflow, progress callbacks |
| `MongoService` | Motor (async) MongoDB connectivity, export, exponential backoff retry |
| `S3Service` | aioboto3 uploads, public-read ACL, UUID-obfuscated filenames |
| `CompressionService` | Gzip and Brotli compression |
| `FileService` | Async file I/O (aiofiles) |
| `DiscordThreadService` | Discord thread creation and message posting |

### Discord Commands (Cogs)
Commands are in `src/nightscout_backup_bot/cogs/`:
- `admin/` — Owner-only operations: `/backup`, purge, site management, system controls, thread management, DB queries
- `general/` — Public: `/ping`, `/dbstats`, `/listbackups`

Permission enforcement is via decorators in `utils/checks.py`.

### Configuration
`config.py` defines a Pydantic v2 `Settings` class. It loads from environment variables and `.env` / `.env.vault` files. Environment-specific behavior: production loads `.env.production` only; development loads `.env`. Connection strings for MongoDB Atlas are generated from individual credential fields.

### PM2 Integration
`utils/pm2_process_manager.py` manages bot/API restart via SSH — used by the `/system` admin cog for remote process management on the Linode deployment.

## Code Style

- **Line length**: 120 characters (Black + Ruff)
- **Python**: 3.12+, fully async (`async`/`await` throughout)
- **Type checking**: Mypy strict mode — all new code requires type annotations
- **Commits**: Conventional commits format (`feat:`, `fix:`, `chore:` etc.) — drives semantic-release versioning

## Testing

- `pytest-asyncio` in `auto` mode — async tests work without `@pytest.mark.asyncio`
- Integration tests require real credentials and are excluded by default (`-m "not integration"`)
- Mocks for AWS S3 use `moto`; shared fixtures are in `tests/__mocks__/`
- Coverage target: ~87%

## Versioning

Two independently versioned components tracked via `semantic-release`:
- Bot: `src/nightscout_backup_bot/__init__.py` and `pyproject.toml`
- API: `src/nightscout_backup_bot/api/__init__.py`

See `SEMANTIC_VERSIONING.md` for the full convention.

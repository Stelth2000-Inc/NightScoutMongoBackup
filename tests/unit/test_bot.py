"""Unit tests for bot initialization and configuration."""

import asyncio
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import disnake
import pytest

from nightscout_backup_bot.bot import NightScoutBackupBot, create_bot
from nightscout_backup_bot.config import settings


@pytest.fixture(autouse=True)
def cleanup_bot_commands() -> Generator[None, None, None]:
    """Clean up Discord command registrations after bot tests to prevent test pollution."""
    yield
    # Clear any registered commands after each test
    # This prevents "command already registered" errors when tests run in sequence
    import gc

    gc.collect()  # Force garbage collection to clean up bot instances


@pytest.mark.asyncio
async def test_bot_initialization() -> None:
    """Test bot initializes with correct configuration."""
    bot = NightScoutBackupBot()

    # Check intents are properly configured
    assert bot.intents.message_content, "Message content intent should be enabled"
    assert bot.intents.guilds, "Guilds intent should be enabled"

    # Check backup service is initialized
    assert bot.backup_service is not None, "Backup service should be initialized"

    # Scheduler task should not be running yet
    assert bot._scheduler_task is None


@pytest.mark.asyncio
async def test_create_bot_function() -> None:
    """Test create_bot function returns configured bot."""
    with patch("nightscout_backup_bot.bot.setup_logging"):
        bot = create_bot()

        assert isinstance(bot, NightScoutBackupBot), "Should return NightScoutBackupBot instance"
        assert bot.backup_service is not None, "Backup service should be initialized"


@pytest.mark.asyncio
async def test_bot_on_ready_event(caplog: pytest.LogCaptureFixture) -> None:
    """Test on_ready starts the nightly backup scheduler when enabled."""
    bot = NightScoutBackupBot()

    mock_user = MagicMock()
    mock_user.id = 123456789
    mock_user.__str__ = MagicMock(return_value="TestBot#1234")  # type: ignore[method-assign]

    mock_guilds = [MagicMock(), MagicMock()]

    mock_task = MagicMock(spec=asyncio.Task)

    with (
        patch.object(type(bot), "user", new=mock_user),
        patch.object(type(bot), "guilds", new=mock_guilds),
        patch("nightscout_backup_bot.bot.asyncio.create_task", return_value=mock_task) as mock_create_task,
    ):
        await bot.on_ready()

        if settings.enable_nightly_backup:
            mock_create_task.assert_called_once()
            assert bot._scheduler_task is mock_task


@pytest.mark.asyncio
async def test_bot_on_ready_skips_scheduler_if_already_running() -> None:
    """Test on_ready does not start a second scheduler if one is already running."""
    bot = NightScoutBackupBot()

    mock_user = MagicMock()
    mock_user.id = 123456789
    mock_user.__str__ = MagicMock(return_value="TestBot#1234")  # type: ignore[method-assign]

    mock_guilds = [MagicMock(), MagicMock()]

    # Simulate an already-running task
    existing_task = MagicMock(spec=asyncio.Task)
    existing_task.done.return_value = False
    bot._scheduler_task = existing_task

    with (
        patch.object(type(bot), "user", new=mock_user),
        patch.object(type(bot), "guilds", new=mock_guilds),
        patch("nightscout_backup_bot.bot.asyncio.create_task") as mock_create_task,
    ):
        await bot.on_ready()

        mock_create_task.assert_not_called()
        assert bot._scheduler_task is existing_task


@pytest.mark.asyncio
async def test_bot_slash_command_logging() -> None:
    """Test slash command event logging."""
    bot = NightScoutBackupBot()

    # Create mock interaction
    mock_inter = MagicMock()
    mock_inter.application_command.name = "test_command"
    mock_inter.author.id = 111111111
    mock_inter.author.__str__ = MagicMock(return_value="TestUser#1234")
    mock_inter.guild_id = 987654321

    # This should not raise an exception
    await bot.on_slash_command(mock_inter)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_bot_slash_command_error_handling() -> None:
    """Test slash command error handler."""
    from disnake.ext.commands import CommandError

    bot = NightScoutBackupBot()

    # Create mock interaction and error
    mock_inter = MagicMock()
    mock_inter.application_command.name = "test_command"
    mock_inter.author.id = 111111111

    # Use CommandError instead of generic Exception
    error = CommandError("Test error")

    # This should not raise an exception (type ignore needed for mock interaction)
    await bot.on_slash_command_error(mock_inter, error)  # pyright: ignore


@pytest.mark.asyncio
async def test_bot_cog_loading() -> None:
    """Test that cogs are loaded correctly."""
    with patch("nightscout_backup_bot.bot.setup_logging"):
        bot = create_bot()

        # Check that cogs were loaded
        cog_names = [cog.qualified_name for cog in bot.cogs.values()]

        # We expect at least one cog to be loaded
        assert len(cog_names) > 0, "At least one cog should be loaded"


@pytest.mark.asyncio
async def test_nightly_backup_task_disabled() -> None:
    """Test that nightly backup scheduler respects the enable_nightly_backup setting."""
    bot = NightScoutBackupBot()

    mock_user = MagicMock()
    mock_user.id = 123456789
    mock_user.__str__ = MagicMock(return_value="TestBot#1234")  # type: ignore[method-assign]

    mock_guilds = [MagicMock()]

    with (
        patch.object(type(bot), "user", new=mock_user),
        patch.object(type(bot), "guilds", new=mock_guilds),
        patch("nightscout_backup_bot.bot.settings") as mock_settings,
        patch("nightscout_backup_bot.bot.asyncio.create_task") as mock_create_task,
    ):
        mock_settings.enable_nightly_backup = False

        await bot.on_ready()

        mock_create_task.assert_not_called()
        assert bot._scheduler_task is None


@pytest.mark.asyncio
async def test_nightly_backup_scheduler_computes_next_run() -> None:
    """_nightly_backup_scheduler sleeps until the next Eastern target time then runs the backup."""
    import datetime

    bot = NightScoutBackupBot()
    bot.wait_until_ready = AsyncMock()
    bot.nightly_backup = AsyncMock()  # type: ignore[method-assign]

    # Feed a known "now" so we can assert the sleep duration
    eastern = datetime.timezone(datetime.timedelta(hours=-4))  # EDT
    fake_now = datetime.datetime(2026, 3, 30, 2, 30, tzinfo=eastern)  # 30 min past target

    sleep_calls: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)
        raise asyncio.CancelledError  # stop the loop after first iteration

    with (
        patch("nightscout_backup_bot.bot.asyncio.sleep", side_effect=fake_sleep),
        patch("nightscout_backup_bot.bot.datetime") as mock_dt,
        patch("nightscout_backup_bot.bot.settings") as mock_settings,
    ):
        mock_settings.backup_hour = 2
        mock_settings.backup_minute = 0
        mock_dt.datetime.now.return_value = fake_now
        mock_dt.datetime.side_effect = lambda *a, **kw: datetime.datetime(*a, **kw)
        mock_dt.timedelta = datetime.timedelta

        with pytest.raises(asyncio.CancelledError):
            await bot._nightly_backup_scheduler()

    # 30 min past → next target is ~23.5 hours away
    assert len(sleep_calls) == 1
    assert 23 * 3600 < sleep_calls[0] < 24 * 3600


@pytest.mark.asyncio
async def test_nightly_backup_task_execution() -> None:
    """Test nightly backup task execution."""
    bot = NightScoutBackupBot()

    # Mock backup service
    mock_backup_result = {"success": True, "url": "https://example.com/backup.tar.gz"}
    bot.backup_service.execute_backup = AsyncMock(return_value=mock_backup_result)

    # Mock channel - must be a TextChannel instance
    mock_channel = MagicMock(spec=disnake.TextChannel)
    mock_channel.send = AsyncMock()
    bot.get_channel = MagicMock(return_value=mock_channel)

    # Mock thread management cog
    mock_cog = MagicMock()
    mock_cog.manage_threads_impl = AsyncMock(return_value=(2, 1))  # 2 archived, 1 deleted
    bot.get_cog = MagicMock(return_value=mock_cog)

    # Mock settings
    with patch("nightscout_backup_bot.bot.settings") as mock_settings:
        mock_settings.backup_channel_id = "123"

        # Execute the task
        await bot.nightly_backup()

        # Verify backup was executed
        bot.backup_service.execute_backup.assert_called_once_with(mock_channel)
        mock_channel.send.assert_called()
        # Verify thread management was called
        mock_cog.manage_threads_impl.assert_called_once_with(mock_channel)


@pytest.mark.asyncio
async def test_nightly_backup_channel_not_found() -> None:
    """Test nightly backup when channel is not found."""
    bot = NightScoutBackupBot()
    bot.get_channel = MagicMock(return_value=None)
    bot.backup_service.execute_backup = AsyncMock()

    with patch("nightscout_backup_bot.bot.settings") as mock_settings:
        mock_settings.backup_channel_id = "123"

        # Execute the task - should not raise, just log error
        await bot.nightly_backup()

        # Backup service should not be called
        bot.backup_service.execute_backup.assert_not_called()


@pytest.mark.asyncio
async def test_nightly_backup_channel_not_text_channel() -> None:
    """Test nightly backup when channel is not a text channel."""
    bot = NightScoutBackupBot()
    mock_voice_channel = MagicMock()
    bot.get_channel = MagicMock(return_value=mock_voice_channel)
    bot.backup_service.execute_backup = AsyncMock()

    with patch("nightscout_backup_bot.bot.settings") as mock_settings:
        mock_settings.backup_channel_id = "123"

        # Execute the task - should not raise, just log error
        await bot.nightly_backup()

        # Backup service should not be called
        bot.backup_service.execute_backup.assert_not_called()


@pytest.mark.asyncio
async def test_nightly_backup_failure() -> None:
    """Test nightly backup error handling."""
    bot = NightScoutBackupBot()

    # Mock backup service to raise exception
    bot.backup_service.execute_backup = AsyncMock(side_effect=Exception("Backup failed"))

    # Mock channel - must be a TextChannel instance
    mock_channel = MagicMock(spec=disnake.TextChannel)
    mock_channel.send = AsyncMock()
    bot.get_channel = MagicMock(return_value=mock_channel)

    with patch("nightscout_backup_bot.bot.settings") as mock_settings:
        mock_settings.backup_channel_id = "123"

        # Execute the task - should not raise, just log error
        await bot.nightly_backup()

        # Backup service should have been called
        bot.backup_service.execute_backup.assert_called_once()


@pytest.mark.asyncio
async def test_nightly_backup_no_thread_management_cog() -> None:
    """Test nightly backup when thread management cog is not loaded."""
    bot = NightScoutBackupBot()

    # Mock backup service
    mock_backup_result = {"success": True, "url": "https://example.com/backup.tar.gz"}
    bot.backup_service.execute_backup = AsyncMock(return_value=mock_backup_result)

    # Mock channel - must be a TextChannel instance
    mock_channel = MagicMock(spec=disnake.TextChannel)
    mock_channel.send = AsyncMock()
    bot.get_channel = MagicMock(return_value=mock_channel)

    # Mock cog not found
    bot.get_cog = MagicMock(return_value=None)

    with patch("nightscout_backup_bot.bot.settings") as mock_settings:
        mock_settings.backup_channel_id = "123"

        # Execute the task - should not raise
        await bot.nightly_backup()

        # Backup should still complete
        bot.backup_service.execute_backup.assert_called_once()


@pytest.mark.asyncio
async def test_create_bot_with_sentry() -> None:
    """Test create_bot initializes Sentry when configured."""
    with (
        patch("nightscout_backup_bot.bot.setup_logging"),
        patch("nightscout_backup_bot.bot.settings") as mock_settings,
    ):
        mock_settings.sentry_dsn = "https://test@sentry.io/123"
        mock_settings.node_env = "production"
        mock_settings.is_production = True

        # Mock sentry_sdk import
        import sys

        mock_sentry = MagicMock()
        with patch.dict(sys.modules, {"sentry_sdk": mock_sentry}):
            bot = create_bot()

            assert isinstance(bot, NightScoutBackupBot)
            # Sentry init should be called if import succeeds
            mock_sentry.init.assert_called_once()


@pytest.mark.asyncio
async def test_create_bot_without_sentry() -> None:
    """Test create_bot skips Sentry when not configured."""
    with (
        patch("nightscout_backup_bot.bot.setup_logging"),
        patch("nightscout_backup_bot.bot.settings") as mock_settings,
    ):
        mock_settings.sentry_dsn = None

        bot = create_bot()

        assert isinstance(bot, NightScoutBackupBot)
        # Sentry should not be initialized when DSN is None


@pytest.mark.asyncio
async def test_create_bot_sentry_error() -> None:
    """Test create_bot handles Sentry initialization errors gracefully."""
    with (
        patch("nightscout_backup_bot.bot.setup_logging"),
        patch("nightscout_backup_bot.bot.settings") as mock_settings,
    ):
        mock_settings.sentry_dsn = "https://test@sentry.io/123"
        mock_settings.node_env = "production"

        # Mock sentry_sdk import with init that raises
        import sys

        mock_sentry = MagicMock()
        mock_sentry.init = MagicMock(side_effect=Exception("Sentry init failed"))
        with patch.dict(sys.modules, {"sentry_sdk": mock_sentry}):
            # Should not raise, just log warning
            bot = create_bot()

            assert isinstance(bot, NightScoutBackupBot)

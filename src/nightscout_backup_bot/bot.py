"""Discord bot initialization and setup."""

import asyncio
import datetime
import zoneinfo
from collections.abc import Awaitable, Callable
from typing import cast, override

import disnake
from disnake.ext import commands

from nightscout_backup_bot.config import settings
from nightscout_backup_bot.logging_config import StructuredLogger, setup_logging
from nightscout_backup_bot.services.backup_service import BackupService
from nightscout_backup_bot.utils.pm2_process_manager import PM2ProcessManager

logger = StructuredLogger(__name__)


class NightScoutBackupBot(commands.Bot):
    """Custom bot class for NightScout backup operations."""

    backup_service: BackupService
    pm2_process_manager: PM2ProcessManager
    _scheduler_task: "asyncio.Task[None] | None"

    def __init__(self) -> None:
        """Initialize the bot."""
        intents = disnake.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(
            command_prefix="!",  # Not used, but required
            intents=intents,
            # Set to specific guild IDs for faster command sync during development
            test_guilds=settings.test_guild_ids,
        )

        self.backup_service = BackupService()
        self.pm2_process_manager = PM2ProcessManager()
        self._scheduler_task = None

    async def on_ready(self) -> None:
        """Called when bot is ready."""
        logger.info(
            "Bot is ready",
            bot_user=str(self.user),
            bot_id=self.user.id if self.user else None,
            guilds=len(self.guilds),
        )

        # Start nightly backup scheduler if enabled
        if settings.enable_nightly_backup:
            if self._scheduler_task is None or self._scheduler_task.done():
                self._scheduler_task = asyncio.create_task(self._nightly_backup_scheduler())
                logger.info(
                    "Nightly backup scheduler started",
                    hour=settings.backup_hour,
                    minute=settings.backup_minute,
                )

    async def on_slash_command(self, inter: disnake.ApplicationCommandInteraction["NightScoutBackupBot"]) -> None:
        """Called when a slash command is used."""
        logger.info(
            "Slash command executed",
            command=inter.application_command.name,
            user_id=inter.author.id,
            user=str(inter.author),
            guild_id=inter.guild_id if inter.guild else None,
        )

    @override
    async def on_slash_command_error(
        self,
        interaction: disnake.ApplicationCommandInteraction["NightScoutBackupBot"],
        exception: commands.CommandError,
    ) -> None:
        """Handle slash command errors."""
        logger.error(
            "Slash command error",
            command=interaction.application_command.name,
            error=str(exception),
            user_id=interaction.author.id,
        )

    async def _nightly_backup_scheduler(self) -> None:
        """Sleep until the next configured Eastern time, then run the backup — forever.

        Using datetime.datetime.now(ZoneInfo(...)) gives ZoneInfo a concrete date so it can
        resolve EST vs. EDT correctly.  The offset is recomputed on every iteration, meaning
        DST transitions are handled automatically without a bot restart.
        """
        await self.wait_until_ready()
        eastern = zoneinfo.ZoneInfo("America/New_York")
        while True:
            now = datetime.datetime.now(eastern)
            target = now.replace(
                hour=settings.backup_hour,
                minute=settings.backup_minute,
                second=0,
                microsecond=0,
            )
            if target <= now:
                target += datetime.timedelta(days=1)

            wait_seconds = (target - now).total_seconds()
            logger.debug(
                "Nightly backup sleeping until next run",
                next_run_eastern=str(target),
                wait_seconds=round(wait_seconds),
            )
            await asyncio.sleep(wait_seconds)
            await self.nightly_backup()

    async def nightly_backup(self) -> None:
        """Execute nightly backup."""
        try:
            logger.info("Starting nightly backup")

            # Get the backup channel
            channel = self.get_channel(int(settings.backup_channel_id))
            if not isinstance(channel, disnake.TextChannel):
                logger.error("Backup channel not found or not a text channel")
                return

            # Send start message to main channel
            _ = await channel.send("Backup started! Progress and download link will be posted in the thread.")

            # Execute backup
            result = await self.backup_service.execute_backup(channel)

            logger.info("Nightly backup completed", success=result["success"], url=result.get("url"))

            # Send completion message to main channel if successful
            if result.get("success"):
                _ = await channel.send("✅ Backup completed successfully!")

                # Thread management: archive/delete old threads
                cog = self.get_cog("ThreadManagement")
                logger.debug(
                    "Loaded cogs:",
                    cogs=list(self.cogs.keys()),
                    thread_management_cog_type=str(type(cog)) if cog else None,
                )
                if cog and hasattr(cog, "manage_threads_impl"):
                    # Call method directly without isinstance check to avoid circular import
                    # Using getattr to avoid type checker error; hasattr check ensures safety
                    method = cast(
                        Callable[[disnake.TextChannel], Awaitable[tuple[int, int]]],
                        getattr(cog, "manage_threads_impl"),  # noqa: B009
                    )
                    thread_result = await method(channel)
                    archived_count, deleted_count = thread_result

                    # Report results in the backup channel
                    _ = await channel.send(
                        f"🧹 Thread management complete.\nArchived threads: {archived_count}\nDeleted threads: {deleted_count}"
                    )
                else:
                    logger.warning(
                        "ThreadManagement cog not loaded or missing manage_threads_impl method; skipping thread management."
                    )

        except Exception as e:
            logger.error("Nightly backup failed", error=str(e))

    def load_cogs(self) -> None:
        """Load all cogs."""
        cogs = [
            "nightscout_backup_bot.cogs.general.ping",
            "nightscout_backup_bot.cogs.admin.querydb",
            "nightscout_backup_bot.cogs.general.dbstats",
            "nightscout_backup_bot.cogs.general.listbackups",
            "nightscout_backup_bot.cogs.admin.backup",
            "nightscout_backup_bot.cogs.admin.site",
            "nightscout_backup_bot.cogs.admin.system",
            "nightscout_backup_bot.cogs.admin.thread_management",
            "nightscout_backup_bot.cogs.admin.purge",
        ]

        for cog in cogs:
            try:
                self.load_extension(cog)
                logger.info("Loaded cog", cog=cog)
            except Exception as e:
                logger.error("Failed to load cog", cog=cog, error=str(e))


def create_bot() -> NightScoutBackupBot:
    """
    Create and configure the bot instance.

    Returns:
        Configured bot instance.
    """
    # Setup logging
    setup_logging()

    # Initialize Sentry if configured
    if settings.sentry_dsn:
        try:
            import sentry_sdk

            _ = sentry_sdk.init(
                dsn=settings.sentry_dsn,
                environment=settings.node_env,
                traces_sample_rate=1.0 if not settings.is_production else 0.1,
            )
            logger.info("Sentry initialized", environment=settings.node_env)
        except Exception as e:
            logger.warning("Failed to initialize Sentry", error=str(e))

    # Create bot
    bot = NightScoutBackupBot()
    bot.load_cogs()

    return bot

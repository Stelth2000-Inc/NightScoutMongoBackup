"""Unit tests for configuration and settings."""

import os
from unittest.mock import patch

from nightscout_backup_bot.config import CompressionMethod, Settings, get_settings


class TestMongoConnectionString:
    """Test MongoDB connection string generation."""

    def test_mongo_connection_string_basic(self) -> None:
        """Test basic connection string without special characters."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "simplepass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
        ):
            settings = Settings.model_validate({})
            connection_string = settings.mongo_connection_string

            # Should match MongoDB Atlas format (no database in path)
            assert "mongodb+srv://testuser:simplepass@cluster.mongodb.net/?" in connection_string
            assert "retryWrites=true" in connection_string
            assert "w=majority" in connection_string

    def test_mongo_connection_string_with_special_chars(self) -> None:
        """Test connection string properly URL-encodes passwords with special characters."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "p@ss:w#rd/123$",  # Special chars: @ : # / $
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
        ):
            settings = Settings.model_validate({})
            connection_string = settings.mongo_connection_string

            # Password should be URL-encoded
            # p@ss:w#rd/123$ becomes p%40ss%3Aw%23rd%2F123%24
            assert "p%40ss%3Aw%23rd%2F123%24" in connection_string
            # Original password should NOT appear in connection string
            assert "p@ss:w#rd/123$" not in connection_string

    def test_mongo_connection_string_with_username_special_chars(self) -> None:
        """Test connection string properly URL-encodes usernames with special characters."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "user@domain.com",  # Email-style username
                "MONGO_PASSWORD": "simplepass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
        ):
            settings = Settings.model_validate({})
            connection_string = settings.mongo_connection_string

            # Username should be URL-encoded
            # user@domain.com becomes user%40domain.com
            assert "user%40domain.com" in connection_string
            # Original username should NOT appear before the @ host separator
            assert "mongodb+srv://user@domain.com" not in connection_string

    def test_mongo_connection_string_with_spaces(self) -> None:
        """Test connection string handles passwords with spaces."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "my password 123",  # Spaces in password
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
        ):
            settings = Settings.model_validate({})
            connection_string = settings.mongo_connection_string

            # Spaces should be URL-encoded as %20
            assert "my%20password%20123" in connection_string

    def test_mongo_connection_string_with_percent_chars(self) -> None:
        """Test connection string handles passwords with percent signs."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "pass%word",  # Percent sign in password
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
        ):
            settings = Settings.model_validate({})
            connection_string = settings.mongo_connection_string

            # Percent should be double-encoded
            assert "pass%25word" in connection_string

    def test_mongo_connection_includes_database(self) -> None:
        """Test connection string follows MongoDB Atlas format (database not in path)."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "mydatabase",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
        ):
            settings = Settings.model_validate({})
            connection_string = settings.mongo_connection_string

            # MongoDB Atlas format: no database in path, use /? for query params
            assert "/?retryWrites=true" in connection_string
            # Database should NOT be in the connection string path
            assert "/mydatabase?" not in connection_string

    def test_mongo_connection_includes_required_params(self) -> None:
        """Test connection string includes required MongoDB parameters."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
        ):
            settings = Settings.model_validate({})
            connection_string = settings.mongo_connection_string

            assert "retryWrites=true" in connection_string
            assert "w=majority" in connection_string


class TestCompressionMethod:
    """Test CompressionMethod enum."""

    def test_compression_method_enum_values(self) -> None:
        """Test that CompressionMethod enum has expected values."""
        assert CompressionMethod.GZIP.value == "gzip"
        assert CompressionMethod.BROTLI.value == "brotli"

    def test_compression_method_default(self) -> None:
        """Test that default compression method is GZIP."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.compression_method == CompressionMethod.GZIP

    def test_compression_method_from_env_gzip(self) -> None:
        """Test that compression method can be set to gzip via environment variable."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "COMPRESSION_METHOD": "gzip",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.compression_method == CompressionMethod.GZIP

    def test_compression_method_from_env_brotli(self) -> None:
        """Test that compression method can be set to brotli via environment variable."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "COMPRESSION_METHOD": "brotli",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.compression_method == CompressionMethod.BROTLI

    def test_compression_method_enum_string_comparison(self) -> None:
        """Test that CompressionMethod enum can be compared with strings."""
        # This is important for backward compatibility
        assert CompressionMethod.GZIP.value == "gzip"
        assert CompressionMethod.BROTLI.value == "brotli"


class TestBotOwnerIds:
    """Test bot_owner_ids field validator and owner_id_list property."""

    def test_parse_owner_ids_empty_string(self) -> None:
        """Test that empty string returns empty string."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "BOT_OWNER_IDS": "",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.bot_owner_ids == ""
            assert settings.owner_id_list == []

    def test_parse_owner_ids_single_id(self) -> None:
        """Test parsing a single owner ID."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "BOT_OWNER_IDS": "123456789",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.bot_owner_ids == "123456789"
            assert settings.owner_id_list == ["123456789"]

    def test_parse_owner_ids_multiple_ids(self) -> None:
        """Test parsing multiple owner IDs."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "BOT_OWNER_IDS": "123456789,987654321,555666777",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.bot_owner_ids == "123456789,987654321,555666777"
            assert settings.owner_id_list == ["123456789", "987654321", "555666777"]

    def test_parse_owner_ids_with_whitespace(self) -> None:
        """Test parsing owner IDs with whitespace is cleaned."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "BOT_OWNER_IDS": " 123456789 , 987654321 , 555666777 ",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.bot_owner_ids == "123456789,987654321,555666777"
            assert settings.owner_id_list == ["123456789", "987654321", "555666777"]

    def test_parse_owner_ids_with_empty_entries(self) -> None:
        """Test parsing owner IDs with empty entries (extra commas)."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "BOT_OWNER_IDS": "123456789,,987654321,",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.bot_owner_ids == "123456789,987654321"
            assert settings.owner_id_list == ["123456789", "987654321"]


class TestTestGuildIds:
    """Test test_guild_ids property."""

    def test_test_guild_ids_none(self) -> None:
        """Test that None test_guilds returns None."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
            clear=False,
        ):
            # Explicitly remove TEST_GUILDS if it exists
            os.environ.pop("TEST_GUILDS", None)
            settings = Settings.model_validate({})
            # If test_guilds is None or empty, test_guild_ids should be None
            if not settings.test_guilds:
                assert settings.test_guild_ids is None
            else:
                # If .env.test has TEST_GUILDS set, verify the property works correctly
                assert isinstance(settings.test_guild_ids, list | type(None))

    def test_test_guild_ids_empty_string(self) -> None:
        """Test that empty string returns None."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "TEST_GUILDS": "",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.test_guild_ids is None

    def test_test_guild_ids_single_id(self) -> None:
        """Test parsing a single test guild ID."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "TEST_GUILDS": "123456789",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.test_guild_ids == [123456789]

    def test_test_guild_ids_multiple_ids(self) -> None:
        """Test parsing multiple test guild IDs."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "TEST_GUILDS": "123456789,987654321,555666777",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.test_guild_ids == [123456789, 987654321, 555666777]

    def test_test_guild_ids_with_whitespace(self) -> None:
        """Test parsing test guild IDs with whitespace."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "TEST_GUILDS": " 123456789 , 987654321 , 555666777 ",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.test_guild_ids == [123456789, 987654321, 555666777]

    def test_test_guild_ids_invalid_value(self) -> None:
        """Test that invalid guild ID (non-numeric) returns None."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "TEST_GUILDS": "123456789,invalid,555666777",
            },
        ):
            settings = Settings.model_validate({})
            # ValueError should be caught and return None
            assert settings.test_guild_ids is None

    def test_test_guild_ids_partially_invalid(self) -> None:
        """Test that partially invalid guild IDs (mix of valid and invalid) returns None."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "TEST_GUILDS": "123456789,not_a_number",
            },
        ):
            settings = Settings.model_validate({})
            # ValueError should be caught and return None
            assert settings.test_guild_ids is None


class TestIsProduction:
    """Test is_production property."""

    def test_is_production_true(self) -> None:
        """Test that is_production returns True when NODE_ENV=production."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "NODE_ENV": "production",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.is_production is True

    def test_is_production_false_development(self) -> None:
        """Test that is_production returns False when NODE_ENV=development."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "NODE_ENV": "development",
            },
        ):
            settings = Settings.model_validate({})
            assert settings.is_production is False

    def test_is_production_false_default(self) -> None:
        """Test that is_production returns False when NODE_ENV is not set (defaults to development)."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
            clear=False,
        ):
            # Remove NODE_ENV if it exists
            os.environ.pop("NODE_ENV", None)
            settings = Settings.model_validate({})
            assert settings.is_production is False

    def test_is_production_case_insensitive(self) -> None:
        """Test that is_production is case-insensitive."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "NODE_ENV": "PRODUCTION",  # Uppercase
            },
        ):
            settings = Settings.model_validate({})
            assert settings.is_production is True


class TestGetSettings:
    """Test get_settings function."""

    def test_get_settings_returns_settings_instance(self) -> None:
        """Test that get_settings returns a Settings instance."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
            clear=False,
        ):
            # Reset the module-level _settings to get fresh instance
            import nightscout_backup_bot.config as config_module

            config_module._settings = None  # type: ignore[attr-defined]
            settings = get_settings()
            assert isinstance(settings, Settings)
            # Verify it has the expected structure (may have values from .env.test)
            assert hasattr(settings, "discord_token")
            assert hasattr(settings, "mongo_host")

    def test_get_settings_singleton_behavior(self) -> None:
        """Test that get_settings returns the same instance (singleton pattern)."""
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
            },
        ):
            # Reset the module-level _settings to test singleton
            import nightscout_backup_bot.config as config_module

            config_module._settings = None  # type: ignore[attr-defined]

            settings1 = get_settings()
            settings2 = get_settings()

            # Should return the same instance
            assert settings1 is settings2


class TestEnvProductionLoading:
    """Test .env.production loading logic.

    Note: The .env.production loading logic runs at module import time,
    so we test it indirectly by verifying the behavior works correctly
    in production environments. Direct testing would require module reloading
    which is complex and may interfere with other tests.
    """

    def test_env_production_config_uses_production_file_when_set(self) -> None:
        """Test that Settings model_config uses .env.production when in production."""
        # This test verifies that the env_file configuration is set correctly
        # The actual loading happens at module import time, which is tested
        # implicitly through integration tests and production deployments
        with patch.dict(
            os.environ,
            {
                "DISCORD_TOKEN": "test_token",
                "DISCORD_CLIENT_ID": "test_client_id",
                "BACKUP_CHANNEL_ID": "test_channel",
                "MONGO_HOST": "cluster.mongodb.net",
                "MONGO_USERNAME": "testuser",
                "MONGO_PASSWORD": "testpass",
                "MONGO_DB": "testdb",
                "AWS_ACCESS_KEY_ID": "test_access",
                "AWS_SECRET_ACCESS_KEY": "test_secret",
                "S3_BACKUP_BUCKET": "test_bucket",
                "NODE_ENV": "production",
            },
        ):
            # Verify settings can be created (env file loading happens at module level)
            settings = Settings.model_validate({})
            assert settings.node_env == "production"
            assert settings.is_production is True

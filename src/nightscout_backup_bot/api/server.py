"""FastAPI server for backup operations."""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..config import settings
from ..logging_config import StructuredLogger
from ..services.backup_service import BackupService

logger = StructuredLogger("api.server")

app = FastAPI(
    title="NightScout Backup API",
    description="HTTP API for triggering MongoDB backups",
    version="1.0.0",
)

# Configure CORS - allow origins from settings
cors_origins = [origin.strip() for origin in settings.backup_api_cors_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

backup_service = BackupService()

# Security: API Key authentication
security = HTTPBearer()


def verify_api_key(
    authorization: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    """
    Verify API key from Authorization header.

    Expected format: Bearer <api_key>
    """
    # Check if API key is configured
    if not settings.backup_api_key:
        logger.error("API key not configured - API endpoints are disabled for security")
        raise HTTPException(
            status_code=500, detail="API authentication not configured. Please set BACKUP_API_KEY environment variable."
        )

    if not authorization:
        logger.warning("API request missing authorization header")
        raise HTTPException(status_code=401, detail="Missing authorization header")

    provided_key = authorization.credentials

    # Use constant-time comparison to prevent timing attacks
    if not _constant_time_compare(provided_key, settings.backup_api_key):
        logger.warning("API request with invalid API key")
        raise HTTPException(status_code=401, detail="Invalid API key")

    logger.debug("API request authenticated successfully")


def _constant_time_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to prevent timing attacks.

    Args:
        a: First string to compare
        b: Second string to compare

    Returns:
        True if strings are equal, False otherwise
    """
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a.encode(), b.encode(), strict=True):
        result |= x ^ y

    return result == 0


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/backup")
async def create_backup(_: None = Depends(verify_api_key)) -> dict[str, object]:
    """
    Trigger a MongoDB backup.

    Requires API key authentication via Bearer token in Authorization header.

    Returns:
        Dictionary with backup results including success status, S3 URL, and statistics.
    """
    try:
        logger.info("Backup request received via API")
        result = await backup_service.execute_backup_api()
        return result
    except Exception as e:
        error_msg = str(e)
        logger.error("Backup API request failed", error=error_msg)
        raise HTTPException(status_code=500, detail=error_msg) from e


@app.get("/test-connections")
async def test_connections(_: None = Depends(verify_api_key)) -> dict[str, bool]:
    """
    Test connections to MongoDB and S3.

    Requires API key authentication via Bearer token in Authorization header.

    Returns:
        Dictionary with connection test results.
    """
    try:
        results = await backup_service.test_connections()
        return results
    except Exception as e:
        error_msg = str(e)
        logger.error("Connection test failed", error=error_msg)
        raise HTTPException(status_code=500, detail=error_msg) from e

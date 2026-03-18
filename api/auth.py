from fastapi import HTTPException, Request, Depends
import logging

logger = logging.getLogger(__name__)

async def get_current_user_id(request: Request) -> str:
    """
    Mock auth - extract user ID from Authorization header
    In production, validate JWT/OAuth token
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authentication token")

    token = auth_header.split(" ")[1]

    # Mock: In production, verify JWT token
    if token == "sandbox-token":
        return "a1b2c3d4-e5f6-7890-abcd-1234567890ab"

    # For testing, use token as user ID
    return token

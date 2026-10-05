from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from core.config.settings import get_settings
from core.models.enums import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class Principal(BaseModel):
    subject: str
    roles: set[Role]


# bcrypt only reads the first 72 bytes; reject longer input instead of silently truncating.
MAX_PASSWORD_BYTES = 72
# Hash used when the user does not exist, so login timing does not reveal valid usernames.
_DUMMY_HASH = bcrypt.hashpw(b"threat-nexus-dummy-password", bcrypt.gensalt()).decode()


def hash_password(password: str) -> str:
    raw = password.encode("utf-8")
    if len(raw) > MAX_PASSWORD_BYTES:
        raise ValueError("Password exceeds 72 bytes")
    return bcrypt.hashpw(raw, bcrypt.gensalt(rounds=12)).decode()


def verify_password(password: str, hashed: str | None) -> bool:
    raw = password.encode("utf-8")
    if len(raw) > MAX_PASSWORD_BYTES:
        return False
    try:
        ok = bcrypt.checkpw(raw, (hashed or _DUMMY_HASH).encode())
    except ValueError:
        return False
    return ok and hashed is not None


def _signing_secret() -> str:
    secret = get_settings().jwt_secret
    if not secret:
        raise RuntimeError("JWT secret is not configured")
    return secret


def create_access_token(subject: str, roles: set[Role]) -> str:
    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_minutes)
    payload = {"sub": subject, "roles": [role.value for role in roles], "exp": expires_at}
    return str(jwt.encode(payload, _signing_secret(), algorithm=settings.jwt_algorithm))


async def get_principal(token: Annotated[str, Depends(oauth2_scheme)]) -> Principal:
    settings = get_settings()
    try:
        payload = jwt.decode(token, _signing_secret(), algorithms=[settings.jwt_algorithm])
        subject = payload.get("sub")
        roles = {Role(role) for role in payload.get("roles", [])}
        if not subject or not roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return Principal(subject=subject, roles=roles)
    except (JWTError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def require_roles(*required: Role) -> Callable[[Principal], Awaitable[Principal]]:
    async def dependency(principal: Annotated[Principal, Depends(get_principal)]) -> Principal:
        if principal.roles.isdisjoint(required):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return principal

    return dependency

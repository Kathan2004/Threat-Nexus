from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from core.config.settings import get_settings
from core.models.enums import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Principal(BaseModel):
    subject: str
    roles: set[Role]


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_context.verify(password, hashed)


def create_access_token(subject: str, roles: set[Role]) -> str:
    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_minutes)
    payload = {"sub": subject, "roles": [role.value for role in roles], "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


async def get_principal(token: Annotated[str, Depends(oauth2_scheme)]) -> Principal:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        subject = payload.get("sub")
        roles = {Role(role) for role in payload.get("roles", [])}
        if not subject or not roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return Principal(subject=subject, roles=roles)
    except (JWTError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def require_roles(*required: Role):
    async def dependency(principal: Annotated[Principal, Depends(get_principal)]) -> Principal:
        if principal.roles.isdisjoint(required):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return principal

    return dependency

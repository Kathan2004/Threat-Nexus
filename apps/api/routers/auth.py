from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field

from apps.api.ratelimit import limiter
from core.auth.security import Principal, create_access_token, require_roles, verify_password
from core.auth.users import UserRepository, UserView
from core.database.mongo import get_database
from core.models.enums import Role

router = APIRouter(prefix="/auth", tags=["auth"])

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class TokenRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str = Field(min_length=12, max_length=72)
    roles: set[Role] = Field(default_factory=lambda: {Role.VIEWER})


async def user_repo(db: AsyncIOMotorDatabase = Depends(get_database)) -> UserRepository:
    return UserRepository(db)


@router.post("/token", response_model=TokenResponse)
@limiter.limit("10/minute")
async def token(
    request: Request,
    body: TokenRequest,
    users: Annotated[UserRepository, Depends(user_repo)],
) -> TokenResponse:
    user = await users.get(body.username)
    # verify_password runs bcrypt even for unknown users so timing does not leak usernames.
    if not verify_password(body.password, user.password_hash if user else None) or user is None:
        raise INVALID_CREDENTIALS
    if user.disabled:
        raise INVALID_CREDENTIALS
    return TokenResponse(access_token=create_access_token(user.username, user.roles))


@router.get("/me", response_model=Principal)
async def me(principal: Annotated[Principal, Depends(require_roles(*Role))]) -> Principal:
    return principal


@router.get("/users", response_model=list[UserView], dependencies=[Depends(require_roles(Role.ADMIN))])
async def list_users(users: Annotated[UserRepository, Depends(user_repo)]) -> list[UserView]:
    return await users.list()


@router.post(
    "/users",
    response_model=UserView,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.ADMIN))],
)
async def create_user(body: CreateUserRequest, users: Annotated[UserRepository, Depends(user_repo)]) -> UserView:
    if await users.get(body.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User exists")
    user = await users.create(body.username, body.password, body.roles)
    return UserView.model_validate(user.model_dump())

from datetime import UTC, datetime
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field

from core.auth.security import hash_password
from core.models.enums import Role


class User(BaseModel):
    username: str
    password_hash: str
    roles: set[Role] = Field(default_factory=lambda: {Role.VIEWER})
    disabled: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UserView(BaseModel):
    username: str
    roles: set[Role]
    disabled: bool
    created_at: datetime


class UserRepository:
    """Analyst accounts, stored in the `users` collection with bcrypt hashes."""

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.collection = db["users"]

    async def ensure_indexes(self) -> None:
        await self.collection.create_index("username", unique=True)

    async def get(self, username: str) -> User | None:
        data: dict[str, Any] | None = await self.collection.find_one({"username": username.lower()}, {"_id": 0})
        return User.model_validate(data) if data else None

    async def count(self) -> int:
        return int(await self.collection.count_documents({}))

    async def create(self, username: str, password: str, roles: set[Role]) -> User:
        user = User(username=username.lower(), password_hash=hash_password(password), roles=roles)
        await self.collection.insert_one(user.model_dump(mode="json"))
        return user

    async def list(self) -> list[UserView]:
        cursor = self.collection.find({}, {"_id": 0, "password_hash": 0}).sort("username", 1)
        return [UserView.model_validate(doc) async for doc in cursor]

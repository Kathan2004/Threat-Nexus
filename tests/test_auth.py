import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.ratelimit import limiter
from apps.api.routers.auth import user_repo
from core.auth.security import create_access_token, hash_password, verify_password
from core.auth.users import User, UserView
from core.models.enums import Role


class FakeUsers:
    def __init__(self) -> None:
        self.users: dict[str, User] = {}

    async def get(self, username: str) -> User | None:
        return self.users.get(username.lower())

    async def count(self) -> int:
        return len(self.users)

    async def create(self, username: str, password: str, roles: set[Role]) -> User:
        user = User(username=username.lower(), password_hash=hash_password(password), roles=roles)
        self.users[user.username] = user
        return user

    async def list(self) -> list[UserView]:
        return [UserView.model_validate(u.model_dump()) for u in self.users.values()]


@pytest.fixture
def users():
    fake = FakeUsers()
    fake.users["admin"] = User(
        username="admin", password_hash=hash_password("correct horse battery"), roles={Role.ADMIN}
    )
    fake.users["viewer"] = User(
        username="viewer", password_hash=hash_password("viewer password 1"), roles={Role.VIEWER}
    )
    app.dependency_overrides[user_repo] = lambda: fake
    limiter.reset()
    yield fake
    app.dependency_overrides.clear()


@pytest.fixture
def client(users):
    return TestClient(app)


def login(client, username, password):
    return client.post("/auth/token", json={"username": username, "password": password})


def test_password_hashing_roundtrip():
    hashed = hash_password("s3cure-passphrase")
    assert verify_password("s3cure-passphrase", hashed)
    assert not verify_password("wrong", hashed)
    assert not verify_password("anything", None)


def test_password_over_72_bytes_rejected():
    with pytest.raises(ValueError):
        hash_password("x" * 73)


def test_admin_with_wrong_password_is_rejected(client):
    # Regression: the old handler issued an admin token for username "admin" and any password.
    assert login(client, "admin", "anything").status_code == 401


def test_unknown_user_is_rejected(client):
    assert login(client, "ghost", "whatever-password").status_code == 401


def test_valid_login_returns_token_with_stored_roles(client):
    r = login(client, "viewer", "viewer password 1")
    assert r.status_code == 200
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {r.json()['access_token']}"})
    assert me.json()["roles"] == ["viewer"]


def test_disabled_user_cannot_login(client, users):
    users.users["viewer"].disabled = True
    assert login(client, "viewer", "viewer password 1").status_code == 401


def test_only_admin_can_create_users(client):
    viewer = create_access_token("viewer", {Role.VIEWER})
    body = {"username": "analyst1", "password": "analyst password", "roles": ["analyst"]}
    r = client.post("/auth/users", json=body, headers={"Authorization": f"Bearer {viewer}"})
    assert r.status_code == 403

    admin = create_access_token("admin", {Role.ADMIN})
    r = client.post("/auth/users", json=body, headers={"Authorization": f"Bearer {admin}"})
    assert r.status_code == 201 and r.json()["roles"] == ["analyst"]
    assert login(client, "analyst1", "analyst password").status_code == 200


def test_forged_token_rejected(client):
    from jose import jwt

    forged = jwt.encode({"sub": "x", "roles": ["admin"]}, "change-me-with-a-32-byte-secret", "HS256")
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {forged}"})
    assert r.status_code == 401


def test_login_is_rate_limited(client):
    codes = [login(client, "admin", "bad").status_code for _ in range(12)]
    assert 429 in codes

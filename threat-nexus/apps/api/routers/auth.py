from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.auth.security import create_access_token
from core.models.enums import Role

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse)
async def token(request: TokenRequest) -> TokenResponse:
    if not request.username or not request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    roles = {Role.ADMIN} if request.username == "admin" else {Role.ANALYST}
    return TokenResponse(access_token=create_access_token(request.username, roles))

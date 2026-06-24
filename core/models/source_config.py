from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class SourceConfig(BaseModel):
    id: str
    enabled: bool = False
    base_url: str | None = None
    credentials: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_by: str | None = None


class SourceConfigUpdate(BaseModel):
    enabled: bool | None = None
    base_url: str | None = None
    credentials: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceConfigView(BaseModel):
    id: str
    display_name: str
    enabled: bool
    base_url: str | None = None
    required_credentials: list[str] = Field(default_factory=list)
    configured_credentials: list[str] = Field(default_factory=list)
    missing_credentials: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime | None = None
    updated_by: str | None = None

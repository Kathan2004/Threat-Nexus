from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def touch(self) -> None:
        self.updated_at = datetime.now(UTC)


class SourceAttribution(BaseModel):
    source: str
    url: str | None = None
    confidence: int = Field(ge=0, le=100, default=50)
    collected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    raw_reference: dict[str, Any] = Field(default_factory=dict)

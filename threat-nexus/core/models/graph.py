from pydantic import Field

from core.models.base import Entity, SourceAttribution


class Relationship(Entity):
    source_id: str
    source_type: str
    target_id: str
    target_type: str
    relation: str
    score: float = Field(ge=0, le=1, default=0.5)
    sources: list[SourceAttribution] = Field(default_factory=list)

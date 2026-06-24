from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from core.models.domain import ThreatEvent


class PluginHealth(BaseModel):
    healthy: bool
    details: dict[str, Any] = Field(default_factory=dict)


class PluginRuntimeConfig(BaseModel):
    enabled: bool = True
    base_url: str | None = None
    credentials: dict[str, str] = Field(default_factory=dict)
    required_credentials: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def missing_credentials(self) -> list[str]:
        return [name for name in self.required_credentials if not self.credentials.get(name)]


class CollectorPlugin(ABC):
    name: str
    version: str
    source_reputation: int = 50
    runtime_config: PluginRuntimeConfig = PluginRuntimeConfig()

    def configure(self, config: PluginRuntimeConfig) -> None:
        self.runtime_config = config

    @abstractmethod
    async def collect(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def normalize(self, raw: dict[str, Any]) -> ThreatEvent:
        raise NotImplementedError

    @abstractmethod
    async def validate(self, event: ThreatEvent) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> PluginHealth:
        raise NotImplementedError

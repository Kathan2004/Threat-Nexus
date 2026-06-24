from core.models.graph import Relationship


class GraphTraversalService:
    def neighbors(self, entity_id: str, relationships: list[Relationship]) -> list[Relationship]:
        return [rel for rel in relationships if rel.source_id == entity_id or rel.target_id == entity_id]

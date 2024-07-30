from typing import List
from pydantic import BaseModel, Field

class EntityExtractionModel(BaseModel):
    paragraph: List[str] = Field(..., description="List of paragraph types")
    requirement: List[str] = Field(..., description="List of requirement types")

    def validate_entities(self) -> bool:
        return all(entity in self.paragraph for entity in self.requirement)

class NerExtractionModel(BaseModel):
    id: str = Field(default="", description="UUID for the message")
    entity_extraction: EntityExtractionModel = Field(..., description="Entity extraction details")
    is_matching_entities: bool = Field(default=False, description="Indicates if the extraction is complete")
    guidance: str = Field(default="", description="guidance why the extraction is incomplete")
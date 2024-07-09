import uuid
from pydantic import BaseModel, Field, UUID4

class CompletenessMessage(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4, description="UUID for the message")
    paragraph: str = Field(..., description="Give a paragraph from a financial notes")
    question: str = Field(..., description="Provide a question from a checklist")
    
llm_prompt_structure_extraction_message_entity = """[
  {
    "id": "uuid",
    "paragraph_entitiy_extraction": "Location: Germany, Organisation: VW GmbH",
    "question_entity_extraction": "Location"
  },
  {
    "id": "uuid",
    "paragraph_entitiy_extraction": "Location: Germany, Organisation: VW GmbH",
    "question_entity_extraction": "Number"
  }
]"""

llm_prompt_structure_completion_message_entity_evaluation = """[
  {
    "id": "uuid",
    "paragraph_entitiy_extraction": "Location: Germany, Organisation: VW GmbH",
    "question_entity_extraction": "Location"
    "is_complete": True
  },
  {
    "id": "uuid",
    "paragraph_entitiy_extraction": "Location: Germany, Organisation: VW GmbH",
    "question_entity_extraction": "Number"
    "is_complete": False
  }
]"""
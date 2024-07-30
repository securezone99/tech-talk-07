from pydantic import BaseModel, Field

class CompletenessMessage(BaseModel):
    id: str = Field(default="", description="UUID for the message")
    paragraph: str = Field(..., description="Give a paragraph from a financial notes")
    requirement: str = Field(..., description="Provide a requirement from a checklist")
    
llm_prompt_structure_extraction_message_entity = """{
    "id": "uuid",
    "entity_extraction": {
      "paragraph": ["Location", "Organisation"],
      "requirement": ["Location"]
    }
  }
"""

llm_prompt_structure_completion_message_entity_evaluation = """{
    "id": "uuid",
    "entity_extraction": {
      "paragraph": ["Location", "Organisation"],
      "requirement": ["Location"]
    },
    "is_matching_entities": true
    "guidance": "string"
  }"""
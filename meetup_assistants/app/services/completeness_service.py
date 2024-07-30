import json, logging
from typing import List

from assistants.completeness_agents.completeness_agents_chat import AgentsExecutor
from models.completeness_message import CompletenessMessage

class CompletenessService:
    def __init__(self):
        pass

    def execute_completeness_agents(self, completenessMessage: CompletenessMessage) -> str:
        try:
            # Using Pydantic's model_dump_json() method to serialize the object
            completenessMessageJson = completenessMessage.model_dump_json()
            agents_result = AgentsExecutor().execute_completeness_agents_in_sequence(completenessMessageJson)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
            return "Not valid JSON Format. Please try again."

        return agents_result
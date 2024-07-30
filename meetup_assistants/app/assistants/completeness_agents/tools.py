import json
import logging
import os
import time
from typing import Annotated

from models.ner_extraction_model import NerExtractionModel

class Tools:

    async def verify_llm_extraction_json(self, completeness_message: Annotated[str, "JSON string to be verified"]) -> str:
        try:
            logging.info(f"\n\n\n##### Call verify_llm_extraction_json: {completeness_message}")
            completeness_message_json = json.loads(completeness_message)

            if isinstance(completeness_message_json, dict):
                completeness_message_json = [completeness_message_json]
                
            for item in completeness_message_json:
                ner_extraction_model = NerExtractionModel(**item)
                if ner_extraction_model.entity_extraction.validate_entities():
                    ner_extraction_model.is_matching_entities = True

                ner_extraction_dict = ner_extraction_model.model_dump()
                # Convert UUID to string
                ner_extraction_dict['id'] = str(ner_extraction_dict['id'])
                self.save_file("assistant_output.json", json.dumps(ner_extraction_dict, indent=2))

            time.sleep(1)
            return "Valid JSON Format. You can TERMINATE now the chat."
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
            return f"Not valid JSON Format. Fix the following error: {e}"

    async def verify_llm_evaluation_string(self, guidance: Annotated[str, "guidance string to be verified"]) -> str:
        try:
            logging.info(f"\n\n\n##### Call verify_llm_evaluation_string: {guidance}\n\n\n")
            
            completeness_message_json = self.load_json_file("assistant_output.json")
            if isinstance(completeness_message_json, dict):
                completeness_message_json = [completeness_message_json]
            
            for item in completeness_message_json:
                ner_extraction_model = NerExtractionModel(**item)

                ner_extraction_model.guidance = guidance #"All extracted Entities covered by the paragraph."
                ner_extraction_dict = ner_extraction_model.model_dump()
                self.save_file("assistant_output.json", json.dumps(ner_extraction_dict, indent=2))
        
            time.sleep(1)
            return "Valid Format. You can TERMINATE now the chat."
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
            return f"Not valid Format. Fix the following error: {e}"


    def load_json_file(self, file_name: str) -> dict:
        try:
            file_path = os.path.join(os.getcwd(), file_name)
            if not os.path.exists(file_path):
                return {"error": "File does not exist"}
        
            with open(file_path, 'r') as file:
                content = json.load(file)
            return content
        except Exception as e:
            logging.error(f"Failed to load JSON file: {e}")
            return {"error": f"Failed to load JSON file: {e}"}
        
    def save_file(self, file_name: str, content: str) -> str:
        try:
            file_path = os.path.join(os.getcwd(),  file_name)
            with open(file_path, 'w') as file:
                file.write(content)
            return f"Saved file: {file_path}"
        except Exception as e:
            return f"Failed to save file: {e}"

    def delete_file(self, file_name: str) -> str:
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"Deleted file: {file_path}"
        else:
            return f"File does not exist: {file_path}"
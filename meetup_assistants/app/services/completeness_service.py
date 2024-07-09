import json
import logging
import os

class CompletenessService:
    def __init__(self):
        pass

    
    def save_file(self, file_name: str, content: str) -> str:
        file_path = os.path.join(os.getcwd(), file_name)
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            logging.info(f"Saved file: {file_path}")
            return f"Saved file: {file_path}"
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
            return f"Failed to save file: {e}"

    def delete_file(self, file_path: str) -> str:
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Deleted file: {file_path}")
            return f"Deleted file: {file_path}"
        else:
            logging.info(f"File does not exist: {file_path}")
            return f"File does not exist: {file_path}"
        
    def load_json_file(self, file_name: str) -> dict:
        file_path = os.path.join(os.getcwd(), file_name)
        if not os.path.exists(file_path):
            logging.info(f"File does not exist: {file_path}")
            return {"error": "File does not exist"}
        try:
            with open(file_path, 'r') as file:
                content = json.load(file)
            logging.info(f"Loaded JSON file: {file_path}")
            return content
        except Exception as e:
            logging.error(f"Failed to load JSON file: {e}")
            return {"error": f"Failed to load JSON file: {e}"}
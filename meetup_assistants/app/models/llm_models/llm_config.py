import os
from dotenv import load_dotenv

load_dotenv()

class ConfigProvider:
    def __init__(self):
        self.llm_cloud_config_llama_1 = {
            "config_list": [
                {
                    "model": "llama3-70b-8192",
                    "base_url": "https://api.groq.com/openai/v1",
                    "api_key": os.getenv("GROQ_API_KEY"),
                    "api_type": "groq",
                    "price": None
                }
            ],
        }

        self.llm_cloud_config_llama_2 = {
            "config_list": [
                {
                    "model": "llama3-70b-8192",
                    "base_url": "https://api.groq.com/openai/v1",
                    "api_key": os.getenv("GROQ_API_KEY_2"),
                    "api_type": "groq",
                    "price": None
                }
            ],
        }

    def get_llm_cloud_config_llama_1(self):
        return self.llm_cloud_config_llama_1

    def get_llm_cloud_config_llama_2(self):
        return self.llm_cloud_config_llama_2

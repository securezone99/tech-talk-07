import json, autogen, logging, functools

from .prompts import secure_zone_proxy_system_message, extraction_checker_message, evaluation_checker_message
from .tools import Tools
from models.llm_models.llm_config import ConfigProvider

class AgentsExecutor:
    def __init__(self):
        self.tools = Tools()
        self.llm_cloud_config_llama_1 = ConfigProvider().get_llm_cloud_config_llama_1()
        self.llm_cloud_config_llama_2 = ConfigProvider().get_llm_cloud_config_llama_2()
        
        self.extraction_assistant = autogen.AssistantAgent(name="Extraction Assistant", system_message=extraction_checker_message, llm_config=self.llm_cloud_config_llama_1)
        self.evaluation_assistant = autogen.AssistantAgent(name="Evaluation Assistant", system_message=evaluation_checker_message, llm_config=self.llm_cloud_config_llama_2)

        self.secure_zone_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            system_message=secure_zone_proxy_system_message,
            is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            code_execution_config={"use_docker": False},
        )

        verify_llm_extraction_json_bound = functools.partial(self.tools.verify_llm_extraction_json)
        verify_llm_evaluation_string_bound = functools.partial(self.tools.verify_llm_evaluation_string)

        self.secure_zone_proxy.register_for_execution(name="verify_llm_extraction_json")(verify_llm_extraction_json_bound)
        self.secure_zone_proxy.register_for_execution(name="verify_llm_evaluation_string")(verify_llm_evaluation_string_bound)
        self.extraction_assistant.register_for_llm(name="verify_llm_extraction_json", description="Verify the JSON structure and save it if valid.")(verify_llm_extraction_json_bound)
        self.evaluation_assistant.register_for_llm(name="verify_llm_evaluation_string", description="Verify the JSON structure and save it if valid.")(verify_llm_evaluation_string_bound)

    async def execute_completeness_agents_in_sequence(self, completenessMessageJson: json) -> json:
        
        logging.info(f" Starting Completeness Agents with:\n\n {completenessMessageJson}")
        
        # First Assistant Chat
        task = f""" Firstly: Extract NER's from given paragraph and requirement and Secondly use the function call to save the json as string. \n
        Here is the original format (keep the original uuid's):\n{completenessMessageJson}"""
        
        await self.secure_zone_proxy.a_initiate_chat(self.extraction_assistant, message=task)
        
        #loaded_completeness_extraction_json = self.tools.load_json_file("assistant_output.json")
        
        # Second Assistant Chat
        task = f""" Firstly: Evaluation based on the given paragraph and requirement the reason why the requirement 
        can't be a answered. Use a function call and only return the reason as a string: Here is the original input:\n{completenessMessageJson}"""

        await self.secure_zone_proxy.a_initiate_chat(self.evaluation_assistant, message=task)

        final_loaded_json = self.tools.load_json_file("assistant_output.json")
        #self.tools.delete_file("assistant_output.json")
        
        return final_loaded_json

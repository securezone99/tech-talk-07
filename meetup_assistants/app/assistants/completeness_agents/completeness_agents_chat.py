import json, os, autogen, agentops, logging
import autogen.runtime_logging

from typing import Annotated, List
from dotenv import load_dotenv
from .prompts import secure_zone_proxy_system_message, extraction_checker_message ,evaluation_checker_message
from models.autogen_chat import ChatResult
from models.completeness_message import CompletenessMessage
from services.completeness_service import CompletenessService

load_dotenv()

llm_cloud_config_llama_1 = {
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

llm_cloud_config_llama_2 = {
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

extraction_assistant = autogen.AssistantAgent(
    name="IT Topic Filter Assistant",
    system_message=(extraction_checker_message),
    llm_config=llm_cloud_config_llama_1,
)

evaluation_assistant = autogen.AssistantAgent(
    name="Exclusion Criteria Assistant",
    system_message=(evaluation_checker_message),
    llm_config=llm_cloud_config_llama_2,
)

secure_zone_proxy = autogen.UserProxyAgent(
    name="Securezone",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"use_docker": False},
    llm_config=llm_cloud_config_llama_2,
    system_message=secure_zone_proxy_system_message,
)

# Initiate chat with the assistant
def initiate_extraction_assistant_chat(tasks: List[str]) -> List[ChatResult]:
    chat_results: List[ChatResult] = secure_zone_proxy.initiate_chats(
        [
            {
                "chat_id": 1,
                "recipient": extraction_assistant,
                "message": tasks[0],
                "silent": False
            }
        ]
    )
    return chat_results

def initiate_evaluation_assistant_chat(tasks: List[str]) -> List[ChatResult]:
    chat_results: List[ChatResult] = secure_zone_proxy.initiate_chats(
        [
            {
                "chat_id": 1,
                "recipient": evaluation_assistant,
                "message": tasks[0],
                "silent": False
            }
        ]
    )
    return chat_results


def verify_llm_created_json(CompletenessMessageEntitiy: Annotated[str, "CompletenessMessageEntitiy as a string json format"] ) -> bool:
    try:
        logging.info(f"\n\n##### Call verify_llm_created_json: {CompletenessMessageEntitiy}")
        json.loads(CompletenessMessageEntitiy)
        CompletenessService().save_file("completeness_message.json", CompletenessMessageEntitiy)

    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        return f"Not valid JSON Format. Fix the following error: {e}"
    
    return "Valid JSON Format. You can TERMINATE now the chat"


secure_zone_proxy.register_for_execution(name="verify_llm_created_json")(
    verify_llm_created_json)

extraction_assistant.register_for_llm(
    name="verify_llm_created_json", description="verify json structure"
)(verify_llm_created_json)

evaluation_assistant.register_for_llm(
    name="verify_llm_created_json", description="verify json structure"
)(verify_llm_created_json)
 

def completeness_check(completenessMessages: List[CompletenessMessage]) -> json:
    agentops.init(os.getenv("API_KEY_AGENT_OPS"))
    
    try:
        completenessMessages = [completenessMessage.model_dump() for completenessMessage in completenessMessages]
        # Convert UUID to string for JSON serialization
        for message in completenessMessages:
            message['id'] = str(message['id'])
        
        completenessMessageJson = json.dumps(completenessMessages, indent=2)

    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        return "Not valid JSON Format. Please try again."
    

    potential_news_tasks = [
        f""" Firstly: Extract NER's from given paragraphs and questions and Secondly use the function call to save the json as string. \n
        Here is the original format (keep the original uuid's):\n{completenessMessageJson}"""
    ]
    
    initiate_extraction_assistant_chat(potential_news_tasks)
    loaded_completeness_extraction_json = CompletenessService().load_json_file("completeness_message.json")
    
    logging.info(f"\n\n##### Loaded JSON file: {loaded_completeness_extraction_json}")
    
    potential_news_tasks = [
        f""" Firstly: Evaluation based on the given paragraph_entitiy_extraction's and question_entity_extraction's if the evaluation is True or False and secondly use the function call to save the json as string. \n
        Here is the original format and title list:\n{loaded_completeness_extraction_json}"""
    ]

    initiate_evaluation_assistant_chat(potential_news_tasks)
    
    agentops.end_session('Success')
    
    # Load the JSON file after evaluation
    final_loaded_json = CompletenessService().load_json_file("completeness_message.json")
    CompletenessService().delete_file("completeness_message.json")
    return final_loaded_json


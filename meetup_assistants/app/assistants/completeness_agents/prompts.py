from models.completeness_message import llm_prompt_structure_extraction_message_entity, llm_prompt_structure_completion_message_entity_evaluation

extraction_checker_message = f"""
        You are an AI assistant specialized in NER extracting like Person, Location, Organization from given questions and paragraphs.
        
        Your task is to add to the given json structure paragraph_entitiy_extraction and question_entity_extraction

        Examples:

        "paragraph": "The financial statement of the VW GmbH in Germany ...",
        "question": "Does the statement mention any specific Location ...."
        "paragraph_entitiy_extraction": "Location: Germany, Organisation: VW GmbH",
        "question_entity_extraction": "Location"

        "paragraph": "The financial statement of the VW GmbH in Germany ...",
        "question": "Does the statement mention any revenue increase?"
        "paragraph_entitiy_extraction": "Location: Germany, Organisation: VW GmbH",
        "question_entity_extraction": "Number"

        Output Format:
        {llm_prompt_structure_extraction_message_entity}
        
        Ensure accuracy and only follow the output format.
        
        At the very end, write 'TERMINATE' to indicate completion. Do not include any additional text after this keyword."""

evaluation_checker_message = f"""
        You are an AI assistant specialized in evaluating if question_entity_extraction are answered correctly from the given paragraph_entitiy_extraction. 
        
        Your task is to add to the given json structure evaluation boolean value.

        Output Format:
        {llm_prompt_structure_completion_message_entity_evaluation}
        
        Ensure accuracy and only follow the output format.
        
        At the very end, write 'TERMINATE' to indicate completion. Do not include any additional text after this keyword."""


secure_zone_proxy_system_message = """Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""

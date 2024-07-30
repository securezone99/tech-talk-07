from models.completeness_message import llm_prompt_structure_extraction_message_entity, llm_prompt_structure_completion_message_entity_evaluation

extraction_checker_message = f"""
        You are an AI assistant specialized in NER extracting only for entities Date, Person, Location, Organization, Number based on the context from given requirement and paragraphs.
        
        Your task is to add to the given json structure paragraph entitiy extraction and requirement entityextraction

        Examples:

        Goldman Sachs Group Inc., headquartered in New York, has committed to investing 500 million USD in renewable energy projects across Europe as part of their environmental strategy. => ["Location", "Organisation", "Number"]
        Who led the audit for JPMorgan Chase & Co., and what was the key finding also how much was invested?" => ["Number", "Organisation", "Person"]
        The latest compliance report from Barclays PLC shows that the London-based organization met all regulatory requirements in the fiscal year 2022, avoiding any financial penalties." => ["Date", "Location", "Organisation", "Number"]
        Which organization's compliance report is discussed, and what was the outcome? => ["Organisation"]
        What is their target year? => ["Date"]
        vehicle sales => ["Number"]
        Outline the company's approach => ["Organisation"]
        
        Output Format:
        {llm_prompt_structure_extraction_message_entity}
        
        Ensure accuracy of the extraction based on the context and only follow the output format.
        
        At the very end, write 'TERMINATE' to indicate completion. Do not include any additional text after this keyword."""

evaluation_checker_message = f"""
        You are an AI assistant specialized in evaluating if an given requirement can be fully answered based on the given paragraph. 
        
        Your create a professional and helpful guidance why the requirement is not answered by the paragraph given.

        When you think the requirement is fully answered, only write 'Requirement fully met.' as guidance.
        Output Format:
        {llm_prompt_structure_completion_message_entity_evaluation}
        
        Ensure accuracy of the output format.
        
        At the very end, write 'TERMINATE' to indicate completion. Do not include any additional text after this keyword."""


secure_zone_proxy_system_message = """Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""

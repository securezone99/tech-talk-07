from typing import List
from fastapi import APIRouter, Body

from assistants.completeness_agents.completeness_agents_chat import completeness_check
from models.completeness_message import CompletenessMessage

router = APIRouter()

@router.post("/verify_completion")
def completeness(completenessMessages: List[CompletenessMessage] = Body(..., example=[
                {
                    "id": "d290f1ee-6c54-4b01-90e6-d701748f0853",
                    "paragraph": "In the recent annual financial disclosure, Apple Inc. reported a robust increase in total revenue, primarily attributed to an upsurge in iPhone sales across the U.S. and European markets. According to IFRS 15, revenue from contracts with customers was recognized at the point of transfer of goods, reflecting Apple's effective management of its product launches and customer engagement strategies.",
                    "question": "According to the paragraph, does Apple Inc. apply IFRS 15 in its revenue recognition for iPhone sales?"
                },
                {
                    "id": "d290f1ee-6c54-4b01-90e6-d701748f0854",
                    "paragraph": "Apple Inc.'s financial statement for the fiscal year reveals significant investment in property, plant, and equipment, focusing on expanding manufacturing facilities in China and Vietnam. This aligns with IFRS 16 requirements, where such expenditures are recognized as assets and depreciated over their useful life. The company’s strategy to decentralize its production line has also been detailed.",
                    "question": "Does the financial statement reflect compliance with IFRS 16 for the treatment of PPE investments in Asia?"
                }
            ])):
    return completeness_check(completenessMessages)

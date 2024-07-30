from typing import List
from fastapi import APIRouter, Body

from services.completeness_service import CompletenessService
from models.completeness_message import CompletenessMessage

router = APIRouter()

@router.post("/verify_completion_async")
async def completeness_async(completenessMessages: CompletenessMessage = Body(..., example=
                {
                    "id": "d290f1ee-6c54-4b01-90e6-d701748f0853",
                    "paragraph": "In the recent annual financial disclosure, Apple Inc. reported a robust increase in total revenue, primarily attributed to an upsurge in iPhone sales across the U.S. and European markets. According to IFRS 15, revenue from contracts with customers was recognized at the point of transfer of goods, reflecting Apple's effective management of its product launches and customer engagement strategies.",
                    "requirement": "According to the paragraph, does Apple Inc. apply IFRS 15 in its revenue recognition for iPhone sales and how many have been sold?"
                }
            )):

    return await CompletenessService().execute_completeness_agents(completenessMessages)

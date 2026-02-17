from services.llm_service import generate_response
from app.prompt_manager import get_prompt

async def get_intent(message: str) -> str:
    system_instruction = await get_prompt("intent")
    intent = await generate_response(message, system_instruction)
    return intent.upper()

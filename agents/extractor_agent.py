from services.llm_service import generate_response
from app.prompt_manager import get_prompt
import json
import re

async def extract_data(message: str) -> dict:
    system_instruction = await get_prompt("extract")
    response = await generate_response(message, system_instruction)
    try:
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return json.loads(response)
    except Exception as e:
        print(f"Error parsing Extractor JSON: {e}")
        return {"product": None, "quantity": None, "customer_type": None}

from services.llm_service import generate_response
from app.prompt_manager import get_prompt

async def generate_reply(customer_type: str, product: str, quantity: int, price: float, stock_status: str, goal: str) -> str:
    template = await get_prompt("response")
    prompt = template.format(
        customer_type=customer_type,
        product=product or "unknown",
        quantity=quantity or "unknown",
        price=price or "unknown",
        stock_status=stock_status,
        goal=goal
    )
    response = await generate_response("Draft the response now.", prompt)
    return response

# Placeholder for customer classifier
from typing import Optional

def classify_customer_type(message: str) -> Optional[str]:
    message_lower = message.lower()
    if "wholesale" in message_lower or "bulk" in message_lower:
        return "wholesaler"
    elif "retail" in message_lower or "shop" in message_lower:
        return "retailer"
    elif "individual" in message_lower or "personal" in message_lower:
        return "individual"
    return None

"""
Validation schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal

class ExtractedData(BaseModel):
    product: Optional[str] = Field(None, max_length=100)
    quantity: Optional[int] = Field(None, ge=1, le=10000)
    customer_type: Optional[Literal["wholesaler", "retailer", "individual"]] = None

class IncomingMessage(BaseModel):
    user: str
    message: str
    platform: str

class OutgoingResponse(BaseModel):
    reply: str

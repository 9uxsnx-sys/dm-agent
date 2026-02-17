from pydantic import BaseModel

class IncomingMessage(BaseModel):
    user: str
    message: str
    platform: str

class OutgoingResponse(BaseModel):
    reply: str

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    analysis: str
    explanation: str
    recommendations: list[str]
    evidence: list[str]

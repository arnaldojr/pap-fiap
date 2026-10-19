from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=1000)

    @field_validator("conversation_id", "message")
    @classmethod
    def remover_espacos_externos(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("o campo não pode conter apenas espaços")

        return value


class ChatResponse(BaseModel):
    conversation_id: str
    response: str


class HealthResponse(BaseModel):
    status: str

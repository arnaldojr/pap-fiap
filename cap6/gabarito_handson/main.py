import logging

from fastapi import FastAPI, HTTPException

from agent import responder
from schemas import ChatRequest, ChatResponse


logger = logging.getLogger(__name__)

app = FastAPI(
    title="API do Assistente de Biblioteca",
    description=(
        "API para consultar livros e empréstimos por meio "
        "de um agente de IA."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = responder(
            message=request.message,
            conversation_id=request.conversation_id,
        )
    except Exception as error:
        logger.exception("Falha ao processar a mensagem.")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível processar a mensagem.",
        ) from error

    return ChatResponse(
        conversation_id=request.conversation_id,
        response=response,
    )

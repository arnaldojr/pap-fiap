import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from agent import criar_agente, responder
from schemas import ChatRequest, ChatResponse, HealthResponse


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent = await criar_agente()
    yield


app = FastAPI(
    title="API do Assistente Acadêmico",
    description=(
        "API para consultar matrículas, cursos e calendário "
        "por meio de um agente de IA."
    ),
    version="2.0.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    request: Request,
) -> ChatResponse:
    try:
        response = await responder(
            agent=request.app.state.agent,
            message=payload.message,
            conversation_id=payload.conversation_id,
        )
    except Exception as error:
        logger.exception(
            "Falha ao processar a conversa %s.",
            payload.conversation_id,
        )
        raise HTTPException(
            status_code=500,
            detail="Não foi possível processar a mensagem.",
        ) from error

    return ChatResponse(
        conversation_id=payload.conversation_id,
        response=response,
    )

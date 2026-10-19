from pathlib import Path

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.mcp import MCPAdapter
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from config import MODEL_NAME, validar_configuracao
from tools import consultar_matricula
from tools_api import consultar_curso_api


consultar_matricula_tool = tool(consultar_matricula)
consultar_curso_api_tool = tool(consultar_curso_api)

SYSTEM_PROMPT = """
Você atende estudantes de uma plataforma de cursos.

- Use as ferramentas para consultar matrículas, cursos e calendário.
- Não invente códigos, registros, prazos ou resultados.
- Se faltar um identificador necessário, peça esse dado.
- Quando a pergunta partir de uma matrícula, consulte primeiro a matrícula.
- Use o codigo_curso obtido nas consultas seguintes.
- Consulte novamente dados operacionais quando o usuário perguntar pelo valor atual.
- Responda de forma objetiva depois de obter os dados necessários.
"""

checkpointer = InMemorySaver()


async def carregar_tools_mcp() -> list:
    servidor = Path(__file__).with_name("mcp_server.py")

    async with MCPAdapter(servidor) as adapter:
        return await adapter.list_tools()


async def criar_agente():
    validar_configuracao()
    model = init_chat_model(MODEL_NAME)
    mcp_tools = await carregar_tools_mcp()

    return create_agent(
        model=model,
        tools=[
            consultar_matricula_tool,
            consultar_curso_api_tool,
            *mcp_tools,
        ],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )


async def responder(
    agent,
    message: str,
    conversation_id: str,
) -> str:
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": conversation_id,
            },
            "metadata": {
                "thread_id": conversation_id,
                "canal": "api",
            },
            "tags": ["cap7", "assistente-academico"],
            "run_name": "assistente_academico",
        },
    )

    return result["messages"][-1].text

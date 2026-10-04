from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from config import MODEL_NAME


livros = {
    "LIV-101": {
        "codigo": "LIV-101",
        "titulo": "Python Fluente",
        "paginas": 640,
    },
    "LIV-202": {
        "codigo": "LIV-202",
        "titulo": "Clean Code",
        "paginas": 464,
    },
}

emprestimos = {
    "EMP-500": {
        "emprestimo": "EMP-500",
        "status": "ativo",
        "codigo_livro": "LIV-101",
    }
}


def consultar_livro(codigo: str) -> dict:
    """Consulta título e quantidade de páginas de um livro pelo código."""
    codigo = codigo.strip().upper()

    if not codigo.startswith("LIV-"):
        return {"erro": "código de livro inválido"}

    livro = livros.get(codigo)

    if livro is None:
        return {"erro": "livro não encontrado"}

    return livro.copy()


def consultar_emprestimo(emprestimo: str) -> dict:
    """Consulta status e código do livro associado a um empréstimo."""
    emprestimo = emprestimo.strip().upper()

    if not emprestimo.startswith("EMP-"):
        return {"erro": "identificador de empréstimo inválido"}

    registro = emprestimos.get(emprestimo)

    if registro is None:
        return {"erro": "empréstimo não encontrado"}

    return registro.copy()


def renovar_emprestimo(emprestimo: str) -> dict:
    """Renova um empréstimo ativo e devolve seu novo estado."""
    emprestimo = emprestimo.strip().upper()

    if not emprestimo.startswith("EMP-"):
        return {"erro": "identificador de empréstimo inválido"}

    registro = emprestimos.get(emprestimo)

    if registro is None:
        return {"erro": "empréstimo não encontrado"}

    if registro["status"] != "ativo":
        return {
            "erro": "empréstimo não pode ser renovado",
            "status_atual": registro["status"],
        }

    registro["status"] = "renovado"
    return registro.copy()


consultar_livro_tool = tool(consultar_livro)
consultar_emprestimo_tool = tool(consultar_emprestimo)
renovar_emprestimo_tool = tool(renovar_emprestimo)

tools_biblioteca = [
    consultar_livro_tool,
    consultar_emprestimo_tool,
    renovar_emprestimo_tool,
]

SYSTEM_PROMPT = """
Você atende usuários de uma biblioteca.

- Use as tools para consultar livros e empréstimos.
- Não invente livros, empréstimos, códigos ou resultados.
- Se faltar um identificador necessário, peça esse dado.
- Para descobrir informações do livro associado a um empréstimo,
  consulte primeiro o empréstimo e use o codigo_livro retornado.
- Use renovar_emprestimo somente quando o usuário pedir explicitamente
  a renovação.
- Responda de forma objetiva depois de obter os dados necessários.
"""

model = init_chat_model(MODEL_NAME)
checkpointer = InMemorySaver()

agente_biblioteca = create_agent(
    model=model,
    tools=tools_biblioteca,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)


def responder(message: str, conversation_id: str) -> str:
    result = agente_biblioteca.invoke(
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
            }
        },
    )

    return result["messages"][-1].text

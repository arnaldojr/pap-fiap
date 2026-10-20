from fastmcp import FastMCP

from dados import CALENDARIO, CRITERIOS_CONCLUSAO


mcp = FastMCP("Calendário Acadêmico")


def buscar_calendario(codigo_curso: str) -> dict:
    codigo_curso = codigo_curso.strip().upper()

    if not codigo_curso.startswith("CUR-"):
        return {"erro": "código de curso inválido"}

    atividade = CALENDARIO.get(codigo_curso)

    if atividade is None:
        return {"erro": "atividade não encontrada"}

    return atividade.copy()


def buscar_criterios_conclusao(codigo_curso: str) -> dict:
    codigo_curso = codigo_curso.strip().upper()

    if not codigo_curso.startswith("CUR-"):
        return {"erro": "código de curso inválido"}

    criterios = CRITERIOS_CONCLUSAO.get(codigo_curso)

    if criterios is None:
        return {"erro": "critérios de conclusão não encontrados"}

    return criterios.copy()


@mcp.tool
def consultar_calendario(codigo_curso: str) -> dict:
    """Consulta a próxima atividade e o prazo de um curso."""
    return buscar_calendario(codigo_curso)


@mcp.tool
def consultar_criterios_conclusao(codigo_curso: str) -> dict:
    """Consulta a nota mínima e o percentual mínimo de atividades
    exigidos para concluir um curso.
    """
    return buscar_criterios_conclusao(codigo_curso)


if __name__ == "__main__":
    mcp.run()

import httpx

from config import CATALOGO_API_URL


def consultar_curso_api(codigo: str) -> dict:
    """Consulta nome, carga horária e modalidade de um curso na API de catálogo."""
    codigo = codigo.strip().upper()

    if not codigo.startswith("CUR-"):
        return {"erro": "código de curso inválido"}

    try:
        response = httpx.get(
            f"{CATALOGO_API_URL}/cursos/{codigo}",
            timeout=3.0,
        )
    except httpx.TimeoutException:
        return {"erro": "tempo limite excedido ao consultar o catálogo"}
    except httpx.RequestError:
        return {"erro": "catálogo indisponível"}

    if response.status_code == 404:
        return {"erro": "curso não encontrado"}

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError:
        return {
            "erro": "falha ao consultar o catálogo",
            "status_code": response.status_code,
        }

    return response.json()

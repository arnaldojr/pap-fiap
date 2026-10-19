from dados import MATRICULAS


def consultar_matricula(matricula: str) -> dict:
    """Consulta o status e o curso associado a uma matrícula."""
    matricula = matricula.strip().upper()

    if not matricula.startswith("MAT-"):
        return {"erro": "identificador de matrícula inválido"}

    registro = MATRICULAS.get(matricula)

    if registro is None:
        return {"erro": "matrícula não encontrada"}

    return registro.copy()

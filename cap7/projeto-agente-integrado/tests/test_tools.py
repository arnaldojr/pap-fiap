from mcp_server import buscar_calendario
from tools import consultar_matricula


def test_consultar_matricula_existente() -> None:
    resultado = consultar_matricula(" mat-500 ")

    assert resultado["status"] == "ativa"
    assert resultado["codigo_curso"] == "CUR-101"


def test_consultar_matricula_com_formato_invalido() -> None:
    resultado = consultar_matricula("500")

    assert resultado == {"erro": "identificador de matrícula inválido"}


def test_buscar_calendario_existente() -> None:
    resultado = buscar_calendario("cur-101")

    assert resultado["atividade"] == "Projeto de automação"
    assert resultado["prazo"] == "2026-11-14"

from mcp_server import buscar_criterios_conclusao


def test_buscar_criterios_existentes() -> None:
    resultado = buscar_criterios_conclusao(" cur-101 ")

    assert resultado == {
        "codigo_curso": "CUR-101",
        "nota_minima": 7.0,
        "percentual_minimo_atividades": 75,
    }


def test_buscar_criterios_com_codigo_invalido() -> None:
    resultado = buscar_criterios_conclusao("101")

    assert resultado == {"erro": "código de curso inválido"}


def test_buscar_criterios_nao_cadastrados() -> None:
    resultado = buscar_criterios_conclusao("CUR-999")

    assert resultado == {"erro": "critérios de conclusão não encontrados"}

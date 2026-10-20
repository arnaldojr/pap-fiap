import httpx

import tools_api


def test_consultar_curso_api(monkeypatch) -> None:
    def resposta_controlada(*args, **kwargs):
        return httpx.Response(
            status_code=200,
            json={
                "codigo": "CUR-101",
                "nome": "Python para Automação",
                "carga_horaria": 40,
                "modalidade": "online",
            },
            request=httpx.Request("GET", "http://catalogo/cursos/CUR-101"),
        )

    monkeypatch.setattr(tools_api.httpx, "get", resposta_controlada)

    resultado = tools_api.consultar_curso_api("cur-101")

    assert resultado["codigo"] == "CUR-101"
    assert resultado["carga_horaria"] == 40


def test_consultar_curso_api_indisponivel(monkeypatch) -> None:
    def falha_controlada(*args, **kwargs):
        raise httpx.ConnectError("falha simulada")

    monkeypatch.setattr(tools_api.httpx, "get", falha_controlada)

    resultado = tools_api.consultar_curso_api("CUR-101")

    assert resultado == {"erro": "catálogo indisponível"}

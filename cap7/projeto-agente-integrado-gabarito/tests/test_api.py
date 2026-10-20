from fastapi.testclient import TestClient

import main


class AgenteControlado:
    pass


async def criar_agente_controlado():
    return AgenteControlado()


async def responder_controlado(agent, message, conversation_id):
    return f"Resposta para {conversation_id}: {message}"


def criar_cliente(monkeypatch) -> TestClient:
    monkeypatch.setattr(main, "criar_agente", criar_agente_controlado)
    monkeypatch.setattr(main, "responder", responder_controlado)
    return TestClient(main.app)


def test_health(monkeypatch) -> None:
    with criar_cliente(monkeypatch) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_valido(monkeypatch) -> None:
    with criar_cliente(monkeypatch) as client:
        response = client.post(
            "/chat",
            json={
                "conversation_id": "teste-001",
                "message": "Consulte MAT-500",
            },
        )

    assert response.status_code == 200
    assert response.json()["conversation_id"] == "teste-001"
    assert "Consulte MAT-500" in response.json()["response"]


def test_chat_com_mensagem_vazia(monkeypatch) -> None:
    with criar_cliente(monkeypatch) as client:
        response = client.post(
            "/chat",
            json={
                "conversation_id": "teste-001",
                "message": "   ",
            },
        )

    assert response.status_code == 422

import asyncio

from agent import criar_agente, responder


async def main() -> None:
    agent = await criar_agente()
    conversa = "validacao-001"

    resposta_1 = await responder(
        agent=agent,
        message=(
            "Minha matrícula é MAT-500. Em qual curso estou "
            "e qual é a próxima atividade?"
        ),
        conversation_id=conversa,
    )
    print("Turno 1:")
    print(resposta_1)

    resposta_2 = await responder(
        agent=agent,
        message="Qual é a carga horária desse curso?",
        conversation_id=conversa,
    )
    print("\nTurno 2 na mesma conversa:")
    print(resposta_2)

    resposta_3 = await responder(
        agent=agent,
        message="Qual é a carga horária desse curso?",
        conversation_id="validacao-002",
    )
    print("\nPrimeiro turno em outra conversa:")
    print(resposta_3)


if __name__ == "__main__":
    asyncio.run(main())

# Projeto de Agente Integrado

Aplicação de referência do Capítulo 7 de PAP. O projeto integra uma tool
Python local, uma tool que consulta uma API REST, tools de calendário e
critérios de conclusão descobertas em um servidor MCP, memória de curto prazo,
uma API FastAPI e tracing opcional no LangSmith.

## Requisitos

- Python 3.10 ou superior
- chave válida da API Gemini
- conta e chave do LangSmith apenas se o tracing for habilitado

## Como executar

1. Crie e ative um ambiente virtual.
2. Instale as dependências.

   ```bash
   pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env` e informe a chave do Gemini.
4. Inicie a API de catálogo em um terminal.

   ```bash
   fastapi dev catalogo_api.py --port 8001
   ```

5. Inicie a API do assistente em outro terminal.

   ```bash
   fastapi dev main.py --port 8000
   ```

6. Acesse `http://127.0.0.1:8000/docs`.

O servidor MCP é iniciado por `MCPAdapter` pelo transporte stdio. Ele não
precisa ser iniciado em um terceiro terminal.

## Como habilitar tracing

Altere as variáveis abaixo no arquivo `.env`.

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=sua_chave_langsmith_aqui
LANGSMITH_PROJECT=pap-cap7-agente-integrado
```

Reinicie a API do assistente. As próximas execuções serão enviadas para o
projeto informado no LangSmith.

## Como validar

Execute os testes determinísticos.

```bash
python -m pytest -v
```

Com as duas APIs em execução, valide o agente e a continuidade da conversa.

```bash
python validar_integracao.py
```

## Hands-on de critérios de conclusão

A tool `consultar_criterios_conclusao` recebe `codigo_curso` e devolve os
critérios fictícios definidos em `dados.py`:

| Curso | Nota mínima (0 a 10) | Atividades concluídas (0 a 100%) |
| --- | --- | --- |
| CUR-101 | 7,0 | 75% |
| CUR-202 | 6,0 | 100% |

Esses dados descrevem regras do curso. A aplicação não possui notas ou
percentuais individuais para afirmar que um estudante já cumpriu os requisitos.

A consulta normaliza o código, valida o prefixo `CUR-` e devolve uma cópia do
registro encontrado. Um identificador inválido retorna
`{"erro": "código de curso inválido"}`. Um código sem registro retorna
`{"erro": "critérios de conclusão não encontrados"}`.

Execute os três testes da nova função:

```bash
python -m pytest tests/test_criterios.py -v
```

Eles verificam normalização e sucesso, código inválido e critérios não
cadastrados, sem chamadas ao modelo ou serviços em funcionamento. Para verificar
também os testes anteriores, execute `python -m pytest -v`.

Depois de alterar `mcp_server.py`, reinicie a API principal para que a descoberta
MCP inclua a nova tool. Mantenha o catálogo em funcionamento e o tracing
habilitado durante a validação integrada.

Envie as mensagens a seguir para `POST /chat` usando os campos
`conversation_id` e `message`. Mantenha a API principal em execução entre os
turnos.

| conversation_id | message | Verificação esperada |
| --- | --- | --- |
| academico-hands-on-001 | Minha matrícula é MAT-500. Em qual curso estou? | Identificação de CUR-101 e Python para Automação. |
| academico-hands-on-001 | Quais são os critérios para concluir esse curso? | Chamada à nova tool com CUR-101; nota mínima 7,0 e 75% das atividades. |
| academico-hands-on-002 | Quais são os critérios para concluir esse curso? | Solicitação de uma informação que identifique o curso. |
| academico-hands-on-003 | Quais são os critérios de conclusão do curso CUR-999? | Comunicação de que os critérios não estão disponíveis. |
| academico-hands-on-004 | Qual é o status da matrícula MAT-500? | Consulta de matrícula sem acionar a nova tool. |

No LangSmith, confira o nome, os argumentos e o resultado da nova tool. Os dois
primeiros turnos devem compartilhar a thread, enquanto os demais pertencem a
conversas separadas. No caso de CUR-999, o erro é um dado retornado pela consulta;
ele não precisa aparecer como uma exceção no tracing.

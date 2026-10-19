# Projeto de Agente Integrado

Aplicação de referência do Capítulo 7 de PAP. O projeto integra uma tool
Python local, uma tool que consulta uma API REST, uma tool descoberta em um
servidor MCP, memória de curto prazo, uma API FastAPI e tracing opcional no
LangSmith.

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

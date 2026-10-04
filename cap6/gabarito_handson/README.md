# Gabarito — API do Assistente de Biblioteca

Projeto de referência do Hands-on do Capítulo 6 de PAP.

A aplicação disponibiliza, por FastAPI, o agente de biblioteca originalmente executado em notebook. O agente mantém as três tools do material-base e utiliza `conversation_id` no contrato HTTP, convertido internamente para o `thread_id` usado pelo checkpointer.

## Estrutura

```text
gabarito_handson_api_biblioteca/
├── main.py
├── agent.py
├── schemas.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 1. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 3. Configurar a chave

Crie `.env` a partir de `.env.example`:

```text
GOOGLE_API_KEY=sua_chave_aqui
```

O arquivo `.env` está incluído no `.gitignore` e não deve ser enviado ao GitHub.

## 4. Iniciar a API

```bash
fastapi dev main.py
```

A documentação interativa estará disponível em:

```text
http://127.0.0.1:8000/docs
```

## 5. Testar a API

### Health check

`GET /health`

Resposta esperada:

```json
{
  "status": "ok"
}
```

### Chat

`POST /chat`

Primeiro turno:

```json
{
  "conversation_id": "biblioteca-001",
  "message": "Tenho o empréstimo EMP-500. A qual livro ele está associado?"
}
```

Segundo turno, mantendo o mesmo identificador:

```json
{
  "conversation_id": "biblioteca-001",
  "message": "Quantas páginas tem esse livro?"
}
```

A segunda resposta deve utilizar o contexto preservado na conversa.

Para validar o isolamento, repita apenas a segunda pergunta usando outro identificador:

```json
{
  "conversation_id": "biblioteca-002",
  "message": "Quantas páginas tem esse livro?"
}
```

A nova conversa não deve herdar o contexto de `biblioteca-001`.

## Dados disponíveis

Livros:

- `LIV-101` — Python Fluente — 640 páginas
- `LIV-202` — Clean Code — 464 páginas

Empréstimo:

- `EMP-500` — ativo — associado a `LIV-101`

O agente também pode renovar explicitamente o empréstimo `EMP-500` por meio da tool `renovar_emprestimo`.

## Observação

O `InMemorySaver` mantém o estado apenas enquanto o processo da aplicação está em execução. Reiniciar o servidor pode apagar o histórico das conversas.

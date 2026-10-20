from fastapi import FastAPI, HTTPException

from dados import CURSOS


app = FastAPI(
    title="Serviço de Catálogo Acadêmico",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/cursos/{codigo}")
def obter_curso(codigo: str) -> dict:
    codigo = codigo.strip().upper()
    curso = CURSOS.get(codigo)

    if curso is None:
        raise HTTPException(status_code=404, detail="curso não encontrado")

    return curso.copy()

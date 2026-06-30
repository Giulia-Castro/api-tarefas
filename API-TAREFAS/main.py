from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()
tarefas = []
proximo_id = 1

class TarefaEntrada(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False

class Tarefa(TarefaEntrada):
    id: int
    criada_em: str

@app.get("/")
def raiz():
    return {"mensagem": "API de Tarefas funcionando!"}

@app.get("/tarefas")
def listar_tarefas():
    return tarefas

@app.post("/tarefas", status_code=201)
def criar_tarefa(dados: TarefaEntrada):
    global proximo_id

    nova_tarefa = {
        "id": proximo_id,
        "titulo": dados.titulo,
        "descricao": dados.descricao,
        "concluida": dados.concluida,
        "criada_em": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    tarefas.append(nova_tarefa)
    proximo_id += 1

    return nova_tarefa

@app.get("/tarefas/{tarefa_id}")
def buscar_tarefa(tarefa_id: int):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, dados: TarefaEntrada):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            tarefa["titulo"] = dados.titulo
            tarefa["descricao"] = dados.descricao
            tarefa["concluida"] = dados.concluida
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int):
    for i, tarefa in enumerate(tarefas):
        if tarefa["id"] == tarefa_id:
            tarefas.pop(i)
            return {"mensagem": f"Tarefa {tarefa_id} deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")
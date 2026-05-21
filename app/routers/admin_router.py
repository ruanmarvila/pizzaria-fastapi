from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import obter_admin_logado
from app.models import Usuario
from app.services import finalizar_pedido, limpar_usuario_inativos, excluir_usuario

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.get("/")
async def home():
    return {
        "messagem": "você está na rota da administração"
    }

@admin_router.post("/pedido/finalizar/{pedido_id}")
async def finalizar(pedido_id: int, usuario_admin: Usuario = Depends(obter_admin_logado), 
                   session: AsyncSession = Depends(get_db)):
    pedido = await finalizar_pedido(pedido_id, usuario_admin, session)
    return {
        "mensagem": f"Pedido nº{pedido_id} finalizado com sucesso",
        "pedido": pedido
    }

@admin_router.post("/excluir_usuarios")
async def excluir_usuarios_inativos(usuario_admin: Usuario = Depends(obter_admin_logado), session: AsyncSession = Depends(get_db)):
    número_usuario = await limpar_usuario_inativos(usuario_admin, session)
    return {
        "mensagem": f"{número_usuario} usuários excluídos com sucesso"
    }

@admin_router.post("/excluir/usuario/{email}")
async def excluir_usuario_especifico(email: str, usuario_admin: Usuario = Depends(obter_admin_logado), session: AsyncSession = Depends(get_db)):
    usuario = await excluir_usuario(email, usuario_admin, session)

    if usuario:
        return {"mensagem": "usuário excluído com sucesso"}
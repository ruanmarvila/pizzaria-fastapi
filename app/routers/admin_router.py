from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import obter_admin_logado
from app.models import Usuario, StatusPedido
from app.services import limpar_usuario_inativos, excluir_usuario, atualizar_pedido

admin_router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(obter_admin_logado)])

@admin_router.get("/")
async def home():
    return {
        "messagem": "você está na rota da administração"
    }

@admin_router.post("/pedido/atualizar/{pedido_id}")
async def atualizar(pedido_id: int, status: StatusPedido ,usuario_admin: Usuario = Depends(obter_admin_logado), 
                   session: AsyncSession = Depends(get_db)):
    pedido = await atualizar_pedido(pedido_id, status, usuario_admin, session)
    return {
        "mensagem": f"Pedido nº{pedido_id} atualizado com sucesso",
        "pedido": pedido
    }

@admin_router.post("/excluir_usuarios")
async def excluir_usuarios_inativos(usuario_admin: Usuario = Depends(obter_admin_logado), session: AsyncSession = Depends(get_db)):
    número_usuarios = await limpar_usuario_inativos(usuario_admin, session)
    return {
        "mensagem": f"{número_usuarios} usuários excluídos com sucesso"
    }

@admin_router.post("/excluir/usuario/{email}")
async def excluir_usuario_especifico(email: str, usuario_admin: Usuario = Depends(obter_admin_logado), session: AsyncSession = Depends(get_db)):
    usuario = await excluir_usuario(email, usuario_admin, session)

    if usuario:
        return {"mensagem": "usuário excluído com sucesso"}

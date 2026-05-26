from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import obter_usuario_logado
from app.models import Usuario
from app.schemas import PedidoCriarSchema, PedidoItemSchema
from app.services import criar_pedido, cancelar_pedido, adicionar_pedido, remover_pedido, listar_pedido, visualizar_pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(obter_usuario_logado)])

@order_router.get("/")
async def home():
    return {"messagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def cadastrar_pedido(pedido_schema: PedidoCriarSchema, usuario: Usuario = Depends(obter_usuario_logado),session: AsyncSession = Depends(get_db)):
    pedido = await criar_pedido(pedido_schema, usuario, session)

    if pedido:
        return {"mensagem": "Pedido criando com sucessso"}
    
@order_router.post("/pedido/cancelar/{pedido_id}")
async def cancelar(pedido_id: int, usuario: Usuario = Depends(obter_usuario_logado), 
                   session: AsyncSession = Depends(get_db)):
    pedido = await cancelar_pedido(pedido_id, usuario, session)
    return {
        "mensagem": f"Pedido nº{pedido_id} cancelado com sucesso",
        "pedido": pedido
    }

@order_router.post("/pedido/adicionar/{pedido_id}")
async def adicionar(pedido_id: int, pedido_item: PedidoItemSchema, usuario: Usuario = Depends(obter_usuario_logado),
                    session: AsyncSession = Depends(get_db)):
    pedido = await adicionar_pedido(pedido_id, pedido_item, usuario, session)
    return {
        "mensagem": "item adicionado com sucesso",
        "pedido": pedido
    }

@order_router.post("/pedido/remover/{pedido_item_id}")
async def remover(pedido_item_id: int, usuario: Usuario = Depends(obter_usuario_logado) ,session: AsyncSession = Depends(get_db)):
    pedido = await remover_pedido(pedido_item_id, usuario, session)

    if pedido:
        return {"mensagem": "item removido com sucesso"}

@order_router.get("/listar")
async def listar(usuario: Usuario = Depends(obter_usuario_logado), 
                         session: AsyncSession = Depends(get_db)):
    lista = await listar_pedido(session, usuario)
    return {
        "pedido": lista
    }

@order_router.get("/listar/{pedido_id}")
async def visualizar(pedido_id: int, usuario: Usuario = Depends(obter_usuario_logado), session: AsyncSession = Depends(get_db)):
    pedido = await visualizar_pedido(pedido_id, usuario, session)
    return {
        "quantidade": len(pedido.itens),
        "pedido": pedido
    }

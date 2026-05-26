from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.exceptions import AcessoNegadoError, PedidoNaoEncontradoError, ModelError, AtualizarStatusPedidoError
from app.models import Pedido, PedidoItem, Usuario, StatusPedido
from app.schemas import PedidoCriarSchema


async def criar_pedido(pedido_schema: PedidoCriarSchema, usuario: Usuario, db: AsyncSession) -> bool:
    if pedido_schema.usuario_id != usuario.id:
        raise AcessoNegadoError()

    novo_pedido = Pedido(usuario_id=pedido_schema.usuario_id)
    
    for item in pedido_schema.itens:
        novo_item = PedidoItem(
            pedido_id=pedido_schema,
            quantidade=item.quantidade,
            sabor=item.sabor,
            tamanho=item.tamanho,
            preco_unitario=item.preco_unitario
        )

        novo_pedido.itens.append(novo_item)
    
    novo_pedido.calcular_preco()
    db.add(novo_pedido)
    await db.commit()
    return True


async def cancelar_pedido(pedido_id: int, usuario: Usuario, db: AsyncSession) -> Pedido:
    query = select(Pedido).where(Pedido.id == pedido_id)
    resultado = await db.execute(query)
    pedido = resultado.scalars().first()

    if not pedido:
        raise PedidoNaoEncontradoError()
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise AcessoNegadoError()
    if pedido.status != StatusPedido.PENDENTE:
        raise AtualizarStatusPedidoError("Pedido não pode ser cancelado")
    
    pedido.status = StatusPedido.CANCELADO
    await db.commit()
    await db.refresh(pedido)
    return pedido


async def atualizar_pedido(pedido_id: int, novo_status: StatusPedido, usuario_admin: Usuario, db: AsyncSession):
    query = select(Pedido).where(Pedido.id == pedido_id)
    resultado = await db.execute(query)
    pedido = resultado.scalars().first()

    if not pedido:
        raise PedidoNaoEncontradoError()
    
    status_atual = StatusPedido(pedido.status)

    if not status_atual.pode_atualizar_para(novo_status):
        raise AtualizarStatusPedidoError()
    
    pedido.status = novo_status
    await db.commit()
    await db.refresh(pedido)
    return pedido
    

async def adicionar_pedido(pedido_id: int, pedido_item: PedidoItem, usuario: Usuario, db: AsyncSession) -> PedidoItem:
    query = select(Pedido).where(Pedido.id == pedido_id).options(joinedload(Pedido.itens))
    resultado = await db.execute(query)
    pedido = resultado.scalars().first()

    if not pedido:
        raise PedidoNaoEncontradoError()
    if pedido.status != "pendente":
        raise ModelError("Não pode modificar um pedido que já entrou em preparo")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise AcessoNegadoError()
    
    novo_pedido_item = PedidoItem(pedido_id, quantidade=pedido_item.quantidade, sabor=pedido_item.sabor, 
                                  tamanho=pedido_item.tamanho, preco_unitario=pedido_item.preco_unitario)

    pedido.itens.append(novo_pedido_item)
    
    db.add(novo_pedido_item)
    pedido.calcular_preco()
    await db.commit()
    await db.refresh(novo_pedido_item)
    return novo_pedido_item


async def remover_pedido(pedido_item_id: int, usuario: Usuario, db: AsyncSession) -> bool:
    query = select(PedidoItem).where(PedidoItem.id == pedido_item_id).options(joinedload(PedidoItem.pedido).joinedload(Pedido.itens))
    resultado = await db.execute(query)
    item_pedido = resultado.scalars().unique().first()
    pedido = item_pedido.pedido

    if not item_pedido:
        raise PedidoNaoEncontradoError("Item do pedido não ecnontrado")
    if pedido.status != "pendente":
        raise ModelError("Não pode modificar um pedido que já entrou em preparo")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise AcessoNegadoError()
    
    pedido.itens.remove(item_pedido)
    await db.delete(item_pedido)
    pedido.calcular_preco()
    await db.commit()
    return True


async def listar_pedido(db: AsyncSession, usuario: Usuario = None) -> Pedido:
    query = select(Pedido).where(Pedido.usuario_id == usuario.id)
    resultado = await db.execute(query)
    lista_pedido = resultado.scalars().all()

    if not lista_pedido:
        raise PedidoNaoEncontradoError("Nenhum pedido encontrado")
    
    return lista_pedido


async def visualizar_pedido(pedido_id: int, usuario: Usuario, db: AsyncSession) -> Pedido:
    query = select(Pedido).where(Pedido.id == pedido_id).options(selectinload(Pedido.itens))
    resultado = await db.execute(query)
    pedido = resultado.scalars().first()

    if not pedido:
        raise PedidoNaoEncontradoError()
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise AcessoNegadoError()
    
    return pedido

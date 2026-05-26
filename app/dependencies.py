from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.exceptions import AcessoNegadoError, UsuarioNaoEncontradoError, UsuarioDesativadoError
from app.models import Usuario
from app.security import verificar_token


async def obter_usuario_logado(usuario_id: int = Depends(verificar_token), db: AsyncSession = Depends(get_db)) -> Usuario:
    query = select(Usuario).where(Usuario.id == usuario_id)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if not usuario:
        raise UsuarioNaoEncontradoError()

    if not usuario.ativo:
        raise UsuarioDesativadoError()
    
    return usuario

async def obter_admin_logado(usuario_id: int = Depends(verificar_token), db: AsyncSession = Depends(get_db)) -> Usuario:
    query = select(Usuario).where(Usuario.id == usuario_id)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if not usuario.admin:
        raise AcessoNegadoError("Disponível somente para administradores")
    
    return usuario

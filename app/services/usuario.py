from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.exceptions import AcessoNegadoError ,CredenciaisInvalidasError, EmailJaCadastradoError, UsuarioNaoEncontradoError
from app.models import Usuario
from app.security import criptografar_senha, verificar_senha


async def cadastrar(nome: str, email: str, senha: str, ativo: bool, admin: bool, db: AsyncSession, 
                    usuario_admin: Usuario = None) -> bool:
    
    if not usuario_admin or not usuario_admin.admin:
        admin = False

    query = select(Usuario).where(Usuario.email == email)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if usuario:
        raise EmailJaCadastradoError()
    
    hashed_senha = criptografar_senha(senha)
    novo_usuario = Usuario(nome, email, hashed_senha, ativo, admin)
    db.add(novo_usuario)
    await db.commit()
    return True

async def login(email: str, senha: str, db: AsyncSession):
    query = select(Usuario).where(Usuario.email == email)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if not usuario or not verificar_senha(senha, usuario.senha):
        raise CredenciaisInvalidasError()
    return usuario

async def deletar(email: str, senha: str, usuario_logado: Usuario, db: AsyncSession):
    if usuario_logado.email != email or not verificar_senha(senha, usuario_logado.senha):
        raise CredenciaisInvalidasError()
    
    usuario_logado.ativo = False
    db.commit()
    return True

async def limpar_usuario_inativos(usuario_admin: Usuario, db: AsyncSession):
    if not usuario_admin or not usuario_admin.admin:
        raise AcessoNegadoError()

    query = select(Usuario).where(Usuario.ativo == False)
    resultado = await db.execute(query)
    usuarios_inativos = resultado.scalars().all()

    if not usuarios_inativos:
        raise UsuarioNaoEncontradoError("Nenhum usuário inativo")

    for usuario in usuarios_inativos:
        await db.delete(usuario)
    
    await db.commit()
    return len(usuarios_inativos)

async def excluir_usuario(email: str, usuario_admin: Usuario, db: AsyncSession):
    if not usuario_admin or not usuario_admin.admin:
        raise AcessoNegadoError()
    
    query = select(Usuario).where(Usuario.email == email)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if not usuario:
        raise UsuarioNaoEncontradoError()

    await db.delete(usuario)
    await db.commit()
    return True
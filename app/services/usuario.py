from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.exceptions import AcessoNegadoError ,CredenciaisInvalidasError, EmailJaCadastradoError, UsuarioNaoEncontradoError, UsuarioDesativadoError, ContaAtivaError, RecuperacaoContaExpiradoError
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

async def login(email: str, senha: str, db: AsyncSession) -> Usuario:
    query = select(Usuario).where(Usuario.email == email)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()
    
    if not usuario or not verificar_senha(senha, usuario.senha):
        raise CredenciaisInvalidasError()
    
    if not usuario.ativo:
        data_delecao = usuario.deletado_em.replace(tzinfo=timezone.utc) if usuario.deletado_em.tzinfo is None else usuario.deletado_em

        if datetime.now(timezone.utc) < data_delecao + timedelta(days=30):
            raise UsuarioDesativadoError("Sua conta foi desativada, mas ainda pode ser recuperada. Acesse a rota de recuperação")
        raise UsuarioNaoEncontradoError()

    return usuario

async def deletar(email: str, senha: str, usuario_logado: Usuario, db: AsyncSession) -> bool:
    if usuario_logado.email != email or not verificar_senha(senha, usuario_logado.senha):
        raise CredenciaisInvalidasError()

    usuario_logado.deletado_em = datetime.now(timezone.utc)
    usuario_logado.ativo = False
    await db.commit()
    return True


async def recuperar_conta(email: str, senha: str, db: AsyncSession) -> bool:
    query = select(Usuario).where(Usuario.email == email)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()
    
    if not usuario or not verificar_senha(senha, usuario.senha):
        raise CredenciaisInvalidasError()
    
    if usuario.ativo:
        raise ContaAtivaError()

    data_delecao = usuario.deletado_em.replace(tzinfo=timezone.utc) if usuario.deletado_em.tzinfo is None else usuario.deletado_em
    if datetime.now(timezone.utc) > data_delecao + timedelta(days=30):
        RecuperacaoContaExpiradoError()
    
    usuario.ativo = True
    usuario.deletado_em = None
    await db.commit()
    return True


async def visualizar_perfil(usuario_logado: Usuario, db: AsyncSession) -> Usuario:
    query = select(Usuario).where(Usuario.id == usuario_logado.id)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if not usuario:
        raise UsuarioNaoEncontradoError()
    
    return usuario

async def editar_perfil(nome: str, email: str, usuario_logado: Usuario, db: AsyncSession) -> Usuario:
    query = select(Usuario).where(Usuario.id == usuario_logado.id)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    usuario.nome = nome
    usuario.email = email
    
    await db.commit()
    await db.refresh(usuario)
    return usuario

async def editar_senha(senha: str, nova_senha: str,usuario_logado: Usuario, db: AsyncSession) -> bool:
    query = select(Usuario).where(Usuario.id == usuario_logado.id)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if not verificar_senha(senha, usuario.senha):
        raise CredenciaisInvalidasError("Senha inválida")

    hashed_senha = criptografar_senha(nova_senha)
    usuario.senha = hashed_senha
    await db.commit()
    return True

# ADMINISTRAÇÃO
async def limpar_usuario_inativos(usuario_admin: Usuario, db: AsyncSession) -> int:
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

async def excluir_usuario(email: str, usuario_admin: Usuario, db: AsyncSession) -> bool:
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

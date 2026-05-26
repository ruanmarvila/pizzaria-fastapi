from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import obter_usuario_logado
from app.models import Usuario
from app.schemas import CadastrarSchema, LoginSchema, EditarPerfilSchema
from app.security import gerar_token
from app.services import cadastrar, login, deletar, recuperar_conta, visualizar_perfil, editar_perfil, editar_senha


auth_router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@auth_router.get("/")
async def home():
    return {"mensagem": "Você acessou a rota de autenticação"}

@auth_router.post("/cadastrar")
async def cadastrar_usuario(usuario: CadastrarSchema, session: AsyncSession = Depends(get_db)):
    usuario = await cadastrar(usuario.nome, usuario.email, usuario.senha,
                              usuario.ativo, usuario.admin, session)
    return {"mensagem": "Usuário cadastrado com sucesso"}

@auth_router.post("/login")
async def login_usuario(usuario: LoginSchema, session: AsyncSession = Depends(get_db)):
    usuario = await login(usuario.email, usuario.senha, session)
    
    acess_token = gerar_token(usuario.id)
    refresh_token = gerar_token(usuario.id, duracao=timedelta(days=7))
    return {
        "access_token": acess_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@auth_router.post("/login_form")
async def login_formulario(formulario: OAuth2PasswordRequestForm = Depends(),
                            session: AsyncSession = Depends(get_db)):
    usuario = await login(formulario.username, formulario.password, session)
    
    acess_token = gerar_token(usuario.id)
    return {
        "access_token": acess_token,
        "token_type": "Bearer"
    }

@auth_router.get("/refresh")
async def refresh_token(usuario: Usuario = Depends(obter_usuario_logado)):
    acess_token = gerar_token(usuario.id)
    return {
        "acess_token": acess_token,
        "token_type": "Bearer"
    }

@auth_router.post("/excluir")
async def excluir_usuario(usuario_schema: LoginSchema, usuario: Usuario = Depends(obter_usuario_logado), 
                          session: AsyncSession = Depends(get_db)):
    usuario = await deletar(usuario_schema.email, usuario_schema.senha, usuario, session)
    return {
        "mensagem": "usuario excluído com sucesso"
    }

@auth_router.post("/recuperar")
async def recuperar_usuario(usuario_schema: LoginSchema, session: AsyncSession = Depends(get_db)):
    resultado = await recuperar_conta(usuario_schema.email, usuario_schema.senha, session)
    return {
        "mensagem": "conta recuperada com sucesso"
    }

@auth_router.get("/perfil")
async def acessar_perfil(usuario: Usuario = Depends(obter_usuario_logado), session: AsyncSession = Depends(get_db)):
    perfil = await visualizar_perfil(usuario, session)
    return {
        "perfil": perfil
    }

@auth_router.post("/perfil/editar")
async def editar_perfil_usuario(perfil_schema: EditarPerfilSchema, usuario: Usuario = Depends(obter_usuario_logado), session: AsyncSession = Depends(get_db)):
    perfil = await editar_perfil(perfil_schema.nome, perfil_schema.email, usuario, session)
    return {
        "perfil": perfil
    }

@auth_router.post("/perfil/editar/senha")
async def mudar_senha(senha: str, nova_senha: str, usuario: Usuario = Depends(obter_usuario_logado), session: AsyncSession = Depends(get_db)):
    resultado = await editar_senha(senha, nova_senha, usuario, session)
    if resultado:
        return {"mensagem": "senha modificada com sucesso!"}
    

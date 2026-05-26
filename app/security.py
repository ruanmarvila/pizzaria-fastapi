from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.main import TokenInvalidoError, TokenExpiradoError


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_hash = PasswordHash((Argon2Hasher(),))
oauth2_schema = OAuth2PasswordBearer(tokenUrl="usuarios/login_form")

def criptografar_senha(senha: str) -> str:
    return pwd_hash.hash(senha)
    
def verificar_senha(normal_senha: str, hashed_senha: str) -> bool:
    return pwd_hash.verify(normal_senha, hashed_senha)

def gerar_token(usuario_id: int, duracao = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    data_expiracao = datetime.now(timezone.utc) + duracao
    info ={
        "user_id": usuario_id,
        "exp": data_expiracao
    }
    jwt_codificado = jwt.encode(info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def verificar_token(token: str = Depends(oauth2_schema)) -> int:
    try:
        info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        usuario_id = int(info.get("user_id"))
    except InvalidTokenError:
        raise TokenInvalidoError()
    except ExpiredSignatureError:
        raise TokenExpiradoError()
    
    return usuario_id

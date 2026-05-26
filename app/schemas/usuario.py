from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class CadastrarSchema(BaseModel):
    nome: str = Field(..., min_length=1)
    email: EmailStr
    senha: str = Field(..., min_length=4)
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    @field_validator('nome', 'senha')
    @classmethod
    def checar_vazios(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O campo não pode ser vazio")
        return valor.strip()

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

    @field_validator('email', 'senha')
    @classmethod
    def checar_vazios(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O campo não pode ser vazio")
        return valor.strip()

    class Config:
        from_attributes = True

class EditarPerfilSchema(BaseModel):
    nome: str = Field(..., min_length=1)
    email: EmailStr

    
    @field_validator('nome')
    @classmethod
    def checar_vazios(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O campo não pode ser vazio")
        return valor.strip()

    class Config:
        from_attributes = True

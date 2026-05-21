from pydantic import BaseModel, Field, field_validator
from typing import List


class PedidoItemSchema(BaseModel):
    quantidade: int = Field(..., gt=0)
    sabor: str = Field(..., min_length=1)
    tamanho: str = Field(..., min_length=1)
    preco_unitario: float = Field(..., gt=0)

    @field_validator('sabor', 'tamanho')
    @classmethod
    def checar_vazios(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O campo não pode ser vazio")
        return valor.strip()

    class Config:
        from_attributes = True

class PedidoCriarSchema(BaseModel):
    usuario_id: int =  Field(..., gt=0)
    itens: List[PedidoItemSchema] = Field(..., min_length=1)


    class Config:
        from_attributes = True
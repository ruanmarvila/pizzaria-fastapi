from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String, default="PENDENTE")
    preco = Column("preco", Float)
    usuario_id = Column("usuario_id", ForeignKey("usuarios.id"))
    itens = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")

    def __init__(self, usuario_id, status="PENDENTE", preco=0):
        self.usuario_id = usuario_id
        self.status = status
        self.preco = preco
    
    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    pedido_id = Column("pedido_id", Integer, ForeignKey("pedidos.id"), nullable=False)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)

    pedido = relationship("Pedido", back_populates="itens")

    def __init__(self, pedido_id, quantidade, sabor, tamanho, preco_unitario):
        self.pedido_id = pedido_id
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
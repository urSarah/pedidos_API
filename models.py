import enum
from sqlalchemy import create_engine,Column,String,Integer,Boolean,Float,ForeignKey,Enum
from sqlalchemy.orm import declarative_base, relationship

#cria a conexão
db = create_engine("sqlite:///database/banco.db")

#cria a base do db
Base = declarative_base()

class OrderStatus(enum.Enum):
    PENDENTE= "PENDENTE"
    CANCELADO= "CANCELADO"
    FINALIZADO= "FINALIZADO"

#criar tabelas do banco
class User(Base):
    __tablename__ = "users"

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    nome = Column("nome",String)
    senha = Column("senha",String)
    email = Column("email",String,nullable=False)
    ativo = Column("ativo",Boolean)
    admin = Column("admin",Boolean,default=False)

    def __init__(self,nome,email,senha,ativo=True,admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

#pedido
class Order(Base):
    __tablename__ = "orders"

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    status = Column("status", Enum(OrderStatus)) #pendente, cancelado,finalizado
    userId = Column("userId",ForeignKey("users.id"))
    preco = Column("preco",Float)
    items = relationship("ItemsOrder", cascade="all, delete")

    def __init__(self,userId,status=OrderStatus.PENDENTE,preco=0):
        self.userId = userId
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        # pecorrer todos os items do pedido
        preco_pedido = 0
        for item in self.items:
            preco_item = item.preco_unitario * item.quantidade
            preco_pedido += preco_item
        # somar todos os preços de todos os items dos pedidos
        # editar no campo "preco" o valor final do preco do pedido
        self.preco = preco_pedido

#itensPedido
class ItemsOrder(Base):
    __tablename__ = "items_orders"

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    quantidade = Column("quantidade",Integer)
    sabor = Column("sabor",String)
    tamanho = Column("tamanho",String)
    preco_unitario = Column("preco_unitario",Float)
    orderId = Column("orderId",ForeignKey("orders.id"))

    def __init__(self,orderId,quantidade,sabor,tamanho,preco_unitario):
        self.orderId = orderId
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario

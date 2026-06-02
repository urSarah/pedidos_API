from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_session
from models import Order
from schemas import OrderSchema
order_router = APIRouter(prefix="/order", tags=["order"])

#edpoint:
#/ordens
@order_router.get("/")
async def order():
    return {"mensagem": "acessada"}

@order_router.post("/create_order")
async def create(order_schema:OrderSchema,session: Session = Depends(pegar_session)):
    new_order = Order(userId=order_schema.userId)
    session.add(new_order)
    session.commit()
    return {"mensagem": f"Pedido {new_order.id} criado com sucesso"}
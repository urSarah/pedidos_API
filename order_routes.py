from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_session, verify_token
from models import Order, OrderStatus
from schemas import OrderSchema
order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])

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

@order_router.post("/cancel/{orderId}")
async def cancel_order(orderId: int, session: Session = Depends(pegar_session)):
    order = session.query(Order).filter(Order.id == orderId).first()

    if not order:
        raise HTTPException(status_code=401,detail="Pedido não encontrado")
    
    order.status = OrderStatus.CANCELADO
    session.commit()

    return {
        "Mensagem": f"Pedido numero: {orderId} cancelado",
        "Order": order
    }
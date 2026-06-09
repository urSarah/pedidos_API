from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import pegar_session, verify_token
from app.services.order_service import add, cancel, create,list
from models import User
from schemas import ItemOrderSchema
order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])

#edpoint:
#/ordens
@order_router.get("/")
async def order():
    return {"mensagem": "acessada"}

@order_router.post("/create_order")
async def create(session: Session = Depends(pegar_session),current_user: User = Depends(verify_token)):
    new_order = create(session,current_user)

    return {
        "mensagem": (
            f"Pedido {new_order.id} "
            f"para {current_user.nome} criado com sucesso"
        )
    }

@order_router.post("/cancel/{orderId}")
async def cancel_order(orderId: int, session: Session = Depends(pegar_session), user: User = Depends(verify_token)):
    order = cancel(orderId,session,user)

    return {
        "Mensagem": f"Pedido numero: {orderId} cancelado",
        "Order": order
    }

@order_router.get("/list")
async def list_order(session: Session = Depends(pegar_session), user: User = Depends(verify_token)):
    order = list(session,user)

    return {"order": order}

@order_router.post("/add_item/{orderId}")
async def add_item(orderId: int,item_order_schema: ItemOrderSchema,session: Session = Depends(pegar_session), user: User = Depends(verify_token)):
    order = add(orderId,item_order_schema,session,user)

    return {
        "mensagem": "Item criado com sucesso",
        "item_id": order["order_item"].id,
        "preço_pedido": order["order"].preco
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_session, verify_token
from models import ItemsOrder, Order, OrderStatus, User
from schemas import ItemOrderSchema
order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])

#edpoint:
#/ordens
@order_router.get("/")
async def order():
    return {"mensagem": "acessada"}

@order_router.post("/create_order")
async def create(session: Session = Depends(pegar_session),current_user: User = Depends(verify_token)):
    # criar pedido de acordo com o usuario que estiver logado
    # exemplo: mau de id 1 logado, pedido com userId = 1 criado
    new_order = Order(userId=current_user.id)
    session.add(new_order)
    session.commit()
    return {"mensagem": f"Pedido {new_order.id} para {current_user.nome} criado com sucesso"}

@order_router.post("/cancel/{orderId}")
async def cancel_order(orderId: int, session: Session = Depends(pegar_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id == orderId).first()

    if not order:
        raise HTTPException(status_code=401,detail="Pedido não encontrado")    
    if not user.admin and user.id != order.userId:
        raise HTTPException(status_code=401,detail="Voce não tem autorização para fazer essa modificação")
    
    order.status = OrderStatus.CANCELADO
    session.commit()

    return {
        "Mensagem": f"Pedido numero: {orderId} cancelado",
        "Order": order
    }

@order_router.get("/list")
async def list_order(session: Session = Depends(pegar_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=401,detail="Voce não tem autorização para fazer essa operação")
    
    order = session.query(Order).all()

    return {"order": order}

@order_router.post("/add_item/{orderId}")
async def add_item(orderId: int,item_order_schema: ItemOrderSchema,session: Session = Depends(pegar_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id == orderId).first()

    if not order:
        raise HTTPException(status_code=401,detail="Pedido não encontrado")    
    if not user.admin and user.id != order.userId:
        raise HTTPException(status_code=401,detail="Voce não tem autorização para fazer essa operação")
    
    order_item = ItemsOrder(orderId,item_order_schema.quantidade,item_order_schema.sabor,item_order_schema.tamanho,item_order_schema.preco_unitario)

    order.calcular_preco()
    session.add(order_item)
    session.commit()

    return {
        "mensagem": "Item criado com sucesso",
        "item_id": order_item.id,
        "preço_pedido": order.preco
    }

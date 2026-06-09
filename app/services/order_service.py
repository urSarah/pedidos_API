from fastapi import HTTPException

from models import (
    Order,
    OrderStatus,
    ItemsOrder
)


def create(session, current_user):
    new_order = Order(userId=current_user.id)

    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    return new_order

def cancel(orderId, session, user): 
    order = session.query(Order).filter(Order.id == orderId).first()

    if not order:
        raise HTTPException(status_code=401,detail="Pedido não encontrado")    
    if not user.admin and user.id != order.userId:
        raise HTTPException(status_code=401,detail="Voce não tem autorização para fazer essa modificação")
    
    order.status = OrderStatus.CANCELADO
    session.commit()
    
    return order

def list(session,user):
    if not user.admin:
        raise HTTPException(status_code=401,detail="Voce não tem autorização para fazer essa operação")
    
    order = session.query(Order).all()

    return order

def add(order_id, item_order_schema,session,user):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404,detail="Pedido não encontrado")

    if not user.admin and user.id != order.userId:
        raise HTTPException(status_code=403,detail="Você não tem autorização")

    order_item = ItemsOrder(
        order_id,
        item_order_schema.quantidade,
        item_order_schema.sabor,
        item_order_schema.tamanho,
        item_order_schema.preco_unitario
    )

    session.add(order_item)

    order.calcular_preco()

    session.commit()
    session.refresh(order_item)

    return {"order":order,"order_item":order_item}
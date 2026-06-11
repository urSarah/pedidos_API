from fastapi import HTTPException

from app.repository.order_repository import OrderRepository
from models import OrderStatus


def create(session, current_user):
    new_order = OrderRepository.create(session,current_user)

    return new_order

def cancel(orderId, session, user): 
    order = OrderRepository.get_by_Id(session, orderId)# AQUI

    if not order:
        raise HTTPException(status_code=401,detail="Pedido não encontrado")    
    if not user.admin and user.id != order.userId:
        raise HTTPException(status_code=401,detail="Voce não tem autorização para fazer essa modificação")
    
    order.status = OrderStatus.CANCELADO
    OrderRepository.update(session)
    
    return order

def list(session,user):
    if not user.admin:
        raise HTTPException(status_code=401,detail="Voce não tem autorização para fazer essa operação")
    
    order = OrderRepository.list_all(session)

    return order

def add(orderId, item_order_schema,session,user):
    order = OrderRepository.get_by_Id(orderId)# AQUI

    if not order:
        raise HTTPException(status_code=404,detail="Pedido não encontrado")

    if not user.admin and user.id != order.userId:
        raise HTTPException(status_code=403,detail="Você não tem autorização")
    

    OrderRepository.add_item(session,orderId,item_order_schema)

    order.calcular_preco()

    OrderRepository.update(session)

    return {"order":order,"order_item":item_order_schema}